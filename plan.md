# Paper 111 Expanded-Standard v5 Plan

Frozen before v5 experiment/manuscript edits: 2026-06-23 12:13:00 +08:00

## Goal

Rebuild Paper 111, `open_robot_data_coverage_gaps`, into a 25+ page ICLR-main-target manuscript with real theory, a much broader CPU-only evidence protocol, honest terminal gates, bright boxed clickable citations, a Downloads-only numbered PDF, and a public GitHub update. Do not mark the paper ICLR-main-ready unless external evidence exists.

## Claim Under Test

Open robot datasets can appear large by trajectories, tasks, embodiments, or scenes while still under-covering causal robot mechanisms: contact transitions, force/tactile cues, recovery after failure, deformable interaction, irreversible side effects, long-horizon dependencies, embodiment schema transfer, provenance/license quality, and annotation uncertainty. A mechanism-coverage audit should predict and reduce held-out downstream failures better than coarse count, embedding-diversity, uncertainty, failure-prediction, and metadata-compliance selectors.

## v5 Evidence Protocol

- Run a deterministic CPU-only/RAM-light local audit with fixed seeds and no GPU dependency.
- Expand from v4.1 to 8 catalog-style public robot dataset families, 10 mechanism-gap regimes, 8 deployment splits, 16 methods, and 10 paired seeds.
- Persist main cell-level results, dataset summaries, main group summaries, seed metrics, hard-aggregate metrics, paired tests, ablations, stress sweeps, fixed-risk calibration, and failure cases.
- Treat public dataset names and citations as catalog anchors, not proof of downloaded training or real downstream policy evaluation.

## Methods

- Count and diversity selectors: trajectory-count, task-count, embodiment-count, random-balanced, embedding-diversity, uncertainty sampling.
- Strong local baselines: failure-prediction selection, value-of-information active selection, dataset-card compliance selection, safety-event mining, label-quality-first selection, domain-mix robust selection, causal-feature coverage, and v4 proposed mechanism coverage.
- Proposed v5: `mechanism_coverage_gap_audit_v5`.
- Oracle: `oracle_mechanism_labeled_selector`, reported only as an upper bound.

## Metrics

- Primary: held-out downstream success and utility.
- Coverage diagnostics: mechanism recall, coverage false-negative rate, rare-mechanism recall, schema-mismatch rate, provenance-risk rate, label-noise risk, and calibration ECE.
- Safety/efficiency diagnostics: tail mechanism failure, unsafe deployment failure, redundancy, annotation burden, selection cost, and regret to oracle.
- Stress/fixed-risk diagnostics: maximum-stress utility, fixed-risk coverage over strict false-negative/tail-failure budgets, and paired hard-split wins.

## Frozen Local Gates

Mark `STRONG_REVISE` only if all local gates pass:

- v5 beats the strongest non-oracle baseline on hard-aggregate success by at least `0.030`.
- v5 beats the strongest non-oracle baseline on hard-aggregate utility by at least `0.050`.
- v5 improves mechanism recall by at least `0.050` or lowers coverage false negatives by at least `0.030`.
- v5 does not increase tail mechanism failure, unsafe deployment failure, redundancy, annotation burden, or selection cost versus the strongest non-oracle baseline.
- v5 wins at least `8/10` paired hard-split seeds against the strongest non-oracle baseline on utility.
- The best removed-component ablation remains below the full method by at least `0.010` success or `0.040` utility.
- The maximum-stress endpoint utility margin over the strongest non-oracle baseline is at least `0.050`.
- Strict fixed-risk coverage is at least `0.300` and not trivially perfect; the strict fixed-risk utility margin must be positive.

Mark `KILL_ARCHIVE` if any local gate fails.

## Scope Gate

The ICLR-main readiness gate remains `no` unless the audit is validated on real public robot datasets with label-quality checks, schema/provenance normalization, and downstream trained policy evaluations. The v5 local/catalog audit can justify only `STRONG_REVISE`, not submission.

## Manuscript Requirements

- Produce a 25+ page ICLR-style PDF with non-padding theory, benchmark design, frozen gates, full results, ablations, stress tests, fixed-risk calibration, failure cases, related work, limitations, and reproducibility checklist.
- Add theory for mechanism-coverage tensors, coarse-count non-identifiability, submodular coverage utility, and false-coverage risk bounds.
- Use bright boxed clickable citation/reference links.
- Keep claims evidence-bound and explicitly report all failed scope conditions.

## Artifact Requirements

- Final numbered PDF: `C:/Users/wangz/Downloads/111.pdf` only.
- No `111.pdf` on the visible Desktop, factory root, or child repo root.
- Update Paper 111 README, child status, audit docs, validation docs, and root ledgers.
- Commit and push to `https://github.com/Jason-Wang313/111_open_robot_data_coverage_gaps` with noreply Git attribution after validation.
