# HPA Memory Scaling Evidence — Task2

Дата: 2026-01-31

## Конфигурация HPA

- **Метрика:** memory (resource)
- **Target:** 80% от request (15Mi)
- **Min replicas:** 1
- **Max replicas:** 10

## Доказательства работы HPA

### 1. Масштабирование (1 → 2 → 3 реплики)

Из лога `Task2/logs/hpa-memory-scaling.md`:
```
Sat Jan 31 13:46:09 CET 2026
NAME                  REFERENCE                 TARGETS           MINPODS   MAXPODS   REPLICAS   AGE
scaletestapp-memory   Deployment/scaletestapp   memory: 99%/80%   1         10        2          158m
---
Sat Jan 31 13:47:36 CET 2026
NAME                  REFERENCE                 TARGETS           MINPODS   MAXPODS   REPLICAS   AGE
scaletestapp-memory   Deployment/scaletestapp   memory: 96%/80%   1         10        3          160m
```

### 2. Статус HPA (describe)

Из лога `Task2/logs/hpa-memory-describe.log`:
```
resource memory on pods  (as a percentage of request):  82% (12924245333m) / 80%
Deployment pods:       3 current / 3 desired
```

### 3. Вывод

HPA на основе памяти работает корректно:
- Метрики памяти собираются через metrics-server
- При превышении target 80% HPA масштабировал деплой до 3 реплик

## Файлы

- `Task2/logs/hpa-memory-scaling.md` — лог мониторинга HPA
- `Task2/logs/hpa-memory-describe.log` — describe HPA memory
- `Task2/logs/locust-memory_stats.csv` — статистика Locust
