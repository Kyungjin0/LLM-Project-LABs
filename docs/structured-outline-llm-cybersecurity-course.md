```{sh}
LLM Cybersecurity Course
├─ Lab 1 – Prompt Hardening (Empathize)
│  ├─ Pain point: LLMs mishandle hostile prompts
│  ├─ Artifacts: guard filters, schema, refusal policy, baseline JSONs
│  ├─ Evidence: Gandalf/RedArena notes, model-comparison report
│  └─ Automation: w01-day, lab1-tests.yml
├─ Lab 2 – Secure Code Review (Define)
│  ├─ Pain point: scanners overwhelm with noisy findings
│  ├─ Loop: promptfoo eval → metrics.csv → FP/FN brief
│  ├─ Deliverables: HTML report, JSON results, metrics, 1-page summary
│  └─ Automation: w02-day, lab2-tests.yml
├─ Lab 3 – Semgrep + Checkov + LLM (Ideate)
│  ├─ Pain point: IaC/app issues need prioritization
│  ├─ Flow: baseline scans → after scans → Gemini triage
│  ├─ Optional: MicroK8s validation
│  └─ Automation: w03-day, lab3-tests.yml
├─ Lab 4 – Guardrails & Red Team (Prototype)
│  ├─ Pain point: attacks keep evolving; guard efficacy must be measured
│  ├─ Dual suite: unguarded.json vs guarded.json
│  ├─ Metrics: refusal rate, unsafe responses, latency
│  └─ Automation: w04-day, lab4-tests.yml
└─ Final Project – Secure RAG or Safe Agent (Test & Deploy)
   ├─ Choice: RAG track (cited answers) or Agent track (allow-listed tools)
   ├─ Shared components: `src/common/guards`, logging, promptfoo gates
   ├─ Deliverables: logs.jsonl, reports, metrics, 3–5 page report
   └─ Automation: w05-day, lab5-tests.yml + project-local CI
```

