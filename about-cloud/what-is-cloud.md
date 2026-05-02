# 클라우드란?

## 클라우드의 정의

**클라우드(Cloud Computing)**는 서비스 구축을 위한 인프라를 빠르고, 높은 효율성과 함께, 규모의 경제를 이용해 비용을 절감할 수 있도록 도와주는 서비스라고 할 수 있다.

모두에게 잘 알려진 비용 절감이나 안정적인 운영을, 클라우드를 사용하는 것만으로는 기대하긴 어렵다. 클라우드의 운영 방식에 맞춰서 어플리케이션이 잘 사용할 수 있도록 아키텍처를 변경하는 과정이 필요하다. 아키텍처를 변경하고, 관리형 서비스를 최대한 활용하면, 운영 리소스를 효율화해 가용한 인적/비용 자원을 비지니스에 집중할 수 있게 된다.

## 공동 책임 모델

클라우드를 사용한다고 해서 모든 보안과 운영 책임이 벤더에게 넘어가는 것은 아니다. 대부분의 클라우드 벤더는 **공동 책임 모델(Shared Responsibility Model)**을 채택하고 있으며, 인프라의 물리적 보안은 벤더가, 그 위에서 동작하는 애플리케이션과 데이터의 보안은 사용자가 책임진다.

AWS, Azure, OCI는 전통적인 공동 책임 모델을 따르고 있다. GCP는 여기서 한 발 더 나아가 **공동 운명 모델(Shared Fate)**이라는 개념을 제시하며, 벤더가 고객의 보안 성공에 더 적극적으로 관여하겠다는 입장을 취하고 있다.

국내 클라우드인 Naver Cloud Platform, KT Cloud, NHN Cloud도 각각의 보안 정책과 컴플라이언스 체계를 갖추고 있으며, 금융 및 공공 분야의 규제 요건에 맞춘 보안 인증(CSAP 등)을 보유하고 있다.

## Well-Architected Framework

각 벤더는 클라우드 위에서 잘 설계된 워크로드를 구축하기 위한 모범 사례를 **Well-Architected Framework**이라는 이름으로 제공하고 있다. 보안, 안정성, 비용 최적화, 운영 효율성 등의 핵심 원칙(Pillar)을 다루며, 클라우드 아키텍처를 설계할 때 반드시 참고해야 할 자료이다.

AWS가 가장 먼저 Well-Architected Framework을 정립했고, 이후 Azure, GCP, OCI가 각각의 버전을 발표했다. Alibaba Cloud와 Tencent Cloud도 자체 Well-Architected 가이드를 제공하고 있다.

## 클라우드 도입 프레임워크

대규모 조직이 클라우드로 전환할 때는 기술뿐 아니라 조직, 프로세스, 거버넌스까지 함께 변화해야 한다. 이를 체계적으로 안내하는 것이 **Cloud Adoption Framework(CAF)**이다. AWS와 Azure가 대표적인 CAF를 제공하고 있으며, GCP는 아키텍처 프레임워크 안에 도입 가이드를 포함하고 있다.

## 참고하기

### AWS

- [공동 책임 모델](https://aws.amazon.com/ko/compliance/shared-responsibility-model/)
- [Well-Architected Framework](https://aws.amazon.com/ko/architecture/well-architected/)
  - [Well-Architected Labs](https://www.wellarchitectedlabs.com/)
- [Cloud Adoption Framework](https://aws.amazon.com/ko/cloud-adoption-framework/)

### Azure

- [클라우드의 공동 책임](https://learn.microsoft.com/ko-kr/azure/security/fundamentals/shared-responsibility)
- [Well-Architected Framework](https://learn.microsoft.com/ko-kr/azure/well-architected/)
- [클라우드 채택 프레임워크](https://learn.microsoft.com/ko-kr/azure/cloud-adoption-framework/)

### GCP

- [공동 운명 모델 (Shared Fate)](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate)
- [아키텍처 프레임워크](https://cloud.google.com/architecture/framework)
- [BeyondCorp (제로 트러스트)](https://cloud.google.com/beyondcorp)

### OCI

- [공동 책임 모델](https://docs.public.content.oci.oraclecloud.com/en-us/iaas/Content/cloud-adoption-framework/oci-shared-responsibility.htm)
- [Well-Architected Framework](https://docs.oracle.com/en/solutions/oci-best-practices/)
- [Cloud Adoption Framework](https://docs.oracle.com/en/solutions/oci-best-practices/toc.htm)

### Alibaba Cloud

- [공동 책임 모델](https://www.alibabacloud.com/help/en/cs/security-responsibility-sharing-model)
- [Well-Architected 가이드](https://www.alibabacloud.com/help/en/well-architected/latest/overview)

### Tencent Cloud

- [공동 책임 모델](https://www.tencentcloud.com/services/compliance-best-practice)
- [Well-Architected Framework (TSA)](https://www.tencentcloud.com/document/product/1079/78581)

### Naver Cloud Platform

- [보안 가이드](https://www.ncloud.com/intro/security)
- [컴플라이언스](https://www.ncloud.com/intro/compliance)

### KT Cloud

- [보안 서비스](https://cloud.kt.com/product/security/)
- [컴플라이언스](https://cloud.kt.com/trust/)

### NHN Cloud

- [보안 서비스](https://www.nhncloud.com/kr/service/security)
- [인증 및 컴플라이언스](https://www.nhncloud.com/kr/support/compliance)
