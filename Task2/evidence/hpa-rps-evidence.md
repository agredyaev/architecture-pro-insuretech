# HPA RPS Scaling Evidence — Task2

Дата: 2026-01-31

## Конфигурация HPA

- **Метрика:** `http_requests_per_second` (custom metric через Prometheus Adapter)
- **Target:** 20 RPS на под
- **Min replicas:** 1
- **Max replicas:** 10

## Нагрузочный тест (Locust)

- **Параметры:** 100 пользователей, spawn rate 20, длительность 120 секунд
- **Результат:** 3951 запрос, 0 ошибок, ~33.1 RPS

## Масштабирование

При нагрузке ~33 RPS HPA увеличил количество реплик с 1 до 2.

**Лог (выдержка):**
```
Sat Jan 31 13:50:09 CET 2026
NAME               REFERENCE                 TARGETS     MINPODS   MAXPODS   REPLICAS   AGE
scaletestapp-rps   Deployment/scaletestapp   32932m/20   1         10        1          61s
NAME                           READY   STATUS    RESTARTS   AGE   IP            NODE    NOMINATED NODE   READINESS GATES
scaletestapp-65c6bc858-qmqcq   0/1     Running   0          1s    10.244.0.21   task2   <none>           <none>
scaletestapp-65c6bc858-tl2hf   1/1     Running   0          9m   10.244.0.17   task2   <none>           <none>
---
Sat Jan 31 13:50:24 CET 2026
NAME               REFERENCE                 TARGETS     MINPODS   MAXPODS   REPLICAS   AGE
scaletestapp-rps   Deployment/scaletestapp   32932m/20   1         10        2          76s
NAME                           READY   STATUS    RESTARTS   AGE   IP            NODE    NOMINATED NODE   READINESS GATES
scaletestapp-65c6bc858-qmqcq   1/1     Running   0          16s   10.244.0.21   task2   <none>           <none>
scaletestapp-65c6bc858-tl2hf   1/1     Running   0          10m  10.244.0.17   task2   <none>           <none>
```

## Вывод

HPA на основе RPS работает корректно: при превышении target (20 RPS) количество реплик увеличивается.

## Файлы

- `Task2/logs/hpa-rps-scaling.log` — полный лог масштабирования
- `Task2/logs/locust-rps_stats.csv` — статистика Locust
- `Task2/logs/locust-rps_stats_history.csv` — временной ряд Locust
