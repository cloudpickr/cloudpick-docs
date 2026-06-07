# GPU 인스턴스

> 최종 업데이트: 2026-06-07

AI/ML 워크로드를 위한 GPU 인스턴스를 클라우드 벤더별로 비교합니다.

## 개요

GPU 인스턴스(GPU Instance)는 머신러닝 학습, 추론, 그래픽 렌더링 등 병렬 연산이 필요한 워크로드를 위한 가상머신입니다. 각 CSP는 NVIDIA GPU를 기반으로 다양한 인스턴스 유형을 제공합니다.

## 벤더별 비교

| 항목 | AWS | Azure | GCP | OCI |
|------|-----|-------|-----|-----|
| 서비스명 | EC2 P/G 시리즈 | NC/ND 시리즈 | A2/G2 시리즈 | GPU 인스턴스 |
| 최신 GPU | NVIDIA H100 (p5) | NVIDIA H100 (ND H100 v5) | NVIDIA H100 (a3-highgpu) | NVIDIA A10 |
| 최대 GPU/노드 | 8 (p5.48xlarge) | 8 (ND H100 v5) | 8 (a3-highgpu-8g) | 2 (GPU.A10.2) |
| Spot/선점형 | Spot Instance (최대 90% 할인) | Spot VM (최대 90%) | Spot VM (최대 91%) | Preemptible (50%) |
| 추론 전용 | Inf2 (Inferentia2) | - | Cloud TPU | - |
| 관리형 학습 | SageMaker | Azure ML | Vertex AI | Data Science |

## 가격 비교 (NVIDIA A100 80GB 기준, 시간당)

| 벤더 | 인스턴스 | On-Demand | Spot/선점형 |
|------|----------|-----------|------------|
| AWS | p4d.24xlarge (8xA100) | ~$32.77/h | ~$12-15/h |
| Azure | NC A100 v4 (1xA100) | ~$3.67/h | ~$1.10/h |
| GCP | a2-highgpu-1g (1xA100) | ~$3.67/h | ~$1.10/h |
| OCI | GPU.A100 (1xA100) | ~$2.95/h | - |

> 💡 OCI는 A100 단가가 가장 저렴하지만 가용 리전이 제한적입니다.

## 선택 가이드

### 대규모 학습 (Training)
- **AWS**: SageMaker + p5 (H100) — 생태계가 가장 풍부
- **Azure**: ND H100 v5 + Azure ML — OpenAI 파트너십으로 LLM 학습에 강점
- **GCP**: A3 + Vertex AI — TPU 대안으로 가격 경쟁력

### 추론 (Inference)
- **AWS**: Inf2 (Inferentia2) — 가성비 최고, SageMaker 엔드포인트
- **GCP**: Cloud TPU — 대규모 추론 시 가격 유리
- **OCI**: A10 — 중소 규모 추론에 가장 저렴

### 비용 절감 팁
1. **Spot/선점형 활용**: 학습 중 체크포인트 저장 필수
2. **Reserved/Committed Use**: 장기 워크로드는 1-3년 약정으로 60-70% 절감
3. **멀티클라우드 전략**: OCI(학습) + AWS Inf2(추론) 조합

## 참고하기

- [AWS EC2 인스턴스 유형](https://aws.amazon.com/ec2/instance-types/)
- [Azure GPU VM](https://learn.microsoft.com/azure/virtual-machines/sizes/gpu-accelerated/overview)
- [GCP GPU 플랫폼](https://cloud.google.com/compute/docs/gpus)
- [OCI GPU 인스턴스](https://docs.oracle.com/iaas/Content/Compute/References/computeshapes.htm)

---

💡 클라우드 GPU 인프라 설계가 필요하신가요? → [무료 30분 상담 예약](https://cal.com/cloudpick/consult)
