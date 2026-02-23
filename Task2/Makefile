SHELL := /bin/bash
.DEFAULT_GOAL := help

KUBECTL ?= kubectl
PYTHON ?= python3
LOCUST ?= locust

ROOT_DIR := $(abspath ..)
MANIFEST_DIR := manifests
LOG_DIR := logs
REPORT_DIR := reports
SCRIPT_DIR := scripts

PORT_FORWARD_LOCAL ?= 18080
PORT_FORWARD_LOG ?= /tmp/scaletestapp-port-forward.log

SERVICE_NAME ?= scaletestapp
NAMESPACE ?= default
APP_LABEL ?= app=scaletestapp

DEPLOYMENT := $(MANIFEST_DIR)/deployment.yaml
SERVICE := $(MANIFEST_DIR)/service.yaml
SERVICE_MONITOR := $(MANIFEST_DIR)/servicemonitor.yaml
PDB := $(MANIFEST_DIR)/pdb.yaml
NETWORK_POLICY := $(MANIFEST_DIR)/network-policy.yaml
INGRESS := $(MANIFEST_DIR)/ingress.yaml

MEMORY_HPA := $(MANIFEST_DIR)/hpa-memory.yaml
RPS_HPA := $(MANIFEST_DIR)/hpa-rps.yaml

WATCH_INTERVAL ?= 5
WATCH_ITERATIONS ?= 36

MEMORY_USERS ?= 150
MEMORY_SPAWN ?= 10
MEMORY_TIME ?= 2m

RPS_USERS ?= 100
RPS_SPAWN ?= 20
RPS_TIME ?= 2m

.PHONY: help apply delete clean-logs \
  apply-memory-hpa apply-rps-hpa \
  watch-memory watch-rps \
  locust-memory locust-rps \
  prom-logs report \
  memory rps all

help: ## Show available targets
	@awk 'BEGIN {FS=":.*##"; OFS=""} \
		/^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

apply: ## Apply deployment and service manifests
	$(KUBECTL) apply -f $(DEPLOYMENT)
	$(KUBECTL) apply -f $(SERVICE)
	-$(KUBECTL) apply -f $(SERVICE_MONITOR)
	-$(KUBECTL) apply -f $(PDB)
	-$(KUBECTL) apply -f $(NETWORK_POLICY)
	-$(KUBECTL) apply -f $(INGRESS)
	$(KUBECTL) rollout status deployment/$(SERVICE_NAME) --timeout=180s

delete: ## Remove deployment and service manifests
	-$(KUBECTL) delete -f $(DEPLOYMENT) --ignore-not-found
	-$(KUBECTL) delete -f $(SERVICE) --ignore-not-found
	-$(KUBECTL) delete -f $(SERVICE_MONITOR) --ignore-not-found
	-$(KUBECTL) delete -f $(PDB) --ignore-not-found
	-$(KUBECTL) delete -f $(NETWORK_POLICY) --ignore-not-found
	-$(KUBECTL) delete -f $(INGRESS) --ignore-not-found
	-$(KUBECTL) delete hpa scaletestapp-memory scaletestapp-rps --ignore-not-found

clean-logs: ## Remove Task2 logs
	@rm -f $(LOG_DIR)/*.log $(LOG_DIR)/*.md $(LOG_DIR)/*.json $(LOG_DIR)/*_stats.csv

apply-memory-hpa: ## Enable memory HPA (and remove RPS HPA)
	$(KUBECTL) delete hpa scaletestapp-rps --ignore-not-found
	$(KUBECTL) apply -f $(MEMORY_HPA)

apply-rps-hpa: ## Enable RPS HPA (and remove memory HPA)
	$(KUBECTL) delete hpa scaletestapp-memory --ignore-not-found
	$(KUBECTL) apply -f $(RPS_HPA)

watch-memory: ## Capture memory HPA scaling log
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR); \
	for i in $$(seq 1 $(WATCH_ITERATIONS)); do \
		date; \
		$(KUBECTL) get hpa scaletestapp-memory -o wide; \
		$(KUBECTL) get pods -l $(APP_LABEL) -o wide; \
		echo "---"; \
		sleep $(WATCH_INTERVAL); \
	done > $(LOG_DIR)/hpa-memory-scaling.md

watch-rps: ## Capture RPS HPA scaling log
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR); \
	for i in $$(seq 1 $(WATCH_ITERATIONS)); do \
		date; \
		$(KUBECTL) get hpa scaletestapp-rps -o wide; \
		$(KUBECTL) get pods -l $(APP_LABEL) -o wide; \
		echo "---"; \
		sleep $(WATCH_INTERVAL); \
	done > $(LOG_DIR)/hpa-rps-scaling.log

locust-memory: ## Run locust for memory scaling
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR); \
	$(KUBECTL) port-forward svc/$(SERVICE_NAME) $(PORT_FORWARD_LOCAL):8080 >$(PORT_FORWARD_LOG) 2>&1 & \
	PF_PID=$$!; \
	cleanup() { kill $$PF_PID >/dev/null 2>&1 || true; }; \
	trap cleanup EXIT INT TERM; \
	ready=0; \
	for i in $$(seq 1 10); do \
		if curl -fsS http://127.0.0.1:$(PORT_FORWARD_LOCAL)/ >/dev/null 2>&1; then ready=1; break; fi; \
		sleep 1; \
	done; \
	if [ $$ready -ne 1 ]; then \
		echo "Port-forward not ready. Check $(PORT_FORWARD_LOG)."; \
		cat $(PORT_FORWARD_LOG); \
		exit 1; \
	fi; \
	HOST="http://127.0.0.1:$(PORT_FORWARD_LOCAL)"; \
	echo "Locust host: $$HOST"; \
	$(LOCUST) -f $(SCRIPT_DIR)/locustfile.py --headless \
		-u $(MEMORY_USERS) -r $(MEMORY_SPAWN) -t $(MEMORY_TIME) \
		--host "$$HOST" --csv $(LOG_DIR)/locust-memory --csv-full-history

locust-rps: ## Run locust for RPS scaling
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR); \
	$(KUBECTL) port-forward svc/$(SERVICE_NAME) $(PORT_FORWARD_LOCAL):8080 >$(PORT_FORWARD_LOG) 2>&1 & \
	PF_PID=$$!; \
	cleanup() { kill $$PF_PID >/dev/null 2>&1 || true; }; \
	trap cleanup EXIT INT TERM; \
	ready=0; \
	for i in $$(seq 1 10); do \
		if curl -fsS http://127.0.0.1:$(PORT_FORWARD_LOCAL)/ >/dev/null 2>&1; then ready=1; break; fi; \
		sleep 1; \
	done; \
	if [ $$ready -ne 1 ]; then \
		echo "Port-forward not ready. Check $(PORT_FORWARD_LOG)."; \
		cat $(PORT_FORWARD_LOG); \
		exit 1; \
	fi; \
	HOST="http://127.0.0.1:$(PORT_FORWARD_LOCAL)"; \
	echo "Locust host: $$HOST"; \
	$(LOCUST) -f $(SCRIPT_DIR)/locustfile.py --headless \
		-u $(RPS_USERS) -r $(RPS_SPAWN) -t $(RPS_TIME) \
		--host "$$HOST" --csv $(LOG_DIR)/locust-rps --csv-full-history

prom-logs: ## Collect Prometheus JSON outputs
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR); \
	$(KUBECTL) get --raw \
		"/api/v1/namespaces/monitoring/services/http:kube-prometheus-stack-prometheus:9090/proxy/api/v1/targets" \
		> $(LOG_DIR)/prometheus-targets.json; \
	$(KUBECTL) get --raw \
		"/api/v1/namespaces/monitoring/services/http:kube-prometheus-stack-prometheus:9090/proxy/api/v1/query?query=http_requests_total" \
		> $(LOG_DIR)/prometheus-http_requests_total.json

report: ## Generate metrics report
	@set -euo pipefail; \
	cd $(ROOT_DIR); \
	$(PYTHON) Task2/scripts/collect_metrics_report.py \
		--output Task2/reports/metrics-report.md

memory: apply apply-memory-hpa ## Run memory HPA test flow
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR) $(REPORT_DIR); \
	sleep 5; \
	$(MAKE) --no-print-directory watch-memory & \
	WATCH_PID=$$!; \
	$(MAKE) --no-print-directory locust-memory; \
	wait $$WATCH_PID; \
	$(KUBECTL) describe hpa scaletestapp-memory > $(LOG_DIR)/hpa-memory-describe.log; \
	$(KUBECTL) describe pods -l $(APP_LABEL) > $(LOG_DIR)/scaletestapp-describe.log; \
	$(MAKE) --no-print-directory prom-logs; \
	$(MAKE) --no-print-directory report

rps: apply apply-rps-hpa ## Run RPS HPA test flow
	@set -euo pipefail; \
	mkdir -p $(LOG_DIR) $(REPORT_DIR); \
	sleep 5; \
	$(MAKE) --no-print-directory watch-rps & \
	WATCH_PID=$$!; \
	$(MAKE) --no-print-directory locust-rps; \
	wait $$WATCH_PID; \
	$(KUBECTL) describe hpa scaletestapp-rps > $(LOG_DIR)/hpa-rps-describe.log; \
	$(KUBECTL) describe pods -l $(APP_LABEL) > $(LOG_DIR)/scaletestapp-describe.log; \
	$(MAKE) --no-print-directory prom-logs; \
	$(MAKE) --no-print-directory report

all: memory rps ## Run memory test then RPS test