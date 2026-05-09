# 오토스케일링

## 개요

VM을 사용하면 서버를 빠르게 만들 수 있지만, 트래픽 변화에 대응하는 것은 여전히 사용자의 몫입니다. 트래픽이 급증하면 수동으로 서버를 추가하고, 줄어들면 다시 제거해야 합니다. 이 과정이 느리면 서비스가 다운되고, 과하면 비용이 낭비됩니다.

**오토스케일링**은 이 판단과 실행을 자동화합니다. CPU 사용률, 요청 수 등의 지표를 모니터링하다가 임계값을 넘으면 자동으로 서버를 추가하고, 부하가 줄면 자동으로 제거합니다.

이것이 클라우드에서 관리형 서비스가 중요한 이유입니다. 사람이 24시간 모니터링하지 않아도, 벤더가 제공하는 자동화 기능이 인프라를 탄력적으로 운영해 줍니다.

## 제품 비교

### VM 오토스케일링

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Auto Scaling Groups | EC2 인스턴스 자동 확장/축소 |
| Azure | VM Scale Sets (VMSS) | VM 배포와 스케일링 통합 관리 |
| GCP | Managed Instance Groups (MIG) | Auto-healing(비정상 인스턴스 자동 교체) 내장 |
| OCI | OCI Autoscaling | Instance Pool 기반. 메트릭/스케줄 기반 스케일링 |

### 예측 스케일링

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Predictive Scaling | 최대 14일 트래픽 학습, 사전 확장 |
| Azure | Autoscale (Predictive) | Preview |
| GCP | Predictive Autoscaling | 과거 패턴 기반 |
| OCI | — | 스케줄 기반 스케일링으로 대응 |

### 애플리케이션 레벨 스케일링

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Application Auto Scaling | ECS, DynamoDB, Lambda 등 다양한 서비스 대상 |
| Azure | Autoscale | App Service, Functions, VMSS 등 |
| GCP | Autoscaler | Compute Engine, GKE 등 |
| OCI | OCI Autoscaling | Compute, OKE 등 |

## 핵심 차이점

- **AWS** — VM뿐 아니라 DynamoDB, ECS 등 다양한 서비스에 통합 오토스케일링을 제공합니다.
- **Azure** — VMSS가 VM 배포와 스케일링을 하나의 리소스로 관리합니다.
- **GCP** — MIG에 Auto-healing이 기본 내장되어 비정상 인스턴스를 자동 교체합니다.

## 참고하기

### AWS

- [AWS Auto Scaling 문서](https://docs.aws.amazon.com/ko_kr/autoscaling/)
- [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/ko_kr/autoscaling/ec2/userguide/)

### Azure

- [Azure VM Scale Sets 문서](https://learn.microsoft.com/ko-kr/azure/virtual-machine-scale-sets/)
- [Azure Autoscale 문서](https://learn.microsoft.com/ko-kr/azure/azure-monitor/autoscale/)

### GCP

- [Google Cloud Autoscaler 문서](https://cloud.google.com/compute/docs/autoscaler)
- [Google Cloud MIG 문서](https://cloud.google.com/compute/docs/instance-groups)

### OCI

- [OCI Autoscaling 문서](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm)
