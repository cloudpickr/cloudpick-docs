---
description: 관리형 Kubernetes, 서버리스 컨테이너, 컨테이너 레지스트리를 4사 비교하고 컨트롤/데이터 플레인을 설명합니다.
---

# 컨테이너 서비스

> 문서 기준: 2026년 5월

## 개요

VM은 유연하지만, 하나의 앱을 배포하기 위해 OS 전체를 포함한 무거운 이미지를 관리해야 합니다. 앱이 10개면 VM도 10개, OS 패치도 10번입니다. 환경 간 "내 PC에서는 되는데 서버에서는 안 돼요" 문제도 빈번합니다.

**컨테이너**는 앱과 그 의존성만 가볍게 패키징하여 어디서든 동일하게 실행되도록 합니다. VM보다 가볍고, 시작이 빠르고, 환경 차이 문제를 해결합니다.

{% hint style="info" %}
EKS를 아시는 분을 위해: Azure는 AKS, GCP는 GKE, OCI는 OKE입니다.
{% endhint %}

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
- **OCI** — OKE 컨트롤 플레인이 무료이며, Virtual Nodes로 서버리스 Kubernetes 운영이 가능합니다.

## 언제 무엇을 선택할 것인가

| 이럴 때 | 이것을 선택 |
| --- | --- |
| Kubernetes 없이 간단하게 컨테이너를 운영하고 싶을 때 | AWS ECS 또는 Azure Container Apps |
| 기존 컨테이너 앱을 코드 수정 없이 서버리스로 실행하고 싶을 때 | GCP Cloud Run |
| Kubernetes가 필요하지만 컨트롤 플레인 비용을 아끼고 싶을 때 | Azure AKS 또는 OCI OKE (컨트롤 플레인 무료) |
| 노드 관리 없이 Pod 단위로만 과금받고 싶을 때 | GKE Autopilot 또는 AWS Fargate |
| 서버리스 Kubernetes를 원할 때 | OCI OKE Virtual Nodes |
| 소스 코드에서 바로 배포하고 싶을 때 | AWS App Runner |

## Kubernetes 컨트롤 플레인 vs 데이터 플레인

관리형 Kubernetes는 두 계층으로 구성됩니다.

| 계층 | 담당 | 관리 주체 |
| --- | --- | --- |
| **컨트롤 플레인** | API 서버, etcd, 스케줄러, 컨트롤러 매니저 | 벤더가 관리 |
| **데이터 플레인** | 워커 노드(VM), kubelet, 컨테이너 런타임 | 사용자가 관리 (또는 서버리스 노드로 위임) |

### 컨트롤 플레인 비용

| 벤더 | 컨트롤 플레인 비용 | 비고 |
| --- | --- | --- |
| AWS EKS | 시간당 ~$0.10 (클러스터당) | 월 ~$73 |
| Azure AKS | 무료 | Uptime SLA 활성화 시 유료 |
| GCP GKE Standard | 시간당 ~$0.10 | 월 ~$73. 월당 한 개 존 무료 |
| GCP GKE Autopilot | 무료 (Pod 단위 과금) | 노드 없음 |
| OCI OKE | 무료 | Enhanced 클러스터 시 유료 |

## 노드 관리 전략

데이터 플레인의 노드를 관리하는 방법에 따라 운영 부담이 달라집니다.

| 전략 | 설명 | 장점 | 단점 |
| --- | --- | --- | --- |
| **셀프 매니지드 노드** | 사용자가 노드 AMI, 패치, 스케일링 직접 관리 | 완전한 제어 | 운영 부담 큼 |
| **관리형 노드 그룹** | 벤더가 노드 프로비저닝/업그레이드 관리 (AWS Managed Node Groups, AKS Node Pools, GKE Node Pools) | 자동 업그레이드, 롤링 업데이트 | 여전히 노드 수 관리 필요 |
| **서버리스 노드 (Fargate/Virtual Nodes/Autopilot)** | 노드 개념 자체가 없음. Pod 단위 실행 | 운영 부담 최소 | Pod별 오버헤드 비용, 일부 제약(hostNetwork, DaemonSet 등) |

### 노드 풀 구성

단일 워크로드 유형이 아닌 다양한 요구사항(GPU, Spot, 스토리지 타입)에 따라 여러 노드 풀을 구성합니다.

- **범용 노드 풀** — 대부분의 애플리케이션
- **GPU 노드 풀** — ML 추론/학습 Pod
- **Spot/Preemptible 노드 풀** — 배치 작업, CI
- **ARM 노드 풀** — 비용 최적화 (Graviton, Cobalt, Ampere, Axion)

## 관련 문서

{% content-ref url="../devops/cicd.md" %}
[CI/CD](../devops/cicd.md)
{% endcontent-ref %}

{% content-ref url="../devops/iac.md" %}
[IaC](../devops/iac.md)
{% endcontent-ref %}

{% content-ref url="serverless.md" %}
[서버리스](serverless.md)
{% endcontent-ref %}

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
