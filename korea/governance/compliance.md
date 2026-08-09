---
description: ISMS-P, CSAP, 금융권 규제 등 한국의 클라우드 규정 준수 인증과 요건을 정리합니다.
---

# 컴플라이언스 (한국)

> 문서 기준: 2026년 8월

## 개요

한국에서 클라우드를 도입할 때는 국제 인증(ISO 27001, SOC 2 등) 외에 한국 고유의 인증·규제를 충족해야 합니다. 공동 책임 모델, 컴플라이언스 운영 자동화 등 **규정 준수의 일반 원칙**은 [규정 준수 (Compliance)](../../governance/compliance.md)에서 다루며, 이 문서는 그 위에 얹히는 **한국 규제 레이어**입니다.

## ISMS-P (정보보호 및 개인정보보호 관리체계 인증)

- **근거 법률**: 정보통신망법, 개인정보 보호법
- **운영**: [KISA (한국인터넷진흥원)](https://isms.kisa.or.kr/)
- **대상**: 정보통신서비스 부문 매출액 100억 원 이상 또는 일평균 이용자 100만 명 이상인 정보통신서비스 제공자 등 (매출액 1,500억 원 기준은 상급종합병원·대학 등 별도 유형에 적용)
- **유효 기간**: 3년, 연 1회 사후 심사
- **클라우드 영향**: 클라우드에 민감 정보를 저장·처리하는 경우, 벤더의 ISMS-P 인증 범위 내 리전을 사용해야 함

공식 벤더별 페이지:

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- OCI: 공식 컴플라이언스 페이지에서 인증 현황 확인

### ISMS-P vs ISO 27001 핵심 차이

| 구분 | ISMS-P | ISO 27001 |
| --- | --- | --- |
| **적용 범위** | 80+22개 기준 전체 충족 필수 | 적용 범위를 조직이 선택 가능 (SoA로 "해당 없음" 가능) |
| **개인정보보호** | 포함 (개인정보 처리 단계별 요구사항) | 미포함 (별도 ISO 27701 필요) |
| **성격** | 한국법 의무 대상 있음 (정보통신서비스 제공자 등) | 국제 자율 인증 |
| **공통점** | 기술뿐 아니라 업무 프로세스(정책, 인력, 변경 관리)를 심사 | ← 동일 |

## CSAP (클라우드 보안 인증제)

- **근거 법률**: 클라우드 컴퓨팅 발전법 제23조의2
- **운영**: [KISA](https://isms.kisa.or.kr/main/csap/intro/)
- **대상**: 공공기관에 클라우드 서비스를 제공하려는 모든 CSP
- **등급 체계** (2024년 상·중·하 등급제 전면 시행):

| 등급 | 대상 시스템 | 요구 수준 |
| --- | --- | --- |
| **상** | 안보·외교 등 국가 중대이익 관련 시스템, 행정기관 내부 업무 시스템 | 물리적 망 분리, 국내 리전, 국내 인력 운영 등 엄격 |
| **중** | 개인정보·중요 정보를 처리하는 일반 공공 시스템 | 논리적 망분리 등 상 등급 대비 완화 |
| **하** | 개인정보를 포함하지 않는 공개 데이터 시스템 (글로벌 CSP 진입 가능) | 최소 보안 요건 |

**글로벌 CSP의 CSAP 인증 현황 (2025년 기준):**

| 벤더 | 등급 | 리전 | 참고 |
| --- | --- | --- | --- |
| AWS | 하 (Low-tier) | 서울 `ap-northeast-2` | [AWS CSAP 공지](https://aws.amazon.com/blogs/security/aws-achieves-cloud-security-assurance-program-csap-low-tier-certification-in-aws-seoul-region/) |
| Azure | 하 (Low-tier) | Korea Central / South | [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap) |
| Google Cloud | 하 (Low-tier) | Seoul `asia-northeast3` | [Google Cloud CSAP](https://cloud.google.com/security/compliance/csap) |
| OCI | — (공식 페이지 확인) | Seoul, Chuncheon | [Oracle 컴플라이언스](https://www.oracle.com/corporate/cloud-compliance/) |

{% hint style="info" %}
CSAP 제도는 N2SF(국가망보안체계) 1.0 공개(2025.9)에 따라 등급별 차등 보안 체계와의 연계가 진행 중입니다. 도입 전 [KISA 공식 사이트](https://isms.kisa.or.kr/main/csap/intro/)와 [NCSC](https://www.ncsc.go.kr)에서 최신 현황을 확인하세요.
{% endhint %}

{% hint style="info" %}
CSAP 등급별 상세 요건, 하이퍼스케일러·국내 CSP 인증 현황, 2027년 국정원 단일 검증체계 개편 동향은 [CSAP (클라우드 보안 인증)](../security/csap.md)에서 깊이 있게 다룹니다.
{% endhint %}

## 금융권 관련 규제

금융 분야는 추가 규제가 적용됩니다.

- **전자금융거래법 / 전자금융감독규정** — 금융회사의 클라우드 이용 시 안전성 확보 요건
- **금융보안원 (FSI)** — 금융권 클라우드 이용 가이드 발간, 보안 컨설팅 제공
- **망분리 규제** — 개인신용정보 처리 시스템은 일반 업무망과 분리 운영 필요. N2SF 1.0에 따라 등급별 차등 적용으로 전환 중 ([망분리와 네트워크 격리](../../security/network-isolation.md) 참고)

공식 자료:

- [금융보안원 클라우드 이용 가이드](https://www.fsec.or.kr/) (통합 인덱스 활용)
- [금융위원회](https://www.fsc.go.kr/)

## 참고하기

- [KISA 인증 · 인정](https://isms.kisa.or.kr/)
- [개인정보보호위원회](https://www.pipc.go.kr/)
- [금융보안원](https://www.fsec.or.kr/)

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/) / [AWS CSAP](https://aws.amazon.com/compliance/csap/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms) / [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
