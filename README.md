# 111 Open Robot Data Coverage Gaps

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for ICLR main-conference development.

This continuation audit reruns and hardens the v4 local mechanism-coverage benchmark for robot data selection. The paper is still not ICLR-main-ready because the audit has not been validated on real public robot datasets, but the local evidence supports continued development.

## Evidence Snapshot

- Benchmark: 5 dataset families x 7 mechanism-gap regimes x 5 deployment splits x 9 methods.
- Seeds: 7 paired seeds, 84 held-out evaluation episodes per dataset/regime/split/method group.
- Strongest non-oracle baseline: `failure_prediction_selection`.
- Proposed: `proposed_mechanism_coverage_audit`.
- Combined-stress success: `0.578 +/- 0.012` proposed vs `0.503 +/- 0.005` strongest baseline.
- Mechanism recall: `0.652` proposed vs `0.486` strongest baseline.
- Tail mechanism failure: `0.078` proposed vs `0.103` strongest baseline.
- Pairwise wins: 7/7 seeds over the strongest baseline.
- Best removed-component ablation: `minus_redundancy_penalty`; full method remains ahead by `0.021` success.
- Expanded stress-sweep seed/dataset/regime rows: 7350.
- Failure cases: 8 documented limitations.

## Continuation Audit

- Log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/111_open_robot_data_coverage_gaps_continuation_rerun_20260615.log`
- CSV row-count gate: passed for metrics, dataset/regime seeds, paired stats, ablations, stress sweep, and failure cases.
- Numeric sanity gate: passed with zero NaN/Inf issues.
- Artifact rule: final numbered PDF belongs in `C:/Users/wangz/Downloads/111.pdf` only.
- PDF SHA256: `BCCC358056B164C0E3AFBE18696F91997381BCB03ED22E44E6B48B105830C55D`.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/111.pdf`
