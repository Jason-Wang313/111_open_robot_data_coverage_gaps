# Submission Version Log

## v3

Decision: KILL_ARCHIVE

Reason: synthetic/template evidence and no real or high-fidelity validation.

## v4

Decision: STRONG_REVISE

Changes:
- Added mechanism-coverage benchmark.
- Added count-based, balanced, embedding-diversity, uncertainty, and failure-prediction baselines.
- Added paired-seed success tests.
- Added tail failure, redundancy, and cost gates.
- Added ablations, stress sweep, failure cases, figures, and generated tables.
- Rewrote manuscript and docs around a narrow mechanism-coverage data audit claim.

Remaining blocker: no real public-dataset validation.

## v4.1

Decision: STRONG_REVISE

Changes:
- Added a paper-specific ICLR submission-readiness execution plan before rerunning.
- Reran the full local benchmark under fixed single-threaded numeric settings.
- Expanded stress-sweep evidence from seed aggregates to 7350 dataset/regime/seed rows while preserving seed-level aggregate confidence intervals.
- Expanded documented failure cases from 4 to 8.
- Rechecked CSV row counts, numeric sanity, strongest baseline, paired seed wins, ablations, stress sweep, and artifact-location requirements.

Remaining blocker: no real public-dataset validation, no downstream trained-policy evidence, and no label-quality audit.
