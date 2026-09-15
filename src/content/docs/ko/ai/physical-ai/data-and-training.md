---
title: "Physical AI 데이터와 학습"
description: "엣지 추론·IoT 하드웨어와 센서 데이터 파이프라인(계층 1), 디지털 트윈·시뮬레이션·공개 데이터셋·Sim-to-Real(계층 2), 그리고 규모에 맞는 학습 인프라 선택을 벤더 중립 관점에서 비교합니다."
---

> 문서 기준: 2026년 9월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

## 개요

이 문서는 Physical AI 파이프라인의 앞단 — **물리 세계에서 데이터가 들어와 학습 자산이 되기까지** — 를 다룹니다. 전체 파이프라인 개관은 [Physical AI 개요](../overview/)를, 학습된 모델을 배포·운영하는 뒷단은 [배포와 운영](../deploy-and-operate/)을 참고하세요.

## 계층 1 — 엣지 추론과 IoT

물리 세계의 데이터는 대량이고 실시간이라, 모두 클라우드로 보내 처리하기 어렵습니다. 현장(엣지)에서 먼저 추론하고, 필요한 데이터만 클라우드로 올리는 구조가 기본입니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| 엣지 런타임 | [IoT Greengrass](https://docs.aws.amazon.com/greengrass/v2/developerguide/) | [Azure IoT Operations](https://learn.microsoft.com/azure/iot-operations/) / [IoT Edge](https://learn.microsoft.com/azure/iot-edge/) | [Google Distributed Cloud (Edge)](https://cloud.google.com/distributed-cloud) | [Roving Edge Infrastructure](https://www.oracle.com/cloud/roving-edge-infrastructure/) |
| 엣지 ML 추론 | Greengrass ML 컴포넌트 (SageMaker AI 모델 배포) | IoT Edge 모듈 + Azure AI 서비스 | Edge TPU / Coral (현행 지원 상태 확인 필요) | RED 상의 컴퓨트로 자체 구성 |
| 산업 데이터 수집 | [IoT SiteWise](https://aws.amazon.com/iot-sitewise/) (OPC UA) | IoT Operations (OPC UA) | — (파트너·자체 구성) | — (자체 구성) |

:::caution
**Azure Percept는 2023년 3월 은퇴**했습니다. 과거 자료에서 Percept를 엣지 AI 하드웨어로 소개하더라도, 현재는 Azure IoT Edge / IoT Operations와 Azure Certified Device 파트너 하드웨어로 유사 기능을 구성합니다(Microsoft가 단일 공식 후속 제품을 지정한 것은 아닙니다). 오래된 제품명을 아키텍처 전제로 삼지 마세요.
:::

### 엣지 추론 하드웨어

엣지 런타임이 소프트웨어 계층이라면, 그 아래에서 실제로 추론을 수행하는 **가속기 하드웨어** 선택이 실현 가능성과 TCO를 좌우합니다. 판단 기준은 네 가지입니다 — 목표 모델을 돌릴 **연산 성능**, 모델이 올라갈 **메모리 용량**, 로봇의 **전력·발열 예산**, 그리고 **소프트웨어 생태계의 수명**입니다.

| 계열 | 성격 | 유의점 |
| --- | --- | --- |
| 로보틱스 특화 엣지 모듈 (예: [NVIDIA Jetson](https://developer.nvidia.com/embedded/jetson-modules) 계열) | 저전력 소형 모듈부터 고성능 모듈까지 폭이 넓어, 로보틱스 VLA 온디바이스 추론에서 자주 검토되는 선택지 | 세대·모듈 간 성능과 메모리 차이가 크고 가격대도 크게 벌어집니다. 목표 모델이 해당 모듈 메모리에 올라가는지 먼저 확인하세요 |
| 범용 CPU 내장 NPU·소형 가속기 | 분류·검출 같은 경량 비전에 충분하고 전력·단가가 낮음 | 대형 멀티모달·VLA 추론에는 메모리와 대역폭이 부족한 경우가 많습니다 |
| FPGA·산업용 SoC | 결정론적 지연과 장기 공급 보장이 중요한 설비에 유리 | 개발 난이도가 높고 모델 이식 비용이 큽니다 |
| 클라우드 사업자 엣지 어플라이언스 | 클라우드 운영 도구·관리 체계를 현장으로 확장 | 현장 서버·게이트웨이 용도이며, 로봇 온보드의 실시간 제어를 대체하지 않습니다 |

:::caution
**TOPS 수치만으로 비교하지 마세요.** 벤더가 제시하는 연산 성능은 정밀도(INT8·FP4 등)와 희소성(sparsity) 적용 여부에 따라 기준이 달라, 서로 다른 조건의 숫자를 나란히 놓으면 비교가 성립하지 않습니다. 실제 추론 속도는 메모리 용량·대역폭과 모델의 적합성이 좌우하는 경우가 많으므로, **목표 모델을 대상 모듈에서 실제로 측정**하는 편이 확실합니다.
:::

:::caution
엣지 가속기는 **소프트웨어 생태계의 수명**이 하드웨어 수명만큼 중요합니다. 드라이버·런타임 업데이트가 멈춘 제품은 새 커널·새 모델 포맷을 지원하지 못해 조기에 교체 압력이 생깁니다. 위 계층 1 표의 [Google Edge TPU / Coral](https://developers.google.com/coral/guides/faq)이 그 예로, 공식 제품 EOL 공지가 없는 상태에서도 [레거시 API 저장소가 아카이브되어 '더 이상 유지보수되지 않는다'고 명시](https://github.com/google-coral/edgetpu)되어 있습니다. 이름이 비슷한 **Coral NPU는 실리콘 파트너용 오픈소스 NPU IP로 별개**이며 Edge TPU 모듈 제품군의 공식 후속이 아니므로, 같은 제품의 후속으로 읽지 마세요. 신규 설계에 넣기 전 **현행 지원 상태와 드라이버 업데이트 이력을 직접 확인**하세요. 가격도 고정값이 아니어서 세대 교체 시점에 조정되는 사례가 있으므로, 대량 배포 계획은 견적을 다시 받아 검증해야 합니다.
:::

### 센서 데이터 파이프라인 — 수집·저장·라벨링

엣지에서 올라온 데이터를 바로 학습에 쓸 수는 없습니다. Physical AI의 데이터는 **1D 시계열(관절 각도·전류·온도), 2D 영상, 3D 포인트 클라우드, 설비 메타데이터가 섞인 멀티모달**이라, 수집 → 저장 → 정제·라벨링 단계를 거쳐야 학습 파이프라인에 들어갑니다.

| 단계 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| 스트림·영상 수집 | [IoT Core](https://aws.amazon.com/iot-core/) (엣지 입구) / [Kinesis Video Streams](https://aws.amazon.com/kinesis/video-streams/)·[Data Streams](https://aws.amazon.com/kinesis/data-streams/) (다운스트림 적재) | [Event Hubs](https://learn.microsoft.com/azure/event-hubs/) + IoT Operations | [Pub/Sub](https://cloud.google.com/pubsub) | [OCI Streaming](https://www.oracle.com/cloud/streaming/) |
| 데이터 레이크 | [S3](https://aws.amazon.com/s3/) | [Data Lake Storage](https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-introduction) | [Cloud Storage](https://cloud.google.com/storage) | [Object Storage](https://www.oracle.com/cloud/storage/object-storage/) |
| 학습용 병렬 파일 시스템 | [FSx for Lustre](https://aws.amazon.com/fsx/lustre/) | [Azure Managed Lustre](https://azure.microsoft.com/products/managed-lustre) | [Managed Lustre](https://cloud.google.com/products/managed-lustre) / [Parallelstore](https://cloud.google.com/parallelstore) | [File Storage with Lustre](https://www.oracle.com/cloud/storage/file-storage-with-lustre/) |
| 라벨링 | [SageMaker Ground Truth](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html) (신규 고객 접수 종료) | [Azure ML 데이터 라벨링](https://learn.microsoft.com/azure/machine-learning/how-to-label-data) | — (관리형 종료, 파트너·오픈소스) | [OCI Data Labeling](https://www.oracle.com/artificial-intelligence/data-labeling/) |

:::caution
**관리형 라벨링 서비스는 오히려 줄어드는 추세입니다.** Google Cloud의 Vertex AI 데이터 라벨링은 [2024년 10월 3일 종료](https://cloud.google.com/vertex-ai/docs/deprecations)되었고, AWS SageMaker Ground Truth는 2026년 7월 30일부터 신규 고객을 받지 않습니다(기존 고객은 계속 사용, 신규 기능 추가 계획 없음). Ground Truth Plus는 2026년 6월 30일 지원이 종료되었습니다. 라벨링을 특정 클라우드의 관리형 서비스에 묶어 설계하지 말고, **오픈소스·파트너 도구로 대체 가능한 구조**를 기본값으로 두세요.
:::

:::note
GPU 학습에서 병목은 연산이 아니라 **데이터 로딩과 체크포인트 쓰기**인 경우가 많습니다. 객체 스토리지에서 직접 읽으면 GPU가 놀게 되므로, 학습 구간에는 병렬 파일 시스템을 앞단에 두고 객체 스토리지와 연동하는 구성이 일반적입니다. 스토리지 계층 일반 비교는 [블록·파일 스토리지](../../../storage/block-and-file/), 체크포인트 전략은 [분산 학습](../../gpu-infra/distributed-training/)을 참고하세요.
:::

## 계층 2 — 디지털 트윈과 시뮬레이션

로봇·차량을 실제 세계에서만 학습시키면 비용·위험·시간이 큽니다. 그래서 물리 환경을 가상으로 복제한 **디지털 트윈**과 **시뮬레이션**에서 대량의 시나리오를 생성·학습한 뒤 현실로 옮기는 sim-to-real 접근이 자리 잡았습니다.

| 항목 | AWS | Azure | Google Cloud | OCI | 크로스벤더 |
| --- | --- | --- | --- | --- | --- |
| 디지털 트윈 | [IoT TwinMaker](https://aws.amazon.com/iot-twinmaker/) | [Azure Digital Twins](https://learn.microsoft.com/azure/digital-twins/) | — (Spanner Graph·BigQuery 등으로 자체 구성) | — | [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/) |
| 로봇·물리 시뮬레이션 | — (RoboMaker 지원 종료, 자체 구성) | — (파트너·자체 구성) | — (파트너·자체 구성) | — | [NVIDIA Isaac Sim / Isaac Lab](https://developer.nvidia.com/isaac/sim) |

:::caution
**AWS RoboMaker는 2025년 9월 10일 지원이 종료**되었습니다. 현재 AWS에서 로봇 시뮬레이션은 전용 관리형 서비스 없이 GPU 인스턴스 + 오픈소스(Isaac Sim, Gazebo 등)로 직접 구성합니다. EOL(지원 종료)된 서비스를 신규 설계에 넣지 않도록 주의하세요.
:::

:::note
디지털 트윈·로봇 시뮬레이션 계층은 **NVIDIA Omniverse·Isaac 생태계가 널리 활용되고 있습니다.** 주요 클라우드 모두 이 스택을 GPU 인스턴스 위에서 실행하는 형태로 지원하며, 특정 클라우드의 전용 관리형 제품에 의존하기보다 **어느 클라우드에서도 옮겨 실행할 수 있는지(이식성)** 를 먼저 확인하는 것이 락인을 줄이는 길입니다.
:::

### 학습 데이터는 왜 부족한가

시뮬레이션이 선택이 아니라 전제가 되는 이유는 **데이터 희소성** 때문입니다. 언어 모델은 인터넷 텍스트라는 사실상 무한한 사전학습 데이터에서 출발했지만, "로봇이 실제로 물건을 집어 옮긴" 데이터는 자릿수가 다르게 적습니다. Physical AI 학습은 값싸고 많은 데이터로 부족한 부분을 메우는 설계에서 시작합니다.

| 데이터 층 | 성격 | 한계 |
| --- | --- | --- |
| 인터넷 영상·이미지·텍스트 | 사실상 무한하고 값쌈. 일반 상식·물체 지식을 제공 | 로봇의 몸·관절 명령과 직접 연결되지 않음 |
| 사람 작업 영상(1인칭) | 상대적으로 많음. 동작 순서·의도의 힌트를 제공 | 사람 몸 기준이라 로봇 embodiment로 그대로 옮기지 못함 |
| 로봇 teleop 에피소드 | 실제 관절 명령을 담아 가장 정확 | 사람이 로봇을 직접 조종해 만들어야 해 수집 비용이 가장 높음 |

**teleoperation(원격 조작)** 은 사람이 조종기·VR 장비로 로봇을 직접 움직여 시연 데이터를 만드는 방식이고, 이 데이터를 그대로 따라 하도록 학습시키는 것이 **모방학습(imitation learning)** 입니다. 가장 확실한 방법이지만 사람의 시간이 곧 비용이라 규모를 키우기 어렵습니다.

:::note
클라우드 비용 산정 관점에서 이 구조는 **GPU 비용과 별개의 축이 존재한다**는 뜻입니다. 데이터 수집(장비·인건비), 저장·전송, 라벨링 비용이 학습 연산 비용과 독립적으로 발생하므로, GPU 시간만으로 TCO를 추정하면 크게 빗나갑니다.
:::

### 공개 데이터셋과 벤치마크 생태계

데이터 희소성은 한 조직이 혼자 메우기 어렵기 때문에, 여러 기관이 데이터를 모으고 평가 과제를 공유하는 공개 생태계가 형성되어 있습니다. 스택을 고를 때 **"이 스택에서 어떤 공개 자산을 그대로 쓸 수 있는가"** 는 락인을 판단하는 실질적 기준이 됩니다.

| 구분 | 대표 자산 | 무엇에 쓰나 |
| --- | --- | --- |
| 교차 로봇 데이터셋 | [Open X-Embodiment](https://github.com/google-deepmind/open_x_embodiment) ([논문](https://arxiv.org/abs/2310.08864)) | 여러 기관의 로봇 데이터를 통합한 컬렉션. cross-embodiment 사전학습의 기준선 |
| 대규모 조작 데이터셋 | [DROID](https://github.com/droid-dataset/droid) | 다양한 환경에서 수집한 teleop 데이터 |
| 시뮬레이션 벤치마크 | [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO), [CALVIN](https://github.com/mees/calvin), [RoboCasa](https://github.com/robocasa/robocasa), [Meta-World](https://github.com/Farama-Foundation/Metaworld) | 표준 과제 모음에서 작업 성공률로 정책을 비교 |
| 사람 작업 영상 | [Ego4D](https://ego4d-data.org/) | 1인칭 작업 영상. 위 데이터 3층의 중간층에 해당 |
| 오픈 툴체인 | [LeRobot](https://github.com/huggingface/lerobot) | 데이터 포맷·학습·평가를 묶은 오픈소스 스택 |

:::caution
공개 데이터셋은 **라이선스 조건이 자산마다 다릅니다.** 연구용으로만 허용되거나 출처 표시·파생물 공개를 요구하는 경우가 있어, 상업적 제품에 학습 자산으로 쓰기 전에 각 데이터셋의 라이선스와 하위 구성 요소(개별 기관이 기여한 부분)의 조건을 함께 확인해야 합니다. 예를 들어 Open X-Embodiment는 단일 라이선스가 아니라 **구성 데이터셋별로 조건이 다르고**, Ego4D는 상업적 이용에 별도 약관이 적용되는 경우가 있습니다.
:::

:::note
공개 데이터셋으로 사전학습된 모델을 쓰면 초기 데이터 수집량을 줄일 수 있지만, **자사 로봇의 embodiment와 대상 작업이 그 데이터에 포함되어 있는지**가 실제 효과를 가릅니다. 벤치마크 성적도 마찬가지로, 측정 조건이 다르면 비교 대상이 되지 않습니다([무엇으로 합격을 판정할 것인가](../deploy-and-operate/#무엇으로-합격을-판정할-것인가) 참고).
:::

### Sim-to-Real Gap

시뮬레이션의 가치는 명확하지만, **시뮬레이터의 물리·센서·재질 모델은 현실과 미세하게 다릅니다.** 마찰 계수, 조명, 센서 노이즈, 부품 유격 같은 차이가 쌓여 시뮬레이션에서 성공한 정책이 실제 로봇에서 실패하는 현상을 **Sim-to-Real Gap**이라고 합니다.

일반적인 완화 방법은 세 가지입니다.

- **도메인 랜덤화** — 마찰·질량·조명·텍스처 같은 물리 파라미터를 학습 중에 무작위로 흔들어, 현실이 그 분포 안에 들어오게 만듭니다.
- **실물 데이터 소량 미세조정** — 시뮬레이션으로 사전학습한 정책을 실제 로봇 데이터로 마무리 조정합니다.
- **실물 검증 게이트** — 시뮬레이션 성공률과 별도로, 실제 장비에서의 성공률을 배포 기준으로 둡니다.

:::caution
**시뮬레이션 성공률을 배포 근거로 그대로 쓰지 마세요.** 시뮬레이션 지표는 회귀 감지에는 유용하지만 현실 성능을 보장하지 않습니다. 시뮬레이터를 고를 때도 렌더링 품질뿐 아니라 **대상 도메인의 물리 정확도**(접촉·마찰·변형 등)를 함께 보아야 합니다.
:::

## 규모에 맞는 학습 인프라

Physical AI에서 흔한 오해가 "로봇 모델 학습에는 무조건 대형 GPU 클러스터가 필요하다"는 것입니다. 실제로는 **사전학습된 로봇 파운데이션 모델을 자사 로봇·작업에 맞추는 미세조정**이 대부분이고, 이 구간은 LLM 사전학습과 규모가 전혀 다릅니다. 소규모 PEFT·어댑터 학습은 단일 GPU의 단기 작업으로 끝나는 경우가 많습니다.

| 단계 | 작업 성격 | 인프라 패턴 | 비용 전략 |
| --- | --- | --- | --- |
| 초기 검증 | 시연 데이터 소량, LoRA·PEFT 어댑터 학습 | 단일 GPU 인스턴스 1대 | 스팟·선점형 인스턴스가 기본값. 중단돼도 재시작 비용이 작음 |
| 작업 특화 | 시연 데이터 중간 규모, 전체 미세조정 | 단일 노드 다중 GPU + 관리형 학습 작업 | 자동 체크포인트·재개가 있는 관리형 학습 서비스 |
| 플랫폼화 | 다수 로봇·다수 작업, 반복 재학습 | 다중 노드 + 고속 인터커넥트 | 예약·약정 할인. 노드 자동 복구 필요 ([분산 학습](../../gpu-infra/distributed-training/) 참고) |

:::note
이 사다리의 실질적 함의는 **첫 단계에서 대규모 약정을 하지 말라**는 것입니다. 초기·작업 특화 구간은 스팟/선점형 인스턴스와 종량제로 충분한 경우가 많고, 예약·약정은 재학습 주기가 정례화된 뒤에 검토해도 늦지 않습니다. 반대로 시뮬레이션은 병렬 환경 수를 늘릴수록 GPU를 오래 점유하므로, 학습보다 시뮬레이션이 비용을 지배하는 경우가 자주 있습니다. GPU 인스턴스 계열·인터커넥트의 벤더 매핑은 [GPU 워크로드와 아키텍처](../../gpu-infra/workload-and-architecture/)를 참고하세요.
:::

## 자주 하는 실수

- **모든 데이터를 클라우드로 보내기** — 지연·대역폭·비용을 무시한 설계는 실시간 제어에서 실패합니다. 엣지 추론 분담이 먼저입니다.
- **EOL 제품을 신규 설계에 사용** — RoboMaker·Percept·관리형 라벨링 서비스처럼 지원이 종료되거나 축소된 서비스를 오래된 자료만 보고 채택하지 마세요.
- **단일 벤더 시뮬레이터에 종속** — 특정 클라우드 전용 시뮬레이션에 학습 파이프라인을 묶으면 이식·비교가 어려워집니다.
- **GPU 비용만으로 TCO 추정** — 데이터 수집·저장·라벨링과 시뮬레이션 점유 비용이 학습 연산과 별개로 발생합니다.
- **시뮬레이션 성공률을 배포 근거로 사용** — 실물 rollout 검증 게이트 없이 배포하면 Sim-to-Real Gap이 현장에서 드러납니다.

## 체크리스트

### 데이터·비용

- [ ] 센서 데이터의 저장·정제·라벨링 계층을 설계하고, 라벨링 도구의 대체 가능성을 확인했는가?
- [ ] 데이터 수집·저장·라벨링·시뮬레이션 비용을 GPU 비용과 별도로 산정했는가?
- [ ] 사용할 공개 데이터셋·벤치마크의 라이선스와 자사 embodiment 커버리지를 확인했는가?

### 하드웨어·학습

- [ ] 엣지 가속기를 TOPS 수치가 아니라 목표 모델 실측으로 선정하고, 드라이버·런타임의 지원 수명을 확인했는가?
- [ ] 학습 규모에 맞는 인프라 단계를 골랐는가(초기 검증에 과도한 약정을 하지 않았는가)?
- [ ] 디지털 트윈·시뮬레이션 스택이 다른 클라우드로 이식 가능한가(락인 점검)?
- [ ] 사용하려는 IoT·로보틱스 서비스가 현행 지원 상태인가(EOL 확인)?

## 관련 문서

- [Physical AI 개요](../overview/) — 전체 파이프라인·계층 구조·미해결 문제
- [배포와 운영](../deploy-and-operate/) — 로보틱스 파운데이션 모델·안전·아키텍처·fleet 배포
- [블록·파일 스토리지](../../../storage/block-and-file/) — 병렬 파일 시스템 비교
- [GPU 인프라](../../gpu-infra/workload-and-architecture/) — 클라우드 학습·시뮬레이션용 GPU 클러스터
- [분산 학습](../../gpu-infra/distributed-training/) — 다중 노드 학습·체크포인트 전략

## 참고하기

### AWS

- [AWS IoT Greengrass 개발자 가이드](https://docs.aws.amazon.com/greengrass/v2/developerguide/)
- [AWS IoT TwinMaker](https://aws.amazon.com/iot-twinmaker/)
- [AWS IoT SiteWise](https://aws.amazon.com/iot-sitewise/)
- [Amazon FSx for Lustre](https://aws.amazon.com/fsx/lustre/)
- [Amazon SageMaker Ground Truth 문서](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html)

### Azure

- [Azure IoT Operations 문서](https://learn.microsoft.com/azure/iot-operations/)
- [Azure Digital Twins 문서](https://learn.microsoft.com/azure/digital-twins/)
- [Azure Managed Lustre](https://azure.microsoft.com/products/managed-lustre)
- [Azure Machine Learning 데이터 라벨링](https://learn.microsoft.com/azure/machine-learning/how-to-label-data)

### Google Cloud

- [Google Distributed Cloud](https://cloud.google.com/distributed-cloud)
- [Coral / Edge TPU](https://cloud.google.com/edge-tpu)
- [Google Cloud Managed Lustre](https://cloud.google.com/products/managed-lustre)
- [Google Cloud Parallelstore](https://cloud.google.com/parallelstore)

### OCI

- [Oracle Roving Edge Infrastructure](https://www.oracle.com/cloud/roving-edge-infrastructure/)
- [OCI File Storage with Lustre](https://www.oracle.com/cloud/storage/file-storage-with-lustre/)
- [OCI Data Labeling](https://www.oracle.com/artificial-intelligence/data-labeling/)

### 공개 데이터셋·툴체인

- [Open X-Embodiment (저장소)](https://github.com/google-deepmind/open_x_embodiment) · [논문](https://arxiv.org/abs/2310.08864)
- [LeRobot (오픈소스 로보틱스 툴체인)](https://github.com/huggingface/lerobot)
- [Ego4D](https://ego4d-data.org/)
