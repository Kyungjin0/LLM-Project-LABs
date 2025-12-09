# Lab 1 Starter Validation Notes

## CLI Baseline — Gemini 2.5 Flash
- Executed `.venv/bin/python -m src.app` with the production Gemini key and default `MODEL_ID=gemini-2.5-flash`.
- Hardened `src/app.py` to:
  - request `response_mime_type="application/json"` and strip Markdown fences;
  - normalise `cwe` fields (lists → comma-delimited strings);
  - retry transient `ServerError` (503) up to three times before logging the failure;
  - catch `google.genai.errors.APIError` and unexpected exceptions so runs degrade gracefully.
- Latest run stored in `reports/baseline.json` and mirrored at `reports/baseline_gemini-2.5-flash.json`.
  - Output conforms to the JSON schema; no findings triggered validation failures.

## Alternate Model — Gemini Flash Latest
- Ran `MODEL_ID=gemini-flash-latest .venv/bin/python -m src.app` to compare risk coverage.
- Captured results at `reports/baseline_gemini-flash-latest.json`.
- Observed slightly shorter responses and fewer CWE references; no JSON violations.
- Transient 503 overload responses were resolved via the built-in retry loop; final report contains all prompts.

## Automated Tests
- Added `tests/test_app.py` covering successful parsing, malformed JSON handling, retry logic, and eventual success after transient `ServerError`.
- Run with `.venv/bin/python -m unittest discover tests` (stdlib `unittest`, no extra deps).

## CI Integration
- Added `.github/workflows/lab1-tests.yml` to run the unittest suite on every push/PR touching the Lab 1 starter.
- Workflow installs the starter’s dependencies and sets dummy `GEMINI_API_KEY`/`MODEL_ID` values so tests stay offline-friendly.

## Extended Model Coverage
- `MODEL_ID=gemini-2.5-pro` run archived at `reports/baseline_gemini-2.5-pro.json`; responses skew conservative (several prompts yielded empty findings while sensitive prompts still mapped to LLM01/LLM06).
- `MODEL_ID=gemini-2.5-flash-lite` run archived at `reports/baseline_gemini-2.5-flash-lite.json`; outputs mirror default Flash with briefer rationales and consistent CWE tagging.

## Notebook Workflows
- `notebooks/lab1_stub_validation.ipynb` preserves the stubbed path for offline exercises.
- Added `notebooks/lab1_live_run.ipynb` which imports `src.app`, runs `app.main()` against the live API, and previews the first two findings.
- Verified both notebooks with `nbclient`; the live run regenerates `reports/baseline.json` using the active `.env`.

## Environment + Ops
- Virtualenv `.venv` contains runtime deps plus notebook stack (`nbformat`, `nbclient`, `ipykernel`).
- `.env` lists the active Gemini key and optional model variants; keys remain git-ignored.
- Reports remain ignored (`reports/*.json`) to avoid committing API outputs.

## Follow-ups
- Severity values are now normalized to `low|medium|high|critical` in post-processing; adjust `SEVERITY_CANONICAL` in `src/app.py` if you need a different vocabulary.
- Monitor Gemini API rate limits and update retry/backoff strategy if quotas tighten.
- Extend findings post-processing to add confidence scoring or enforce severity vocab if required by downstream tooling.
