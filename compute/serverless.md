# 서버리스

## 개요

VM과 컨테이너는 서버 생성과 배포를 자동화했지만, 여전히 "서버가 몇 대 필요한가", "언제 스케일링할 것인가"를 사용자가 결정해야 합니다. 오토스케일링이 도와주지만, 최소 인스턴스를 유지하는 비용은 남습니다.

**서버리스**는 이 마지막 관리 부담마저 제거합니다. 서버의 존재를 의식하지 않고, 요청이 있을 때만 코드가 실행됩니다. 관리 부담이 가장 적고 과금이 실제 사용량에 가장 가깝기 때문에, 적합한 워크로드에서는 비용 효율이 높습니다.

| 단계 | 관리 대상 | 과금 방식 | 유휴 비용 |
| --- | --- | --- | --- |
| **인스턴스 (VM)** | OS, 패치, 스케일링 전부 | 시간 단위 (켜져 있으면 과금) | 있음 |
| **컨테이너** | 앱 + 오케스트레이션 | 노드 시간 또는 Pod 단위 | 일부 있음 |
| **서버리스** | 코드만 | 요청 수 + 실행 시간 | **없음 (0원)** |

## 왜 서버리스인가?

- **비용** — 트래픽이 없으면 비용이 0. VM은 꺼도 디스크 비용이 남지만, 서버리스는 완전히 0.
- **운영** — OS 패치, 보안 업데이트, 스케일링을 벤더가 전부 처리합니다.
- **속도** — 인프라 설정 없이 코드만 배포하면 즉시 실행됩니다.

## 아직 서버리스가 어려운 경우

- **Cold Start** — 일정 시간 호출이 없으면 인스턴스가 해제되어, 다시 호출 시 수백ms~수초 지연이 발생합니다.
- **실행 시간 제한** — 장시간 실행되는 작업에는 제한이 있습니다.
- **상시 부하** — 24시간 일정한 트래픽이면 VM이 더 경제적일 수 있습니다.

이러한 제약은 점차 완화되고 있으며 (Provisioned Concurrency, 실행 시간 연장 등), 서버리스 적용 범위는 계속 넓어지고 있습니다.

## 제품 비교

### FaaS (Function as a Service)

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Lambda | 최대 15분. 200+ AWS 서비스 이벤트 연동 |
| Azure | Azure Functions | Premium: 무제한 실행. Durable Functions로 상태 유지 워크플로우 |
| GCP | Cloud Functions | 2세대: 최대 60분. Eventarc 연동 |

### 서버리스 컨테이너

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Fargate | ECS/EKS에서 서버 없이 컨테이너 실행 |
| AWS | App Runner | 소스/이미지에서 바로 배포 |
| Azure | Container Apps | 이벤트 기반 스케일링 내장 |
| GCP | Cloud Run | HTTP 기반. 기존 컨테이너 앱을 수정 없이 서버리스 전환 |

### 워크플로우 오케스트레이션

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Step Functions | 시각적 워크플로우 편집기 |
| Azure | Durable Functions / Logic Apps | 코드 기반 / 로우코드 |
| GCP | Workflows | YAML 기반 서비스 오케스트레이션 |

## 핵심 차이점

- **AWS Lambda** — 이벤트 소스 연동이 가장 풍부합니다. AWS 생태계 안에서 서버리스 아키텍처를 가장 완성도 높게 구성할 수 있습니다.
- **GCP Cloud Run** — 기존 컨테이너 앱을 코드 수정 없이 서버리스로 전환할 수 있어, 서버리스 여정의 진입 장벽이 가장 낮습니다.
- **Azure Functions** — Durable Functions로 장시간 상태 유지 워크플로우까지 서버리스로 처리할 수 있습니다.

## 참고하기

### AWS

- [AWS Lambda 문서](https://docs.aws.amazon.com/ko_kr/lambda/)
- [AWS Step Functions 문서](https://docs.aws.amazon.com/ko_kr/step-functions/)
- [서버리스 아키텍처](https://docs.aws.amazon.com/ko_kr/wellarchitected/latest/serverless-applications-lens/welcome.html)

### Azure

- [Azure Functions 문서](https://learn.microsoft.com/ko-kr/azure/azure-functions/)
- [Azure Durable Functions 문서](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/)

### GCP

- [Google Cloud Functions 문서](https://cloud.google.com/functions/docs)
- [Google Cloud Run 문서](https://cloud.google.com/run/docs)
- [Google Cloud Workflows 문서](https://cloud.google.com/workflows/docs)
