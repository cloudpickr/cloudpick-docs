---
title: "추론 서빙·안정성·비용 최적화"
description: "GPU 추론 서빙 운영, 노드 장애 자동 재개, 용량 운영(Capacity Blocks·예약·멀티리전 폴백), GPU 비용 최적화를 벤더 중립 관점으로 정리합니다."
---

> 문서 기준: 2026년 9월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

:::note
이 문서는 GPU 인프라의 운영 단계(추론 서빙·장애 대응·용량·비용)를 다룹니다. 학습 병렬화는 [분산 학습 표준 아키텍처](../distributed-training/)를, 클러스터 아키텍처는 [GPU 워크로드 특성과 레퍼런스 아키텍처](../workload-and-architecture/)를 참고하세요.
:::

## 개요

GPU 인프라는 구축 이후 운영 단계에서 비용과 안정성이 갈립니다. 이 문서는 추론 서빙(지연·오토스케일), 장애 복구(체크포인트·노드 재투입), 그리고 GPU 용량 확보와 비용 최적화(약정·스팟·용량 예약)를 다룹니다. 특히 2026년 현재는 성능보다 **원할 때 GPU를 실제로 확보할 수 있느냐**가 가장 큰 제약입니다.

추론과 학습은 성격이 다릅니다. 학습이 오래·크게·한 번에 돌리는 일이라면, 추론은 사용자 요청이 올 때마다 **빨리 응답**해야 하고 요청량에 따라 **자동으로 늘었다 줄었다** 해야 합니다.

## 추론 서빙

추론은 학습과 반대되는 운영 프로파일을 가집니다. 학습은 장시간·고통신·배치 지향인 반면, 추론은 **지연 민감·요청 단위·오토스케일 지향**입니다.

- **지연 vs 처리량** — 실시간 서빙은 낮은 지연(빠른 응답)이, 배치 추론은 높은 처리량(한꺼번에 많이)이 목표입니다. 동적 배칭(dynamic batching = 짧은 시간 동안 들어온 요청을 모아 한 번에 처리)으로 둘의 균형을 맞춥니다.
- **오토스케일** — 요청량에 따라 GPU 복제본을 늘리고 줄입니다. 단, GPU는 켜질 때 모델 가중치를 메모리에 올리는 시간(콜드 스타트)이 길어 CPU보다 반응이 느립니다. 그래서 최소 몇 대는 늘 켜두거나 미리 예열해 둡니다.
- **모델 병렬 서빙** — 단일 GPU에 담기지 않는 대형 모델은 추론에서도 텐서 병렬을 사용합니다. ([병렬화 전략](../distributed-training/) 참고)
- **토큰 단위 비용·라우팅** — 파운데이션 모델 API의 토큰 비용·프롬프트 캐싱·모델 라우팅은 [LLMOps](../../../ai/llmops/)와 [AI 플랫폼과 모델 비교 — 추론 비용 최적화](../../../ai/ai-ml/#추론-비용-최적화)에서 다룹니다.

## 안정성·장애 대응

노드가 많을수록 학습 도중 하드웨어가 고장 날 확률이 높아집니다. 수백 장 GPU 규모에서는 고장이 예외가 아니라 일상입니다. 그래서 "고장은 난다"를 전제로 대비합니다.

- **고장 감지** — 노드 헬스체크와 GPU 오류 신호(Xid 오류 = NVIDIA 드라이버가 보고하는 GPU 오류 코드, 메모리 오류, 통신 링크 끊김)로 이상 노드를 빨리 찾아 격리합니다.
- **체크포인트로 재개** — 마지막으로 저장해둔 지점([체크포인트](../distributed-training/#체크포인트-전략))부터 다시 시작합니다. 고장 난 노드는 교체하고, 나머지 노드는 잠시 기다렸다가 다시 맞춥니다.
- **느림보 노드(straggler) 대응** — 한 노드만 느려져도(네트워크 문제나 발열로 인한 속도 저하) 전체가 그 노드를 기다리느라 함께 느려집니다. 이런 느림보(straggler)를 찾아 격리·교체합니다.
- **매니지드 클러스터의 자동 복구** — [매니지드 GPU 클러스터](../workload-and-architecture/#매니지드-gpu-클러스터)(예: SageMaker HyperPod)는 고장 감지·자동 교체·체크포인트 재개를 통째로 제공해 이 부담을 덜어줍니다.

## 용량 운영

2026년 현재 최신 세대 GPU는 **원할 때 즉시 확보되지 않는** 경우가 많습니다. 용량 확보는 인프라 설계의 1급 제약입니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **용량 예약** | [Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html), On-Demand Capacity Reservations | On-Demand Capacity Reservations | [Future Reservations](https://cloud.google.com/compute/docs/instances/reservations-overview), Calendar mode | Capacity Reservation |
| **약정 할인** | Savings Plans, Reserved Instances | Reserved VM Instances | CUD (Committed Use Discount) | Universal Credits, 약정 |
| **선점형** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |

- **용량 블록·예약 큐** — 특정 기간의 GPU 용량을 미리 예약합니다. 대규모 학습은 시작 전 용량 확보가 전제입니다.
- **리전 희소성** — 최신 GPU는 소수 리전에만 있고 물량이 제한적입니다. 원하는 리전·세대의 실제 가용성을 사전 확인해야 합니다.
- **멀티리전·멀티클라우드 폴백** — 단일 리전 용량 부족에 대비해 대체 리전·세대를 폴백으로 준비합니다. 데이터 위치·이그레스 비용을 함께 고려합니다.

:::caution
최신 GPU 세대일수록 리전 가용성이 제한적이고 약정 확보 경쟁이 큽니다. "인스턴스 타입이 문서에 존재함"과 "원하는 리전에서 원하는 수량을 지금 확보 가능함"은 전혀 다른 문제입니다. 용량은 설계 초기에 확인하고 예약하세요.
:::

:::note
위 표의 축은 성격이 다릅니다. **용량 확보**(Capacity Blocks·Future Reservations 등)는 "물량을 잡는" 메커니즘이고, **약정 할인**(Savings Plans·CUD·RI 등)은 "가격을 낮추는" 재무 약정입니다. 둘은 일반적으로 서로 겹쳐 적용되지 않으므로, 용량 확보와 비용 절감을 별개로 설계해야 합니다. 또한 OCI Universal Credits는 GPU 용량 할인이 아니라 계정 단위의 소비 약정이라는 점에 유의하세요.
:::

## 비용 최적화

GPU는 클라우드에서 가장 비싼 자원이므로, 활용률과 구매 방식이 비용을 좌우합니다.

- **구매 방식 조합** — 상시 워크로드는 약정 할인(Savings Plans/CUD/RI)으로, 학습·배치는 선점형(Spot)으로, 예측 가능한 대규모 학습은 용량 예약으로 배분합니다.
- **선점형 + 체크포인트** — 선점형은 최대 수십 %까지 저렴하지만 중단될 수 있으므로, [체크포인트](../distributed-training/#체크포인트-전략)와 조합해 중단 시 재개합니다.
- **right-sizing** — 워크로드에 과도한 GPU 세대를 쓰지 않습니다. 추론·파인튜닝은 상위 세대가 불필요한 경우가 많습니다.
- **유휴 회수** — [GPU 공유(MIG/time-slicing)](../kubernetes-and-scheduling/#gpu-공유--mig와-time-slicing)와 유휴 노드 스케일다운으로 낭비를 줄입니다.
- **GPU-시간 FinOps** — GPU 시간당 비용·활용률을 팀별로 배분·추적하는 체계는 [FinOps](../../../governance/finops/)와, 모델 라이선스·사용료는 [AI 라이선싱](../../../ai/licensing/)에서 다룹니다.

## 관련 문서

이 문서는 GPU 인프라 시리즈의 마지막(4부)입니다. 시리즈 전체는 [GPU 워크로드 특성과 레퍼런스 아키텍처](../workload-and-architecture/)에서 시작합니다.

- **클러스터 아키텍처·매니지드 클러스터** — [GPU 워크로드 특성과 레퍼런스 아키텍처](../workload-and-architecture/)
- **병렬화·체크포인트** — [분산 학습 표준 아키텍처](../distributed-training/)
- **스케줄링·GPU 공유·관측성** — [GPU 쿠버네티스와 스케줄링](../kubernetes-and-scheduling/)
- **비용 배분·예산** — [FinOps](../../../governance/finops/)
- **토큰·프롬프트 비용** — [LLMOps](../../../ai/llmops/)

## 자주 하는 실수

- **용량 확보를 설계 마지막에 확인** — 원하는 리전·세대의 GPU가 없어 프로젝트 일정이 지연
- **추론에 학습과 같은 구성 사용** — 지연·오토스케일 요구를 무시하고 학습용 대규모 구성을 그대로 적용해 비용 낭비
- **선점형을 체크포인트 없이 학습에 사용** — 중단 시 진행분을 전부 잃음
- **활용률 모니터링 없는 상시 온디맨드** — 유휴 GPU를 온디맨드로 계속 켜둬 비용이 누적

## 체크리스트

- [ ] 추론 서빙에 동적 배칭·오토스케일·콜드 스타트 완화를 적용했는가
- [ ] 대규모 학습에 실패 감지와 체크포인트 기반 자동 재개를 구성했는가
- [ ] 원하는 리전·세대의 GPU 용량을 사전 확인하고 예약했는가
- [ ] 멀티리전/폴백 전략을 데이터 위치·이그레스와 함께 검토했는가
- [ ] 약정·선점·용량예약을 워크로드 특성에 맞게 조합했는가
- [ ] GPU 활용률을 팀별로 추적하고 FinOps에 연계했는가

## 참고하기

### AWS

- [EC2 Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html)
- [Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)

### Azure

- [On-Demand Capacity Reservations](https://learn.microsoft.com/azure/virtual-machines/capacity-reservation-overview)
- [Azure Spot Virtual Machines](https://learn.microsoft.com/azure/virtual-machines/spot-vms)

### Google Cloud

- [Compute 예약](https://cloud.google.com/compute/docs/instances/reservations-overview)
- [Spot VMs](https://cloud.google.com/compute/docs/instances/spot)

### OCI

- [Capacity Reservation](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/reserve-capacity.htm)
- [Preemptible Instances](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/preemptible.htm)
