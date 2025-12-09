# Lab 1 Reset & Setup Commands

These commands reproduce a clean Lab 1 environment starting from the monorepo root (`/home/btj/llm-course`). They mirror the steps in `README-student.md` and include a short cleanup stage.

```bash
# --- Cleanup (optional if you are starting fresh) ---
rm -rf /home/btj/llm-course/.venv
rm -rf /home/btj/llm-course/starter-labs/llm-sec-lab1-starter/llm-sec-lab1/.venv
rm -f  /home/btj/llm-course/starter-labs/llm-sec-lab1-starter/llm-sec-lab1/.env
find /home/btj/llm-course/starter-labs/llm-sec-lab1-starter/llm-sec-lab1 -type d -name '__pycache__' -exec rm -rf {} +

# --- Setup (from README-student.md) ---
cd /home/btj/llm-course/starter-labs/llm-sec-lab1-starter/llm-sec-lab1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then edit .env to add your real GEMINI_API_KEY

# --- Notebook support (optional, required for .ipynb execution) ---
pip install ipykernel nbformat nbclient
python -m ipykernel install --user --name llm-sec-lab1 --display-name "Python (llm-sec-lab1)"

# --- Run lab1_live_run notebook ---
# Headless execution (writes an executed copy). PYTHONPATH tells Python where to find src/.
source .venv/bin/activate
PYTHONPATH="$(pwd)" jupyter nbconvert --to notebook --execute notebooks/lab1_live_run.ipynb \
    --output notebooks/lab1_live_run-executed.ipynb
# Interactive editing (opens VS Code/Jupyter UI):
# PYTHONPATH="$(pwd)" jupyter lab notebooks/lab1_live_run.ipynb

# --- Run baseline app (needs real GEMINI_API_KEY) ---
source .venv/bin/activate
python -m src.app

# --- Quick verification (offline) ---
GEMINI_API_KEY=dummy MODEL_ID=gemini-2.5-flash python -m unittest discover -v tests
```

Notes:
- After editing `.env` with a real API key, run the full baseline via `python -m src.app` (or use the notebooks with the `Python (llm-sec-lab1)` kernel).
- To make the notebooks work out of the box, select the Lab 1 virtualenv kernel or add the Lab 1 root to `sys.path` in the first cell.
