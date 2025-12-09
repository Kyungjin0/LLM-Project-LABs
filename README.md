LLM Cyberecurity Course
=======================================================
> Author : Badr TAJINI - LLM Cybersecurity - ECE 2025/2026


## Quick start
> **Note: updates may occur. Always refer to the latest README in the repo.**
- **Lab runbooks:**
  - Lab 1: `starter-labs/llm-sec-lab1-starter/llm-sec-lab1/README-student.md`
  - Lab 2: `starter-labs/llm-sec-lab2-starter/llm-sec-lab2/README-student.md`
  - Lab 3: `starter-labs/llm-sec-lab3-starter/llm-sec-lab3/README-student.md`
  - Lab 4: `starter-labs/llm-sec-lab4-starter/llm-sec-lab4/README-student.md`
  - Final project: `starter-project/llm-sec-final-project-starter/README-student.md`
- **Automation:**
  - `make w01-day` (Lab 1 tests + model comparison reminder)
  - `make w02-day` (Lab 2 metrics regression tests)
  - `make w03-day` (Lab 3 Checkov/Semgrep regression tests + microk8s note)
  - `make w04-day` (Lab 4 guardrails suite regression tests)
  - `make w05-day` (Final project unit tests + promptfoo/metrics reminder)
- **CI Workflows:**
  - `.github/workflows/lab1-tests.yml`
  - `.github/workflows/lab2-tests.yml`
  - `.github/workflows/lab3-tests.yml`
  - `.github/workflows/lab4-tests.yml`
  - `.github/workflows/lab5-tests.yml` (final project unit tests)
- **Evaluation outputs:** each starter writes to its `reports/` directory (e.g., lab1 baselines, lab2 metrics, lab3 promptfoo, lab4 guardrail deltas, final-project promptfoo + metrics).

---

# Labs & project starters

* **Lab 1 starter** — Prompting + secure patterns: `llm-sec-lab1-starter`
* **Lab 2 starter** — SAST + IaC triage loop: `llm-sec-lab2-starter`
* **Lab 3 starter** — Minimal RAG + evals: `llm-sec-lab3-starter`
* **Lab 4 starter** — Guardrails + red-team suite: `llm-sec-lab4-starter`
* **Final project starter** — Secure RAG **and** Safe Agent with shared guards/CI: `llm-sec-final-project-starter`

> **Instructor note:** archival ZIP starters (`legacy/*`) are distributed separately; request a fresh copy if you need the original (from scratch) starter set.

# 0) Environments at zero cost

* **Gemini API via AI Studio.** Create a key. Quickstart shows Python SDK. Student AI Pro trials exist by region. Verify eligibility. ([Google AI for Developers][1])
* **Google Colab.** Free hosted notebooks. No setup. GPUs and TPUs with limits. ([Google Research][2])
* **Gandalf and RedArena.** Browser-based jailbreak practice. Use for Lab 1 warm-ups. ([Gandalf][3])
* **GitHub Education.** Student Developer Pack. Codespaces hours and Actions minutes for verified students. Classroom support for teachers. ([GitHub][4])
* **Hugging Face Spaces.** Free CPU Spaces to host demos. Check terms and storage limits. ([Hugging Face][5])

# 1) Course spine references

* **OWASP Top-10 for LLM Applications** and **OWASP GenAI**. Use for risk names and mitigations. ([OWASP][6])
* **MITRE ATLAS.** Use for tactics and case studies in your threat models. ([MITRE ATLAS][7])

# 2) Labs 

## Lab 1 — Prompting + secure patterns (Modules 1–2)

**Goal.** Move from naive prompts to secure, structured outputs.
**Warm-up.** Play Gandalf or RedArena 15–20 min. Discuss why LLM01 (prompt injection) works. ([Gandalf][3])
**Hands-on.**

* Run the starter app. Enforce JSON schema. Add role, constraints, examples.
* Add output contract: `{"findings":[{cwe, file, line, evidence}], "confidence", "next_steps"}`.
* Add minimal refusal policy for dangerous requests.
  **Deliverables.** One before/after transcript. One short reflection.
  **Rubric (10 pts).** Contract adherence 3, jailbreak awareness 2, prompt clarity 2, refusal quality 2, reflection 1.

## Lab 2 — SAST + IaC loop (Modules 3–4)

**Goal.** Triage Semgrep and Checkov alerts with an LLM. Don’t replace static analysis.
**Hands-on.**

* Run Semgrep on a small repo and export JSON. Write a prompt that asks for CWE mapping and evidence lines. ([Semgrep][8])
* Run Checkov on sample Terraform or plan JSON. Export SARIF/JSON. Map to risk. ([Checkov][9])
* Aggregate to a markdown report. Track false positives and “unknowns”.
  **Deliverables.** `semgrep.json`, `checkov.json`, triage report.
  **Rubric (10 pts).** Data wiring 3, CWE mapping 2, false-positive handling 2, IaC insights 2, report quality 1.

## Lab 3 — Minimal RAG + evals (Module 6 + start of 7)

**Goal.** Local TF-IDF retrieval. JSON answers with citations. Eval with promptfoo.
**Hands-on.**

* Run the RAG starter. Ask 5 factual questions covered by the corpus.
* Add two adversarial questions that try to elicit secrets; expect `safety="unsafe"`.
* Run promptfoo. Add an `is-json` assertion and one JS check for citation presence. ([Promptfoo][10])
  **Deliverables.** `reports/report.html`, `reports/results.json`, `metrics.csv`.
  **Rubric (10 pts).** JSON validity 3, citation rate 3, safety handling 2, test coverage 2.

## Lab 4 — Guardrails + automated attacks (Module 8)

**Goal.** Measure block-rate delta with input/output guards.
**Hands-on.**

* Run `--mode unguarded` vs `--mode guarded`.
* Tune `policy.yaml` deny-regex for your most common failures.
* Discuss LLM02 (insecure output handling) and how output guards prevent sink hazards.
* Optional: contrast with NeMo Guardrails or Guardrails-AI validators. ([NVIDIA Docs][11])
  **Deliverables.** `reports/unguarded.json`, `reports/guarded.json`, `metrics.csv`, 1-page write-up.
  **Rubric (10 pts).** Block-rate improvement 4, unsafe-pass reduction 3, policy clarity 2, write-up 1.

# 3) Final project 

Pick **one**:

* **Secure RAG.** Local retrieval. JSON answers with citations. Safety field set and justified.
* **Safe Agent.** Allow-listed tools only (`search_corpus`, `calc`). ≤3 steps. Return strict JSON with step transcript.

**Required** in both tracks: replay logging, guards, promptfoo evals, CI gates.

**Professor gates in CI.** JSON ≥ 0.95. Safety-field ≥ 0.85.
Plus RAG: citation-present ≥ 0.80. Gates enforced in workflow.

**Stretch.** Swap simple guards with **NeMo Guardrails** Colang flows or run a **PyRIT** campaign and compare. ([NVIDIA Docs][12])

**References for project write-ups.**

* OWASP LLM Top-10 and GenAI project pages. ([OWASP][13])
* MITRE ATLAS fact sheet and site. ([MITRE ATLAS][14])
* PyRIT blog and repo for automated red teaming. ([Microsoft][15])

# 4) One-page student runbooks

## Lab 1 runbook

1. Install deps. Create `.env` with Gemini key.
2. Try one naive prompt. Save output.
3. Add schema. Add role and constraints. Add two examples.
4. Rerun. Compare diffs.
5. Play two Gandalf levels. Note which payload types worked and why. ([Gandalf][3])

## Lab 2 runbook

1. `semgrep scan --json > semgrep.json` on the provided repo. Start from the rule packs page or quickstart. ([Semgrep][8])
2. `checkov -d ./iac -o json > checkov.json` or scan Terraform plan JSON. ([Checkov][9])
3. Feed both to your triage prompt. Ask for CWE, file:line, evidence quote, and recommendation.
4. Mark each as true/false/unknown after manual check.

## Lab 3 runbook

1. Run RAG app with 5 knowledge questions.
2. Add 2 adversarial questions. Expect `safety="unsafe"`.
3. `promptfoo eval -c promptfooconfig.yaml …` and export metrics. ([Promptfoo][10])

## Lab 4 runbook

1. `run_suite.py --mode unguarded` then `--mode guarded`.
2. Inspect blocked reasons vs OWASP LLM01/LLM02.
3. Tune `policy.yaml`. Re-run. Report deltas.

## Final project runbook

1. Pick track. Fill `data/corpus/` if RAG.
2. Keep JSON contract and guards intact.
3. Add 10 eval tests: 6 knowledge, 4 safety.
4. Turn on CI. Confirm gates pass on PR.

# 5) Grading rubrics

* **Labs 1–4**: 10 pts each. Total 40 pts.
* **Project**: 60 pts.

  * Design and threat model 15
  * Implementation quality and guards 15
  * Evals and CI gates 15
  * Report quality with OWASP/ATLAS mapping 15

# 6) Professor checklist

* Verify all students can obtain a **Gemini** API key via AI Studio. Note regional limits. ([Google AI for Developers][1])
* Post links to **Gandalf** and **RedArena** for warm-ups. ([Gandalf][3])
* Pre-seed repos for Semgrep/Checkov. Link official docs. ([Semgrep][8])
* Ensure **promptfoo** is installed on at least one machine per team and link assertion docs. ([Promptfoo][10])
* Optional advanced: demo **NeMo Guardrails** and show Colang flow snippets. ([NVIDIA Docs][11])
* Optional advanced: show **PyRIT** run and how to map findings to ATLAS. ([Azure][16])

# 7) Safety, legality, and scope

* No real secrets, keys, or production URLs in prompts.
* Treat model output as **untrusted**. Validate and sanitize. This is LLM02. ([OWASP][13])
* Do not run exploit code or malware. Use simulated targets and synthetic data.

# 8) Troubleshooting quick answers

* **JSON keeps breaking.** Reduce temperature. Remind model to return only JSON. Add a final “return strictly JSON” line. See JSON eval docs. ([Promptfoo][17])
* **Eval passes locally, fails in CI.** Check environment variables and provider rate limits. Ensure the same model ID.
* **Semgrep/Checkov output huge.** Filter by severity. Export JSON and sample only a subset for triage. ([Semgrep][8])
* **Students lack laptops with compilers.** Use Colab notebooks or Codespaces. ([Google Research][2])


[1]: https://ai.google.dev/gemini-api/docs/quickstart "Gemini API quickstart - Google AI for Developers"
[2]: https://research.google.com/colaboratory/faq.html "Google Colab"
[3]: https://gandalf.lakera.ai/ "Gandalf | Lakera – Test your AI hacking skills"
[4]: https://github.com/education/students "Students - GitHub Education"
[5]: https://huggingface.co/docs/hub/en/spaces "Spaces"
[6]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for Large Language Model Applications"
[7]: https://atlas.mitre.org/ "MITRE ATLAS™"
[8]: https://semgrep.dev/docs/getting-started/quickstart "Quickstart"
[9]: https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html "CLI Command Reference"
[10]: https://www.promptfoo.dev/docs/configuration/expected-outputs/ "Assertions and Metrics - LLM Output Validation"
[11]: https://docs.nvidia.com/nemo/guardrails/latest/index.html "About NeMo Guardrails"
[12]: https://docs.nvidia.com/nemo/guardrails/latest/colang-2/overview.html "Overview — NVIDIA NeMo Guardrails"
[13]: https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf "OWASP Top 10 for LLM Applications 2025"
[14]: https://atlas.mitre.org/pdf-files/MITRE_ATLAS_Fact_Sheet.pdf "A COLLABORATION ACROSS INDUSTRY, ACADEMIA, ..."
[15]: https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative-ai-systems/ "Announcing Microsoft's open automation framework to red ..."
[16]: https://azure.github.io/PyRIT/ "PyRIT - Azure documentation"
[17]: https://www.promptfoo.dev/docs/guides/evaluate-json/ "LLM evaluation techniques for JSON outputs"



## Appendix: What the starters include (and what they don’t)

Each lab folder (e.g., `starter-labs/llm-sec-lab1-starter`, `…-lab2-starter`) ships as scaffolding only:

- **Prompts & filters need tuning.** You must harden schemas, add refusals, and tighten input filters to meet the rubric.
- **Evidence collection is required.** Gandalf/RedArena transcripts, FP/FN tables, and write-ups are empty placeholders.
- **Evaluations are blank slates.** Promptfoo configs run, but no `reports/` outputs are provided—learners generate and interpret their own results.
- **Code extensions remain TODOs.** Guards, new assertions, better prompts/metrics are part of the assignment work.
