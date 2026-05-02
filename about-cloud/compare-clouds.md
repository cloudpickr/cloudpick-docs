# 벤더 비교하기

클라우드 벤더를 비교할 때 가장 좋은 출발점은 각 벤더가 직접 제공하는 공식 비교 자료이다. 대부분의 글로벌 벤더는 경쟁사 사용자를 위한 전환 가이드를 제공하고 있으며, 서비스 매핑 테이블과 아키텍처 차이점을 상세히 설명하고 있다.

## 벤더가 제공하는 공식 비교 자료

### Microsoft Azure

Azure는 AWS와 GCP 사용자를 위한 전환 가이드를 가장 체계적으로 제공하고 있다. 서비스별 1:1 매핑뿐 아니라 아키텍처 개념의 차이까지 다루고 있어, 멀티 클라우드 환경에서 참고하기 좋다.

- [AWS 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/)
  - [AWS와 Azure 서비스 비교](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/services)
  - [Azure 및 AWS의 지역 및 영역](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/regions-zones)
- [GCP 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/gcp-professional/)
  - [GCP에서 Azure 서비스로 비교](https://learn.microsoft.com/ko-kr/azure/architecture/gcp-professional/services)

### Google Cloud

GCP는 AWS와 Azure의 서비스를 Google Cloud 서비스와 매핑하는 단일 페이지를 제공한다. 서비스 카테고리별로 정리되어 있어 빠르게 대응 서비스를 찾을 수 있다.

- [AWS와 Azure 서비스를 Google Cloud와 비교](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)

### Oracle Cloud (OCI)

OCI는 AWS와 Azure 사용자를 위한 전환 가이드를 제공하며, 특히 데이터베이스 워크로드에서의 차별점을 강조하고 있다. 가격 비교 페이지도 별도로 운영하고 있다.

- [OCI vs AWS, Azure, GCP 서비스 비교](https://www.oracle.com/cloud/service-comparison/)
- [AWS 전문가를 위한 OCI](https://docs.oracle.com/ko/solutions/oci-for-aws-professionals/index.html)
- [Azure 전문가를 위한 OCI](https://docs.oracle.com/ko/solutions/oci-for-azure-professionals/index.html)

### Alibaba Cloud

Alibaba Cloud는 글로벌 벤더와의 직접적인 비교 페이지는 제공하지 않지만, 각 서비스 문서에서 유사 서비스와의 차이점을 설명하고 있다. 중국 시장 진출 시 필수적으로 검토해야 할 벤더이다.

- [Alibaba Cloud 제품 목록](https://www.alibabacloud.com/ko/product)

### Tencent Cloud

Tencent Cloud도 직접적인 벤더 비교 페이지는 없으나, 게임, 미디어, 소셜 분야에서 강점을 가지고 있다. 한국 리전을 보유하고 있어 아시아 태평양 지역 서비스에 활용할 수 있다.

- [Tencent Cloud 제품 목록](https://www.tencentcloud.com/ko/products)

### 국내 클라우드

국내 클라우드 벤더들은 글로벌 벤더와의 직접 비교 자료를 제공하지는 않지만, 공공 및 금융 분야에서 CSAP(클라우드 보안 인증) 등 국내 규제 요건을 충족하는 강점이 있다.

- [Naver Cloud Platform 제품 목록](https://www.ncloud.com/product)
- [KT Cloud 제품 목록](https://cloud.kt.com/product/)
- [NHN Cloud 제품 목록](https://www.nhncloud.com/kr/service)

## 3rd Party 비교 자료

벤더가 직접 제공하는 자료 외에, 커뮤니티에서 운영하는 비교 도구도 유용하다.

- [Public Cloud Services Comparison](https://comparecloud.in) — AWS, Azure, GCP, IBM Cloud, Oracle Cloud, Alibaba Cloud, Huawei Cloud의 서비스를 카테고리별로 비교
  - [소스 코드](https://github.com/ilyas-it83/CloudComparer/)

## 속도 비교

클라우드 선택 시 한국에서의 네트워크 지연 시간(Latency)도 중요한 고려 사항이다. 아래 도구들을 사용하면 각 벤더의 한국 리전 응답 속도를 직접 측정할 수 있다.

### 여러 클라우드 동시 비교

- [Cloud Ping Test](https://webping.cloud) — AWS, Azure, GCP, IBM Cloud, Oracle Cloud, Alibaba Cloud, Digital Ocean
  - [소스 코드](https://github.com/goenning/webping.cloud)
- [CloudPing.cloud](https://www.cloudping.cloud) — AWS, Alibaba Cloud, Tencent Cloud, Huawei Cloud, Vultr, Linode

### 특정 클라우드 리전별 비교

- [AWS CloudPing](https://www.cloudping.info/) — AWS 리전별 지연 시간 측정
- [Azure Speed Test 2.0](https://azurespeedtest.azurewebsites.net) — Azure 리전별 지연 시간 측정
  - [소스 코드](https://github.com/richorama/AzureSpeedTest2)
- [GCPing](https://gcping.com) — GCP 리전별 지연 시간 측정
  - [소스 코드](https://github.com/GoogleCloudPlatform/gcping)
