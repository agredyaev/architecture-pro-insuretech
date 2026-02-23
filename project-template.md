# InsureTech Architecture Project — навигация для ревью

## Быстрый доступ
- [Task1 — технологическая архитектура](#task1--технологическая-архитектура)
- [Task2 — динамическое масштабирование](#task2--динамическое-масштабирование)
- [Task3 — переход на Event-Driven](#task3--переход-на-event-driven)
- [Task4 — проектирование ОСАГО](#task4--проектирование-осаго)
- [Task5 — GraphQL API](#task5--graphql-api)
- [Task6 — Rate Limiting](#task6--rate-limiting)

## Матрица артефактов (для быстрой проверки)

| Задача | Ключевые решения | Артефакты | Evidence/отчёты |
| --- | --- | --- | --- |
| Task1 | Multi-region + DR, GeoDNS, HPA/CA, PITR | [ADR-0001](Task1/ADR-0001-architecture-decisions.md), [C4 diagram (puml)](Task1/inuretech-tech-arch-to-be.puml), [C4 diagram (png)](Task1/inuretech-tech-arch-to-be.png) | — |
| Task2 | HPA по memory и RPS, Prometheus | [README](Task2/README.md), [manifests/](Task2/manifests/) | [evidence/](Task2/evidence/), [logs/](Task2/logs/), [metrics-report](Task2/reports/metrics-report.md) |
| Task3 | Event-Driven + Transactional Outbox | [risks](Task3/risks.md), [container diagram (puml)](Task3/insuretech-container-to-be.puml), [container diagram (png)](Task3/insuretech-container-to-be.png) | — |
| Task4 | osago-aggregator, gRPC + Kafka, SSE, CB/R/T/RL | [ADR-0002](Task4/ADR-0002-osago-architecture-decisions.md), [osago diagram (puml)](Task4/insuretech-osago-to-be.puml), [osago diagram (png)](Task4/insuretech-osago-to-be.png) | — |
| Task5 | GraphQL контракт client-info | [Swagger](Task5/client-inf.yml), [GraphQL schema](Task5/client-info.schema.graphql) | — |
| Task6 | Nginx rate limiting | [trace-matrix](Task6/trace-matrix.md), [nginx.conf](Task6/nginx.conf) | — |

---

## Task1 — технологическая архитектура
**Ключевые решения:** multi-region active+DR, GeoDNS + L7 health checks, независимые Kubernetes-кластеры, HPA + Cluster Autoscaler, PITR, без шардинга при 50 GB.

**Артефакты:**
- ADR: [Task1/ADR-0001-architecture-decisions.md](Task1/ADR-0001-architecture-decisions.md)
- Диаграммы:
  - PlantUML: [Task1/inuretech-tech-arch-to-be.puml](Task1/inuretech-tech-arch-to-be.puml)
  - PNG: [Task1/inuretech-tech-arch-to-be.png](Task1/inuretech-tech-arch-to-be.png)

## Task2 — динамическое масштабирование
**Ключевые решения:** HPA по памяти (80%) и по RPS через Prometheus Adapter.

**Артефакты:**
- Инструкция запуска: [Task2/README.md](Task2/README.md)
- Манифесты:
  - Deployment: [Task2/manifests/deployment.yaml](Task2/manifests/deployment.yaml)
  - Service: [Task2/manifests/service.yaml](Task2/manifests/service.yaml)
  - HPA memory: [Task2/manifests/hpa-memory.yaml](Task2/manifests/hpa-memory.yaml)
  - HPA RPS: [Task2/manifests/hpa-rps.yaml](Task2/manifests/hpa-rps.yaml)
  - Prometheus Adapter: [Task2/manifests/prometheus-adapter-values.yaml](Task2/manifests/prometheus-adapter-values.yaml)
  - ServiceMonitor: [Task2/manifests/servicemonitor.yaml](Task2/manifests/servicemonitor.yaml)
- Evidence и отчёты:
  - Evidence: [Task2/evidence/](Task2/evidence/)
  - Логи: [Task2/logs/](Task2/logs/)
  - Отчёт: [Task2/reports/metrics-report.md](Task2/reports/metrics-report.md)

## Task3 — переход на Event-Driven
**Ключевые решения:** Kafka для асинхронного обмена, Transactional Outbox, отказ от синхронных REST цепочек.

**Артефакты:**
- Риски: [Task3/risks.md](Task3/risks.md)
- Диаграммы:
  - PlantUML: [Task3/insuretech-container-to-be.puml](Task3/insuretech-container-to-be.puml)
  - PNG: [Task3/insuretech-container-to-be.png](Task3/insuretech-container-to-be.png)

## Task4 — проектирование ОСАГО
**Ключевые решения:** osago-aggregator, PostgreSQL + Redis, gRPC + Kafka, SSE, паттерны CB/R/T/RL.

**Артефакты:**
- ADR: [Task4/ADR-0002-osago-architecture-decisions.md](Task4/ADR-0002-osago-architecture-decisions.md)
- Диаграммы:
  - PlantUML: [Task4/insuretech-osago-to-be.puml](Task4/insuretech-osago-to-be.puml)
  - PNG: [Task4/insuretech-osago-to-be.png](Task4/insuretech-osago-to-be.png)

## Task5 — GraphQL API
**Ключевые решения:** единая GraphQL-схема для client-info вместо множества REST ресурсов.

**Артефакты:**
- Swagger контракт: [Task5/client-inf.yml](Task5/client-inf.yml)
- GraphQL схема: [Task5/client-info.schema.graphql](Task5/client-info.schema.graphql)

## Task6 — Rate Limiting
**Ключевые решения:** Nginx limit_req_zone, лимит 10 r/m, 429 при превышении.

**Артефакты:**
- Trace matrix: [Task6/trace-matrix.md](Task6/trace-matrix.md)
- Nginx config: [Task6/nginx.conf](Task6/nginx.conf)
