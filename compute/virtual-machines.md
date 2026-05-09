# 가상머신

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

## 핵심 차이점

- **AWS** — 인스턴스 유형이 가장 다양하고, 자체 Arm 프로세서(Graviton)로 비용 절감 가능합니다.
- **Azure** — 기존 Windows 라이선스를 활용한 Hybrid Benefit으로 비용을 줄일 수 있습니다.
- **GCP** — CPU와 메모리를 자유롭게 조합하는 Custom Machine Type을 제공합니다.

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
