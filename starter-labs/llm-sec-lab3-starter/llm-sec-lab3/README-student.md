Lab 3 Student Runbook — Config & IaC Security (Checkov + Semgrep + Gemini)
=======================================================
> Author : Badr TAJINI - LLM Cybersecurity - ECE 2025/2026

**Goal:** baseline **Checkov/Semgrep** findings for the provided **Terraform**, **Kubernetes**, and **Docker** assets, remediate at least three issues, re-scan, and explain the improvement. **Gemini** is optional but encouraged for remediation suggestions.

---

## 0. Prereqs

- Python 3.9+
- `pip install checkov` and `pip install semgrep`
- Optional Gemini key (Google AI Studio) if you plan to use the AI remediation helper
- Git + VS Code (or editor of choice)

### Optional microk8s environment
If you want to validate Kubernetes manifests in a local cluster, install microk8s (works on Ubuntu/macOS with multipass):

```bash
sudo snap install microk8s --classic
sudo usermod -a -G microk8s "$USER"
microk8s status --wait-ready
microk8s enable dns storage
# To inspect manifests locally (optional)
microk8s kubectl apply -f k8s/
```
This is **not** required for grading; static scans (`scripts/run_checkov.py`, `scripts/run_semgrep.py`) are sufficient.

---

## 1. Get the starter

```bash
git clone <your-private-fork> llm-sec-lab3
cd llm-sec-lab3/starter-labs/llm-sec-lab3-starter/llm-sec-lab3
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # only needed if using Gemini for remediation
```

---

## 2. Baseline scans

```bash
python scripts/run_checkov.py            # writes reports/checkov.json
python scripts/run_semgrep.py            # writes reports/semgrep.json
```

Record key findings in `reports/summary.md` before making changes.

---

## 3. Generate remediation hints (optional)

```bash
python src/gemini_remediate.py reports/checkov.json reports/semgrep.json \
  > reports/remediation_suggestions.json
```

Pick concrete fixes in `terraform/`, `k8s/`, or `docker/`. Cite official docs (links included in README references or microk8s docs).

---

## 4. Apply fixes & re-scan

```bash
python scripts/run_checkov.py --after
python scripts/run_semgrep.py --after
```

Update `reports/summary.md` table: issue → change → status (`fixed`/`ignored`/`false positive`) → reference link. Add a 1-page reflection discussing trends and a policy/CI idea to prevent regressions.

---

## 5. Run automated tests

```bash
python -m unittest discover tests   # or: make w03-day from repo root (added in Makefile)
```

The tests mock Checkov/Semgrep CLIs and ensure the scripts write their JSON output.

---

## 6. Publish your work

```bash
git status -sb
# stage only intentional files (reports summaries, README updates, code changes)
git add reports/checkov*.json reports/semgrep*.json reports/summary.md \
        terraform/ k8s/ docker/
git commit -m "Lab3: remediated S3 bucket and k8s security context"
git push
```

Keep your repo private; never commit real API keys. Attach your reflection + summary when submitting.

Good luck hardening the config stack!
