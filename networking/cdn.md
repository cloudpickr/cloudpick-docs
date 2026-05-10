---
description: CDN 개념, 캐싱 전략, 엣지 컴퓨팅을 4개 벤더별로 비교합니다.
---

# CDN

> 문서 기준: 2026년 5월

## 개요

**CDN** (Content Delivery Network)은 전 세계 엣지 로케이션에 콘텐츠를 캐싱하여, 사용자에게 가장 가까운 위치에서 빠르게 전달하는 서비스입니다. 오리진 서버까지 가지 않고 엣지에서 응답하므로 지연 시간이 크게 줄어듭니다.

클라우드 CDN은 기본적으로 **HTTPS 전용**입니다. TLS 인증서 관리가 통합되어 있어, 별도 인증서 구매 없이 무료 SSL/TLS를 제공합니다.

### 핵심 개념

- **오리진** (Origin) — 원본 콘텐츠가 있는 서버. S3, Blob Storage, VM, 로드밸런서 등이 오리진이 됩니다.
- **엣지** (Edge) — 사용자에게 가까운 캐시 서버. 오리진에서 가져온 콘텐츠를 저장하고 서빙합니다.
- **캐시 히트/미스** — 엣지에 콘텐츠가 있으면 히트(빠름), 없으면 미스(오리진에서 가져옴).
- **TTL(Time To Live)** — 캐시 유효 시간. 만료되면 오리진에서 다시 가져옵니다.

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | CloudFront | 400+ 엣지 로케이션. Origin Shield(오리진 보호 캐시 계층) |
| Azure | Azure CDN / Front Door | Front Door에 CDN + WAF + 글로벌 LB 통합 |
| GCP | Cloud CDN | Cloud Load Balancing과 통합. 캐시 무효화 빠름 |
| OCI | — | 자체 CDN 미제공. Akamai, Cloudflare 등 3rd party 사용 |

## 핵심 차이점

**AWS CloudFront** — 엣지 로케이션 수가 가장 많고, Lambda@Edge/CloudFront Functions로 엣지에서 코드를 실행할 수 있습니다. Origin Shield로 오리진 부하를 추가로 줄일 수 있습니다.

**Azure Front Door** — CDN, 글로벌 로드밸런서, WAF를 하나의 서비스로 통합합니다. 별도 CDN 설정 없이 Front Door 하나로 전체 트래픽을 관리할 수 있습니다.

**GCP Cloud CDN** — Cloud Load Balancing에 체크박스 하나로 활성화할 수 있어 설정이 가장 간단합니다. 캐시 무효화(Invalidation)가 수 초 내에 전파됩니다.

## 적용 대상

CDN은 정적 파일뿐 아니라 다양한 워크로드에 적용할 수 있습니다.

| 대상 | 설명 |
| --- | --- |
| **정적 파일** | 이미지, CSS, JS. 가장 기본적인 CDN 활용 |
| **API 응답** | 변경이 드문 API 응답을 엣지에서 캐싱. 오리진 부하 감소 |
| **동영상 스트리밍** | MP4 다운로드, HLS/DASH 적응형 스트리밍. 대용량 전송에 필수 |
| **동적 콘텐츠** | 캐싱은 안 되지만, 엣지 ↔ 오리진 간 최적화된 네트워크 경로 활용 |

## 캐싱 계층과 전략

| 계층 | 위치 | 제어 방법 |
| --- | --- | --- |
| **브라우저 캐시** | 사용자 디바이스 | `Cache-Control`, `ETag` 헤더 |
| **CDN 엣지 캐시** | 벤더 엣지 로케이션 | TTL 정책, 캐시 키 설정 |
| **오리진 캐시** | 오리진 서버 앞단 (선택) | 리버스 프록시, 오리진 쉴드 |

캐시 무효화(Invalidation)는 전 세계 엣지에 전파해야 하므로 시간이 걸리고, 빈번하면 CDN의 이점이 사라집니다. 무효화를 최소화하는 것이 좋은 캐시 전략입니다.

**파일명에 버전/해시를 포함하세요.** 파일 내용이 바뀌면 파일명도 바뀌므로, 캐시 무효화 없이 즉시 새 버전이 서빙됩니다.

```text
❌ /static/app.js          → 내용 바뀌어도 URL 동일, 캐시 무효화 필요
✅ /static/app.a3f2c1.js   → 내용 바뀌면 해시 변경, 자동으로 새 파일 요청
```

| 전략 | 방법 | TTL 설정 |
| --- | --- | --- |
| **해시 파일명** | `app.a3f2c1.js` (빌드 시 해시 삽입) | 매우 길게 (1년). 무효화 불필요 |
| **버전 쿼리** | `app.js?v=2` | 중간. 일부 CDN에서 캐시 키로 인식 안 할 수 있음 |
| **짧은 TTL** | 동일 URL, TTL 5분 | API 응답 등 자주 바뀌는 콘텐츠에 적합 |
| **무효화** | 수동 Invalidation 요청 | 긴급 수정 시에만. 비용 발생 가능 |

대부분의 프론트엔드 빌드 도구(Webpack, Vite 등)는 해시 파일명을 자동 생성합니다. `index.html`만 짧은 TTL로 설정하고, 나머지 정적 파일은 긴 TTL + 해시 파일명으로 운영하는 것이 일반적인 패턴입니다.

## 엣지 컴퓨팅

CDN 엣지에서 코드를 실행하여 요청/응답을 변환하거나, 간단한 로직을 오리진 없이 처리할 수 있습니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | CloudFront Functions | 경량 (요청/응답 헤더 변환, 리다이렉트). 밀리초 이내 |
| AWS | Lambda@Edge | 풀 기능 (오리진 요청/응답 변환, 인증). 수 밀리초 |
| Azure | Front Door Rules Engine | 규칙 기반 라우팅/변환 |
| GCP | Cloud CDN + Cloud Functions | 별도 조합 |
| OCI | — | 자체 CDN/엣지 컴퓨팅 미제공 |

## 참고하기

### AWS

- [Amazon CloudFront 문서](https://docs.aws.amazon.com/ko_kr/cloudfront/)
- [Lambda@Edge 문서](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/lambda-edge.html)
- [CloudFront Functions 문서](https://docs.aws.amazon.com/ko_kr/AmazonCloudFront/latest/DeveloperGuide/cloudfront-functions.html)

### Azure

- [Azure Front Door 문서](https://learn.microsoft.com/ko-kr/azure/frontdoor/)
- [Azure CDN 문서](https://learn.microsoft.com/ko-kr/azure/cdn/)

### GCP

- [Cloud CDN 문서](https://cloud.google.com/cdn/docs)
- [Media CDN 문서](https://cloud.google.com/media-cdn/docs)
