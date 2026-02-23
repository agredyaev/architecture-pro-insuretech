# Task2 — запуск стенда

## Предусловия
- Активен нужный kubecontext (кластер Minikube).
- В кластере запущены metrics-server и Prometheus (Prometheus Adapter настроен).
- Python + `uv` доступны (Locust установлен через зависимости проекта).

## Быстрый запуск
```bash
uv run -- make -C Task2 clean-logs
uv run -- make -C Task2 memory
uv run -- make -C Task2 rps
```

## Что делает Makefile
- Разворачивает Deployment/Service.
- По очереди включает HPA memory или HPA RPS.
- Запускает Locust в headless режиме.
- Собирает логи, JSON из Prometheus и генерирует отчёт.

## Результаты
- Логи: `Task2/logs/`
- Отчёт: `Task2/reports/metrics-report.md`
- Evidence: `Task2/evidence/*.md`

> В Makefile используется `kubectl port-forward` на `localhost:18080` для стабильного доступа к сервису.
