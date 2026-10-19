---
name: dataset-curation
description: "Curate, validate, and version datasets for machine learning and robotics, mitigating class imbalance, labeling drift, and schema violations."
---

# Dataset Curation & Validation Protocol

Use this skill when collecting training datasets, designing annotation schemas, filtering out noisy labels, or implementing data validation gates.

## Data Quality & Schema Enforcement

1. **Automated Schema Validation**:
   - Define explicit boundary constraints for all tabular and sensor inputs: null checks, numerical bounds, categorical cardinality, and string patterns.
   - Fail data ingestion pipelines immediately when unexpected schema shifts or missing critical fields occur.
2. **Annotation Consistency & Inter-Annotator Agreement**:
   - Quantify labeling consistency across human or automated annotators using **Cohen's Kappa** ($\kappa$) or **Krippendorff's Alpha** ($\alpha$).
   - Flag samples with high annotator disagreement for consensus review or active learning re-querying.
3. **Class Imbalance Mitigation**:
   - Inspect class distributions: if the minority class is $<5\%$, do not rely on random undersampling.
   - Use stratified sampling across all splits.
   - Combine focal loss ($\mathcal{L}_{\text{focal}} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$) with class-weighted re-sampling.

## Dataset Versioning & Lineage

- Track raw data, intermediate transformations, and final model training splits using deterministic tools (e.g. DVC, Git LFS, or Content-Addressable Storage).
- Fingerprint datasets with SHA-256 manifests to guarantee exact experimental reproducibility.
- Record metadata: source environment, sensor hardware revision, capture lighting conditions, and legal licensing terms.
