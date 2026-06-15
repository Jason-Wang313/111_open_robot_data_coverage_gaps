# Final Audit

Paper: 111 open_robot_data_coverage_gaps

Decision: STRONG_REVISE

The v4 rebuild adds a local mechanism-coverage benchmark with paired seeds, strong local data-selection baselines, ablations, stress sweeps, failure cases, LaTeX tables, and figures. The proposed mechanism coverage audit beats the strongest non-oracle baseline, `failure_prediction_selection`, by `0.075 +/- 0.013` paired success under combined stress.

Mechanism diagnostics pass: mechanism recall improves by `0.167`, tail mechanism failure falls by `0.025`, redundancy falls by `0.049`, and selection cost falls by `0.054`.

Remaining blocker: the evidence is local. The paper should not be submitted to ICLR main without validation on real public robot datasets and downstream trained policies.
