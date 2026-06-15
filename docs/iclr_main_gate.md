# ICLR Main Gate

Paper: 111 open_robot_data_coverage_gaps

Previous v3 decision: KILL_ARCHIVE

Gate verdict after v4 rebuild: STRONG_REVISE

Evidence digest: local mechanism-coverage benchmark, 5 dataset families, 7 mechanism-gap regimes, 5 splits, 9 methods, 7 paired seeds, 84 episodes per group.

Gate outcomes:
- Success margin over strongest non-oracle baseline: PASS (`0.075`).
- Diagnostic improvement: PASS (`+0.167` mechanism recall).
- Tail/redundancy/cost non-regression: PASS.
- Pairwise seeds: PASS (7/7 wins).
- Ablation margin: PASS (`0.021`).

ICLR main ready: NO. Real public-dataset validation is still required.
