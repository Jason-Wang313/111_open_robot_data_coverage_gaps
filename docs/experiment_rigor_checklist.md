# Experiment Rigor Checklist

Version: v5_expanded

Decision: STRONG_REVISE

- Plan frozen before execution: yes.
- CPU-only/RAM-light protocol: yes.
- Strongest non-oracle baseline identified after the run: `proposed_mechanism_coverage_audit_v4`.
- Strong baselines included: trajectory count, task count, embodiment count, random balance, embedding diversity, uncertainty, failure prediction, value of information, dataset-card compliance, safety mining, label quality, domain mix, causal feature, v4, v5, and oracle.
- Main cells: 102,400.
- Ablation cells: 8,000.
- Stress cells: 48,000.
- Fixed-risk cells: 51,200.
- Paired hard seeds: 10.
- Failure cases retained: 24.
- Non-pretty fixed-risk result: yes, strict fixed-risk coverage is `0.32000`, not perfect.
- Scope gate: failed because external public-dataset and trained-policy evidence is absent.

Final PDF SHA256: `A2204B83096B7F570DD9C429A139E71A4FA8886BA2FF99C7DC5129FFC6C8481A`
