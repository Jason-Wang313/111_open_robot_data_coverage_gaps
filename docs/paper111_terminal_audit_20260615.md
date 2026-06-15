# Paper 111 Terminal Audit

Date: 2026-06-15

Paper: `111_open_robot_data_coverage_gaps`

Terminal decision: STRONG_REVISE

ICLR main ready: no

## What Passed

- Plan-first execution document created before rerun.
- `src/run_experiment.py` compiles.
- Full experiment rerun completed.
- CSV row-count gate passed for primary metrics, dataset/regime seed metrics, split seed metrics, paired stats, ablations, stress sweep, and failure cases.
- Numeric sanity found zero NaN/Inf issues.
- Strongest non-oracle baseline is `failure_prediction_selection`.
- Proposed audit beats the strongest baseline by `0.075 +/- 0.013` paired success and wins `7/7` seeds.
- Mechanism recall improves from `0.486` to `0.652`.
- Coverage false-negative rate falls from `0.092` to `0.045`.
- Tail mechanism failure, redundancy, and selection cost are lower than the strongest baseline.
- Full method remains above the best removed-component ablation by `0.021` success.
- Stress sweep at level `1.0` keeps proposed above embedding diversity, uncertainty sampling, and failure-prediction selection.
- Eight failure cases are documented.
- PDF rebuild passed and produced `C:/Users/wangz/Downloads/111.pdf`.
- PDF SHA256: `BCCC358056B164C0E3AFBE18696F91997381BCB03ED22E44E6B48B105830C55D`.
- No `C:/Users/wangz/Desktop/111.pdf` copy exists.

## What Still Blocks Submission

- No real public robot dataset validation.
- No downstream trained-policy evaluation.
- No label-quality audit.
- No license/provenance normalization study.
- Oracle remains higher than proposed, indicating unresolved mechanism-labeling headroom.

## Honest Outcome

This paper should continue as `STRONG_REVISE`, not be submitted to ICLR main. The next version needs real public-dataset validation and downstream policy evidence before the central claim can be treated as submission-ready evidence.
