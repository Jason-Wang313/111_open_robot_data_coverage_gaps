# Hostile Prior Work

The broad claim "robot datasets have coverage gaps" is not novel.

Relevant pressure points:
- Open X-Embodiment/RT-X already aggregates many robot datasets and studies cross-embodiment transfer.
- DROID and BridgeData-style datasets already emphasize scale and real-world manipulation diversity.
- RoboNet and related datasets already study cross-robot visual foresight and robot data sharing.
- Active learning, uncertainty sampling, embedding diversity, and failure prediction already select data.

The novelty boundary is narrow: this paper tests mechanism-level coverage, not just task, embodiment, trajectory, or embedding diversity, and asks whether that coverage better predicts held-out mechanism failures.
