# ICLR Main Gate

Version: v5_expanded

Decision: STRONG_REVISE

ICLR main ready: no

## Passed Local Gates

- Hard success margin: pass (`+0.06536` vs strongest non-oracle).
- Hard utility margin: pass (`+0.08963` vs strongest non-oracle).
- Diagnostic gate: pass (`+0.08828` mechanism recall and lower false coverage).
- Non-regression gate: pass on tail failure, unsafe deployment failure, redundancy, selection cost, and annotation burden.
- Paired hard utility gate: pass (`10/10` wins).
- Ablation gate: pass (`+0.02812` success vs best removed component).
- Stress endpoint gate: pass (`+0.09256` utility margin).
- Strict fixed-risk gate: pass with non-perfect coverage (`0.32000`) and positive utility margin (`0.16322`).

## Failed Scope Gate

The manuscript is not ICLR-main-ready because it has no real public-dataset annotation campaign, no released-data label-quality validation, no schema/provenance normalization audit on public data, no downstream trained-policy experiment, and no deployment logs or rollout videos.

This failed scope gate is decisive rather than cosmetic.
