Lab 4 Student Runbook — Guardrails + Automated Red Team
=======================================================
> Author : Badr TAJINI - LLM Cybersecurity - ECE 2025/2026

Goal: measure how much **guardrails** improve **block rate** and reduce **unsafe passes** by running the **provided attack** set in both **`unguarded`** and **`guarded`** modes.

---

## 0. Prereqs

- Python 3.9+
- `pip install -r requirements.txt`
- Gemini API key (`.env`)

Optional: If you want to extend the guardrails stack, you can install microk8s and NVIDIA NeMo Guardrails per the README; not required for baseline.

---

## 1. Setup

```bash
git clone <your-private-fork>
cd starter-labs/llm-sec-lab4-starter/llm-sec-lab4
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set GEMINI_API_KEY and MODEL_ID if needed
```

---

## 2. Baseline runs

```bash
python src/run_suite.py --mode unguarded --limit 50
python src/run_suite.py --mode guarded --limit 50
python src/metrics.py reports/unguarded.json reports/guarded.json reports/metrics.csv
```

`reports/metrics.csv` shows block rate and unsafe-pass rate for each mode. Include these values in your 1-page analysis and cite example attacks.

---

## 3. Customize guardrails (required)

- Update `config/policy.yaml` with deny-regex patterns tailored to your attack set.
- Add PII or custom pattern entries.
- Update `src/guardrails.py` TODO comment if you adapt the system instruction.

You must demonstrate at least **two new rules** (input or output) and show their impact in `reports/metrics.csv`.

---

## 4. Optional microk8s sandbox

To experiment with hosting the attack runner or integrating NeMo Guardrails:

```bash
sudo snap install microk8s --classic
sudo usermod -a -G microk8s "$USER"
microk8s status --wait-ready
# Example: microk8s enable dns storage dashboard
```

Use `microk8s kubectl` to deploy the guardrails service if you convert it into a microservice. This is optional but a good demonstration for advanced teams.

---

## 5. Automated tests

```bash
python -m unittest discover tests
# or from repo root: make w04-day
```

Tests mock the attack loop to ensure `run_suite` writes reports and `metrics.py` computes expected stats. Passing tests are required before submitting PRs.

---

## 6. Publish changes

```bash
git status -sb
git add config/policy.yaml src/guardrails.py reports/*.json reports/metrics.csv
# include your write-up (PDF/MD) and examples
git commit -m "Lab4: tuned guardrails and metrics"
git push
```

Keep the repo private and avoid committing real API keys.

Deliverables checklist:

- ✅ `reports/unguarded.json` and `reports/guarded.json`
- ✅ `reports/metrics.csv`
- ✅ Updated `config/policy.yaml` plus guardrails explanation
- ✅ 1-page report with before/after stats and examples

