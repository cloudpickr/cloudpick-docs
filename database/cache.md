---
description: 인메모리 캐시의 개념, 캐시 패턴, 벤더별 관리형 서비스를 비교합니다.
---

# 캐시와 인메모리 데이터베이스

> 문서 기준: 2026년 5월

## 개요

데이터베이스 조회는 디스크 I/O가 발생하여 수 ms\~수십 ms가 걸립니다. **인메모리 캐시**는 자주 조회되는 데이터를 메모리에 저장하여 응답 시간을 마이크로초 단위로 줄입니다.

{% hint style="info" %}
캐시 운영 시 주의할 안티패턴(영구 저장소처럼 사용, TTL 미설정, 캐시 의존 아키텍처 등)은 [데이터베이스 운영 — 캐시 안티패턴](operations.md#캐시-안티패턴)을 참고하세요.
{% endhint %}

## 캐시 패턴

| 패턴 | 동작 | 적합한 경우 |
| --- | --- | --- |
| **Cache-Aside** | 앱이 캐시 확인 → 미스 시 DB 조회 → 캐시 저장 | 읽기 중심, 가장 일반적 |
| **Write-Through** | 앱이 캐시에 쓰기 → 캐시가 DB에 동기 쓰기 | 일관성 중요, 쓰기 지연 허용 |
| **Write-Behind** | 앱이 캐시에 쓰기 → 캐시가 비동기로 DB에 쓰기 | 쓰기 성능 중요, 일시적 불일치 허용 |
| **Read-Through** | 캐시가 DB 조회를 대행 | 캐시 라이브러리가 DB 연동 지원 시 |

## 벤더별 서비스 비교

| 벤더 | 서비스 | 엔진 | 특징 |
| --- | --- | --- | --- |
| AWS | [ElastiCache for Valkey](https://docs.aws.amazon.com/elasticache/) | Valkey (Redis 포크) | **기본 권장**. Serverless 옵션. 벡터 검색 지원 |
| AWS | [ElastiCache for Redis](https://docs.aws.amazon.com/elasticache/) | Redis | 기존 워크로드 호환용 |
| AWS | [MemoryDB for Valkey](https://docs.aws.amazon.com/memorydb/) | Valkey | 내구성 보장 (디스크 영속). 프라이머리 DB로 사용 가능 |
| Azure | [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/) | Redis | Enterprise 티어 (Redis Enterprise 기반) |
| GCP | [Memorystore for Valkey](https://cloud.google.com/memorystore/docs) | Valkey | **기본 권장**. Cluster 모드, 자동 장애 조치 |
| GCP | [Memorystore for Redis](https://cloud.google.com/memorystore/docs) | Redis | 기존 호환용 |
| OCI | [OCI Cache](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm) | Redis 호환 | 관리형 Redis 클러스터 |

{% hint style="info" %}
**Valkey란?** Redis가 2024년 라이선스를 변경(BSD → SSPL/RSALv2)하면서, Linux Foundation 산하에서 오픈소스 포크로 탄생한 프로젝트입니다. 기존 Redis 클라이언트와 호환되며, AWS와 GCP가 기본 엔진으로 전환했습니다. 신규 프로젝트는 Valkey 기반을 권장합니다.
{% endhint %}

## Valkey/Redis vs Memcached

| 항목 | Valkey/Redis | Memcached |
| --- | --- | --- |
| **데이터 구조** | String, Hash, List, Set, Sorted Set, Stream | String만 (key-value) |
| **영속성** | RDB/AOF 스냅샷 가능 | 없음 (순수 캐시) |
| **복제/HA** | 리플리카 + 자동 장애 조치 | 없음 (클라이언트 샤딩) |
| **Pub/Sub** | 지원 | 미지원 |
| **적합한 경우** | 세션 스토어, 리더보드, 실시간 분석, Pub/Sub | 단순 캐시, 대용량 객체 캐싱 |

## 언제 무엇을 선택할 것인가

| 요구사항 | 권장 |
| --- | --- |
| DB 읽기 부하 분산 (일반 캐시) | ElastiCache/Memorystore Redis (Cache-Aside) |
| 세션 스토어 (TTL + 구조화 데이터) | Redis (Hash 타입) |
| 프라이머리 DB 대체 (내구성 필요) | MemoryDB |
| 단순 key-value, 최대 처리량 | Memcached |
| 실시간 리더보드/카운터 | Redis (Sorted Set) |

## 참고하기

### 오픈소스

- [Valkey 공식 사이트](https://valkey.io/) — Linux Foundation 산하 Redis 포크
- [Valkey GitHub](https://github.com/valkey-io/valkey)

### AWS

- [Amazon ElastiCache 문서](https://docs.aws.amazon.com/elasticache/)
- [Amazon MemoryDB 문서](https://docs.aws.amazon.com/memorydb/)

### Azure

- [Azure Cache for Redis 문서](https://learn.microsoft.com/azure/azure-cache-for-redis/)

### GCP

- [Memorystore 문서](https://cloud.google.com/memorystore/docs)

### OCI

- [OCI Cache 문서](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm)
