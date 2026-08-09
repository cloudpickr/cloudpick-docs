---
title: "API Gateway"
description: "Compares the role of API Gateway, authentication integration, and deployment strategies across vendors."
---

> Last reviewed: May 2026

## Overview

When exposing backend services externally as APIs, implementing authentication, rate limiting, request transformation, and monitoring separately for every service creates duplication. **API Gateway** acts as a front door that handles these common concerns in one place.

This is similar to putting authentication/routing logic into a reverse proxy (Nginx, HAProxy) on-premises, but a cloud API Gateway is managed and provides integrated scaling, monitoring, and even a developer portal.

### Key Features

- **Authentication/authorization** — Access control via API keys, OAuth, JWT, IAM
- **Rate limiting (throttling)** — Protects the backend by limiting requests per second
- **Request/response transformation** — Adding headers, body mapping, protocol conversion
- **Caching** — Caches responses for repeated requests
- **Monitoring** — Automatically collects request counts, latency, error rates
- **Developer portal** — Auto-generated API documentation, key issuance

### Authentication/Authorization Integration

API Gateway itself doesn't handle authentication logic — it integrates with an external authentication service.

| Vendor | Authentication service | Notes |
| --- | --- | --- |
| AWS | Cognito | User pools + social login. Native integration with API Gateway |
| AWS | Lambda Authorizer | Implement custom authentication logic in Lambda |
| Azure | Entra ID (formerly Azure AD) | OAuth 2.0 / OpenID Connect |
| Azure | APIM Policy (validate-jwt) | Configure JWT token validation as a policy |
| Google Cloud | Firebase Auth / Identity Platform | Social login, multi-factor authentication |
| Google Cloud | Service Account + IAM | Service-to-service authentication |
| OCI | OCI IAM / Identity Domains | OAuth 2.0, JWT validation |

### Additional Features

| Feature | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Usage plans/quotas** | Usage Plans + API Keys | Subscription + Quota Policy | Apigee Rate Limiting | Rate Limiting Policy |
| **Request validation** | Request Validator (model schema) | APIM Policy (validate-content) | Apigee OAS Validation | Request Validation Policy |
| **Custom domain** | Custom Domain + ACM certificate | Custom Domain + Managed Certificate | Custom Domain + SSL | Custom Domain + SSL certificate |
| **WebSocket** | WebSocket API | — (separate SignalR) | — (separate Firebase Realtime) | — |
| **GraphQL** | AppSync | — (3rd party) | — (3rd party) | — |

## Product Comparison

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | API Gateway (REST/HTTP/WebSocket) | Native integration with Lambda. Ideal for serverless API composition |
| AWS | AppSync | GraphQL-only. Supports real-time subscriptions |
| Azure | API Management (APIM) | Built-in developer portal. Unifies multicloud/hybrid APIs |
| Google Cloud | Apigee | Enterprise API management platform. Analytics/monetization features |
| Google Cloud | API Gateway | Lightweight. Good fit for Cloud Functions/Cloud Run integration |
| OCI | OCI API Gateway | OCI Functions integration. Supports authentication, rate limiting, request transformation |

## Key Differences

**AWS API Gateway** — Has the deepest integration with Lambda, optimized for exposing serverless backends as APIs. It's split into 3 types for different purposes (REST API / HTTP API / WebSocket API), and HTTP API costs about 1/3 of REST API. Most new projects start with HTTP API, choosing REST API only when caching, WAF, or Usage Plans are needed.

**Azure API Management** — A full-featured platform with a built-in developer portal, API versioning, and policy engine. A single service handles REST, WebSocket, and GraphQL. On-premises and cloud APIs can be unified under a single gateway.

**Google Cloud Apigee** — An enterprise platform that manages APIs as a product. A single service handles all protocols, with strengths in API usage analytics, monetization, and partner management.

**OCI API Gateway** — Natively integrates with OCI Functions, and a single service lets you configure authentication (JWT validation), rate limiting, and request transformation as policies.

## API Deployment Stages and Version Management

Since an API becomes hard to change once deployed to production, staged deployment (dev→staging→production) and version management are important.

| Feature | AWS API Gateway | Azure APIM | Google Cloud Apigee | OCI API Gateway |
| --- | --- | --- | --- | --- |
| **Stage/environment** | Stages (dev, staging, prod) | Environments | Environments (test, prod) | Deployments |
| **Canary deployment** | Canary Deployment (weight-based) | Revision + Release | Revision + TargetServer | Route Rule (weight-based) |
| **Version management** | API Version (v1, v2 as separate endpoints) | API Revision + Version | API Revision + Version | Spec Version |
| **Rollback** | Switch to a previous Deployment | Switch Revision | Switch Revision | Switch to a previous Deployment |

## Progressive Deployment Strategies

:::note
Once an API is exposed publicly, **maintaining backward compatibility** is essential. Don't delete or change the response format of an endpoint with existing consumers — instead, manage it by adding a new version (`/v2`).
:::

| Strategy | Description | Vendor implementation |
| --- | --- | --- |
| **Canary** | Send a small amount of traffic (5-10%) to the new version, monitor, then expand | AWS: API Gateway Canary Deployment (Stage weighting), Azure APIM: Revision + Traffic Split, Google Cloud Apigee: TargetServer weighting |
| **Blue/Green** | Run two environments simultaneously, then switch traffic. Immediate rollback possible | AWS: switch Stage, Azure APIM: switch Revision, Google Cloud: switch Revision |
| **Version separation** | Coexist as separate `/v1`, `/v2` endpoints | Supported by every vendor. New version added without affecting existing consumers |

:::caution
API Gateway's own Canary feature is a canary for "gateway configuration changes." A canary for backend code deployment must be handled separately, via Lambda Alias weighting, load balancer Target Group weighting, or a service mesh.
:::

## OpenAPI (Swagger) Integration

Teams that defined API specs with Swagger on-premises can maintain the same workflow in the cloud.

- **Import**: Automatically generate the API Gateway from an OpenAPI spec (supported by AWS, Azure APIM, and Apigee)
- **Export**: Extract the OpenAPI spec from the API Gateway for documentation
- **IaC integration**: Define the OpenAPI spec inline in CloudFormation/Terraform to manage the API configuration as code
- **Developer portal**: Azure APIM and Apigee automatically generate interactive API documentation from the OpenAPI spec

## API Testing Tools

| Tool | Role | Relationship with API Gateway |
| --- | --- | --- |
| Postman | Manual API testing, collection management, environment variables | Manage per-stage URLs as environments, auto-refresh auth tokens |
| Swagger UI | Interactive documentation based on the OpenAPI spec | Auto-generated from the spec exported by API Gateway |
| Vendor console testing | AWS console Test tab, APIM Test tab | Quick validation before deployment |
| curl / httpie | Fast CLI-based testing | Smoke testing in a CI/CD pipeline |

Cloud APIs have complex authentication flows (OAuth, API Key, IAM Sig v4) and frequently switch between environments (dev/staging/prod), so it's efficient to manage environment variables and authentication systematically with a tool like Postman.

## Common Mistakes

- **Starting with REST API without distinguishing it from HTTP API** — On AWS, HTTP API costs 1/3 and meets most requirements. Choose REST API only when caching, WAF, or Usage Plans are needed.
- **Changing an existing response format without API versioning** — Existing consumers (clients) break immediately. Add a new version (`/v2`) and keep the existing version running.
- **Mistaking API Gateway's Canary for a backend code deployment canary** — API Gateway Canary is about gateway configuration changes. Backend code deployment needs to be configured separately, via Lambda Alias weighting or an LB Target Group.

## Checklist

- [ ] Is authentication/authorization (API Key, JWT, IAM) applied to every endpoint?
- [ ] Is rate limiting (throttling) configured to prevent backend overload?
- [ ] Is the OpenAPI spec synced with IaC so the API configuration is managed as code?

## References

### AWS

- [Amazon API Gateway Documentation](https://docs.aws.amazon.com/ko_kr/apigateway/)
- [API Gateway Authentication/Authorization](https://docs.aws.amazon.com/ko_kr/apigateway/latest/developerguide/apigateway-control-access-to-api.html)
- [Amazon Cognito Documentation](https://docs.aws.amazon.com/ko_kr/cognito/)
- [AWS AppSync Documentation](https://docs.aws.amazon.com/ko_kr/appsync/)

### Azure

- [Azure API Management Documentation](https://learn.microsoft.com/ko-kr/azure/api-management/)
- [APIM Authentication Policies](https://learn.microsoft.com/ko-kr/azure/api-management/authentication-authorization-overview)
- [Microsoft Entra ID Documentation](https://learn.microsoft.com/ko-kr/entra/identity/)

### Google Cloud

- [Apigee Documentation](https://cloud.google.com/apigee/docs)
- [API Gateway Documentation](https://cloud.google.com/api-gateway/docs)
- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)
- [Identity Platform Documentation](https://cloud.google.com/identity-platform/docs)

### OCI

- [OCI API Gateway Documentation](https://docs.oracle.com/en-us/iaas/Content/APIGateway/home.htm)
