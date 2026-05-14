---
description: 범용, Arm, GPU 가상머신 제품과 이미지(OS 템플릿)를 벤더별로 비교합니다.
---

# 가상머신

> 문서 기준: 2026년 5월

## 개요

자체 전산센터에서 서버를 운영하려면 하드웨어 구매, 설치, OS 설정, 네트워크 구성을 직접 해야 합니다. 장비 도입에 수 주가 걸리고, 사양을 바꾸려면 물리적으로 교체해야 합니다.

**가상머신** (VM)은 이 과정을 소프트웨어로 대체합니다. 몇 분 안에 원하는 사양의 서버를 생성하고, 필요 없어지면 즉시 삭제할 수 있습니다. 물리 서버의 유연성 문제를 해결한 클라우드의 가장 기본적인 서비스입니다.

다만 VM은 여전히 OS 패치, 보안 설정, 장애 대응을 사용자가 직접 관리해야 합니다. 이 관리 부담을 줄이기 위해 컨테이너, 서버리스 같은 더 높은 수준의 추상화가 등장했습니다.

## 제품 비교

### 범용 VM

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | EC2 (Elastic Compute Cloud) | 가장 다양한 인스턴스 유형 (400+) |
| Azure | Virtual Machines | Windows 워크로드에 강점 (Hybrid Benefit) |
| GCP | Compute Engine | Custom Machine Type으로 CPU/메모리 자유 조합 |
| OCI | OCI Compute | Flexible Shape으로 CPU/메모리 자유 조합. Ampere A1 무료 티어 |

### Arm 기반 VM

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | EC2 Graviton (t4g, m7g 등) | 자체 설계 Arm 프로세서. x86 대비 높은 가격 대비 성능 |
| Azure | Dpsv5/Dplsv5 시리즈 | Ampere Altra 기반 |
| GCP | Tau T2A | Arm 기반 범용 |
| OCI | Ampere A1 Compute | Ampere Altra 기반. 무료 티어 제공 |

### GPU / AI 가속기

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | P5, G5, Inf2, Trn1 | NVIDIA + 자체 칩(Inferentia, Trainium) |
| Azure | NC, ND, NV 시리즈 | NVIDIA A100, H100 |
| GCP | A2, G2 시리즈 + TPU | NVIDIA + 자체 TPU |
| OCI | GPU Instances (A10, A100, H100) | NVIDIA GPU. Bare Metal 옵션 제공 |

### 이미지 (OS 템플릿)

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | AMI (Amazon Machine Image) | Marketplace에서 3rd party 이미지 제공 |
| Azure | VM Image / Shared Image Gallery | |
| GCP | Image / Image Family | |
| OCI | Custom Image / Platform Image | Marketplace에서 3rd party 이미지 제공 |

{% hint style="info" %}
VM은 **관리 부담이 가장 큰 컴퓨팅 서비스**입니다. OS 패치, 보안 설정, 고가용성 구성을 직접 해야 합니다. 운영 부담을 줄이고 싶다면 관리형 컨테이너 서비스나 서버리스를 검토하세요.
{% endhint %}

## 핵심 차이점

- **AWS** — 인스턴스 유형이 가장 다양하고, 자체 Arm 프로세서(Graviton)로 비용 절감 가능합니다.
- **Azure** — 기존 Windows 라이선스를 활용한 Hybrid Benefit으로 비용을 줄일 수 있습니다.
- **GCP** — CPU와 메모리를 자유롭게 조합하는 Custom Machine Type을 제공합니다.
- **OCI** — Flexible Shape으로 CPU/메모리를 자유 조합하며, Ampere A1 무료 티어를 제공합니다.

## 언제 무엇을 선택할 것인가

| 이럴 때 | 이것을 선택 |
| --- | --- |
| Windows 워크로드 + 기존 라이선스 활용 | Azure VM (Hybrid Benefit) |
| 인스턴스 유형 선택지가 가장 많아야 할 때 | AWS EC2 |
| CPU/메모리를 1 vCPU 단위로 자유 조합하고 싶을 때 | GCP Compute Engine (Custom Machine Type) 또는 OCI (Flexible Shape) |
| Arm 기반 비용 절감이 목표일 때 | AWS EC2 Graviton |
| 무료 티어로 Arm VM을 사용하고 싶을 때 | OCI Ampere A1 |
| GPU/AI 가속기 + 자체 칩(Inferentia, Trainium)이 필요할 때 | AWS EC2 (P5, Inf2, Trn1) |
| Bare Metal 서버가 필요할 때 | OCI Bare Metal 또는 AWS Bare Metal |

## 구매 옵션 (가격 모델)

같은 VM이라도 약정 방식에 따라 가격이 크게 차이납니다.

| 옵션 | 설명 | 할인율 | 위험 |
| --- | --- | --- | --- |
| **온디맨드 (On-Demand / Pay-As-You-Go)** | 사용한 만큼 초/시간 단위 과금 | 0% (기준가) | 없음 |
| **예약 (Reserved)** | 1년 또는 3년 약정 | 최대 72% | 사용 안 해도 요금 발생 |
| **약정 사용 할인 (Savings Plans / Savings Plan / CUD)** | 시간당 사용 금액 약정 | 최대 72% | 유연하지만 사용량 약정 |
| **Spot / Preemptible** | 남는 용량을 저렴하게 이용 | 최대 90% | 언제든 회수될 수 있음 |
| **Reserved Capacity** | 특정 AZ/존에 용량 예약 | — | 용량 확보 보장 |

### 구매 옵션 비교

| 벤더 | 온디맨드 | 장기 약정 | Spot |
| --- | --- | --- | --- |
| AWS | On-Demand | Reserved Instance + Savings Plans | Spot Instance |
| Azure | Pay-As-You-Go | Reserved VM Instance + Savings Plan | Spot VM |
| GCP | On-Demand | Committed Use Discount (CUD) | Preemptible / Spot VM |
| OCI | Pay-As-You-Go | Monthly Flex / Annual Flex / Universal Credits | Preemptible Instance |

{% hint style="info" %}
비용 구조에 대한 상세 내용은 [비용 구조 이해하기](../about-cloud/pricing-model.md)를 참고하세요.
{% endhint %}

## 배치 그룹과 전용 호스트

고성능/컴플라이언스 요구사항에 따라 VM을 물리적으로 제어할 수 있습니다.

| 기능 | 설명 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- | --- |
| **동일 랙 배치** | 저지연 통신 (HPC, 분산 DB) | Placement Group (Cluster) | Proximity Placement Group | Compact Placement | Cluster Network |
| **분산 배치** | 단일 장애점 제거 | Placement Group (Spread) | Availability Set | Spread Placement | Fault Domain |
| **전용 물리 서버** | 라이선스/컴플라이언스 | Dedicated Host | Dedicated Host | Sole-tenant Node | Dedicated VM Host |

## 참고하기

### AWS

- [Amazon EC2 문서](https://docs.aws.amazon.com/ko_kr/ec2/)
- [Amazon EC2 인스턴스 유형](https://docs.aws.amazon.com/ko_kr/ec2/latest/instancetypes/)

### Azure

- [Azure Virtual Machines 문서](https://learn.microsoft.com/ko-kr/azure/virtual-machines/)
- [Azure VM 크기](https://learn.microsoft.com/ko-kr/azure/virtual-machines/sizes/)

### GCP

- [Google Compute Engine 문서](https://cloud.google.com/compute/docs)
- [Google Compute Engine 머신 유형](https://cloud.google.com/compute/docs/machine-types)

### OCI

- [OCI Compute 문서](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm)
- [OCI Compute Shapes](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm)
