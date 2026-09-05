---
title: "ISMAP (일본 정부 클라우드 조달 인증)"
description: "일본 정부 정보시스템 클라우드 보안평가 제도(ISMAP)의 개요, 등록 프로세스, ISMAP-LIU 구분, 하이퍼스케일러 등록 현황과 외국계 기업의 시사점을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

ISMAP(정부 정보시스템을 위한 보안평가 제도, Information system Security Management and Assessment Program, 政府情報システムのためのセキュリティ評価制度)은 일본 정부기관이 클라우드 서비스를 조달할 때 요구하는 보안 수준을 사전에 평가·등록해두는 제도입니다. 2020년 6월 운용을 시작했으며, 국가사이버통괄실(国家サイバー統括室, NCO — 2025년 7월 NISC를 개편한 조직), 디지털청(デジタル庁), 총무성, 경제산업성이 소관 부처로 참여하고, 정보처리추진기구(IPA)가 등록 심사를 지원하는 운영지원기관 역할을 맡습니다.

일본 정부는 「정부 정보시스템에서의 클라우드 서비스 적절한 이용에 관한 기본방침」을 통해 클라우드 우선 원칙(クラウド・バイ・デフォルト原則)을 채택했고, 디지털청이 구축하는 정부공통 클라우드 기반인 거번먼트 클라우드(ガバメントクラウド)도 ISMAP 등록을 이용 조건으로 두고 있습니다. 즉 ISMAP은 타국의 공공 클라우드 인증(미국의 FedRAMP, 한국의 CSAP 등)과 유사하게, 일본 공공 부문 클라우드 조달의 **사실상 진입 관문** 역할을 합니다.

:::note
ISMAP은 ISO 27001, SOC 2 등 국제 인증과 별개의 일본 고유 제도입니다. 국제 인증을 보유하고 있어도 ISMAP 미등록 상태로는 원칙적으로 일본 정부기관에 클라우드 서비스를 공급할 수 없습니다.
:::

## 등록 프로세스

ISMAP 등록은 대략 아래 순서로 진행됩니다.

1. **대상 서비스 결정** — 등록을 신청할 클라우드 서비스(리전·서비스 범위 포함)를 확정합니다.
2. **내부 통제 체계 구축·운영** — ISMAP 관리기준(정보보호관리기준·거버넌스기준·관리책기준 등)에 맞춰 사내 보안 체계를 구축하고 실제로 운영합니다.
3. **외부 감사** — ISMAP에 등록된 감사기관으로부터 관리기준 준수 여부에 대한 외부 감사를 받습니다.
4. **등록 신청** — 감사 결과를 포함한 서류를 IPA에 제출합니다.
5. **기술 심사** — IPA가 감사 결과의 내용을 기술적으로 검토합니다.
6. **등록 결정** — ISMAP 운영위원회(ISMAP 制度의 최고 의사결정 기구)가 최종 등록 여부를 결정합니다. 신청 접수 후 등록 결정까지 원칙적으로 6개월 이내를 목표로 합니다.

등록 이후에도 연 1회 이상의 갱신 심사가 있어, 일회성 인증이 아니라 지속적으로 유지해야 하는 체계입니다.

### ISMAP과 ISMAP-LIU

비교적 중요도가 낮은 정보를 다루는 SaaS까지 정식 ISMAP 수준의 심사를 요구하면 중소 SaaS 사업자의 진입 장벽이 지나치게 높아진다는 문제의식에서, 2022년 11월 **ISMAP-LIU**(ISMAP for Low-Impact Use, 저위험 이용을 위한 ISMAP)가 도입되었습니다.

| 구분 | ISMAP | ISMAP-LIU |
| --- | --- | --- |
| **대상** | 정부 정보시스템 전반 (기밀성이 높은 정보 포함 가능) | 상대적으로 기밀성이 낮은 정보를 다루는 SaaS |
| **심사 항목** | 관리기준 전체 | 클라우드 인프라·구성에 큰 영향을 미치는 리스크 중심으로 축소 |
| **감사 범위** | 폭넓은 관리 전략 검증 | 핵심 리스크 관련 관리 전략에 집중 |
| **적합 대상** | 대규모 인프라(IaaS/PaaS), 다부처 공통 이용 서비스 | 중소 규모 SaaS, 특정 업무용 SaaS |

:::note
2025년 4월 1일부터 ISMAP-LIU의 사전신청(事前申請) 절차가 폐지되었습니다. 이제 저위험 여부 확인 책임은 조달 시점의 정부 조달기관 쪽으로 이동했으며, 등록 절차 자체는 사실상 일반 ISMAP과 유사하게 운영됩니다. 최신 운영 방식은 [ISMAP 포털](https://www.ismap.go.jp/)에서 확인이 필요합니다.
:::

## 하이퍼스케일러 및 주요 사업자 등록 현황 (2026년 8월 기준)

| 사업자 | 등록 현황 | 비고 |
| --- | --- | --- |
| AWS | 등록됨 (도쿄·오사카 리전 포함, 다수 서비스) | ISMAP 제도 초기부터 등록 유지 (유효기간 만료 전 갱신 반복) |
| Microsoft Azure | 등록됨 (Japan East/Japan West 및 계약상 이용 가능한 해외 리전 포함) | Microsoft 365 등 관련 서비스도 함께 등록 |
| Google Cloud | 등록됨 (Looker 등 개별 서비스 단위로도 순차 등록) | 서비스별로 등록 시점이 다를 수 있어 최신 목록 확인 필요 |
| Oracle Cloud Infrastructure (OCI) | 등록됨 (2021년 6월 최초 등록, 이후 PaaS·Exadata Cloud@Customer 등 확대) | |
| Sakura Internet (さくらのクラウド) | 등록됨 (2021년 12월) | 일본 국내 사업자 중 최초로 거번먼트 클라우드 사업자에도 선정 |
| Cloudflare | 등록됨 (2026년 1월 발표, 효력은 2025년 12월 22일부터) | CDN·WAF·DDoS 방어, Zero Trust, Workers 등 다수 서비스 포함 |

:::caution
위 표는 웹 검색으로 확인한 시점 기준 요약이며, 등록 서비스 범위·리전·유효기간은 사업자별로 다르고 수시로 갱신됩니다. 실제 조달·설계 시에는 반드시 [ISMAP 클라우드 서비스 목록](https://www.ismap.go.jp/csm)에서 대상 서비스명과 리전을 직접 확인하세요.
:::

## 게이트 성격: 미등록 시 공공조달 배제

ISMAP은 인증이라기보다 **조달 자격 목록(리스트)** 성격에 가깝습니다. 정부기관은 원칙적으로 ISMAP 클라우드 서비스 목록 또는 ISMAP-LIU 목록에 등재된 서비스 중에서 조달하도록 되어 있으므로, 목록에 없는 서비스는 개별 심사 절차 없이는 정부 조달 대상에서 사실상 배제됩니다. 거번먼트 클라우드 참여 조건에도 ISMAP 등록이 포함되어 있어, 지방자치단체 시스템의 거번먼트 클라우드 이관이 확대될수록 ISMAP의 영향 범위는 중앙정부를 넘어 지자체·공공기관 전반으로 확장되는 추세입니다.

## 외국계 기업 및 글로벌 SaaS의 일본 공공 진출 시사점

- **진입 장벽이자 신뢰 신호**: ISMAP은 일본 공공 부문 진입의 전제조건이지만, 동시에 등록 자체가 민간 대기업·규제 산업 고객에게도 보안 수준을 입증하는 신호로 활용됩니다. 공공 조달을 목표로 하지 않더라도 참고할 가치가 있습니다.
- **감사·심사 비용과 기간**: 외부 감사기관 선정, 관리기준 대응, IPA 기술 심사, 운영위원회 결정까지 최소 수개월에서 1년 가까이 소요될 수 있어, 일본 진출 로드맵에 조기에 반영해야 합니다.
- **ISMAP-LIU 활용 여지**: 정부 전체 시스템이 아닌 특정 업무용 SaaS로 시작하는 외국계 기업이라면 ISMAP-LIU 경로가 상대적으로 부담이 적습니다. 다만 2025년 4월 사전신청 폐지 이후 절차가 일반 ISMAP에 가까워졌으므로 최신 요건을 확인해야 합니다.
- **현지 법인·현지 감사 대응 필요**: 감사·심사 과정에서 일본어 문서화, 일본 현지 감사기관과의 협업이 사실상 필수적입니다.
- **외국계 기업의 등록 현황**: 글로벌 하이퍼스케일러 외에 비일본계 독립 SaaS 기업의 등록 사례는 상대적으로 제한적이므로 사전 준비가 중요합니다 (최신 등록 현황은 ISMAP 포털에서 직접 조회 권장).

## 참고하기

- [ISMAP 포털](https://www.ismap.go.jp/) — 등록 서비스 목록·제도 규정 원문
- [ISMAP 제도 개요 (NISC·디지털청·총무성·경제산업성, 2023년 11월)](https://www.ismap.go.jp/csm/sys_attachment.do?sys_id=4560318293da26102e57189dc7373c60)
- [ISMAP-LIU 소개 자료 (2025년 4월 1일)](https://www.ismap.go.jp/csm/sys_attachment.do?sys_id=097c91ad8369fa10aa68c6a8beaad316)
- [내각 사이버시큐리티센터: 정부 정보시스템을 위한 보안평가 제도(ISMAP)](https://www.cyber.go.jp/policy/group/general/ismap.html)
- [AWS ISMAP 컴플라이언스 페이지](https://aws.amazon.com/compliance/ismap/)
- [Microsoft ISMAP 컴플라이언스 페이지](https://learn.microsoft.com/compliance/regulatory/offering-ismap)
- [Google Cloud ISMAP 등록 관련 발표](https://cloud.google.com/blog/ja/products/identity-security/google-cloud-completes-ismap-registration-for-looker)
- [Oracle Cloud Infrastructure ISMAP 대응](https://www.oracle.com/jp/corporate/cloud-compliance/ismap/)
- [さくらのクラウド ISMAP 안내](https://manual.sakura.ad.jp/cloud/ismap/index.html)
- [Cloudflare ISMAP 등록 발표 (2026년 1월)](https://www.cloudflare.com/press/press-releases/2026/cloudflare-successfully-completes-ismap-registration-to-support-japans/)
