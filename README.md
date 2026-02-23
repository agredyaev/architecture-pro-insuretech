# InsureTech Architecture Project

## Technology Stack

<p>
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white" alt="Kubernetes" />
  <img src="https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white" alt="Prometheus" />
  <img src="https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white" alt="Nginx" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white" alt="Apache Kafka" />
  <img src="https://img.shields.io/badge/GraphQL-E10098?logo=graphql&logoColor=white" alt="GraphQL" />
  <img src="https://img.shields.io/badge/gRPC-00B5E2?logo=grpc&logoColor=white" alt="gRPC" />
  <img src="https://img.shields.io/badge/PlantUML-6DB33F?logo=plantuml&logoColor=white" alt="PlantUML" />
</p>

Insurance platform architecture with multi-region resilience, event-driven communication, and auto-scaling capabilities.

## Architecture Overview

![Architecture Diagram](Task1/inuretech-tech-arch-to-be.png)

![Event-Driven Architecture](Task3/insuretech-container-to-be.png)

![OSAGO Extension](Task4/insuretech-osago-to-be.png)

## Project Artifacts

| Focus | Key Artifacts |
|-------|---------------|
| Multi-region architecture | [ADR-0001](Task1/ADR-0001-architecture-decisions.md), [C4 diagrams](Task1/inuretech-tech-arch-to-be.puml) |
| Dynamic auto-scaling | [HPA configs](Task2/manifests/), [metrics report](Task2/reports/metrics-report.md) |
| Event-driven migration | [Transactional outbox](Task3/risks.md), [container diagram](Task3/insuretech-container-to-be.puml) |
| OSAGO service design | [gRPC+Kafka pattern](Task4/ADR-0002-osago-architecture-decisions.md) |
| GraphQL API | [Schema design](Task5/client-info.schema.graphql) |
| Rate limiting | [Nginx config](Task6/nginx.conf), [trace matrix](Task6/trace-matrix.md) |

## Key Decisions

- **Multi-region active-active** with GeoDNS and automated failover
- **Event-driven communication** using Kafka with transactional outbox pattern
- **Auto-scaling** based on memory (80%) and RPS metrics via Prometheus
- **OSAGO aggregator** implementing gRPC services with Circuit Breaker pattern

## Navigation

📋 **For detailed review**: See [project-template.md](project-template.md) for complete artifact matrix and evidence.
