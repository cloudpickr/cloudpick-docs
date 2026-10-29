#!/usr/bin/env python3
"""
새 소식 → ko 문서 매핑 봇 (축2, council 합의 2단계 — 제보 전용).

whats-new 등으로 수집한 벤더 신규 발표 항목을, 반영 대상이 될 만한 ko(SOT) 문서
후보에 결정론적으로 매핑해 '제보'한다. 자동 수정·자동 PR 없음(advisory, exit 0).
실제 반영은 사람/에이전트가 공식 출처 확인 후 근거 패킷 PR로 한다(AGENTS.md 4대 축 ②).

매핑 신호(결정론):
  - 문서 인덱스: 각 ko 문서의 프론트매터 title + H2/H3 헤딩 + 경로 토큰.
  - 소식: 항목 title을 벤더/제품 별칭 테이블로 정규화한 토큰.
  - 점수: 토큰 겹침(별칭 히트 가중) → 상위 N개 문서 후보. 임계 미만은 'unmapped'.
    unmapped가 반복되면 '범위 밖 새 주제(축3)' 신호가 될 수 있다(별도 판단).

원칙:
  - "매핑 ≠ 반영 지시". 후보는 사람이 판단할 출발점일 뿐.
  - LLM·네트워크 없음(순수 결정론). 과신 금지: 점수는 '관련도 힌트'지 사실 판정이 아니다.

사용법:
  # 소식 JSON(항목 배열; 각 {title, url, csp?})을 입력으로
  python3 scripts/map-news-to-docs.py --news /tmp/news.json
  python3 scripts/map-news-to-docs.py --news /tmp/news.json --json
  # 소식 JSON이 없으면 stdin에서 제목 1줄씩 받기도 가능
  echo "AWS Bedrock AgentCore is now generally available" | python3 scripts/map-news-to-docs.py --stdin
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

DOCS_KO = "src/content/docs/ko"
TOP_N = 3            # 소식당 상위 후보 수
MIN_SCORE = 2        # 이 미만이면 unmapped(범위 밖 후보 신호)

# 벤더/제품 별칭 — 소식 제목을 문서 토큰과 잇기 위한 정규화 사전.
# 키(정규화 토큰) → 별칭들. 별칭이 소식·문서 양쪽에 있으면 가중 히트.
ALIASES = {
    "aws": ["aws", "amazon web services", "amazon"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["google cloud", "gcp", "google"],
    "oci": ["oci", "oracle cloud", "oracle"],
    "bedrock": ["bedrock", "agentcore"],
    "sagemaker": ["sagemaker"],
    "api-gateway": ["api gateway", "api management", "apim", "apigee"],
    "kms": ["kms", "key management", "cloud kms", "key vault"],
    "finops": ["finops", "cost", "billing", "cost explorer"],
    "serverless": ["lambda", "functions", "cloud run", "serverless"],
    "containers": ["eks", "aks", "gke", "kubernetes", "ecs", "fargate"],
    "cdn": ["cloudfront", "cdn", "front door", "cloud cdn"],
    "vpc": ["vpc", "vnet", "subnet"],
    "rdb": ["rds", "aurora", "cloud sql", "sql database"],
    "nosql": ["dynamodb", "cosmos", "firestore", "bigtable"],
    "object-storage": ["s3", "blob storage", "cloud storage", "object storage"],
    "ai-agents": ["agent", "agents", "copilot"],
    "rag": ["rag", "retrieval", "knowledge base", "vector"],
    "security": ["iam", "guardduty", "security", "defender", "sentinel"],
}

STOP = set("the a an is are now available for to of in on and or with your new".split())

# 벤더명은 거의 모든 문서에 흔해 변별력이 없다 — 별칭 가중에서 제외(제품/주제 별칭만 가중).
VENDOR_KEYS = {"aws", "azure", "gcp", "oci"}


def tokenize(s: str) -> set[str]:
    s = s.lower()
    toks = set(re.findall(r"[a-z0-9]+", s))
    return {t for t in toks if t not in STOP and len(t) > 1}


def alias_tokens(s: str) -> set[str]:
    """문자열에서 별칭 사전 키를 히트시킨 정규화 토큰 집합."""
    low = s.lower()
    hits = set()
    for key, variants in ALIASES.items():
        if any(v in low for v in variants):
            hits.add(key)
    return hits


def build_doc_index(root: str):
    """각 ko 문서 → (경로, 제목·헤딩·경로 토큰, 별칭 토큰)."""
    index = []
    for dirpath, _, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith((".md", ".mdx")):
                continue
            p = os.path.join(dirpath, f)
            with open(p, encoding="utf-8") as fh:
                text = fh.read()
            title = ""
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.M)
            if m:
                title = m.group(1)
            headings = " ".join(re.findall(r"^#{1,3}\s+(.+)$", text, re.M)[:40])
            rel = os.path.relpath(p, root)
            blob = f"{title} {headings} {rel.replace('/', ' ').replace('-', ' ')}"
            index.append({
                "path": os.path.relpath(p),
                "title": title,
                "tokens": tokenize(blob),
                "aliases": alias_tokens(blob),
            })
    return index


def score(news_title, doc):
    nt = tokenize(news_title)
    na = alias_tokens(news_title)
    tok_overlap = len(nt & doc["tokens"])
    # 벤더명(aws/azure/…)은 변별력이 없어 가중 제외 — 제품/주제 별칭 일치만 가중.
    product_alias_overlap = len((na & doc["aliases"]) - VENDOR_KEYS) * 2
    return tok_overlap + product_alias_overlap


def map_news(items, index):
    out = []
    for it in items:
        title = it.get("title") or ""
        ranked = sorted(
            ({"path": d["path"], "title": d["title"], "score": score(title, d)} for d in index),
            key=lambda x: -x["score"],
        )
        top = [r for r in ranked if r["score"] >= MIN_SCORE][:TOP_N]
        out.append({
            "news": title,
            "url": it.get("url"),
            "csp": it.get("csp"),
            "candidates": top,
            "status": "mapped" if top else "unmapped",  # unmapped 반복 = 축3(범위 밖) 신호
        })
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--news", help="소식 JSON(항목 배열 또는 {items:[...]})")
    ap.add_argument("--stdin", action="store_true", help="stdin에서 제목 1줄씩")
    ap.add_argument("--root", default=DOCS_KO)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    items = []
    if args.news:
        with open(args.news, encoding="utf-8") as fh:
            data = json.load(fh)
        items = data.get("items", data) if isinstance(data, dict) else data
    elif args.stdin:
        items = [{"title": ln.strip()} for ln in sys.stdin if ln.strip()]
    else:
        ap.error("--news 또는 --stdin 필요")

    index = build_doc_index(args.root)
    results = map_news(items, index)
    mapped = [r for r in results if r["status"] == "mapped"]
    unmapped = [r for r in results if r["status"] == "unmapped"]

    if args.json:
        print(json.dumps({
            "summary": {"total": len(results), "mapped": len(mapped), "unmapped": len(unmapped)},
            "mapped": mapped, "unmapped": unmapped,
        }, ensure_ascii=False, indent=2))
        return 0

    print("# 새 소식 → ko 문서 매핑 (축2, 결정론 · 제보 전용)\n")
    print(f"소식 {len(results)}건 · 매핑 {len(mapped)} · 미매핑 {len(unmapped)}\n")
    print("※ '매핑 = 반영 지시'가 아님. 공식 출처 확인 후 사람/에이전트가 근거 패킷 PR로 반영.\n")
    if mapped:
        print("## 반영 후보 (관련 문서)\n")
        for r in mapped:
            print(f"- {r['news']}" + (f"  ({r['url']})" if r["url"] else ""))
            for c in r["candidates"]:
                print(f"    → `{c['path']}` (score {c['score']}, {c['title']})")
    if unmapped:
        print("\n## 미매핑 — 기존 범위 밖일 수 있음 (반복되면 축3 신설 검토)\n")
        for r in unmapped:
            print(f"- {r['news']}" + (f"  ({r['url']})" if r["url"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
