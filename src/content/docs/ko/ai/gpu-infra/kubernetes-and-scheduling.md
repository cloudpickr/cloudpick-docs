---
title: "GPU 쿠버네티스와 스케줄링"
description: "GPU 노드풀·device plugin, MIG/time-slicing 공유, ResourceQuota·anti-hoarding, gang scheduling(Kueue/Volcano), DCGM 관측성을 벤더 중립 관점으로 정리합니다."
---

> 문서 기준: 2026년 9월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

:::note
이 문서는 쿠버네티스 위에서 GPU를 스케줄링·공유·통제하는 방법을 다룹니다. 클러스터 업그레이드·노드 관리 등 일반적인 쿠버네티스 운영은 [쿠버네티스 운영](../../../devops/kubernetes-operations/)에서, GPU 클러스터 통신·배치는 [GPU 워크로드 특성과 레퍼런스 아키텍처](../workload-and-architecture/)에서 다룹니다.
:::

## 개요

GPU는 비싸고 귀합니다. 그래서 보통 한 팀이 독차지하지 않고 여러 팀·여러 작업이 **하나의 GPU 클러스터를 나눠 씁니다.** 이때 "누구에게 GPU를 얼마나, 언제 주느냐"를 정하는 것이 스케줄러이고, 이 배분이 잘못되면 값비싼 GPU가 놀거나 특정 팀이 독점하게 됩니다.

쿠버네티스(컨테이너를 자동 배치·관리하는 표준 도구)는 GPU를 특별한 자원으로 다룹니다. 어려운 점은 성격이 정반대인 두 작업을 한 클러스터에서 함께 받아야 한다는 것입니다 — **학습 작업**은 "필요한 GPU를 한꺼번에 다 줘야" 시작되고, **추론 작업**은 "적은 GPU를 오래 붙잡고" 돌아갑니다.

:::note
쿠버네티스 자체가 처음이라면 [컨테이너 서비스](../../../compute/containers/)와 [쿠버네티스 운영](../../../devops/kubernetes-operations/)을 먼저 보는 것을 권합니다. 이 문서는 그 위에서 **GPU에 특화된** 부분만 다룹니다.
:::

## GPU 노드풀과 device plugin

쿠버네티스는 기본적으로 GPU를 인식하지 못하므로, 벤더 device plugin과 드라이버·오퍼레이터를 설치해 GPU를 스케줄링 가능한 리소스로 노출합니다.

- **GPU 노드풀** — 범용 노드와 분리된 GPU 전용 노드풀을 구성합니다. ([노드 풀 구성](../../../compute/containers/#노드-풀-구성) 참고)
- **device plugin / 오퍼레이터** — [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)가 드라이버·device plugin·DCGM을 일괄 배포하는 사실상 표준입니다.
- **taint/toleration** — GPU 노드에 taint를 걸어 비 GPU 워크로드가 값비싼 GPU 노드를 점유하지 못하게 합니다.

## GPU 공유 — MIG와 time-slicing

단일 GPU를 여러 작업이 나눠 쓰면 소규모 추론·개발 워크로드의 활용률을 높일 수 있습니다.

| 방식 | 격리 수준 | 적합 워크로드 | 한계 |
| --- | --- | --- | --- |
| **MIG (Multi-Instance GPU)** | 하드웨어 파티션 (메모리·연산 격리) | 예측 가능한 다중 테넌트 추론 | 지원 GPU·프로파일 제약, 동적 변경 부담 |
| **MPS (Multi-Process Service)** | 프로세스 공간 공유 (부분 격리) | 협조적 다중 프로세스, 소규모 추론 | 메모리 격리 미보장, 장애 전파 가능 |
| **Time-slicing** | 시간 분할 (격리 없음) | 개발·실험, 버스티 워크로드 | 성능 간섭·OOM 위험, 공정성 미보장 |

MIG는 하드웨어 격리로 가장 강하고, time-slicing은 격리가 없으며, MPS는 그 중간에서 여러 프로세스가 하나의 GPU 컨텍스트를 공유합니다. 세 방식 모두 NVIDIA GPU의 공통 기능이며 특정 벤더 전용이 아닙니다.

:::caution
Time-slicing은 메모리·연산을 격리하지 않으므로 한 작업의 OOM이나 폭주가 같은 GPU의 다른 작업에 영향을 줍니다. 프로덕션 다중 테넌트에는 MIG(하드웨어 격리)를 우선 검토하세요. MIG는 지원 GPU 세대·프로파일이 제한적이므로 대상 GPU의 지원 여부를 먼저 확인해야 합니다.
:::

## 쿼터·공정성·anti-hoarding

공유 클러스터의 골칫거리는 **한 팀이 GPU를 잡아두고 안 놓는 것**(독점, hoarding)입니다. 그러면 다른 작업이 GPU를 못 받고 계속 굶습니다. 이를 막는 장치들:

- **ResourceQuota (총량 상한)** — 팀(네임스페이스)마다 쓸 수 있는 GPU 수의 상한을 정합니다.
- **우선순위·선점(preemption)** — 작업마다 우선순위를 매기고(PriorityClass), 급한 작업이 오면 덜 급한 작업을 잠시 밀어내(선점) GPU를 양보시킵니다.
- **놀리는 GPU 회수(anti-hoarding)** — 잡아만 두고 실제로 안 쓰는 GPU를, 큐 기반 스케줄러가 공정 배분·회수 규칙으로 되찾아 다른 작업에 돌립니다.
- **큐 기반 배분** — 아래 gang scheduling 계층에서 팀별 몫과 대기 줄을 관리합니다.

## Gang scheduling

분산 학습은 필요한 GPU를 **한꺼번에 전부** 확보해야 시작할 수 있습니다. 예를 들어 GPU 16장이 필요한데 10장만 잡고 나머지 6장을 기다리면, 이미 잡은 10장이 아무 일도 못 하고 놀면서 자원만 묶어둡니다(심하면 서로 기다리다 멈추는 교착 상태). Gang scheduling은 이를 막기 위해 **"필요한 만큼 전부 잡히면 시작, 아니면 아예 시작 안 함(전부-아니면-전무)"** 방식으로 스케줄링합니다. "gang(한 무리)"을 통째로 잡는다는 뜻입니다.

| 도구 | 특징 |
| --- | --- |
| [Kueue](https://kueue.sigs.k8s.io/) | 쿠버네티스 네이티브 잡 큐잉, 쿼터·공정 공유, 계층적 큐 |
| [Volcano](https://volcano.sh/) | 배치 스케줄러, gang scheduling·큐·선점 통합, HPC/AI 지향 |

:::note
Kueue와 Volcano는 모두 벤더 중립 오픈소스이며 어느 클라우드의 쿠버네티스에서도 동작합니다. 매니지드 학습 플랫폼(SageMaker HyperPod, Vertex AI 등)은 유사한 큐잉·gang scheduling을 내장 제공하므로, 직접 구성 대신 활용할 수 있습니다.
:::

## 벤더별 매니지드 쿠버네티스 GPU 지원

| 항목 | AWS (EKS) | Azure (AKS) | Google Cloud (GKE) | OCI (OKE) |
| --- | --- | --- | --- | --- |
| **GPU 노드풀** | 관리형 노드 그룹 | GPU 노드 풀 | GPU 노드 풀 | GPU 노드 풀 |
| **드라이버 설치** | GPU Operator / EKS 최적화 AMI | GPU Operator / AKS GPU 이미지 | GPU Operator / GKE 드라이버 자동 설치 | GPU Operator / OKE 이미지 |
| **GPU 공유** | MIG, MPS, time-slicing | MIG, MPS, time-slicing | MIG, MPS, time-slicing | MIG, MPS, time-slicing |

:::note
GPU 공유·gang scheduling·오퍼레이터는 대부분 오픈소스 계층에서 동작하므로 벤더 간 개념이 유사합니다. 다만 노드풀 프로비저닝 API, 드라이버 자동 설치 방식, 지원 GPU 세대는 벤더마다 다르므로 각 벤더 공식 문서로 확인하세요.
:::

## 관측성 — DCGM과 GPU 메트릭

GPU 클러스터는 CPU 중심 관측성만으로는 병목을 진단할 수 없습니다. [NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html)(Data Center GPU Manager, GPU 상태·성능을 수집하는 표준 도구)으로 GPU 활용률·메모리·온도·통신망 트래픽을 모읍니다.

- **핵심 지표** — GPU 활용률(단순 점유율이 아닌 실제 연산 활용), 메모리 사용량, 패브릭 대역폭, 전력·온도
- **활용률의 함정** — "GPU가 할당됨"과 "GPU가 실제로 계산 중"은 다릅니다. 낮은 실효 활용률은 데이터 로딩·통신 병목의 신호입니다.
- **SLO 연계** — 수집한 GPU 메트릭을 [SLO](../../../devops/slo/)·[관측성](../../../devops/observability/) 체계에 통합해 학습 처리량·추론 지연을 지속 관리합니다.

## 관련 문서

- **다음: 추론 서빙·장애·용량·비용** — [추론 서빙·안정성·비용 최적화](../serving-reliability-cost/)
- **일반 쿠버네티스 운영(업그레이드·노드 관리)** — [쿠버네티스 운영](../../../devops/kubernetes-operations/)
- **클러스터 통신·배치·매니지드 클러스터** — [GPU 워크로드 특성과 레퍼런스 아키텍처](../workload-and-architecture/)
- **병렬화 전략(TP/PP/DP)** — [분산 학습 표준 아키텍처](../distributed-training/)

## 자주 하는 실수

- **gang scheduling 없이 분산 학습 제출** — GPU를 일부만 확보한 채 대기해 자원이 묶이고 교착 발생
- **time-slicing을 프로덕션 다중 테넌트에 사용** — 격리가 없어 한 작업의 OOM이 다른 작업에 전파
- **ResourceQuota·선점 정책 부재** — 한 팀이 GPU를 독점(hoarding)해 다른 작업이 굶음
- **GPU 할당률만 보고 활용률을 안 봄** — 낮은 실효 활용률(데이터·통신 병목)을 놓쳐 값비싼 GPU가 낭비됨

## 체크리스트

- [ ] GPU 전용 노드풀에 taint를 걸어 비 GPU 워크로드 점유를 막았는가
- [ ] 다중 테넌트 추론에 time-slicing 대신 MIG(하드웨어 격리)를 검토했는가
- [ ] 네임스페이스별 ResourceQuota와 PriorityClass·선점 정책을 설정했는가
- [ ] 분산 학습에 gang scheduling(Kueue/Volcano 또는 매니지드 내장)을 적용했는가
- [ ] DCGM으로 실효 GPU 활용률을 수집하고 SLO에 연계했는가

## 참고하기

### 공통 (벤더 중립)

- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)
- [NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html)
- [Kueue](https://kueue.sigs.k8s.io/)
- [Volcano](https://volcano.sh/)

### 벤더별

- [AWS — EKS GPU 워크로드](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html)
- [Azure — AKS GPU 노드 풀](https://learn.microsoft.com/azure/aks/gpu-cluster)
- [Google Cloud — GKE GPU](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)
- [OCI — OKE GPU 노드](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengrunninggpunodes.htm)
