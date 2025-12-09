# Gemini Model Comparison — Lab 1 Baseline

| Model ID | Notes | JSON Artifacts |
| --- | --- | --- |
| `gemini-2.5-flash` (default) | Most verbose rationales, consistent CWE tagging. Serves as the course baseline. | `reports/baseline_gemini-2.5-flash.json` |
| `gemini-flash-latest` | Similar coverage with shorter answers; intermittent `thought_signature` warnings but valid JSON thanks to retry and fence stripping. | `reports/baseline_gemini-flash-latest.json` |
| `gemini-2.5-pro` | Conservative: some low-risk prompts return empty findings, but high-risk prompts still map to `LLM01`/`LLM06`. Useful when over-reporting is a concern. | `reports/baseline_gemini-2.5-pro.json` |
| `gemini-2.5-flash-lite` | Mirrors Flash decisions with even shorter rationales; good for tighter budgets. | `reports/baseline_gemini-2.5-flash-lite.json` |

**Guidance**

- Pick Flash when you want richer rationales for grading or demos.
- Flash-Lite keeps schema fidelity with lower latency/cost; ensure that shorter explanations are properly understood
- Pro may under-report on benign prompts—pair it with stricter guardrails or human review.
- `thought_signature` warnings are informational; the JSON responses remain valid after the fence-stripping and retry logic introduced in `src/app.py`.

Use these baselines to explain model trade-offs during lab briefings or to justify the default `MODEL_ID` in `.env.example`.
