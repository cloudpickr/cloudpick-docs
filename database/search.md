---
description: 전문 검색, 벡터 검색, 로그 분석 서비스를 벤더별로 비교합니다.
---

# 검색과 로그 분석

> 문서 기준: 2026년 5월

## 개요

### 현업에서 검색이 필요한 곳

| 유즈케이스 | 설명 | 왜 DB의 LIKE/WHERE로 안 되는가 |
| --- | --- | --- |
| 제품/콘텐츠 검색 | 쇼핑몰 상품 검색, 사내 문서 검색 | 형태소 분석, 유사어, 랭킹 필요 |
| 로그/액세스 로그 분석 | 수억 건 로그에서 에러 패턴 찾기 | RDB는 대량 텍스트 스캔에 부적합 |
| 보안 이벤트 탐지 (SIEM) | 이상 패턴 실시간 탐지 | 시계열 + 전문 검색 + 집계 조합 |
| AI 질의응답 (RAG) | 사용자 질문과 의미적으로 유사한 문서 찾기 | 키워드 매칭으로는 의미 파악 불가 |
| 자동완성/추천 | 타이핑 중 실시간 제안 | ms 단위 응답 + prefix 매칭 + 인기도 반영 |

### 검색 방식 비교 — 키워드 vs 시맨틱 vs 하이브리드

| 방식 | 동작 원리 | 장점 | 단점 |
| --- | --- | --- | --- |
| **키워드 (BM25)** | 역인덱스 + TF-IDF/BM25 스코어링 | 정확한 용어 매칭, 빠름, 예측 가능 | "자동차"로 검색하면 "차량" 못 찾음 |
| **시맨틱 (벡터)** | 텍스트를 임베딩 벡터로 변환 → 코사인 유사도 | 의미 기반, 유사어/다국어 대응 | 정확한 고유명사/코드 검색에 약함 |
| **하이브리드** | 키워드 + 벡터 결과를 결합 (RRF 등) | 양쪽 장점 조합 | 복잡도 증가, 튜닝 필요 |

벡터 검색 상세는 [벡터 스토어](../ai/vector-store.md)를 참고하세요.

### 기술 계보

```
Apache Lucene (검색 엔진 라이브러리)
  ├─ Apache Solr (2004~, 독립 검색 서버)
  └─ Elasticsearch (2010~, 분산 검색 + 분석)
       └─ OpenSearch (2021~, AWS 포크, Apache 2.0 라이선스)
```

- **Solr**: 여전히 사용되지만 클라우드 관리형 서비스가 거의 없음. 온프렘 레거시에 남아있는 경우 많음
- **Elasticsearch**: Elastic사가 라이선스 변경 (SSPL). Elastic Cloud로 관리형 제공
- **OpenSearch**: AWS가 포크. 클라우드 관리형의 주류. Valkey와 비슷한 맥락 (라이선스 이슈 → 오픈소스 포크)

### 로그 분석이 왜 "검색"인가

로그 분석의 핵심은 **대량 비정형 텍스트에서 패턴을 찾는 것**입니다. 전문 검색 엔진(역인덱스)이 이 작업에 적합하기 때문에 ELK/EFK 스택(Elasticsearch + Logstash/Fluentd + Kibana)이 로그 분석의 사실상 표준이 되었습니다.

### 검색 유형 요약

"검색"은 용도에 따라 전혀 다른 서비스를 사용합니다.

| 유형 | 목적 | 대표 기술 |
| --- | --- | --- |
| **전문 검색** (Full-text) | 텍스트 키워드 매칭, 형태소 분석 | Elasticsearch/OpenSearch, Solr |
| **벡터 검색** (Semantic) | 의미 기반 유사도 검색 (AI/RAG) | 벡터 DB, pgvector |
| **로그 분석** | 대량 로그 수집·검색·시각화 | OpenSearch, Loki, BigQuery |

이 문서는 전문 검색과 로그 분석에 집중합니다.

## 벤더별 서비스 비교

| 벤더 | 전문 검색 | AI 검색 (하이브리드) | 로그 분석 |
| --- | --- | --- | --- |
| AWS | [OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) | OpenSearch + k-NN | [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/) |
| Azure | [Azure AI Search](https://learn.microsoft.com/azure/search/) | AI Search (벡터 + 키워드 + 시맨틱) | [Log Analytics](https://learn.microsoft.com/azure/azure-monitor/logs/) |
| GCP | — (Firestore 전문 검색 제한적) | [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs) | [Cloud Logging](https://cloud.google.com/logging/docs) + [BigQuery](https://cloud.google.com/bigquery/docs) |
| OCI | [OCI Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm) | OpenSearch + k-NN | [OCI Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm) |

## 언제 무엇을 선택할 것인가

| 요구사항 | 권장 |
| --- | --- |
| 제품 카탈로그 검색 (키워드 + 필터) | OpenSearch, Azure AI Search |
| AI 기반 질의응답 (RAG) | [벡터 스토어](../ai/vector-store.md) + 하이브리드 검색 |
| 대량 로그 검색 + 대시보드 | OpenSearch (Dashboards), Log Analytics, Cloud Logging |
| 비용 최소화 로그 장기 보관 + 쿼리 | S3 + Athena, BigQuery, OCI Object Storage + Logging Analytics |
| 한국어 형태소 분석 필요 | OpenSearch (nori 플러그인), Azure AI Search (한국어 분석기) |

## 참고하기

### AWS

- [Amazon OpenSearch Service 문서](https://docs.aws.amazon.com/opensearch-service/)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)

### Azure

- [Azure AI Search 문서](https://learn.microsoft.com/azure/search/)
- [Log Analytics 문서](https://learn.microsoft.com/azure/azure-monitor/logs/)

### GCP

- [Vertex AI Search 문서](https://cloud.google.com/generative-ai-app-builder/docs)
- [Cloud Logging 문서](https://cloud.google.com/logging/docs)

### OCI

- [OCI Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm)
- [OCI Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm)
