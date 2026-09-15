# CaseIntel

**AI-Powered Cybercrime Complaint Intelligence, Case Correlation & Investigation Assistance System**
CaseIntel is a cybersecurity application designed to assist in the analysis of cybercrime complaints by combining **PII protection, machine-learning-based complaint classification, cybercrime indicator extraction, and case correlation**.

The system converts unstructured complaint data into structured and privacy-protected information that can help investigators identify related complaints and prioritize potentially connected cases.

## Overview

CaseIntel is a prototype system that helps cybercrime investigators by automatically:

1. **Protecting privacy** — detecting and redacting PII in complaint text before it moves downstream
2. **Classifying** each complaint by crime type
3. **Extracting** structured scammer indicators (phone, UPI ID, bank account, URL, IP)
4. **Correlating** complaints that share indicators or textual similarity into case clusters
5. **Presenting** prioritized case clusters to investigators via a dashboard

## Architecture

```
Complaint Input → PII Protection → AI Classification → Indicator Extraction → Case Correlation → Investigation Dashboard
```

See `frontend/caseintel_system_architecture.svg` and `frontend/caseintel_data_flow.svg` for diagrams.

## Project structure
```text
CaseIntel/
│
├── README.md
├── .gitignore
├── Data/
│   ├── generate_dataset.py
│   ├── complaints_dataset.csv
│   ├── complaints_dataset.json
│   ├── real_india_sms_raw.csv
│   ├── merge_datasets.py
│   ├── combined_dataset.csv
│   ├── pii_protected_complaints.json
│   ├── extracted_indicators.json
│   ├── case_clusters.json
│   ├── dashboard_data.json
│   ├── references.md
│   ├── github_push_order.md
│   │
│   └── models/
│       ├── classifier.joblib
│       └── vectorizer.joblib
│
├── modules/
│   ├── privacy/
│   │   └── pii_protection.py
│   │
│   ├── classification/
│   │   └── classify.py
│   │
│   ├── extraction/
│   │   └── extract_indicators.py
│   │
│   └── correlation/
│       └── correlate.py
│
├── Frontend/
│   ├── dashboard.html
│   ├── dashboard_template.html
│   ├── caseintel_data_flow.svg
│   └── caseintel_system_architecture.svg
│
├── Results/
    ├── classification_report.txt
    └── confusion_matrix.png
```

## Setup
```bash
pip install scikit-learn pandas joblib
```

## Running the pipeline
Complaint
    ↓
PII Redaction
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression
    ↓
Crime Category

## Dataset
- 400 synthetic cybercrime complaints (5 crime types), generated with deliberately shared scammer indicators to simulate real fraud campaigns
- Merged with a real public India-specific SMS fraud dataset for authentic scam-language grounding
- Every row is tagged `source: synthetic` or `source: real` in `combined_dataset.csv`

## Results (current prototype)
```text
| Metric | Value |
| Total complaints processed | 427 |
| Classification test accuracy | 95% |
| PII instances redacted | 511 |
| Indicators extracted | 524 |
| Correlated case clusters found | 10 |
```
## Team
```text
| Module | Owner |
| PII Protection | *Palak* |
| AI Classification | *Rishabh* |
| Indicator Extraction | *Nancy* |
| Case Correlation | *Shreyansh* |
| Dashboard & Visualization | *Vishnu* |
```
## References
See `data/references.md`.
