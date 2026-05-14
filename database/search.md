---
description: 전문 검색, 벡터 검색, 로그 분석 서비스를 벤더별로 비교합니다.
---

# 검색과 로그 분석

> 문서 기준: 2026년 5월

## 개요

"검색"은 용도에 따라 전혀 다른 서비스를 사용합니다.

| 유형 | 목적 | 대표 기술 |
| --- | --- | --- |
| **전문 검색** (Full-text) | 텍스트 키워드 매칭, 형태소 분석 | Elasticsearch/OpenSearch, Solr |
| **벡터 검색** (Semantic) | 의미 기반 유사도 검색 (AI/RAG) | 벡터 DB, pgvector |
| **로그 분석** | 대량 로그 수집·검색·시각화 | OpenSearch, Loki, BigQuery |

벡터 검색의 상세는 [벡터 스토어와 AI 데이터](../ai/vector-store.md)를 참고하세요. 이 문서는 전문 검색과 로그 분석에 집중합니다.

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
