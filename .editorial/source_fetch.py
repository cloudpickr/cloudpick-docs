#!/usr/bin/env python3
"""
공식 근거(source) 독립 fetch — SSRF 방어 포함.

계약: froguin/multi-agent-stack@53618d6 §Evidence packet
  "The fetcher must reject private/metadata destinations and unsafe redirects,
   and cap bytes/time."

패킷의 quote는 리뷰 보조일 뿐, 이 모듈이 출처를 '독립적으로' 다시 가져와 대조한다.

방어:
  - https만 허용(http·file·gopher 등 거부)
  - DNS 해석 결과가 사설/loopback/link-local/CGNAT/metadata(169.254.169.254)면 거부
  - 리다이렉트를 수동 추적하며 매 홉마다 목적지를 재검증(unsafe redirect 차단)
  - 응답 바이트 상한·전체 시간 상한
  - 리뷰 잡에서만 호출(트러스트된 base 코드), 임의 URL은 패킷의 source_url/sources에서만.
"""
from __future__ import annotations

import ipaddress
import socket
import ssl
import time
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser

MAX_BYTES = 2 * 1024 * 1024      # 2 MiB
MAX_TIME_SECONDS = 20
MAX_REDIRECTS = 5
USER_AGENT = "cloudpick-editorial-source-check/1"

# metadata / 특수 목적 대역(사설 IP 판정에 더해 명시 차단).
_BLOCKED_EXACT = {"169.254.169.254", "100.100.100.200"}  # AWS/GCP·Alibaba metadata


class FetchError(Exception):
    """근거 fetch 실패(차단 포함). 승인으로 이어지지 않는다."""


@dataclass
class FetchResult:
    url: str
    status: int
    body_bytes: int
    body_sha256: str
    text_sample: str  # 앞부분 일부(대조 보조)
    visible_sha256: str | None = None  # 선택적 본문 관측용, 사실 검증이 아님


class _VisibleText(HTMLParser):
    """Visible main/article text only; ignore navigation, scripts and UI chrome."""
    BLOCKED = {'script', 'style', 'noscript', 'svg', 'template', 'iframe', 'nav', 'footer', 'form', 'button', 'head'}
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.invalid = False
        self.text = []

    OPTIONAL = {'p', 'li', 'dt', 'dd', 'option', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td'}

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        attributes = dict(attrs)
        sidebar = tag == 'aside' and attributes.get('role') in {'navigation', 'menu'}
        blocked = (self.stack[-1][1] if self.stack else False) or tag in self.BLOCKED or sidebar
        main = (self.stack[-1][2] if self.stack else False) or tag in {'main', 'article'} or attributes.get('role') == 'main' or attributes.get('id') == 'main-col-body'
        self.stack.append((tag, blocked, main))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        matching = next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i][0] == tag), None)
        if matching is None:
            if self.stack and (self.stack[-1][1] or self.stack[-1][2]):
                self.invalid = True
            return
        if any(row[0] not in self.OPTIONAL for row in self.stack[matching+1:]):
            self.invalid = True
        del self.stack[matching:]

    def handle_data(self, value):
        if self.stack and self.stack[-1][2] and not self.stack[-1][1]:
            cleaned = ' '.join(value.split())
            if cleaned:
                self.text.append(cleaned)


def _visible_digest(raw: bytes, content_type: str) -> str | None:
    import hashlib
    mime = content_type.split(';', 1)[0].strip().lower()
    try:
        decoded = raw.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        return None
    if mime in ('text/html', 'application/xhtml+xml'):
        parser = _VisibleText()
        parser.feed(decoded)
        if parser.invalid or any(row[2] for row in parser.stack):
            return None
        text = ' '.join(' '.join(parser.text).split())
    elif mime == 'text/plain':
        text = ' '.join(decoded.split())
    else:
        return None
    # Tiny/JS-only/soft error pages have no dependable semantic content.
    if len(text) < 100:
        return None
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _ip_is_safe(ip_str: str) -> bool:
    """공인(글로벌) 유니캐스트만 허용."""
    if ip_str in _BLOCKED_EXACT:
        return False
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    if (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_multicast or ip.is_reserved or ip.is_unspecified):
        return False
    # IPv4 CGNAT 100.64.0.0/10
    if ip.version == 4 and ip in ipaddress.ip_network("100.64.0.0/10"):
        return False
    return ip.is_global


def _resolve_and_check(host: str) -> list[str]:
    """호스트의 모든 A/AAAA를 해석해 하나라도 안전하지 않으면 거부."""
    try:
        infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise FetchError(f"DNS resolution failed for {host}: {exc}") from exc
    ips = sorted({info[4][0] for info in infos})
    if not ips:
        raise FetchError(f"no addresses for {host}")
    for ip in ips:
        if not _ip_is_safe(ip):
            raise FetchError(f"blocked destination IP {ip} for {host} (SSRF guard)")
    return ips


def _validate_url(url: str) -> tuple[str, str]:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise FetchError(f"only https allowed, got {parsed.scheme!r}")
    if not parsed.hostname:
        raise FetchError("missing hostname")
    return parsed.hostname, url


def fetch_source(url: str, *, opener=None, resolver=None, normalize_content=False) -> FetchResult:
    """
    안전 fetch. opener/resolver 주입으로 테스트 가능.
    resolver(host) -> [ip...] (안전성 검사 포함), opener(url) -> (status, headers, body_reader).
    """
    import hashlib

    resolver = resolver or _resolve_and_check
    deadline = time.monotonic() + MAX_TIME_SECONDS
    current = url
    for _hop in range(MAX_REDIRECTS + 1):
        host, current = _validate_url(current)
        resolver(host)  # 매 홉마다 목적지 재검증(리다이렉트 SSRF 방지)
        if time.monotonic() > deadline:
            raise FetchError("time budget exceeded")

        status, headers, body = _do_request(current, opener, deadline)
        if status in (301, 302, 303, 307, 308):
            location = headers.get("Location") or headers.get("location")
            if not location:
                raise FetchError(f"redirect {status} without Location")
            from urllib.parse import urljoin
            current = urljoin(current, location)
            continue  # 다음 홉에서 재검증
        # 최종 응답
        h = hashlib.sha256()
        total = 0
        chunks = []
        full = [] if normalize_content else None
        while True:
            if time.monotonic() > deadline:
                raise FetchError("time budget exceeded during read")
            chunk = body.read(65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise FetchError(f"response exceeds {MAX_BYTES} bytes")
            h.update(chunk)
            if full is not None:
                full.append(chunk)
            if len(chunks) < 4:
                chunks.append(chunk)
        sample = b"".join(chunks)[:4096].decode("utf-8", errors="replace")
        content_type = next((v for k, v in headers.items() if k.lower() == 'content-type'), '')
        visible = _visible_digest(b''.join(full), content_type) if full is not None else None
        return FetchResult(current, status, total, h.hexdigest(), sample, visible)
    raise FetchError("too many redirects")


def _do_request(url, opener, deadline):
    """실제 HTTPS 요청(리다이렉트 자동추적 비활성). opener 주입 시 그것을 사용."""
    if opener is not None:
        return opener(url)
    remaining = max(1.0, deadline - time.monotonic())

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None  # 자동 리다이렉트 금지(수동 처리)

    ctx = ssl.create_default_context()
    handler = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=ctx))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        resp = handler.open(req, timeout=remaining)
        return resp.status, dict(resp.headers), resp
    except urllib.error.HTTPError as exc:
        # 3xx는 HTTPError로 오지 않게 _NoRedirect가 처리하지만, 4xx/5xx는 여기로.
        return exc.code, dict(exc.headers or {}), exc


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: source_fetch.py <https-url>", file=sys.stderr)
        sys.exit(2)
    try:
        r = fetch_source(sys.argv[1])
        print(f"{r.status} {r.body_bytes}B sha256={r.body_sha256[:12]}… {r.url}")
    except FetchError as exc:
        print(f"::error::source fetch blocked/failed: {exc}", file=sys.stderr)
        sys.exit(1)
