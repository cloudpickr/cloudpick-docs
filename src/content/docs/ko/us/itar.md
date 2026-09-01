---
title: "ITAR/EAR"
description: "방산·항공우주 기술 데이터 수출통제 규정 ITAR/EAR가 클라우드 아키텍처에 갖는 의미와 FedRAMP와의 차이를 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

ITAR(International Traffic in Arms Regulations)와 EAR(Export Administration Regulations)는 미국의 수출통제 규정으로, 방산·항공우주·이중용도(dual-use) 기술이 국외로 유출되는 것을 통제합니다.

- **ITAR**: 국무부(State Department) 산하 DDTC(Directorate of Defense Trade Controls)가 관장하며, USML(United States Munitions List)에 등재된 방산 물자·서비스·기술 데이터를 규율합니다.
- **EAR**: 상무부(Commerce Department) 산하 BIS(Bureau of Industry and Security)가 관장하며, 상용·이중용도 품목·기술(첨단 반도체, 암호화 소프트웨어 등)을 ECCN(Export Control Classification Number) 체계로 분류·통제합니다.

하나의 품목·기술은 ITAR 또는 EAR 둘 중 하나로만 분류되며, 일반적으로 ITAR가 EAR보다 훨씬 엄격합니다. ITAR는 위반 시 형사상 건당 최대 100만 달러 벌금 및 최대 20년 징역에 처할 수 있습니다. EAR도 형사 처벌은 건당 최대 100만 달러·최대 20년 징역으로 동일한 수준이며, 행정(민사) 제재는 건당 최대 약 37만 달러(물가연동 조정, 2025년 기준 $374,474) 또는 거래액의 2배 중 큰 금액입니다.

| 구분 | ITAR | EAR |
| --- | --- | --- |
| **관장 기관** | 국무부 DDTC | 상무부 BIS |
| **대상 품목** | 방산 물자·서비스·기술 데이터 (USML) | 상용·이중용도 품목·기술 (ECCN) |
| **등록 의무** | 제조·수출업체 사전 등록 필수 | 별도 사전 등록 요건 없음 |
| **라이선스 예외** | 매우 제한적 | 상대적으로 다양한 예외 존재 |

:::note
품목·기술이 ITAR와 EAR 중 어디에 해당하는지 판단하는 것(Jurisdiction/Classification)은 그 자체로 전문적인 법률 판단 영역입니다. 자체 판단이 어려운 경우 DDTC의 CJ(Commodity Jurisdiction) 절차나 수출통제 전문 변호사의 자문을 거치는 것이 안전합니다.
:::

## US Persons 접근 제한이 클라우드에 갖는 의미

ITAR로 통제되는 기술 데이터(technical data)는 원칙적으로 **US Person**(미국 시민권자, 영주권자, 특정 보호 대상자, 미국 내에 설립된 법인 등)만 접근할 수 있으며, 외국인(Foreign Person)이 접근하려면 DDTC의 별도 허가(라이선스, TAA 등)가 필요합니다. 이를 클라우드 환경에 적용하면 다음을 의미합니다.

- 별도 예외가 없는 한, 기술 데이터가 저장되는 서버는 미국 내(CONUS)에 두고 운영·유지보수 인력도 US Person으로 제한하는 것이 기본 전제입니다. 다만 §120.54의 종단간 암호화 요건을 충족한 데이터의 국외 전송·저장은 "수출"로 간주되지 않는 예외가 있어, 법률상 일률적인 미국 내 저장 의무는 아닙니다(아래 종단간 암호화 예외 참조).
- 클라우드 콘솔 로그인, 파일 업로드, 화면 공유 등으로 외국인이 미허가 상태에서 데이터를 열람하는 것도 "수출"(deemed export)로 간주될 수 있습니다.
- 따라서 IAM 정책만으로 국적 기반 접근 통제를 완벽히 구현하기는 어렵고, 조직 구조(별도 US Person 전담팀·자회사 구성)와 클라우드 환경 선택을 함께 설계해야 실효성 있는 통제가 가능합니다.
- **2020년 암호화 예외 규정(End-to-End Encryption Carve-out)**: 2020년 3월 25일 발효된 개정 규칙에 따라, ITAR 기술 데이터가 FIPS 140-2 수준의 종단간(end-to-end) 암호화로 보호되고 복호화 수단(키)이 클라우드 벤더를 포함한 제3자에게 제공되지 않는 경우, 해당 데이터가 국외 서버를 경유·저장되더라도 "수출"로 간주하지 않습니다. 단, 벤더가 키를 보유하는 서버 측 암호화(server-side encryption)는 이 예외에 해당하지 않으며, 비인가 외국인이 평문 상태로 데이터에 접근하면 암호화 여부와 무관하게 수출로 간주됩니다. 중국, 러시아, 이란, 북한 등 무기 금수국은 이 예외에서도 제외됩니다.

## FedRAMP와의 차이

ITAR와 FedRAMP는 성격이 다른 별개의 요건입니다.

- FedRAMP는 클라우드 서비스의 보안 통제를 평가·인가하는 **인증 프로그램**인 반면, ITAR는 특정 기술 데이터의 수출을 규율하는 **법 규정**입니다. ITAR에는 "ITAR 인증"이라는 공식 자격 자체가 존재하지 않으며, 준수 책임은 데이터를 다루는 기업(수출자) 자신에게 있습니다.
- **FedRAMP 인가를 받았다고 해서 ITAR를 준수하는 것은 아닙니다.** 예를 들어 FedRAMP Moderate 수준의 CUI 처리 요건을 충족하더라도, 종단간 암호화 등 추가 조치 없이는 ITAR 요건을 만족하지 못할 수 있습니다.
- 실무적으로는 AWS GovCloud, Azure Government처럼 ITAR 대응 환경으로 설계된 리전이 동시에 FedRAMP High 인가도 보유한 경우가 많아 두 요건이 함께 언급되지만, 이는 벤더가 두 요건을 모두 충족하도록 인프라를 설계했기 때문이지 FedRAMP 인가 자체가 ITAR 준수를 보장하기 때문이 아닙니다. ITAR 준수 여부는 최종적으로 데이터를 다루는 기업이 스스로 입증해야 합니다.

## GovCloud, GCC High 등 대응 환경

| 환경 | ITAR/EAR 대응 특징 |
| --- | --- |
| **AWS GovCloud (US)** | 미국 내 물리적 위치, AWS 운영 인력을 미국 시민권자로 제한. 계정 소유자는 US Person이어야 하며, 유효한 DDTC 등록을 유지해야 함. 단, GovCloud 내 애플리케이션 사용자(IAM 사용자) 자체가 반드시 US Person일 필요는 없음 — 데이터 접근 통제는 고객이 설계 |
| **Microsoft GCC High** | Microsoft 365를 Azure Government 인프라 위에 배포한 환경. 미국 내 데이터센터, 심사받은 미국 시민권자 인력만 접근. DFARS 252.204-7012, ITAR, EAR, CMMC Level 2/3 요건을 충족하는 유일한 Microsoft 365 환경. 표준 GCC(GCC High 이전 단계)는 ITAR/EAR을 지원하지 않으므로 혼동하지 않도록 주의 |
| **Google Cloud Assured Workloads (ITAR 제어 패키지)** | 미국 리전으로 데이터 상주 제한, 고객 관리 암호화 키(CMEK) 필수, ITAR 관련 기술 지원은 미국 내 US Person으로 라우팅. Premium 등급에서 제공 |
| **OCI Government Cloud** | Oracle 정부 전용 리전에서 유사한 미국 인력·데이터 상주 통제 제공 |

## 방산·항공우주 협력 한국 기업의 유의점

- 한국 기업이 미국 방산·항공우주 프라임 업체와 기술 데이터를 주고받는 경우, 한국 국적 임직원은 원칙적으로 Foreign Person에 해당하여 ITAR 기술 데이터에 직접 접근할 수 없습니다. TAA(Technical Assistance Agreement), MLA(Manufacturing License Agreement) 등 DDTC 허가를 사전에 확보하거나, 미국 내 US Person으로 구성된 별도 조직·자회사를 통해서만 데이터를 취급하는 구조가 필요합니다.
- 클라우드에 업로드·다운로드하는 행위 자체가 "수출"로 간주될 수 있으므로, 협업 툴·파일 공유 서비스 선택 시 ITAR 대응 여부(GCC High 등)를 먼저 확인해야 합니다. 표준 상용 클라우드(GCC, 일반 Microsoft 365, 일반 Google Workspace 등)는 ITAR 기술 데이터 저장에 적합하지 않습니다.
- 종단간 암호화 예외 규정을 활용하면 반드시 미국 인프라를 쓰지 않고도 준수할 여지가 있지만, 키 관리를 벤더가 아닌 자사(또는 신뢰할 수 있는 US Person)가 전적으로 통제해야 하므로 구현 난도가 높습니다. 도입 전 수출통제 전문 법률 자문을 받는 것이 안전합니다.
- 동일한 CUI(통제 미분류 정보)를 다루는 계약은 ITAR와 별개로 CMMC/NIST SP 800-171 요건이 함께 부과되는 경우가 많습니다. 자세한 내용은 [FedRAMP](../../us/fedramp/) 문서의 CMMC 2.0 섹션을 참고하세요.
- EAR 대상 이중용도 기술(예: 첨단 반도체 설계 데이터, 특정 암호화 기술)은 ITAR보다 상대적으로 유연하지만 여전히 라이선스가 필요할 수 있으므로, 데이터가 ITAR·EAR 중 어느 쪽으로 분류되는지부터 사전에 확인해야 합니다.
- FedRAMP 인가 획득 자체를 목표로 하는 경우와 달리, ITAR/EAR 대응은 별도의 "인가 취득" 프로젝트가 아니라 조직의 데이터 취급 프로세스 전반(계약, 인사, 접근 통제, 클라우드 아키텍처)에 걸친 지속적 준수 체계로 접근해야 합니다.

:::caution
ITAR/EAR 위반은 형사 처벌까지 이어질 수 있는 중대한 법적 리스크입니다. 이 문서는 아키텍처 관점의 일반적인 개요이며, 실제 계약·프로젝트 진행 전에는 반드시 수출통제 전문 법률 자문을 받아야 합니다.
:::

## 관련 문서

- [규정 준수 (Compliance)](../../governance/compliance/)
- [망분리와 네트워크 격리](../../security/network-isolation/)

## 참고하기

- [DDTC (ITAR 관장 기관)](https://www.pmddtc.state.gov/)
- [BIS EAR 공식 페이지](https://www.bis.gov/)
- [AWS GovCloud ITAR 준수 가이드](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-itar.html)
- [AWS ITAR 컴플라이언스](https://aws.amazon.com/compliance/itar/)
- [Google Cloud Assured Workloads — ITAR 데이터 경계](https://docs.cloud.google.com/assured-workloads/docs/control-packages/itar)
- [Microsoft GCC High 개요](https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/office-365-us-government/gcc-high-and-dod)
