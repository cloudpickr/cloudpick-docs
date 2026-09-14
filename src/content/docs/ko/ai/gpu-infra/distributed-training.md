---
title: "분산 학습 표준 아키텍처"
description: "데이터·텐서·파이프라인 병렬화(DP/TP/PP)와 3D 하이브리드 병렬화, 분산 학습 프레임워크, 체크포인트 전략을 벤더 중립 관점으로 정리합니다."
---

> 문서 기준: 2026년 9월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

:::note
이 문서는 분산 학습의 병렬화 전략을 다룹니다. 클러스터 통신 계층·배치·패브릭은 [GPU 워크로드 특성과 레퍼런스 아키텍처](../../ai/gpu-infra/workload-and-architecture/)를, 쿠버네티스 상의 스케줄링은 [GPU 쿠버네티스와 스케줄링](../../ai/gpu-infra/kubernetes-and-scheduling/)을 참고하세요.
:::

## 개요

모델과 데이터가 GPU 한 장에 다 들어가면 고민할 게 없습니다. 문제는 요즘 모델이 GPU 한 장의 메모리를 훌쩍 넘긴다는 점입니다. 그래서 일을 여러 GPU에 **나눠서** 학습하는데, 나누는 방식이 크게 세 가지입니다.

큰 요리를 여러 요리사가 나눠 하는 상황에 비유하면 이해가 쉽습니다.

- **데이터 병렬(DP)** — 같은 레시피(모델 전체)를 요리사마다 한 부씩 갖고, 손님(데이터)만 나눠 받아 각자 만든 뒤 결과를 맞춰봅니다.
- **텐서 병렬(TP)** — 요리 하나가 너무 커서 한 요리사가 못 만들 때, 그 요리 한 접시를 여러 요리사가 동시에 나눠 만듭니다.
- **파이프라인 병렬(PP)** — 조리 단계를 나눠, 요리사 A는 손질, B는 굽기, C는 플레이팅처럼 이어달리기로 처리합니다.

대규모 학습은 이 셋을 겹쳐 쓰는데(3D 병렬화), 각 방식은 "얼마나 자주 서로 통신해야 하나 / 메모리를 얼마나 아끼나 / 구현이 얼마나 복잡한가"에서 장단점이 갈립니다.

:::note
여기 나오는 병렬화 방식과 프레임워크(DeepSpeed, Megatron-LM, PyTorch FSDP)는 CUDA/NCCL 위에서 돌아 벤더에 매이지 않습니다. 즉 클라우드를 바꿔도 전략 자체는 대체로 그대로 옮겨집니다. 다만 실제 속도는 [노드 간 통신망 성능](../../ai/gpu-infra/workload-and-architecture/#노드-간-고속-통신-패브릭--벤더-매핑)에 좌우됩니다.
:::

## 데이터 병렬 (Data Parallelism, DP)

모델 전체를 GPU마다 똑같이 복제해두고, 데이터 묶음만 나눠 각자 처리한 뒤 결과(그래디언트)를 서로 맞춥니다. 가장 단순하며, 모델이 GPU 한 장에 들어갈 때 표준으로 씁니다.

- **통신 방식** — 매 학습 단계마다 전 GPU가 계산 결과를 합칩니다. (all-reduce = 모든 GPU의 값을 모아 합산한 뒤 다시 모두에게 나눠주는 통신.)
- **한계** — 모델 자체가 GPU 한 장 메모리를 넘으면 이 방식만으로는 안 됩니다.
- **메모리 아끼기(FSDP/ZeRO)** — 모델의 파라미터·중간 상태를 GPU들에 잘게 쪼개 나눠 저장(sharding)합니다. 데이터 병렬을 유지하면서도 GPU 한 장 한계를 넘어 더 큰 모델을 학습할 수 있습니다.

## 텐서 병렬 (Tensor Parallelism, TP)

레이어(모델을 이루는 계산 층) 하나의 계산을 여러 GPU가 동시에 나눠 처리합니다. 한 층이 GPU 한 장에 안 들어갈 만큼 클 때 씁니다.

- **통신 방식** — 층 내부에서 GPU끼리 매우 자주 주고받습니다. 그래서 지연(반응 속도)에 아주 민감합니다.
- **적용 범위** — 통신이 잦아, 주로 **한 서버 안(NVLink로 이어진 GPU들)**에서만 씁니다.
- **효과** — 층 하나가 GPU 메모리를 넘을 때 필수.

## 파이프라인 병렬 (Pipeline Parallelism, PP)

모델의 층들을 몇 개의 단계(stage)로 나눠 서로 다른 GPU 그룹에 배치하고, 데이터를 작은 조각(마이크로배치)으로 쪼개 이어달리기처럼 흘려보냅니다.

- **통신 방식** — 단계와 단계가 만나는 경계에서만 결과를 넘깁니다. 그래서 통신량이 상대적으로 적습니다.
- **적용 범위** — 통신이 적어 **여러 서버로 넓히기** 쉽습니다.
- **한계** — 이어달리기 특성상 앞 단계를 기다리며 노는 구간(파이프라인 버블)이 생기며, 데이터 조각 수를 늘려 완화합니다.

## 3D 하이브리드 병렬화

대규모 사전학습은 세 방식을 계층적으로 조합합니다. 일반적으로 **노드 내는 TP, 노드 간은 PP, 그 위에 DP**를 얹습니다.

| 병렬화 | 통신량 | 메모리 절감 | 지연 민감도 | 권장 배치 |
| --- | --- | --- | --- | --- |
| **데이터 병렬 (DP)** | 높음 (그래디언트 all-reduce) | 없음 (FSDP/ZeRO 사용 시 큼) | 중간 | 클러스터 전체 |
| **텐서 병렬 (TP)** | 매우 높음 (레이어 내부) | 큼 | 매우 높음 | 노드 내 (NVLink) |
| **파이프라인 병렬 (PP)** | 낮음 (단계 경계) | 큼 | 낮음 | 노드 간 |

:::caution
병렬화 차원을 늘릴수록 구현·디버깅 복잡도가 급격히 증가합니다. 모델이 단일 노드(예: 8×GPU)에 들어간다면 3D 병렬화 없이 FSDP/ZeRO 기반 데이터 병렬만으로 충분한 경우가 많습니다. 통신 지연에 민감한 TP를 노드 간으로 확장하면 패브릭 성능에 따라 처리량이 급락할 수 있습니다.
:::

## 분산 학습 프레임워크

| 프레임워크 | 주요 병렬화 | 특징 |
| --- | --- | --- |
| [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html) | DP (sharding) | PyTorch 네이티브, 파라미터/옵티마이저 상태 분산 |
| [DeepSpeed](https://www.deepspeed.ai/) | DP(ZeRO) + PP + TP | ZeRO 단계별 메모리 최적화, 오프로딩 지원 |
| [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) | TP + PP + DP | 대규모 Transformer 사전학습에 최적화된 TP 구현 |

:::note
프레임워크 선택은 벤더 중립적입니다. 다만 각 클라우드의 매니지드 학습 플랫폼(SageMaker, Vertex AI, Azure ML 등)은 이 프레임워크들을 사전 통합한 분산 학습 라이브러리·레시피를 제공하며, 이를 쓰면 통신 설정·토폴로지 최적화가 자동화되는 대신 해당 플랫폼에 종속됩니다.
:::

## 체크포인트 전략

대규모 학습은 수 시간~수 주간 실행되므로, 노드 실패에 대비한 체크포인트가 필수입니다. 체크포인트 설계는 **저장 빈도와 스토리지 대역폭의 균형** 문제입니다.

- **빈도** — 너무 잦으면 저장 오버헤드로 GPU가 유휴 상태가 되고, 너무 드물면 실패 시 손실되는 계산량이 커집니다.
- **스토리지 대역폭** — 수백 GB~수 TB급 체크포인트를 짧은 시간에 써야 하므로, [스토리지 계층](../../ai/gpu-infra/workload-and-architecture/#레퍼런스-아키텍처--3계층-통신-모델)의 처리량이 병목이 됩니다.
- **비동기·분산 저장** — 학습을 멈추지 않고 백그라운드로 저장하거나, 각 GPU가 자신의 샤드만 병렬 저장해 시간을 단축합니다.
- **자동 재개** — 실패 감지 후 마지막 체크포인트에서 재개하는 흐름은 [추론 서빙·안정성·비용 최적화 — 안정성·장애 대응](../../ai/gpu-infra/serving-reliability-cost/#안정성장애-대응)에서 다룹니다.

## 관련 문서

- **클러스터 통신 계층·패브릭·배치** — [GPU 워크로드 특성과 레퍼런스 아키텍처](../../ai/gpu-infra/workload-and-architecture/)
- **gang scheduling·쿼터** — [GPU 쿠버네티스와 스케줄링](../../ai/gpu-infra/kubernetes-and-scheduling/)
- **장애 자동 재개·용량 운영** — [추론 서빙·안정성·비용 최적화](../../ai/gpu-infra/serving-reliability-cost/)
- **AI 시스템 수명주기 내 학습 파이프라인** — [AI 시스템 수명주기와 엔지니어링](../../ai/lifecycle/)

## 자주 하는 실수

- **불필요한 3D 병렬화 도입** — 단일 노드로 충분한 모델에 텐서·파이프라인 병렬을 얹어 복잡도와 디버깅 비용만 증가
- **텐서 병렬을 노드 간으로 확장** — 지연에 민감한 TP를 NVLink 밖으로 넓혀 통신 병목 발생
- **체크포인트 빈도만 높임** — 스토리지 대역폭을 함께 늘리지 않아 저장 중 GPU 유휴 시간이 증가
- **옵티마이저 상태 메모리 간과** — 파라미터 외에 옵티마이저 상태·그래디언트가 차지하는 메모리를 계산하지 않아 OOM 발생

## 체크리스트

- [ ] 모델·옵티마이저 상태가 단일 GPU/단일 노드 메모리에 들어가는지 계산했는가
- [ ] 단일 노드로 가능하면 FSDP/ZeRO 데이터 병렬을 우선 검토했는가
- [ ] 텐서 병렬을 노드 내(NVLink)로 제한하고 파이프라인 병렬을 노드 간에 배치했는가
- [ ] 체크포인트 빈도와 스토리지 대역폭을 함께 설계했는가
- [ ] 실패 시 자동 재개 흐름을 검증했는가

## 참고하기

### 공통 (벤더 중립)

- [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html)
- [DeepSpeed](https://www.deepspeed.ai/)
- [NVIDIA Megatron-LM](https://github.com/NVIDIA/Megatron-LM)
- [NVIDIA NCCL 문서](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)

### 벤더별 분산 학습

- [AWS — SageMaker 분산 학습](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training.html)
- [Azure — Azure ML 분산 학습](https://learn.microsoft.com/azure/machine-learning/concept-distributed-training)
- [Google Cloud — Vertex AI 분산 학습](https://cloud.google.com/vertex-ai/docs/training/distributed-training)
- [OCI — Data Science 분산 학습](https://docs.oracle.com/en-us/iaas/Content/data-science/using/jobs-distributed-jobs.htm)
