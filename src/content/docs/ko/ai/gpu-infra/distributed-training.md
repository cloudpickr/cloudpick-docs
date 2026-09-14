---
title: "분산 학습 표준 아키텍처"
description: "데이터·텐서·파이프라인 병렬화(DP/TP/PP)와 3D 하이브리드 병렬화, 분산 학습 프레임워크, 체크포인트 전략을 벤더 중립 관점으로 정리합니다."
---

> 문서 기준: 2026년 9월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

:::note
이 문서는 분산 학습의 병렬화 전략을 다룹니다. 클러스터 통신 계층·배치·패브릭은 [GPU 워크로드 특성과 레퍼런스 아키텍처](../../ai/gpu-infra/workload-and-architecture/)를, 쿠버네티스 상의 스케줄링은 [GPU 쿠버네티스와 스케줄링](../../ai/gpu-infra/kubernetes-and-scheduling/)을 참고하세요.
:::

## 개요

모델과 데이터가 단일 GPU 메모리에 담기지 않으면 여러 GPU에 나눠 학습해야 합니다. 나누는 방식은 크게 **데이터 병렬(DP)**, **텐서 병렬(TP)**, **파이프라인 병렬(PP)** 세 가지이며, 대규모 학습에서는 이를 조합한 **3D 병렬화**를 사용합니다. 각 방식은 통신량·메모리 절감·구현 복잡도에서 서로 다른 트레이드오프를 가집니다.

:::note
이 문서의 병렬화 개념과 프레임워크(DeepSpeed, Megatron-LM, PyTorch FSDP)는 CUDA/NCCL 위에서 동작하며 벤더에 종속되지 않습니다. 클라우드를 바꿔도 병렬화 전략 자체는 대체로 이식됩니다. 실제 성능은 [노드 간 패브릭 성능](../../ai/gpu-infra/workload-and-architecture/#노드-간-고속-통신-패브릭--벤더-매핑)에 좌우됩니다.
:::

## 데이터 병렬 (Data Parallelism, DP)

모델 전체를 각 GPU에 복제하고, 데이터 배치를 나눠 처리한 뒤 그래디언트를 동기화합니다. 가장 단순하며 모델이 단일 GPU에 들어갈 때 표준입니다.

- **통신 패턴** — 스텝마다 그래디언트 all-reduce (전 GPU collective)
- **한계** — 모델 자체가 단일 GPU 메모리를 초과하면 사용할 수 없음
- **메모리 최적화(FSDP/ZeRO)** — 모델 파라미터·그래디언트·옵티마이저 상태를 GPU들에 분산 저장(sharding)해, 데이터 병렬을 유지하면서도 단일 GPU 메모리 한계를 넘어 더 큰 모델을 학습

## 텐서 병렬 (Tensor Parallelism, TP)

개별 레이어의 행렬 연산 자체를 여러 GPU에 쪼갭니다. 하나의 레이어를 여러 GPU가 동시에 계산합니다.

- **통신 패턴** — 레이어 내부에서 빈번한 collective 통신 (지연에 매우 민감)
- **적용 범위** — 통신 빈도가 높아 주로 **노드 내 NVLink**로 연결된 GPU 사이에서 사용
- **효과** — 단일 레이어가 GPU 메모리를 초과할 때 필수

## 파이프라인 병렬 (Pipeline Parallelism, PP)

모델의 레이어를 단계(stage)로 나눠 서로 다른 GPU 그룹에 배치하고, 마이크로배치를 파이프라인으로 흘려보냅니다.

- **통신 패턴** — 단계 경계에서만 activation 전달 (통신량이 상대적으로 적음)
- **적용 범위** — 통신이 적어 **노드 간**으로 확장하기 용이
- **한계** — 파이프라인 버블(idle 구간)이 발생하며, 마이크로배치 수로 완화

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
