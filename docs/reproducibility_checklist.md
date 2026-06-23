# Reproducibility Checklist

Version: v5_expanded

Decision: STRONG_REVISE

- Experiment entry point: `python src\run_experiment.py`.
- Manuscript entry point: `python scripts\generate_manuscript.py`.
- Validator: `python scripts\validate_submission_artifacts.py`.
- Seeds: 10 paired seeds.
- Generated CSVs: persisted under `results/`.
- Generated figures: persisted under `figures/`.
- Generated manuscript tables: persisted under `paper/`.
- Canonical PDF: `C:/Users/wangz/Downloads/111.pdf`.
- PDF pages: 25.
- PDF SHA256: `A2204B83096B7F570DD9C429A139E71A4FA8886BA2FF99C7DC5129FFC6C8481A`.
- Desktop PDF copies: forbidden and absent.

The local audit is reproducible, but the paper remains STRONG_REVISE because reproducibility of a local benchmark is not the same as external public-dataset validation.
