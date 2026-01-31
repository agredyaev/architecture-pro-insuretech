# Trace Matrix — Task6 Rate Limiting

## Requirements

### REQ-TASK6-001
Ограничение количества запросов от партнёров для защиты производительности приложения.

## User Stories

### US-TASK6-001
Как оператор системы, я хочу ограничить количество запросов от партнёров, чтобы один партнёр не мог потреблять все ресурсы системы.

## Acceptance Criteria

### AC-TASK6-001
Система SHALL ограничивать количество запросов до 10 в минуту на один IP-адрес.

### AC-TASK6-002
Система SHALL возвращать HTTP-код 429 (Too Many Requests) при превышении лимита.

## Architecture Decisions

### ADR-TASK6-001
Использование Nginx `limit_req_zone` для реализации rate limiting на уровне reverse proxy.

## Tasks

### TASK6-IMPL-001
Создание конфигурации Nginx с rate limiting (10 req/min, 429 response).

## Evidence

### EVID-TASK6-001
Конфигурация `limit_req_zone` с `rate=10r/m` в `Task6/nginx.conf:5`.

### EVID-TASK6-002
Директива `limit_req_status 429` и обработчик `@too_many_requests` в `Task6/nginx.conf:29,42-46`.
