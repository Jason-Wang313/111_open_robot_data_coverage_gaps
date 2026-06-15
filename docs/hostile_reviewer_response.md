# Hostile Reviewer Response

Paper: 111 Open Robot Data Coverage Gaps

## Strongest Technical Threats

- This may be only a relabeling of dataset diversity.
- Failure-prediction selection may already identify the important holes.
- The benchmark is local and not an audit of real public datasets.
- Mechanism labels may be expensive or unreliable.

## Response

The v4 rebuild includes failure-prediction selection as the strongest non-oracle baseline. The proposed audit improves combined-stress success by `0.075 +/- 0.013`, improves mechanism recall by `0.167`, and lowers tail failure, redundancy, and selection cost.

## Honest Action

Mark as `STRONG_REVISE`, not ready acceptance. Submission requires validation on real public robot datasets with label-quality checks and downstream trained policy results.
