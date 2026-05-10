# NoSQL

## 개요

관계형 DB(SQL)는 테이블, 행, 열로 데이터를 정형화하고 SQL로 조회합니다. 스키마가 엄격하고 트랜잭션(ACID)을 보장하지만, 대규모 트래픽에서 수평 확장이 어렵고 스키마 변경이 번거롭습니다.

**NoSQL**은 이러한 제약을 완화하여, 유연한 스키마와 수평 확장이 필요한 워크로드에 적합합니다.

### SQL vs NoSQL

| 항목 | SQL (관계형) | NoSQL |
| --- | --- | --- |
| **스키마** | 엄격 (테이블 구조 사전 정의) | 유연 (스키마리스 또는 스키마 온 리드) |
| **확장** | 수직 확장 위주 (더 큰 서버) | 수평 확장 (서버 추가) |
| **트랜잭션** | ACID 보장 | 일부만 지원 (BASE 모델) |
| **조인** | 복잡한 조인 가능 | 조인 없음 또는 제한적 |
| **적합한 경우** | 정형 데이터, 복잡한 관계, 일관성 중요 | 대규모 트래픽, 유연한 구조, 빠른 응답 |

### 어떤 NoSQL을 선택할까?

NoSQL은 데이터 모델에 따라 여러 유형으로 나뉘며, 워크로드에 맞는 유형을 선택해야 합니다.

| 유형 | 데이터 구조 | 이럴 때 선택 | 사용 사례 |
| --- | --- | --- | --- |
| **키-값** (Key-Value) | 키 하나로 값 조회 | 단순 조회가 초고속이어야 할 때 | 세션, 캐시, 설정, 장바구니 |
| **문서** (Document) | JSON/BSON 문서 | 스키마가 자주 바뀌거나 중첩 구조일 때 | 사용자 프로필, 카탈로그, CMS |
| **와이드 컬럼** (Wide Column) | 행마다 컬럼이 다를 수 있음 | 대규모 시계열/이벤트 데이터 쓰기 | IoT, 로그, 분석, 추천 |
| **그래프** (Graph) | 노드 + 엣지(관계) | 데이터 간 관계/연결이 핵심일 때 | 소셜 네트워크, 사기 탐지, 지식 그래프 |

## 제품 비교

### 키-값 / 문서 DB

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | DynamoDB | 완전 서버리스. 밀리초 지연. 용량 자동 확장 |
| Azure | Cosmos DB | 멀티 모델(문서, 키-값, 그래프, 와이드 컬럼). 글로벌 분산 |
| GCP | Firestore | 문서 DB. 모바일/웹 앱에 최적화. 실시간 동기화 |
| GCP | Bigtable | 와이드 컬럼. 대규모 분석/시계열 |
| OCI | OCI NoSQL Database | 키-값 + 문서 + 와이드 컬럼. 서버리스 용량 관리 |

### 인메모리 캐시

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | ElastiCache for Valkey | Valkey(Redis 오픈소스 포크) 기반. 벡터 검색 지원 (v8.2+) |
| AWS | ElastiCache for Redis | Redis 호환. 기존 워크로드용 |
| AWS | MemoryDB for Valkey | Valkey 호환 + 내구성 보장 (디스크 영속화) |
| Azure | Azure Cache for Redis | |
| GCP | Memorystore for Valkey | Valkey 기반. 2025년 출시 |
| GCP | Memorystore for Redis | |
| OCI | OCI Cache with Redis | Redis 호환 관리형 캐시 |

> **Valkey**는 Redis의 오픈소스 포크로, Linux Foundation에서 관리합니다. Redis가 2024년 라이선스를 변경한 이후 AWS, GCP 등이 Valkey로 전환하고 있습니다. 기존 Redis 클라이언트와 호환됩니다.

### 검색 / 로그 분석 엔진

전문 검색(Full-Text Search)이나 대규모 로그 분석에 특화된 엔진입니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | OpenSearch Service | Elasticsearch/OpenSearch 관리형. 검색 + 로그 분석 + 대시보드 |
| Azure | Azure AI Search (구 Cognitive Search) | 검색 + AI 보강(벡터, 시맨틱) |
| GCP | — | Elastic Cloud on GCP (3rd party) 또는 BigQuery 활용 |
| OCI | OCI Search with OpenSearch | OpenSearch 관리형. 검색 + 로그 분석 |

### 그래프 DB

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Neptune | |
| Azure | Cosmos DB (Gremlin API) | |
| GCP | — | (3rd party 사용: Neo4j on GCP) |

## 핵심 차이점

**AWS DynamoDB** — 완전 서버리스로 용량 관리가 불필요합니다. 단일 자릿수 밀리초 지연을 보장하며, DAX(인메모리 캐시)를 추가하면 마이크로초 지연도 가능합니다.

**Azure Cosmos DB** — 하나의 서비스로 문서, 키-값, 그래프, 와이드 컬럼을 모두 지원합니다. 글로벌 분산(멀티 리전 쓰기)이 기본 기능으로 내장되어 있습니다.

**GCP Firestore** — 모바일/웹 클라이언트에서 직접 접근할 수 있는 실시간 동기화가 강점입니다. Bigtable은 대규모 분석 워크로드에 특화되어 있습니다.

**OCI NoSQL Database** — 키-값, 문서, 와이드 컬럼을 하나의 서비스로 지원하며, 서버리스 용량 관리와 예측 가능한 저지연 성능을 제공합니다.

## 참고하기

### AWS

- [Amazon DynamoDB 문서](https://docs.aws.amazon.com/ko_kr/dynamodb/)
- [Amazon ElastiCache 문서](https://docs.aws.amazon.com/ko_kr/elasticache/)
- [Amazon Neptune 문서](https://docs.aws.amazon.com/ko_kr/neptune/)

### Azure

- [Azure Cosmos DB 문서](https://learn.microsoft.com/ko-kr/azure/cosmos-db/)
- [Azure Cache for Redis 문서](https://learn.microsoft.com/ko-kr/azure/azure-cache-for-redis/)

### GCP

- [Firestore 문서](https://cloud.google.com/firestore/docs)
- [Bigtable 문서](https://cloud.google.com/bigtable/docs)
- [Memorystore 문서](https://cloud.google.com/memorystore/docs)

### OCI

- [OCI NoSQL Database 문서](https://docs.oracle.com/en-us/iaas/nosql-database/index.html)
- [OCI Cache with Redis 문서](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm)
- [OCI Search with OpenSearch 문서](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm)
