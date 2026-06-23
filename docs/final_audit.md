# Final Audit

Paper: 111 open_robot_data_coverage_gaps

Version: v5_expanded

Decision: STRONG_REVISE

ICLR main ready: no

The v5 audit expands the local benchmark to 8 catalog anchors, 10 mechanism-gap regimes, 8 splits, 16 methods, and 10 paired seeds. It persists 102,400 main cells, 10,240 grouped cells, 1,280 seed metrics, 128 aggregate metrics, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, 60 fixed-risk pairwise comparisons, and 24 failure cases.

All frozen local gates pass. The proposed `mechanism_coverage_gap_audit_v5` beats the strongest non-oracle baseline, `proposed_mechanism_coverage_audit_v4`, on hard success (`0.65063` vs `0.58526`) and hard utility (`0.72744` vs `0.63780`). It improves mechanism recall by `0.08828`, reduces false coverage by `-0.02588`, reduces tail failure by `-0.01640`, reduces unsafe deployment failure by `-0.00682`, wins `10/10` paired hard utility seeds, and keeps strict fixed-risk coverage non-perfect at `0.32000`.

The scope gate fails. The paper should not be submitted to ICLR main without real public-dataset annotation, label-quality validation, schema/provenance normalization on released datasets, trained downstream policy evidence, deployment logs, and rollout videos.

Canonical PDF: `C:/Users/wangz/Downloads/111.pdf`

PDF SHA256: `A2204B83096B7F570DD9C429A139E71A4FA8886BA2FF99C7DC5129FFC6C8481A`
