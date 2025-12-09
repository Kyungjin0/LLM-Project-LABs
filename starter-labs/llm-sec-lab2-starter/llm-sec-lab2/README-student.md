Lab 2 Student Runbook — Secure Code Review Prompts + Eval
=======================================================
> Author : Badr TAJINI - LLM Cybersecurity - ECE 2025/2026

Goal: compare a naïve code-review prompt vs a security-hardened prompt on 30 seeded snippets using **promptfoo** + **Gemini**, then score precision/recall/F1.

---

## 0. Prerequisites

- Node.js **20+** (promptfoo ≥0.119 requires Node 20 and rebuilds `better-sqlite3`)
- Python 3.9+
- A Gemini API key from Google AI Studio
- Git CLI or VS Code Source Control

Optional: GitHub CLI (`gh`) if you prefer pushing from the command line.

---

## 1. Getting the starter

### Option A — invited to the private GitHub repo

```bash
git clone https://github.com/btajini/llm-sec-lab2-starter.git
cd llm-sec-lab2-starter
```

### Option B — Professor shares a ZIP archive

```bash
unzip llm-sec-lab2-starter.zip -d ~/projects
cd ~/projects/llm-sec-lab2-starter
# expected layout: .github/  Makefile  starter-labs/

git init
git branch -m main
git add .github starter-labs/llm-sec-lab2-starter .gitignore Makefile
git commit -m "Add lab 2 starter"
```

Publish to GitHub:

- **GitHub CLI (recommended)**
  ```bash
  gh auth login
  gh repo create <your-username>/llm-sec-lab2-starter --private --source=. --remote=origin --push
  ```
- **Manual git**
  ```bash
  git remote add origin https://github.com/<your-username>/llm-sec-lab2-starter.git
  git push -u origin main
  ```
- **VS Code**: open the folder → Source Control (Ctrl+Shift+G / Cmd+Shift+G) → *Initialize Repository* → stage `.github/`, `.gitignore`, `Makefile`, and `starter-labs/llm-sec-lab2-starter/` → commit → *Publish Branch* (mark it private).

`.gitignore` already excludes notes, so only the starter is tracked.

---

## 2. Configure environment

```bash
cd starter-labs/llm-sec-lab2-starter/llm-sec-lab2
cp .env.example .env            # add GEMINI_API_KEY and (optional) MODEL_ID

# Python deps
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Node 20 + promptfoo (skip if already installed)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # load nvm
nvm install 20
nvm use 20
npm install -g promptfoo@latest
```

If you prefer not to install globally, run `npx promptfoo@latest eval ...` **after** `nvm use 20`. Older Node (v18) will fail with EBADENGINE/better-sqlite3 errors.

`.env` defaults to `MODEL_ID=google:gemini-2.5-flash`; adjust if you evaluate other tiers.

---

## 3. Run the evaluation

```bash
nvm use 20                                # ensure Node 20 shell
GEMINI_API_KEY=... promptfoo eval \
  -c promptfooconfig.yaml \
  -o reports/lab2_report.html \
  -o reports/lab2_results.json
```

This compares `prompts/baseline_prompt.txt` vs `prompts/secure_review_prompt.txt` across `_generated/tests.yaml`.

`reports/lab2_report.html` is the human-readable dashboard; `reports/lab2_results.json` feeds the metrics script. If the API key is missing, promptfoo will finish with zero tests—rerun with a valid key before collecting deliverables.

---

## 4. Score metrics

```bash
python tools/metrics.py reports/lab2_results.json reports/metrics.csv
```

`reports/metrics.csv` lists TP/FP/TN/FN plus precision/recall/F1 for each prompt index (0 = naïve, 1 = secure prompt).

---

## 5. Inspect outputs & notes

- `reports/lab2_report.html`: promptfoo dashboard with side-by-side answers and assertions.
- `reports/lab2_results.json`: raw evaluation results (keep for grading).
- `reports/metrics.csv`: summary stats for your brief.

Track false positives/negatives, CWE hints, and schema errors—they feed your 1-page deliverable.

---

## 6. Run automated checks

The starter ships with regression tests for `tools/metrics.py`.

```bash
python -m unittest discover tests
# or, from repo root
make w02-day
```

`make w02-day` mirrors the GitHub Actions workflow (`.github/workflows/lab2-tests.yml`).

---

## 7. Publish updates

```bash
git status -sb          # look for lines starting with 'M '
git add <path>          # stage modified files you want synced
git commit -m "Describe your change"
git push                # upload to your private repo
```

Keep the repo private to protect your API keys and lab answers.

---

## Deliverables checklist

- ✅ `reports/lab2_report.html`
- ✅ `reports/lab2_results.json`
- ✅ `reports/metrics.csv`
- ✅ 1-page brief summarizing FP/FN patterns and prompt improvements

Happy triaging!
