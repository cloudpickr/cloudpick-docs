---
title: "AI 정책과 거버넌스"
description: "미국 연방 AI 행정명령 흐름, 주(州)-연방 선점 갈등, NIST AI RMF, 연방 조달 AI 요건과 클라우드 AI 워크로드 실무 시사점을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

미국의 AI 정책은 2023년 이후 행정부 교체와 함께 방향이 크게 바뀌었고, 2025–2026년에도 행정명령이 잇따라 발표·폐지되며 유동적인 상태가 이어지고 있습니다. 연방 차원은 "규제보다 혁신 촉진"을 축으로 재편되었지만, 동시에 주(state) 단위 AI법은 계속 늘어나고 있어 연방과 주 사이의 선점(preemption) 갈등이 2026년의 핵심 이슈로 떠올랐습니다. 이 문서는 연방 행정명령의 흐름, NIST의 기술 표준, 연방 조달 요건, 그리고 주요 주법 동향을 정리하고 클라우드 AI 워크로드 운영에 대한 실무 시사점을 다룹니다.

:::caution
AI 정책은 2025–2026년 행정부 전환기 동안 발표·폐지·재발표가 반복되어 왔고, 언론·법무법인 보도 간에도 해석 차이가 있습니다. 아래 내용은 백악관(whitehouse.gov), NIST(nist.gov), OMB 공식 문서를 기준으로 확인한 사실이며, 실제 적용 시점에는 반드시 공식 출처에서 최신 상태를 재확인해야 합니다.
:::

## 연방 AI 행정명령 흐름

| 시점 | 조치 | 핵심 내용 |
| --- | --- | --- |
| 2023.10.30 | **EO 14110** (바이든 행정부) | "Safe, Secure, and Trustworthy Development and Use of AI" — AI 안전성 평가, 형평성·시민권 고려, 연방기관 AI 활용 가이드라인 수립 |
| 2025.1.20 | **EO 14148** | EO 14110을 포함한 바이든 행정부 행정명령 다수를 일괄 폐지 |
| 2025.1.23 | **EO 14179** | "Removing Barriers to American Leadership in Artificial Intelligence" — EO 14110을 "위험하고 불필요하게 부담스럽다"고 규정, 혁신 촉진·규제 완화 기조로 전환 |
| 2025.7.23 | **America's AI Action Plan** + 행정명령 3건 | "Winning the Race" — 90여 개 연방 조치를 3대 축(혁신 가속화, AI 인프라 구축, 국제 AI 외교·안보 주도)으로 제시. AI 인프라 인허가 간소화, AI 수출 프로그램 등 동시 서명 |
| 2025.12.11 | **EO 14365** | "Ensuring a National Policy Framework for Artificial Intelligence" — 연방 통일 AI 정책 수립 및 주(州) AI법에 대한 연방 선점을 정책 목표로 명시 |

:::note
EO 14110 폐지는 그 행정명령이 만들어낸 모든 산출물(예: NIST AI RMF, 조달 가이드라인 초안 일부)까지 자동으로 무효화하는 것은 아닙니다. NIST AI RMF 1.0과 생성형 AI 프로파일(AI 600-1)은 행정명령의 존폐와 무관하게 별도 문서로 존속하며, 조달 실무에서 계속 참조되고 있습니다.
:::

## 연방의 주(州) AI법 선점(preemption) 시도 — 진행 중인 사안

연방 행정부는 2025년부터 입법·행정명령 양 경로로 주 AI법을 무력화하려는 시도를 이어왔습니다.

- **입법 시도 실패**: 2025년 예산조정법안("One Big Beautiful Bill Act")에 10년간 주(州)의 AI 규제 집행을 금지하는 조항이 포함되었으나, 아동안전 예외를 둔 절충안 협상이 결렬되며 상원 표결에서 **99대1로 해당 조항이 삭제**되었습니다. 2026 회계연도 국방수권법(NDAA)에도 유사한 선점 조항이 논의되었으나 최종안에는 포함되지 않았습니다.
- **행정명령 경로**: 2025년 12월 11일 서명된 **EO 14365**는 법무부 산하에 "AI 소송 태스크포스(AI Litigation Task Force)"를 **2026년 1월 9일 설치**하도록 지시했으며, 이 조직이 주 AI법이 주간통상(interstate commerce)을 부당하게 저해하거나 연방 규제에 의해 선점된다는 논리로 연방법원에 소송을 제기하도록 했습니다. 실제 개입 사례로는 2026년 4월 24일 법무부가 xAI(현 SpaceXAI)의 콜로라도 AI법(Colorado AI Act) 소송에 참여한 것이 확인됩니다. 또한 상무부에 2026년 3월 11일까지 "과도하게 부담스러운" 주 AI법 목록을 발표하도록 하고, BEAD(광대역 인프라, 총 420억 달러 규모) 프로그램 중 **아직 배정되지 않은 잔여 자금**의 지급 적격성 검토를 "부담스러운 주 AI 규제 폐지" 여부와 연계하는 조건을 부과했습니다(이미 배정·집행된 자금이나 프로그램 전체 420억 달러가 일괄 조건부가 된 것은 아닙니다).

:::caution
**2026년 8월 현재까지 주 AI법을 무효화하는 연방 법률은 제정되지 않았습니다.** EO 14365에 따른 소송·행정 조치는 진행 중이나, 행정명령 자체가 주법을 직접 무효화하지는 못하며 법원 판단을 거쳐야 합니다(아래 콜로라도 사례 참고). 이 사안은 소송·입법 양면에서 계속 변동 중이므로 최신 상태는 백악관·법무부 공식 발표로 재확인이 필요합니다.
:::

## NIST AI 위험관리 프레임워크(AI RMF) 1.0 + 생성형 AI 프로파일

**NIST AI RMF 1.0**(2023년 1월 발표)은 조직이 AI 시스템의 위험을 관리하기 위한 **자발적(voluntary)** 프레임워크로, 법적 강제력은 없지만 연방 조달과 민간 거버넌스 모두에서 사실상의 참조 표준으로 자리잡았습니다. Govern·Map·Measure·Manage 4개 핵심 기능으로 구성됩니다.

2024년 7월 26일 발표된 **NIST AI 600-1(생성형 AI 프로파일, Generative AI Profile)** 은 AI RMF를 생성형 AI에 특화해 확장한 문서로, 환각(confabulation/hallucination), 데이터 포이즈닝, 프롬프트 인젝션, 지적재산권 침해, 과잉 신뢰(over-reliance) 등 **생성형 AI에 고유하거나 기존보다 악화되는 12개 위험 범주**를 식별하고 대응 조치를 제시합니다.

- 공급망 취약점·제3자 모델 평가 관련 위험은 2024년 7월 26일 발행된 원문에 이미 포함되어 있습니다. 일부 매체가 2025년 3월경 개정을 보도했으나, 2026년 8월 기준 NIST 공식 사이트에서 확인되는 최신 정식본은 여전히 2024-07-26 발행본입니다(공식 개정 여부는 NIST 발표로 재확인 필요).
- 2025년 12월에는 AI RMF와 사이버보안 프레임워크(CSF) 2.0을 연결하는 **Cyber AI 프로파일(NIST IR 8596) 초안**이 공개되어, AI 시스템 자체의 사이버보안 리스크 관리로 적용 범위가 확장되고 있습니다.

## 연방 조달의 AI 요건 — OMB 메모

행정명령 전환에 맞춰 OMB(예산관리국)도 연방기관의 AI 사용·조달 지침을 2025년 4월 3일 전면 개정했습니다. 기존 바이든 행정부의 M-24-10을 폐지하고 다음 두 메모로 대체했습니다.

- **M-25-21**(Accelerating Federal Use of AI through Innovation, Governance, and Public Trust): 기관별 AI 전략 수립, 기관 간 AI 기능 공유, 투자 확대를 지시. "고영향 AI(High-Impact AI)" — 법적·중대한 효과를 낳는 결정의 주된 근거가 되는 AI 시스템 — 를 식별·관리하도록 요구하며, **2026년부터 기관별 AI 활용 사례와 리스크 판정을 연 1회 공개 인벤토리로 보고**하도록 의무화
- **M-25-22**(Driving Efficient Acquisition of Artificial Intelligence in Government): 경쟁적인 AI 조달 시장 조성, 성능 추적을 통한 리스크 관리, 부처 간 협업 조달을 3대 원칙으로 제시. **2025년 9월 30일 이후 공고된 조달 건**부터 적용되며, 벤더가 정부의 비공개 데이터를 명시적 동의 없이 상용 AI 모델 학습에 사용하는 것을 금지하는 계약 조항을 의무화

:::note
두 메모는 NIST AI RMF·AI 600-1을 명시적으로 강제하지는 않지만, 실무적으로는 NIST 프레임워크와의 정합성을 입증할 수 있는 벤더가 조달 평가에서 유리한 위치를 점하는 구조입니다. 정부 대상 AI 서비스를 제공하려는 클라우드·SaaS 벤더는 NIST AI RMF 얼라인먼트 문서화를 사실상의 필수 준비물로 간주하는 것이 안전합니다.
:::

## 주별 AI법 동향

연방의 완화 기조와 반대로 주 단위 AI 입법은 2026년에도 계속 늘어나고 있습니다.

| 주 | 법률 | 현황 (2026년 8월 기준) |
| --- | --- | --- |
| 콜로라도 | Colorado AI Act(SB 24-205) | 원 시행일 2026.2.1 → 2025.8 개정으로 2026.6.30 연기 → **2026.5.14 SB 189로 원안을 폐지·대체**, 고위험 AI 포괄 규제 대신 자동화 의사결정 기술(ADMT) 중심의 공개·권리 프레임워크로 축소, 시행일 **2027.1.1**로 재조정. 이와 별개로 2026.4.27 연방 지방법원이 xAI 소송(DOJ 개입 지지)에서 당사자 간 잠정 합의(stipulated stay)를 승인해 법원의 본안 판단 이후 14일까지 원안(SB 24-205)의 집행을 유예 — 위헌 여부에 대한 본안 판단이 아니라 절차적 스탠드스틸(standstill) 성격 |
| 텍사스 | TRAIGA(Texas Responsible AI Governance Act, HB 149) | 2026.1.1 시행. 콜로라도식 고위험 AI 포괄 규제가 아니라, 자살·범죄 조장 AI·아동성착취물·비동의 딥페이크·정부의 사회적 점수화 등 **금지 행위 열거 + 주정부 AI 사용 공개 의무** 중심의 좁은 접근 |
| 캘리포니아 | SB 53(Transparency in Frontier AI Act), AB 2013(학습데이터 투명성법) | 둘 다 2026.1.1 시행. SB 53은 프런티어 모델 개발사의 안전 프레임워크 공개 의무, AB 2013은 생성형 AI 시스템의 학습데이터 출처·유형·저작권·개인정보 포함 여부 등 상세 문서 공개 의무 |
| 일리노이 | HB 3773 등 | 2026.1.1 시행, 고용 등 영역의 AI 사용 공개·차별 방지 규제 |
| 뉴욕 | RAISE Act 등 | 2027년 적용 예정 조항 포함, 프런티어 모델 안전 규제 방향 |

:::caution
콜로라도 사례가 보여주듯 주 AI법은 **시행일 연기, 개정, 소송을 통한 집행 중지**가 반복되는 매우 유동적인 영역입니다. 특정 주에서 AI 서비스를 운영·확장하기 전에는 해당 주 법무장관실 또는 신뢰할 수 있는 법률 트래커에서 최신 시행 상태를 개별 확인해야 합니다.
:::

## 클라우드 AI 워크로드 실무 시사점

- **연방 행정명령 변화를 계약·컴플라이언스 문서에 실시간 반영하기보다 NIST 표준을 기준선으로 삼기**: 행정명령은 정치적 전환에 따라 빠르게 바뀌지만, NIST AI RMF·AI 600-1은 상대적으로 안정적인 기술 표준이자 조달 실무의 공통 언어로 기능합니다. 거버넌스 문서화의 기준선으로 NIST 프레임워크를 채택하면 정책 변화에도 재작업 부담이 작습니다.
- **연방 조달 대상이라면 M-25-21/M-25-22 요건을 설계 초기에 반영**: 고영향 AI 식별·리스크 판정 체계, 공개 데이터/비공개 데이터 학습 사용 동의 절차를 계약·아키텍처 단계에서 갖춰야 2025년 9월 30일 이후 공고된 조달에 대응할 수 있습니다.
- **주(州) AI법은 "완화 추세"로 일반화하지 않기**: 연방은 규제 완화·선점 방향이지만, 다수 주는 오히려 새 AI법을 계속 제정하고 있습니다. 특히 고용·신용·의료 등 소비자에게 중대한 영향을 미치는 자동화 의사결정을 다루는 워크로드는 콜로라도·캘리포니아·일리노이 등 주요 주의 요건을 개별 추적해야 합니다.
- **투명성·데이터 계보(lineage) 체계를 선제적으로 구축**: 캘리포니아 AB 2013(학습데이터 공개), 콜로라도 ADMT 프레임워크 등은 공통적으로 "무엇으로, 어떻게 학습되었고, 어떤 결정에 쓰이는가"에 대한 문서화를 요구하는 방향으로 수렴하고 있습니다. 모델·데이터셋 계보 관리 체계는 향후 여러 주 요건에 재사용 가능한 자산이 됩니다.
- **선점(preemption) 소송 결과를 모니터링**: EO 14365에 따른 AI 소송 태스크포스의 주법 무효화 시도(콜로라도 사례 등)가 다른 주에도 확산될 수 있어, 특정 주법 준수 계획을 세울 때 해당 법의 법적 효력 자체가 소송으로 흔들릴 가능성을 함께 고려해야 합니다.

## 참고하기

- [백악관 — Removing Barriers to American Leadership in AI (EO 14179)](https://www.whitehouse.gov/presidential-actions/2025/01/removing-barriers-to-american-leadership-in-artificial-intelligence/)
- [백악관 — America's AI Action Plan (2025.7)](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf)
- [백악관 — Ensuring a National Policy Framework for AI (EO 14365, 2025.12)](https://www.whitehouse.gov/presidential-actions/2025/12/eliminating-state-law-obstruction-of-national-artificial-intelligence-policy/)
- [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST — AI RMF: Generative AI Profile (NIST AI 600-1)](https://www.nist.gov/itl/ai-risk-management-framework)
- [OMB — M-25-21, M-25-22 (whitehouse.gov OMB memoranda)](https://www.whitehouse.gov/omb/)
- [Colorado Attorney General — Colorado AI Act](https://coag.gov/)
- [Texas Attorney General — TRAIGA](https://www.texasattorneygeneral.gov/)
- [DOJ — xAI 콜로라도 AI법 소송 개입 발표(2026년 4월)](https://www.justice.gov/opa/pr/justice-department-intervenes-xai-lawsuit-challenging-colorados-algorithmic-discrimination)
- [NIST AI 600-1 원문 PDF (2024년 7월 26일 발행)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
