# Hostile Reviewer Response

Version: v5_expanded

Decision: STRONG_REVISE

## Likely Attack: This Is Just A Local Simulator

Response: agreed as a readiness blocker. The paper does not claim ICLR-main readiness. The local simulator is now much stronger, with hard baselines, ablations, stress tests, fixed-risk gates, and failure cases, but external public-dataset and trained-policy evidence is still required.

## Likely Attack: Results Are Too Pretty

Response: not in v5. The oracle remains substantially better than v5, strict fixed-risk coverage is only `0.32000`, ablation margins are positive but not huge, and the scope gate fails.

## Likely Attack: Baselines Are Weak

Response: v5 compares against 15 non-proposed comparators including the prior v4 mechanism-coverage audit. The strongest non-oracle baseline is `proposed_mechanism_coverage_audit_v4`, and v5 still improves hard success and utility.

## Likely Attack: Missing Real Robot Evidence

Response: correct. This is why the terminal decision is STRONG_REVISE, not ACCEPT_READY. Real public-dataset annotation, label-quality validation, downstream trained-policy evidence, deployment logs, and rollout videos are required before submission.
