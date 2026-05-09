# 컨테이너 서비스

## 개요

VM은 유연하지만, 하나의 앱을 배포하기 위해 OS 전체를 포함한 무거운 이미지를 관리해야 합니다. 앱이 10개면 VM도 10개, OS 패치도 10번입니다. 환경 간 "내 PC에서는 되는데 서버에서는 안 돼요" 문제도 빈번합니다.

**컨테이너**는 앱과 그 의존성만 가볍게 패키징하여 어디서든 동일하게 실행되도록 합니다. VM보다 가볍고, 시작이 빠르고, 환경 차이 문제를 해결합니다.

컨테이너가 수십~수백 개로 늘어나면 이를 관리하는 오케스트레이션이 필요합니다. 직접 Kubernetes를 설치하고 운영할 수도 있지만, 클라우드 벤더의 **관리형 서비스**를 사용하면 컨트롤 플레인 관리, 업그레이드, 보안 패치를 벤더가 담당합니다. 사용자는 앱 배포에만 집중할 수 있습니다.

## 제품 비교

### 관리형 Kubernetes

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | EKS (Elastic Kubernetes Service) | 컨트롤 플레인 유료 |
| Azure | AKS (Azure Kubernetes Service) | 컨트롤 플레인 무료 |
| GCP | GKE (Google Kubernetes Engine) | Autopilot 모드: 노드 관리 불필요, Pod 단위 과금 |
| OCI | OKE (Oracle Kubernetes Engine) | 컨트롤 플레인 무료. Virtual Nodes로 서버리스 운영 가능 |

### 서버리스 / 간편 컨테이너 실행

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Fargate | ECS/EKS 모두에서 사용 가능. 서버 관리 불필요 |
| AWS | ECS (Elastic Container Service) | AWS 자체 오케스트레이터. K8s 없이 운영 |
| AWS | App Runner | 소스 코드/이미지에서 바로 배포 |
| Azure | Container Apps | K8s 기반이나 복잡성 숨김. 이벤트 기반 스케일링 내장 |
| Azure | Container Instances (ACI) | 단일 컨테이너 빠르게 실행 |
| GCP | Cloud Run | HTTP 기반 서버리스 컨테이너. 기존 앱 전환 용이 |
| OCI | OCI Container Instances | 서버 관리 없이 컨테이너 실행 |

### 컨테이너 레지스트리

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | ECR (Elastic Container Registry) | |
| Azure | ACR (Azure Container Registry) | |
| GCP | Artifact Registry | 컨테이너 외 패키지도 지원 |
| OCI | OCI Container Registry (OCIR) | |

## 핵심 차이점

- **AWS** — ECS(자체 오케스트레이터)와 EKS(Kubernetes) 두 가지 선택지를 제공합니다.
- **Azure** — Container Apps로 K8s를 몰라도 컨테이너를 운영할 수 있습니다.
- **GCP** — Cloud Run으로 가장 간단하게 컨테이너를 서버리스 실행할 수 있습니다.

## 참고하기

### AWS

- [Amazon EKS 문서](https://docs.aws.amazon.com/ko_kr/eks/)
- [Amazon ECS 문서](https://docs.aws.amazon.com/ko_kr/ecs/)
- [AWS Fargate 문서](https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/userguide/AWS_Fargate.html)

### Azure

- [AKS 문서](https://learn.microsoft.com/ko-kr/azure/aks/)
- [Container Apps 문서](https://learn.microsoft.com/ko-kr/azure/container-apps/)
- [Container Instances 문서](https://learn.microsoft.com/ko-kr/azure/container-instances/)

### GCP

- [Google Kubernetes Engine 문서](https://cloud.google.com/kubernetes-engine/docs)
- [Google Cloud Run 문서](https://cloud.google.com/run/docs)
- [Google Artifact Registry 문서](https://cloud.google.com/artifact-registry/docs)

### OCI

- [OKE (Oracle Kubernetes Engine) 문서](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)
- [OCI Container Instances 문서](https://docs.oracle.com/en-us/iaas/Content/container-instances/home.htm)
- [OCI Container Registry 문서](https://docs.oracle.com/en-us/iaas/Content/Registry/home.htm)
