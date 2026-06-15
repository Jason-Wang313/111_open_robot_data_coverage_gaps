# Paper 111 Rebuild Plan: Open Robot Data Coverage Gaps

Started: 2026-06-15 01:56:00 +0100

## Goal

Rebuild Paper 111 from a v3 archive into an evidence-backed ICLR-main-target submission candidate, or keep it archived if evidence fails. The paper will remain explicitly not submission-ready unless its audit is validated against real public robot datasets and downstream trained policies.

## Core Claim To Test

Open robot datasets can look large by task count, embodiment count, or trajectory count while still missing mechanism coverage: contact transitions, failure recoveries, force/tactile cues, deformable interactions, irreversible side effects, long-horizon repairs, and safety-relevant edge cases. Mechanism-level coverage should predict downstream policy failures better than coarse dataset-size metrics.

## Proposed Method

`proposed_mechanism_coverage_audit`

The method combines:
- Mechanism taxonomy over contact, force, tactile, deformable, recovery, irreversibility, and long-horizon dependency.
- Coverage tensor over dataset family, embodiment, task, object class, sensor modality, and mechanism.
- Gap risk estimator that predicts held-out mechanism failure from coverage holes.
- Redundancy-aware data selection that prioritizes missing mechanisms rather than more trajectories from already-covered regimes.
- Audit cards that separate dataset scale from mechanism diversity.

## Benchmark Design

Run a local mechanism-coverage benchmark with:
- Five dataset families: single-arm tabletop, mobile manipulation, bimanual manipulation, tactile/contact-rich manipulation, and deformable-object manipulation.
- Seven mechanism-gap regimes: contact-transition gap, force/tactile gap, recovery gap, deformable gap, irreversible-side-effect gap, long-horizon-dependency gap, and combined coverage gap.
- Five deployment splits: nominal, seen-task shift, unseen-object shift, unseen-mechanism shift, and combined-stress.
- Nine methods: trajectory-count selection, task-count selection, embodiment-count selection, random balanced selection, embedding-diversity selection, uncertainty sampling, failure-prediction selection, proposed mechanism-coverage audit, and oracle mechanism coverage.
- Seven paired seeds with 84 held-out evaluation episodes per dataset/regime/split/method.

## Primary Metrics

- Downstream held-out success.
- Mechanism recall.
- Coverage false-negative rate.
- Tail mechanism failure rate.
- Redundancy rate.
- Annotation/selection cost.
- Regret to oracle mechanism coverage.

## Decision Gates

Mark `STRONG_REVISE` only if all are true:
- Success margin over the strongest non-oracle baseline is at least 0.030 on combined stress.
- Mechanism recall improves by at least 0.050 or coverage false-negative rate falls by at least 0.050.
- Tail mechanism failure, redundancy, and selection cost do not increase versus the strongest non-oracle baseline.
- Proposed method wins at least 5 of 7 paired seeds versus the strongest non-oracle baseline.
- Removing the mechanism taxonomy reduces success by at least 0.020.

Otherwise mark `KILL_ARCHIVE`.

## Manuscript Changes

- Replace archive framing with a full paper about mechanism-level dataset coverage.
- Add related work around Open X-Embodiment, DROID, BridgeData, RoboNet, RT-X, and data selection/active learning.
- Include local audit tables, stress curves, ablations, failure cases, and limitations.
- Keep the limitation explicit: local metadata simulation is not enough for ICLR-main submission without real public-dataset validation.

## Artifact Requirements

- Produce `C:/Users/wangz/Downloads/111.pdf` only.
- Do not copy a PDF to the visible Desktop.
- Update `README.md`, `child_status.md`, paper docs, and root reports after the terminal decision.
- Commit and push the public GitHub repo only after local audits pass.
