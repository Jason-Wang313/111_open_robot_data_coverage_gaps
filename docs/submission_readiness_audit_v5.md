# Submission Readiness Audit v5

Paper: 111 open_robot_data_coverage_gaps

Version: v5_expanded

Decision: STRONG_REVISE

ICLR main ready: no

## Local Evidence

- Main cells: 102,400.
- Main grouped cells: 10,240.
- Seed metrics: 1,280.
- Aggregate metrics: 128.
- Ablation cells: 8,000.
- Stress cells: 48,000.
- Fixed-risk cells: 51,200.
- Failure cases: 24.
- Hard success margin vs strongest non-oracle: `0.06536`.
- Hard utility margin vs strongest non-oracle: `0.08963`.
- Paired hard utility wins: `10/10`.
- Strict fixed-risk coverage: `0.32000`.
- Strict fixed-risk utility margin: `0.16322`.

## Readiness Decision

The paper survives a much more hostile local audit than v4.1. It does not survive the external evidence requirement for ICLR main because the real public-data and trained-policy artifacts are missing.

Canonical PDF: `C:/Users/wangz/Downloads/111.pdf`

PDF SHA256: `A2204B83096B7F570DD9C429A139E71A4FA8886BA2FF99C7DC5129FFC6C8481A`
