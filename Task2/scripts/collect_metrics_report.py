from __future__ import annotations

# ruff: noqa: RUF001
import argparse
import csv
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def run(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(  # noqa: S603
        cmd, capture_output=True, text=True, check=False
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def run_raw(path: str) -> tuple[int, str, str]:
    return run(["kubectl", "get", "--raw", path])


def fmt_block(title: str, body: str) -> str:
    safe_body = body if body else "(пусто)"
    return f"\n### {title}\n\n```\n{safe_body}\n```\n"


def read_locust_stats(csv_path: Path) -> str:
    if not csv_path.exists():
        return "Файл не найден."
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return "Данные отсутствуют."
    aggregated = [row for row in rows if row.get("Name") == "Aggregated"]
    row = aggregated[-1] if aggregated else rows[-1]
    return (
        "Type={type}, Name={name}, Requests={requests}, Failures={fails}, "
        "RPS={rps}, Avg={avg}, Min={min}, Max={max}".format(
            type=row.get("Type"),
            name=row.get("Name"),
            requests=row.get("# requests"),
            fails=row.get("# failures"),
            rps=row.get("Requests/s"),
            avg=row.get("Average response time"),
            min=row.get("Min response time"),
            max=row.get("Max response time"),
        )
    )


def summarize_prom_targets(raw_json: str) -> str:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return "Не удалось разобрать JSON."
    active = data.get("data", {}).get("activeTargets", [])
    total = len(active)
    up = [t for t in active if t.get("health") == "up"]
    samples = [t.get("labels", {}) for t in up[:3]]
    return f"targets_total={total}, targets_up={len(up)}, sample_labels={samples}"


def summarize_prom_query(raw_json: str) -> str:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return "Не удалось разобрать JSON."
    result = data.get("data", {}).get("result", [])
    if not result:
        return "Результатов нет."
    sample = result[0]
    return f"metric={sample.get('metric')}, value={sample.get('value')}"


def summarize_custom_metric(raw_json: str) -> str:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return "Не удалось разобрать JSON."
    items = data.get("items", [])
    if not items:
        return "Данные отсутствуют."
    sample = items[0]
    return f"items={len(items)}, sample={sample.get('metricName')}={sample.get('value')}"


def generate_report(output_path: Path, namespace: str) -> None:
    now = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M:%S")
    report = [f"# Task2 — Отчет по метрикам\n\nДата: `{now}`\n"]

    sections: list[tuple[str, Iterable[str]]] = [
        (
            "Статус кластера",
            [
                "kubectl config current-context",
                "kubectl get nodes -o wide",
                "kubectl get pods -n kube-system -l k8s-app=metrics-server -o wide",
                "kubectl get apiservice v1beta1.metrics.k8s.io -o wide",
            ],
        ),
        (
            "Статус приложения",
            [
                "kubectl get deploy,svc,pods -l app=scaletestapp -o wide",
                "kubectl get hpa -o wide",
            ],
        ),
        (
            "HPA memory",
            ["kubectl describe hpa scaletestapp-memory"],
        ),
        (
            "HPA RPS",
            ["kubectl describe hpa scaletestapp-rps"],
        ),
        (
            "Метрики ресурса",
            ["kubectl top pods", f"kubectl top pods -n {namespace}"],
        ),
    ]

    for title, commands in sections:
        for cmd in commands:
            code, out, err = run(cmd.split(" "))
            header = f"{title}: {cmd} (exit={code})"
            body = out or err
            report.append(fmt_block(header, body))

    code, raw, err = run_raw("/apis/custom.metrics.k8s.io/v1beta1")
    report.append(fmt_block("Custom Metrics API (list)", raw or err))
    code, raw, err = run_raw(
        f"/apis/custom.metrics.k8s.io/v1beta1/namespaces/{namespace}/pods/*/http_requests_per_second"
    )
    custom_metric_summary = summarize_custom_metric(raw or err)
    report.append(
        fmt_block("Custom Metric http_requests_per_second", custom_metric_summary)
    )

    prom_targets_path = (
        "/api/v1/namespaces/monitoring/services/http:kube-prometheus-stack-prometheus:9090/"
        "proxy/api/v1/targets"
    )
    code, raw, err = run_raw(prom_targets_path)
    report.append(fmt_block("Prometheus targets", summarize_prom_targets(raw or err)))

    prom_query_path = (
        "/api/v1/namespaces/monitoring/services/http:kube-prometheus-stack-prometheus:9090/"
        "proxy/api/v1/query?query=http_requests_total"
    )
    code, raw, err = run_raw(prom_query_path)
    prom_query_summary = summarize_prom_query(raw or err)
    report.append(fmt_block("Prometheus query http_requests_total", prom_query_summary))

    report.append("\n## Locust (memory)\n")
    report.append(read_locust_stats(Path("Task2/logs/locust-memory_stats.csv")))

    report.append("\n## Locust (RPS)\n")
    report.append(read_locust_stats(Path("Task2/logs/locust-rps_stats.csv")))

    output_path.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect metrics and render MD report.")
    parser.add_argument("--output", default="Task2/reports/metrics-report.md")
    parser.add_argument("--namespace", default="default")
    args = parser.parse_args()
    generate_report(Path(args.output), args.namespace)


if __name__ == "__main__":
    main()
