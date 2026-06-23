# Claims

Current version: v5_expanded.

Terminal decision: STRONG_REVISE.

The defensible claim is narrow: in a deterministic local/catalog audit, mechanism-aware coverage selection is stronger than scale-only, diversity-only, uncertainty-only, failure-prediction, dataset-card, domain-mix, causal-feature, and v4 mechanism-coverage selectors under hard mechanism shifts.

The evidence supports this local claim with 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases. V5 beats the strongest non-oracle baseline, `proposed_mechanism_coverage_audit_v4`, by `0.06536` hard success and `0.08963` hard utility.

The paper does not claim ICLR-main readiness. It does not yet show real public dataset labels, real schema/provenance normalization, trained policy transfer, or deployment logs. Those missing artifacts define the failed scope gate.
