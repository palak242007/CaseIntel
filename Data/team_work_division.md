# CaseIntel — Team Work Division

## Project

**CaseIntel — AI-Assisted Cybercrime Complaint Analysis and Case Correlation System**

This document defines the responsibilities, deliverables, dependencies, handoffs, Git workflow, testing responsibilities, and integration plan for the five members of the CaseIntel project team.

---

# 1. Team Objective

The team will develop an integrated prototype that can:

1. Process cybercrime complaint data.
2. Protect unnecessary Personally Identifiable Information (PII).
3. Classify complaints into relevant crime categories.
4. Extract useful investigation indicators.
5. Identify potentially related cases.
6. Generate investigation leads.
7. Display the results through a unified dashboard.

The final system should work as one pipeline rather than as five disconnected modules.

---

# 2. Overall System Pipeline

```text
                         CASEINTEL
                             │
                             ▼
                  ┌────────────────────┐
                  │ Complaint Dataset  │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Member 1           │
                  │ Data + PII         │
                  │ Protection         │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Member 2           │
                  │ AI Classification  │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Member 3           │
                  │ Indicator          │
                  │ Extraction         │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Member 4           │
                  │ Case Correlation   │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Member 5           │
                  │ Dashboard +        │
                  │ Integration        │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Investigator       │
                  │ Dashboard          │
                  └────────────────────┘
```

---

# 3. Team Members

| Member   | Role                            | Primary Responsibility                     |
| -------- | ------------------------------- | ------------------------------------------ |
| Member 1 | Data & Privacy Engineer         | Dataset preparation and PII protection     |
| Member 2 | ML Engineer                     | Crime-category classification              |
| Member 3 | NLP/Extraction Engineer         | Indicator extraction                       |
| Member 4 | Correlation Engineer            | Case similarity and relationship detection |
| Member 5 | Integration & Frontend Engineer | Dashboard and complete-system integration  |

---

# 4. Member 1 — Data + PII Protection

## Primary Responsibility

Member 1 is responsible for preparing the complaint data and protecting sensitive information.

---

## Tasks

### Dataset Preparation

* Obtain or prepare the project dataset.
* Inspect dataset structure.
* Identify relevant columns.
* Remove unnecessary columns.
* Handle missing values.
* Normalize inconsistent data.
* Create a clean dataset for downstream modules.

### PII Protection

Identify potentially sensitive information such as:

* Phone numbers
* Email addresses
* Account numbers
* Addresses
* Government identifiers
* Other identifying information

Apply appropriate masking or redaction where necessary.

---

## Expected Outputs

```text
data/
├── combined_dataset.csv
└── pii_protected_complaints.json
```

---

## Suggested Responsibilities in Code

```text
src/
└── data_processing.py

src/
└── pii_protection.py
```

---

## Handoff to Member 2

Member 1 provides:

```text
Clean Dataset
        +
Protected Complaint Text
        ↓
Member 2
```

Member 2 should not have to clean the same dataset again.

---

## Acceptance Criteria

Member 1 is complete when:

* [ ] Dataset loads successfully.
* [ ] Required columns are present.
* [ ] Missing values are handled appropriately.
* [ ] Sensitive information is identified.
* [ ] PII is masked/redacted where required.
* [ ] Output JSON is valid.
* [ ] Output CSV is readable.
* [ ] No unnecessary real PII is committed to GitHub.
* [ ] Documentation explains the processing steps.

---

# 5. Member 2 — AI Classification

## Primary Responsibility

Member 2 develops the machine-learning model that predicts the category of a cybercrime complaint.

---

## Tasks

### Data Preparation

Use the protected/clean dataset received from Member 1.

### Text Processing

Possible pipeline:

```text
Complaint Text
      ↓
Cleaning
      ↓
TF-IDF
      ↓
Feature Matrix
```

### Model Training

Train an appropriate classifier.

Possible algorithms include:

* Logistic Regression
* Linear SVM
* Naive Bayes
* Other appropriate scikit-learn classifier

The final algorithm should be the one actually tested and selected by the team.

### Evaluation

Calculate appropriate metrics such as:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

---

## Expected Outputs

```text
models/
├── classifier.joblib
└── vectorizer.joblib
```

---

## Suggested Code

```text
src/
└── classification.py
```

---

## Handoff to Member 4 / Member 5

Member 2 provides:

```text
classifier.joblib
vectorizer.joblib
classification output
evaluation metrics
```

These outputs can be consumed by the integration and dashboard modules.

---

## Acceptance Criteria

* [ ] Model trains successfully.
* [ ] Model can be saved.
* [ ] Model can be loaded.
* [ ] New complaint text can be classified.
* [ ] Evaluation metrics are generated.
* [ ] No fabricated accuracy values are used.
* [ ] Model output has a clearly defined format.
* [ ] Required model files are available to the integration process.

---

# 6. Member 3 — Indicator Extraction

## Primary Responsibility

Member 3 extracts structured investigation indicators from complaint text.

---

## Indicators

Depending on the dataset and implementation, indicators may include:

```text
Phone Number
Email Address
URL
UPI Identifier
Account Number
Other Supported Identifiers
```

---

## Extraction Methods

Possible methods include:

* Regular expressions
* Keyword/rule-based extraction
* NLP techniques
* Named Entity Recognition if implemented

---

## Example

Input:

```text
I received a message from 9876543210
asking me to transfer money to demo@upi.
```

Output:

```json
{
  "phone_numbers": [
    "XXXXXX3210"
  ],
  "upi_ids": [
    "demo@upi"
  ]
}
```

---

## Expected Output

```text
data/
└── extracted_indicators.json
```

---

## Suggested Code

```text
src/
└── indicator_extraction.py
```

---

## Handoff to Member 4

Member 3 provides a consistent JSON structure.

Example:

```json
{
  "case_id": "C001",
  "indicators": {
    "phone_numbers": [],
    "email_addresses": [],
    "urls": [],
    "upi_ids": [],
    "account_numbers": []
  }
}
```

The exact schema must be agreed upon with Member 4 before implementation is finalized.

---

## Acceptance Criteria

* [ ] Supported indicators are documented.
* [ ] Extraction rules are implemented.
* [ ] Output is valid JSON.
* [ ] Case IDs are preserved.
* [ ] Indicator types are consistently named.
* [ ] False positives are considered.
* [ ] Sensitive values are masked where appropriate.
* [ ] Member 4 confirms the output format is usable.

---

# 7. Member 4 — Case Correlation

## Primary Responsibility

Member 4 identifies potentially related complaints.

---

## Correlation Signals

Possible signals include:

### Shared Indicators

```text
Same phone number
Same email
Same URL
Same UPI identifier
```

### Text Similarity

Use a suitable similarity method, such as cosine similarity over TF-IDF vectors.

### Category Similarity

Cases with the same predicted category may provide additional context, but category alone should not be treated as evidence of a relationship.

---

## General Workflow

```text
Case A
   │
   ├── Indicators
   │
   └── Text Vector
          │
          ▼
      Comparison
          ▲
          │
   ┌──────┴───────┐
   │              │
Case B          Case C
```

---

## Expected Output

```text
data/
└── case_clusters.json
```

---

## Suggested Code

```text
src/
└── correlation.py
```

---

## Example Output

```json
{
  "case_a": "C001",
  "case_b": "C004",
  "similarity_score": 0.87,
  "shared_indicators": [
    "phone_number",
    "url"
  ],
  "relationship_type": "potential_relationship"
}
```

---

## Important Interpretation Rule

The correlation system must not state:

```text
"These cases were committed by the same person."
```

Instead, use language such as:

```text
"Potential relationship detected."
```

or:

```text
"Shared indicators detected — manual investigation recommended."
```

---

## Acceptance Criteria

* [ ] Cases can be compared.
* [ ] Shared indicators can be detected.
* [ ] Similarity scores can be calculated where applicable.
* [ ] Results are stored in a consistent format.
* [ ] Duplicate/self-comparisons are handled.
* [ ] Thresholds are documented.
* [ ] Potential relationships are clearly distinguished from confirmed relationships.
* [ ] Member 5 can consume the output.

---

# 8. Member 5 — Dashboard + Integration

## Primary Responsibility

Member 5 combines the outputs from Members 1–4 and presents them through the CaseIntel dashboard.

---

## Main Responsibilities

### Dashboard

Maintain:

```text
frontend/dashboard.html
```

### Data Integration

Consume outputs such as:

```text
pii_protected_complaints.json
classifier.joblib
vectorizer.joblib
extracted_indicators.json
case_clusters.json
```

### Dashboard Data

Maintain the final dashboard data structure where required:

```text
data/dashboard_data.json
```

---

## Dashboard Sections

The dashboard should display:

### Overview

```text
Total Cases
Total Categories
Potential Relationships
Investigation Leads
```

### Case Search

Allow the user to find a case by case ID.

### Classification

Display:

```text
Predicted Category
Confidence/Score
```

if supported by the actual model.

### Indicators

Display:

```text
Phone
Email
URL
UPI
Other Supported Indicators
```

### Related Cases

Display:

```text
Case ID
Similarity
Shared Indicators
```

### Investigation Lead

Display:

```text
Priority
Reason
Related Cases
```

---

## Suggested Code

```text
frontend/
├── dashboard.html
└── dashboard_template.html
```

Optional:

```text
api/
└── app.py
```

Only create/use an API if the actual architecture requires one.

---

## Expected Outputs

```text
frontend/
├── dashboard.html
├── dashboard_template.html
├── caseintel_data_flow.svg
└── caseintel_system_architecture.svg

data/
└── dashboard_data.json
```

---

## Acceptance Criteria

* [ ] Dashboard loads.
* [ ] Dashboard displays actual project data.
* [ ] Case search works.
* [ ] Classification results are visible.
* [ ] Indicators are visible.
* [ ] Related cases are visible.
* [ ] Investigation leads are visible.
* [ ] Sensitive information is not unnecessarily exposed.
* [ ] No fake statistics are shown.
* [ ] Complete end-to-end workflow can be demonstrated.

---

# 9. Shared Data Contracts

To avoid integration failures, every module must use clearly defined data formats.

---

## Case ID

Every complaint should have a unique case identifier.

Example:

```text
C001
C002
C003
```

---

## Classification Format

Example:

```json
{
  "case_id": "C001",
  "predicted_category": "Phishing",
  "confidence": 0.94
}
```

If the model does not produce calibrated probabilities, use an appropriate term such as:

```text
model score
```

instead of incorrectly calling it a probability.

---

## Indicator Format

Example:

```json
{
  "case_id": "C001",
  "indicators": {
    "phone_numbers": [
      "XXXXXX3210"
    ],
    "email_addresses": [],
    "urls": [],
    "upi_ids": [],
    "account_numbers": []
  }
}
```

---

## Correlation Format

Example:

```json
{
  "case_a": "C001",
  "case_b": "C004",
  "similarity_score": 0.87,
  "shared_indicators": [
    "phone_number",
    "url"
  ],
  "relationship_type": "potential_relationship"
}
```

---

# 10. Shared File Ownership

| File                                | Owner    | Contributors |
| ----------------------------------- | -------- | ------------ |
| `combined_dataset.csv`              | Member 1 | All          |
| `pii_protected_complaints.json`     | Member 1 | Member 2, 5  |
| `classifier.joblib`                 | Member 2 | Member 5     |
| `vectorizer.joblib`                 | Member 2 | Member 5     |
| `extracted_indicators.json`         | Member 3 | Member 4, 5  |
| `case_clusters.json`                | Member 4 | Member 5     |
| `dashboard_data.json`               | Member 5 | Members 1–4  |
| `dashboard.html`                    | Member 5 | All          |
| `caseintel_data_flow.svg`           | Member 5 | All          |
| `caseintel_system_architecture.svg` | Member 5 | All          |
| `references.md`                     | Shared   | All          |
| `README.md`                         | Shared   | All          |
| `team_work_division.md`             | Shared   | All          |

---

# 11. Git Branch Strategy

Each member should work on a separate branch.

```text
main
│
├── member1-data-privacy
├── member2-classification
├── member3-indicators
├── member4-correlation
└── member5-dashboard-integration
```

---

# 12. Git Workflow

Each member should follow:

```text
Create / switch to branch
        ↓
Make changes
        ↓
Run tests
        ↓
git status
        ↓
git add
        ↓
git commit
        ↓
git push
        ↓
Pull Request
        ↓
Review
        ↓
Merge
```

---

# 13. Commit Message Convention

Use descriptive commit messages.

Good:

```text
feat: add PII masking pipeline
feat: train complaint classifier
feat: add indicator extraction
feat: implement case similarity
feat: integrate dashboard data
fix: correct JSON parsing
fix: handle missing case indicators
test: add correlation tests
docs: update system architecture
```

Avoid:

```text
update
changes
final
final2
new
test
abc
```

---

# 14. Pull Request Rules

Every Pull Request should include:

### Title

A clear description of the change.

Example:

```text
Add indicator extraction module
```

### Description

Include:

```text
What changed?
Why was it changed?
How was it tested?
Does another member need to update their code?
```

### Before Merge

Check:

* [ ] Code runs.
* [ ] Tests pass.
* [ ] No unnecessary files are included.
* [ ] No sensitive information is included.
* [ ] Data format is compatible with dependent modules.
* [ ] Documentation is updated if necessary.

---

# 15. Dependency Map

The modules depend on each other as follows:

```text
Member 1
   │
   ├──────────────► Member 2
   │
   └──────────────► Member 3
                         │
                         ▼
                     Member 4
                         │
                         ▼
                     Member 5
                         ▲
                         │
                    Member 2
```

More specifically:

```text
Member 1
  ├── Dataset
  └── Protected Data
          │
          ├──────────► Member 2
          │
          └──────────► Member 3

Member 2
  └── Classification Output
              │
              └──────────► Member 5

Member 3
  └── Indicators
          │
          └──────────► Member 4

Member 4
  └── Correlations
          │
          └──────────► Member 5

Member 5
  └── Final Dashboard
```

---

# 16. Integration Rules

The following rules apply to all members.

## Rule 1 — Do Not Change Another Member's Output Format Without Discussion

If a module currently produces:

```json
{
  "case_id": "C001",
  "indicators": {}
}
```

do not silently change it to another structure.

Discuss the change first.

---

## Rule 2 — Use Relative/Project-Aware Paths

Avoid hard-coded personal paths such as:

```text
C:\Users\John\Desktop\CaseIntel\data\
```

Use project-relative paths or a consistent path-handling approach.

---

## Rule 3 — No Real PII in GitHub

Do not commit:

* Real phone numbers
* Real email addresses
* Real account numbers
* Real addresses
* Confidential complaint records
* Authentication credentials
* API keys

Use synthetic or appropriately protected data for the repository.

---

## Rule 4 — No Fake Results

Do not fabricate:

* Accuracy
* Precision
* Recall
* F1-score
* Similarity scores
* Case counts
* Relationships
* Investigation leads

Demo values should be clearly identified as sample data if they are not generated by the actual system.

---

# 17. Testing Responsibilities

## Member 1

Test:

* Dataset loading
* Cleaning
* PII detection
* Masking
* Output format

---

## Member 2

Test:

* Training
* Prediction
* Model loading
* Vectorizer loading
* Evaluation metrics

---

## Member 3

Test:

* Phone extraction
* Email extraction
* URL extraction
* UPI extraction
* Missing indicators
* False-positive cases

---

## Member 4

Test:

* Case comparison
* Shared indicators
* Similarity calculation
* Threshold handling
* Duplicate relationships
* Self-comparison prevention

---

## Member 5

Test:

* JSON loading
* Dashboard rendering
* Case search
* Complete data flow
* End-to-end pipeline
* UI behavior

---

# 18. End-to-End Integration Test

The complete system should pass this test:

```text
INPUT
  │
  ▼
Complaint
  │
  ▼
PII Protection
  │
  ▼
Protected Complaint
  │
  ├───────────────┐
  ▼               ▼
Classification   Extraction
  │               │
  ▼               ▼
Category       Indicators
  │               │
  └───────┬───────┘
          ▼
      Correlation
          │
          ▼
 Related Cases
          │
          ▼
 Investigation Lead
          │
          ▼
      Dashboard
```

---

# 19. Definition of Done

A module is considered complete only when:

```text
Code works
   +
Output is generated
   +
Output format is documented
   +
Tests pass
   +
Dependent member can consume output
   +
Changes are committed
   +
Pull Request is created
```

A module is **not** complete merely because its Python script runs locally.

---

# 20. 10-Day Development Plan

## Day 1 — Setup

### All Members

* Confirm project requirements.
* Confirm repository structure.
* Confirm dataset.
* Confirm branch strategy.
* Define shared JSON schemas.

### Member 1

Begin dataset inspection.

### Member 2

Review classification requirements.

### Member 3

Define indicator types and extraction rules.

### Member 4

Define correlation strategy.

### Member 5

Inspect existing dashboard and architecture.

---

# Day 2 — Individual Module Development

### Member 1

Dataset cleaning and PII pipeline.

### Member 2

Text preprocessing and baseline classifier.

### Member 3

Indicator extraction implementation.

### Member 4

Correlation design and initial implementation.

### Member 5

Dashboard structure and data-loading mechanism.

---

# Day 3 — First Working Versions

### Member 1

Generate protected dataset.

### Member 2

Train first working model.

### Member 3

Generate first `extracted_indicators.json`.

### Member 4

Generate first `case_clusters.json`.

### Member 5

Connect sample data to dashboard.

---

# Day 4 — Module Testing

Each member tests their own module.

```text
Member 1 → Data tests
Member 2 → ML tests
Member 3 → Extraction tests
Member 4 → Correlation tests
Member 5 → Dashboard tests
```

---

# Day 5 — First Integration

Connect:

```text
Member 1 → Member 2
Member 1 → Member 3
Member 3 → Member 4
```

Member 5 begins consuming actual outputs.

---

# Day 6 — Full Pipeline

Connect:

```text
Member 1
   ↓
Member 2
   ↓
Member 3
   ↓
Member 4
   ↓
Member 5
```

Run an end-to-end test using sample data.

---

# Day 7 — Debugging

Focus on:

* File paths
* JSON structures
* Missing values
* Model loading
* Dashboard loading
* Incorrect correlations
* UI errors

No major new features should be started unless necessary.

---

# Day 8 — Evaluation + UI

### ML

Finalize evaluation metrics.

### Correlation

Validate thresholds and relationship logic.

### Dashboard

Improve:

* Layout
* Readability
* Case search
* Indicator display
* Related-case display
* Investigation-lead presentation

---

# Day 9 — Final Testing

Perform:

```text
Clean checkout
      ↓
Install dependencies
      ↓
Run pipeline
      ↓
Generate outputs
      ↓
Open dashboard
      ↓
Perform demo case
```

Verify that another team member can reproduce the project.

---

# Day 10 — Presentation Preparation

### All Members

Prepare:

* PPT
* Live demo
* Architecture explanation
* Individual contribution explanation
* Results
* Limitations
* Future scope
* Questions and answers

### Final Repository Check

```text
☐ README complete
☐ references.md complete
☐ team_work_division.md complete
☐ Review 2 slides complete
☐ Code organized
☐ Tests working
☐ No sensitive data
☐ No unnecessary files
☐ Final dashboard working
☐ Final demo tested
```

---

# 21. Communication Protocol

The team should maintain a simple communication process.

When a member changes an interface or output format, they should notify the affected member.

Example:

```text
Member 3:
"I changed extracted_indicators.json so
the indicators are nested under the
'indicators' key."

Member 4:
"Confirmed. I updated correlation.py."
```

Do not silently make breaking changes.

---

# 22. Daily Team Check-In

At the end of each working day, each member should report:

```text
1. Completed:
2. Currently working on:
3. Blocked by:
4. Files changed:
5. What another member needs:
```

Example:

```text
Member 4

Completed:
Case similarity implementation.

Currently working on:
Shared-indicator correlation.

Blocked by:
Need final indicator JSON format from Member 3.

Files:
src/correlation.py
data/case_clusters.json
```

---

# 23. Final Demo Responsibility

## Member 1

Explain:

```text
Dataset
+
PII protection
```

## Member 2

Explain:

```text
NLP
+
Classification
+
Model evaluation
```

## Member 3

Explain:

```text
Indicator extraction
```

## Member 4

Explain:

```text
Case correlation
+
Similarity
+
Investigation leads
```

## Member 5

Demonstrate:

```text
Dashboard
+
Complete integration
```

---

# 24. Suggested Presentation Flow

The final presentation should follow the same logic as the system:

```text
Problem
   ↓
Solution
   ↓
Architecture
   ↓
Data
   ↓
Privacy
   ↓
Classification
   ↓
Indicator Extraction
   ↓
Correlation
   ↓
Dashboard
   ↓
Results
   ↓
Limitations
   ↓
Future Scope
```

This avoids presenting five unrelated mini-projects.

---

# 25. Important System Principle

CaseIntel is an **AI-assisted investigation support system**.

The team should consistently distinguish between:

```text
AI/Algorithmic Signal
```

and:

```text
Confirmed Investigation Finding
```

For example:

### Good

```text
Potential relationship detected.
Shared indicators require manual verification.
```

### Avoid

```text
Same criminal identified.
```

The system should support investigators rather than replace human verification.

---

# 26. Final Team Deliverables

At the end of the project, the team should have:

```text
CaseIntel/
│
├── data/
│   ├── combined_dataset.csv
│   ├── pii_protected_complaints.json
│   ├── extracted_indicators.json
│   ├── case_clusters.json
│   └── dashboard_data.json
│
├── models/
│   ├── classifier.joblib
│   └── vectorizer.joblib
│
├── src/
│   ├── data_processing.py
│   ├── pii_protection.py
│   ├── classification.py
│   ├── indicator_extraction.py
│   └── correlation.py
│
├── frontend/
│   ├── dashboard.html
│   ├── dashboard_template.html
│   ├── caseintel_data_flow.svg
│   └── caseintel_system_architecture.svg
│
├── tests/
│
├── api/
│
├── README.md
├── references.md
├── team_work_division.md
└── review2_slide_content.md
```

The final repository structure should match the actual implementation; files that are not used should not be created merely for appearance.

---

# 27. Final Responsibility Matrix

| Task                 |    M1    |    M2    |    M3    |    M4    |      M5     |
| -------------------- | :------: | :------: | :------: | :------: | :---------: |
| Dataset preparation  | **Lead** |  Support |  Support |  Support |   Support   |
| PII protection       | **Lead** |  Support |  Support |     -    |   Support   |
| NLP preprocessing    |  Support | **Lead** |  Support |  Support |      -      |
| Classification       |     -    | **Lead** |     -    |     -    |   Support   |
| Indicator extraction |     -    |  Support | **Lead** |  Support |   Support   |
| Similarity analysis  |     -    |  Support |  Support | **Lead** |   Support   |
| Case correlation     |     -    |     -    |  Support | **Lead** |   Support   |
| Investigation leads  |     -    |     -    |  Support | **Lead** | **Support** |
| Dashboard            |     -    |     -    |     -    |  Support |   **Lead**  |
| System integration   |  Support |  Support |  Support |  Support |   **Lead**  |
| Architecture diagram |  Support |  Support |  Support |  Support |   **Lead**  |
| Testing              | **Lead** | **Lead** | **Lead** | **Lead** |   **Lead**  |
| Documentation        |  Support |  Support |  Support |  Support |   **Lead**  |

---

# 28. Final Team Goal

The five members should not deliver five separate projects.

The goal is:

```text
                 5 MEMBERS
                     │
                     ▼
              5 MODULES
                     │
                     ▼
            1 INTEGRATED PIPELINE
                     │
                     ▼
              1 CASEINTEL SYSTEM
                     │
                     ▼
           1 INVESTIGATOR DASHBOARD
```

### Final Definition of Success

A reviewer should be able to provide a complaint, follow the processing pipeline, see the predicted category, inspect extracted indicators, view potentially related cases, understand the generated investigation lead, and see the complete result in the CaseIntel dashboard.

**The system should be demonstrable, reproducible, privacy-aware, and honest about the limitations of its AI-generated results.**
