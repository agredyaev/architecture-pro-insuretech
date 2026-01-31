# Prometheus Evidence — Task2

Дата: 2026-01-31

## Метрика http_requests_total

Prometheus успешно собирает метрику `http_requests_total` из приложения `scaletestapp`.

**Запрос:** `http_requests_total`

**Результат (JSON):**
```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "http_requests_total",
          "container": "scaletestapp",
          "endpoint": "http",
          "instance": "10.244.0.17:8080",
          "job": "scaletestapp",
          "namespace": "default",
          "pod": "scaletestapp-65c6bc858-tl2hf",
          "service": "scaletestapp"
        },
        "value": [1769863937.082, "9952"]
      }
    ]
  }
}
```

## Target scaletestapp

```json
{
  "job": "scaletestapp",
  "health": "up"
}
```

## Вывод

- Prometheus корректно скрейпит метрики из `scaletestapp`.
- Метрика `http_requests_total` доступна и увеличивается при запросах.
- Target `scaletestapp` имеет статус `up`.

Файлы:
- `Task2/logs/prometheus-http_requests_total.json`
- `Task2/logs/prometheus-targets.json`
