# Submission Readiness Audit v4.1

Paper: 111 open_robot_data_coverage_gaps

Date: 2026-06-15

Decision: STRONG_REVISE

ICLR main ready: no

## Rerun

- Command: `python -m py_compile src/run_experiment.py`
- Command: `python src/run_experiment.py`
- Log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/111_open_robot_data_coverage_gaps_continuation_rerun_20260615.log`
- Numeric sanity: zero NaN/Inf issues across CSV outputs.
- PDF: `C:/Users/wangz/Downloads/111.pdf`
- PDF SHA256: `BCCC358056B164C0E3AFBE18696F91997381BCB03ED22E44E6B48B105830C55D`
- PDF size: 401383 bytes.
- Desktop PDF copy: absent.

## Coverage

- `metrics.csv`: 45 rows.
- `per_dataset_regime_metrics.csv`: 1575 rows.
- `seed_dataset_regime_metrics.csv`: 11025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_dataset_regime_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 30 rows.
- `stress_sweep_seed_metrics.csv`: 7350 rows.
- `failure_cases.csv`: 8 rows.

## Gate Evidence

- Strongest non-oracle baseline: `failure_prediction_selection`.
- Combined-stress success: `0.578 +/- 0.012` proposed vs `0.503 +/- 0.005` strongest baseline.
- Mechanism recall: `0.652` proposed vs `0.486` strongest baseline.
- Coverage false-negative rate: `0.045` proposed vs `0.092` strongest baseline.
- Tail mechanism failure: `0.078` proposed vs `0.103` strongest baseline.
- Redundancy rate: `0.128` proposed vs `0.177` strongest baseline.
- Selection cost: `0.217` proposed vs `0.272` strongest baseline.
- Paired success gain: `0.075 +/- 0.013`, with `7/7` seed wins.
- Best removed-component ablation: `minus_redundancy_penalty`; full method remains ahead by `0.021` success.
- Max stress level `1.0`: proposed success `0.5622 +/- 0.0049`; failure-prediction selection `0.4832 +/- 0.0082`; uncertainty sampling `0.4670 +/- 0.0074`; embedding diversity `0.4468 +/- 0.0063`; oracle `0.6580 +/- 0.0078`.

## Terminal Assessment

The local evidence supports continuing the paper as a strong-revise candidate: the audit beats the strongest non-oracle baseline, improves mechanism recall, lowers false negatives, lowers tail failure, lowers redundancy and cost, wins paired seeds, survives ablations, and remains above core baselines through the stress sweep.

The paper is still not ICLR-main-ready. The blocker is external validity: no real public robot dataset annotation/validation, no downstream trained-policy evidence, and no label-quality audit.
