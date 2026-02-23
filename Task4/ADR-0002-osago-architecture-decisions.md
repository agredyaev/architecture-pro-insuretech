# ADR-0002 — Архитектурные решения OSAGO (Task4)

Дата: 2026-01-31
Статус: Принято

## Контекст

InsureTech запускает новый продукт — оформление ОСАГО онлайн. Требования:
- Пиковая нагрузка: 2500 одновременных пользователей
- Максимальное время ожидания ответа от страховой: 60 секунд
- Предложения должны отображаться по мере поступления (real-time)
- Интеграция с 10+ страховыми компаниями через REST API
- Сервисы развёрнуты в нескольких репликах (multi-replica deployment)

## Требования

| ID | Формулировка требования | Обоснование | Способ проверки |
|---|---|---|---|
| REQ-OSAGO-001 | Система SHALL выделить отдельный сервис osago-aggregator для взаимодействия со страховыми компаниями. | Изоляция ответственности; независимое масштабирование; упрощение Circuit Breaker логики. | Инспекция архитектурной диаграммы; проверка deployment манифестов. |
| REQ-OSAGO-002 | osago-aggregator SHALL иметь собственное хранилище данных (PostgreSQL) для состояния заявок и предложений. | Идемпотентность при retry; аудит; независимость от core-app при отказах. | Проверка схемы БД; инспекция миграций. |
| REQ-OSAGO-003 | osago-aggregator SHALL использовать Redis для distributed locks и кэширования состояний. | Предотвращение дублирования polling при multi-replica deployment. | Тест параллельного запуска; проверка конфигурации Redis. |
| REQ-OSAGO-004 | Интеграция core-app → osago-aggregator SHALL использовать gRPC с timeout. | Низкая латентность; строгая типизация; поддержка streaming. | Инспекция proto-файлов; измерение латентности. |
| REQ-OSAGO-005 | osago-aggregator SHALL публиковать события OsagoOfferReceived в Kafka для доставки предложений в core-app. | Асинхронная доставка; decoupling; гарантия доставки at-least-once. | Проверка Kafka topics; тест consumer lag. |
| REQ-OSAGO-006 | core-app SHALL предоставлять SSE endpoint для real-time отображения предложений в web-app. | Требование бизнеса: предложения отображаются по мере поступления. | Функциональный тест SSE; измерение задержки доставки. |
| REQ-OSAGO-007 | osago-aggregator SHALL применять Circuit Breaker [CB] для каждой страховой компании с параметрами: failure threshold 50%, wait duration 30s, half-open requests 3. | Изоляция отказов одной страховой от остальных; предотвращение каскадных сбоев. | Тест отказа страховой; проверка метрик CB state. |
| REQ-OSAGO-008 | osago-aggregator SHALL применять Retry [R] с exponential backoff (max 3 attempts, initial 1s, multiplier 2) для polling страховых. | Устойчивость к временным сбоям сети; соблюдение timeout 60s. | Тест retry при 5xx ошибках; проверка логов. |
| REQ-OSAGO-009 | osago-aggregator SHALL применять Timeout [T] для всех внешних вызовов: connection 5s, read 60s. | Соответствие требованию максимального времени ожидания 60s. | Тест timeout; проверка конфигурации HTTP client. |
| REQ-OSAGO-010 | API Gateway SHALL применять Rate Limiting [RL] для защиты от перегрузки; osago-aggregator SHALL применять per-insurer rate limiting согласно SLA. | Защита от DDoS; соблюдение SLA со страховыми компаниями. | Нагрузочный тест; проверка 429 ответов при превышении лимита. |

## Решения

### 1. Хранилище данных osago-aggregator

**Решение:** PostgreSQL (отдельная схема) + Redis

**Альтернативы:**
- Без хранилища (stateless) — отклонено: невозможно обеспечить идемпотентность и аудит
- Только Redis — отклонено: недостаточно для долгосрочного хранения и аудита

### 2. API osago-aggregator ↔ core-app

**Решение:** gRPC для синхронных вызовов + Kafka для событий

**Альтернативы:**
- REST — отклонено: выше латентность, нет строгой типизации
- WebSocket — отклонено: избыточно для server-to-server коммуникации

### 3. API web-app ↔ core-app (real-time)

**Решение:** Server-Sent Events (SSE)

**Альтернативы:**
- WebSocket — отклонено: избыточно для однонаправленного потока
- Long polling — отклонено: выше нагрузка на сервер, хуже UX

### 4. Паттерны отказоустойчивости

**Решение:** Комбинация [CB] + [R] + [T] + [RL]

| Паттерн | Где применяется | Параметры |
|---------|-----------------|-----------|
| Rate Limiting [RL] | API Gateway, osago-aggregator→insurers | Per-client, per-insurer limits |
| Circuit Breaker [CB] | osago-aggregator→каждая страховая | 50% threshold, 30s wait, 3 half-open |
| Retry [R] | osago-aggregator→страховые (polling) | 3 attempts, 1s initial, x2 backoff |
| Timeout [T] | Все внешние вызовы | 5s connect, 60s read |

### 5. Multi-replica deployment

**Решение:** Stateless osago-aggregator + distributed state

- Состояние заявок в PostgreSQL
- Distributed locks через Redis (предотвращение дублирования polling)
- Kafka consumer groups для параллельной обработки событий

## Последствия

- Требуется мониторинг Circuit Breaker state для каждой страховой
- Kafka consumer lag должен отслеживаться для SLA real-time доставки
- Redis требует high availability конфигурации
- Необходимы runbooks для ручного сброса Circuit Breaker при восстановлении страховой

## Связанные артефакты

- Диаграмма: `Task4/insuretech-osago-to-be.puml`
- Предыдущий ADR: `Task1/ADR-0001-architecture-decisions.md`
