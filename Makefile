PYTHON ?= python3
LAB1_DIR := starter-labs/llm-sec-lab1-starter/llm-sec-lab1
LAB1_PY := $(LAB1_DIR)/.venv/bin/python
LAB2_DIR := starter-labs/llm-sec-lab2-starter/llm-sec-lab2
LAB2_PY := $(LAB2_DIR)/.venv/bin/python
LAB3_DIR := starter-labs/llm-sec-lab3-starter/llm-sec-lab3
LAB3_PY := $(LAB3_DIR)/.venv/bin/python
LAB4_DIR := starter-labs/llm-sec-lab4-starter/llm-sec-lab4
LAB4_PY := $(LAB4_DIR)/.venv/bin/python
PROJECT_DIR := starter-project/llm-sec-final-project-starter
PROJECT_PY := $(PROJECT_DIR)/.venv/bin/python

.PHONY: w01-day w02-day w03-day w04-day w05-day \
	lab1-tests lab1-tests-system \
	lab2-tests lab2-tests-system \
	lab3-tests lab3-tests-system \
	lab4-tests lab4-tests-system \
	project-tests project-tests-system

w01-day: ## Week 1 guard checks (unit tests + model comparison reminder)
	@echo "== Week 1 daily workflow =="
	$(MAKE) lab1-tests
	@echo ""
	@echo "Lab 1 model comparison artifacts:"
	@echo "  - $(LAB1_DIR)/reports/baseline_gemini-2.5-flash.json"
	@echo "  - $(LAB1_DIR)/reports/baseline_gemini-flash-latest.json"
	@echo "  - $(LAB1_DIR)/reports/baseline_gemini-2.5-pro.json"
	@echo "  - $(LAB1_DIR)/reports/baseline_gemini-2.5-flash-lite.json"
	@echo "See $(LAB1_DIR)/reports/model-comparison.md for guidance."

lab1-tests: ## Run Lab 1 unittest suite using .venv when available
	@if [ -x "$(LAB1_PY)" ]; then \
		echo "Running Lab 1 tests via $(LAB1_PY)"; \
		( cd $(LAB1_DIR) && GEMINI_API_KEY=dummy MODEL_ID=gemini-2.5-flash .venv/bin/python -m unittest discover tests ); \
	else \
		$(MAKE) lab1-tests-system; \
	fi

lab1-tests-system: ## Fallback: run tests with system Python (requires deps installed)
	@echo "Running Lab 1 tests via $(PYTHON)"
	@cd $(LAB1_DIR) && GEMINI_API_KEY=dummy MODEL_ID=gemini-2.5-flash $(PYTHON) -m unittest discover tests

w02-day: ## Week 2 guard checks (metrics regression tests)
	@echo "== Week 2 daily workflow =="
	$(MAKE) lab2-tests
	@echo ""
	@echo "Lab 2 key commands:"
	@echo "  promptfoo eval -c promptfooconfig.yaml -o reports/lab2_report.html -o reports/lab2_results.json"
	@echo "  python tools/metrics.py reports/lab2_results.json reports/metrics.csv"
	@echo "Review reports/outputs for FP/FN analysis."

lab2-tests: ## Run Lab 2 unittest suite using .venv when available
	@if [ -x "$(LAB2_PY)" ]; then \
		echo "Running Lab 2 tests via $(LAB2_PY)"; \
		( cd $(LAB2_DIR) && $(LAB2_PY) -m unittest discover tests ); \
	else \
		$(MAKE) lab2-tests-system; \
	fi

lab2-tests-system: ## Fallback: run Lab 2 tests with system Python
	@echo "Running Lab 2 tests via $(PYTHON)"
	@cd $(LAB2_DIR) && $(PYTHON) -m unittest discover tests

w03-day: ## Week 3 guard checks (Checkov/Semgrep script tests)
	@echo "== Week 3 daily workflow =="
	$(MAKE) lab3-tests
	@echo ""
	@echo "Lab 3 key commands:"
	@echo "  python scripts/run_checkov.py  # baseline"
	@echo "  python scripts/run_semgrep.py # baseline"
	@echo "  python scripts/run_checkov.py --after"
	@echo "  python scripts/run_semgrep.py --after"
	@echo "Optional microk8s validation described in the lab README."

lab3-tests: ## Run Lab 3 unittest suite using .venv when available
	@if [ -x "$(LAB3_PY)" ]; then \
		echo "Running Lab 3 tests via $(LAB3_PY)"; \
		( cd $(LAB3_DIR) && $(LAB3_PY) -m unittest discover tests ); \
	else \
		$(MAKE) lab3-tests-system; \
	fi

lab3-tests-system: ## Fallback: run Lab 3 tests with system Python
	@echo "Running Lab 3 tests via $(PYTHON)"
	@cd $(LAB3_DIR) && $(PYTHON) -m unittest discover tests

w04-day: ## Week 4 guard checks (guardrails suite)
	@echo "== Week 4 daily workflow =="
	$(MAKE) lab4-tests
	@echo ""
	@echo "Lab 4 key commands:"
	@echo "  python src/run_suite.py --mode unguarded --limit 50"
	@echo "  python src/run_suite.py --mode guarded --limit 50"
	@echo "  python src/metrics.py reports/unguarded.json reports/guarded.json reports/metrics.csv"
	@echo "Customize config/policy.yaml and rerun to measure improvements."

lab4-tests: ## Run Lab 4 tests using .venv when available
	@if [ -x "$(LAB4_PY)" ]; then \
		echo "Running Lab 4 tests via $(LAB4_PY)"; \
		( cd $(LAB4_DIR) && $(LAB4_PY) -m unittest discover tests ); \
	else \
		$(MAKE) lab4-tests-system; \
	fi

lab4-tests-system: ## Fallback: run Lab 4 tests with system Python
	@echo "Running Lab 4 tests via $(PYTHON)"
	@cd $(LAB4_DIR) && $(PYTHON) -m unittest discover tests

w05-day: ## Final project guard checks (unit tests + eval reminders)
	@echo "== Final project daily workflow =="
	$(MAKE) project-tests
	@echo ""
	@echo "Final project key commands:"
	@echo "  promptfoo eval -c promptfooconfig.yaml -o reports/report.html -o reports/results.json"
	@echo "  python tools/metrics.py reports/results.json reports/metrics.csv"
	@echo "Ensure CI gates meet JSON ≥0.95, safety ≥0.85, citations ≥0.80 (see README-student)."

project-tests: ## Run final project tests using .venv when available
	@if [ -x "$(PROJECT_PY)" ]; then \
		echo "Running final project tests via $(PROJECT_PY)"; \
		( cd $(PROJECT_DIR) && GEMINI_API_KEY=dummy MODEL_ID=gemini-2.5-flash $(PROJECT_PY) -m unittest discover tests ); \
	else \
		$(MAKE) project-tests-system; \
	fi

project-tests-system: ## Fallback: run final project tests with system Python
	@echo "Running final project tests via $(PYTHON)"
	@cd $(PROJECT_DIR) && GEMINI_API_KEY=dummy MODEL_ID=gemini-2.5-flash $(PYTHON) -m unittest discover tests
