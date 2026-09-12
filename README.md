# CaseIntel

**AI-Powered Cybercrime Complaint Intelligence, Case Correlation & Investigation Assistance System**

Project Exhibition I · Int. M.Tech Cyber Security · School of Computing Science Engineering and Artificial Intelligence (SCAI), VIT Bhopal · Fall 2026

## Overview

CaseIntel is a prototype system that helps cybercrime investigators by automatically:

1. **Protecting privacy** — detecting and redacting PII in complaint text before it moves downstream
2. **Classifying** each complaint by crime type
3. **Extracting** structured scammer indicators (phone, UPI ID, bank account, URL, IP)
4. **Correlating** complaints that share indicators or textual similarity into case clusters
5. **Presenting** prioritized case clusters to investigators via a dashboard

## Architecture

```
Complaint Input → PII Protection → AI Classification
                                 → Indicator Extraction → Case Correlation → Investigation Dashboard
```

See `frontend/caseintel_system_architecture.svg` and `frontend/caseintel_data_flow.svg` for diagrams.

## Project structure

```
data/           Dataset generation, merging, and module outputs
modules/
  privacy/      Module 1 — PII detection & redaction
  classification/  Module 2 — Crime-type classification
  extraction/   Module 3 — Indicator extraction
  correlation/  Module 4 — Case correlation & clustering
frontend/       Module 5 — Investigation dashboard + diagrams
api/            (planned) REST API layer
```

## Setup

```bash
pip install scikit-learn pandas joblib
```

## Running the pipeline

```bash
# 1. Generate the synthetic dataset
cd data && python3 generate_dataset.py

# 2. Merge with real fraud SMS dataset
python3 merge_datasets.py

# 3. Run each module (from its own folder)
cd ../modules/privacy && python3 pii_protection.py
cd ../classification && python3 classify.py
cd ../extraction && python3 extract_indicators.py
cd ../correlation && python3 correlate.py

# 4. Open the dashboard
# frontend/dashboard.html — open directly in a browser, no server needed
```

## Dataset

- 400 synthetic cybercrime complaints (5 crime types), generated with deliberately shared scammer indicators to simulate real fraud campaigns
- Merged with a real public India-specific SMS fraud dataset for authentic scam-language grounding
- Every row is tagged `source: synthetic` or `source: real` in `combined_dataset.csv`

## Results (current prototype)

| Metric | Value |
|---|---|
| Total complaints processed | 427 |
| Classification test accuracy | 95% |
| PII instances redacted | 511 |
| Indicators extracted | 524 |
| Correlated case clusters found | 10 |

## Team

| Module | Owner |
|---|---|
| PII Protection | *(name)* |
| AI Classification | *(name)* |
| Indicator Extraction | *(name)* |
| Case Correlation | *(name)* |
| Dashboard & Visualization | *(name)* |

## References

See `data/references.md`.

## Status

Prototype built for Review-2 (Project Exhibition I). Next steps: transformer-based classification, FastAPI backend with persistence, expanded real dataset coverage — see `data/review2_slide_content.md` for the full roadmap.
