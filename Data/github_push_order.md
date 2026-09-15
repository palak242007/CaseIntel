# CaseIntel — GitHub Push Order

## Purpose

This document defines the recommended order for developing, committing, pushing, reviewing, and merging CaseIntel files into the shared GitHub repository.

The purpose of following a fixed push order is to prevent:

* Broken dependencies
* Missing files
* Conflicting JSON structures
* Dashboard integration failures
* Model-file mismatches
* Last-minute merge problems
* Unclear ownership of files

The team should integrate continuously rather than waiting until the final day.

---

# 1. Golden Rule

## Push according to dependency order

```text
Member 1
Data + PII Protection
        ↓
Member 2
AI Classification
        ↓
Member 3
Indicator Extraction
        ↓
Member 4
Case Correlation
        ↓
Member 5
Dashboard + Integration
        ↓
Final Integration
```

However, members may develop their modules in parallel.

The **push/merge order applies to shared dependencies**, not necessarily to when members are allowed to start coding.

---

# 2. Repository Branch Structure

The main branch should remain stable.

```text
main
│
├── member1-data-privacy
├── member2-classification
├── member3-indicators
├── member4-correlation
└── member5-dashboard-integration
```

Optional integration branch:

```text
integration
```

Recommended flow:

```text
Feature Branch
      ↓
Pull Request
      ↓
Review
      ↓
Integration Branch
      ↓
Testing
      ↓
Main
```

For a small academic project, the team can also merge directly into `main` after review if that is easier.

---

# 3. Before First Push

Every member should first clone/pull the latest repository.

```bash
git clone <repository-url>
cd CaseIntel
```

Then:

```bash
git checkout main
git pull origin main
```

Create the member's branch:

```bash
git checkout -b member1-data-privacy
```

Replace the branch name according to the member.

---

# 4. Push Order Overview

Recommended order:

```text
PHASE 1
Project structure + documentation
        ↓
PHASE 2
Member 1 — Dataset + PII
        ↓
PHASE 3
Member 2 — Classification
        ↓
PHASE 4
Member 3 — Indicator Extraction
        ↓
PHASE 5
Member 4 — Correlation
        ↓
PHASE 6
Member 5 — Dashboard Integration
        ↓
PHASE 7
End-to-End Testing
        ↓
PHASE 8
Final Merge
```

---

# 5. PHASE 1 — Base Repository

## Owner

Team Lead / Shared Responsibility

---

## Files

Create the basic structure first:

```text
CaseIntel/
│
├── data/
├── models/
├── src/
├── frontend/
├── tests/
├── api/
│
├── README.md
├── references.md
├── team_work_division.md
└── review2_slide_content.md
```

Do not add generated datasets, models, or temporary files yet.

---

## First Commit

Suggested commit:

```text
chore: initialize CaseIntel project structure
```

Push:

```bash
git add .
git commit -m "chore: initialize CaseIntel project structure"
git push origin main
```

---

# 6. PHASE 2 — Member 1

## Data + PII Protection

Member 1 should be the first technical module pushed because the downstream modules depend on the data format.

---

## Files to Push

```text
data/
├── combined_dataset.csv
└── pii_protected_complaints.json

src/
├── data_processing.py
└── pii_protection.py
```

Optional:

```text
tests/
└── test_pii_protection.py
```

---

## Before Push

Member 1 must verify:

```text
☐ Dataset loads
☐ Required columns exist
☐ PII processing works
☐ JSON is valid
☐ CSV is valid
☐ No confidential data is included
☐ No API keys/passwords are included
☐ Paths work from project root
```

---

## Commit

```bash
git add data/combined_dataset.csv
git add data/pii_protected_complaints.json
git add src/data_processing.py
git add src/pii_protection.py
git commit -m "feat: add dataset processing and PII protection"
```

Then:

```bash
git push origin member1-data-privacy
```

---

# 7. Member 1 Pull Request

## PR Title

```text
Add dataset processing and PII protection
```

## PR Description

Include:

```text
Summary:
- Added cleaned complaint dataset
- Added PII protection pipeline
- Added protected complaint JSON
- Added data-processing module

Testing:
- Dataset loading tested
- PII masking tested
- JSON output validated

Dependencies:
- Provides protected data for classification and extraction modules
```

---

# 8. Review Before Merge

At least one other member should review:

* Dataset structure
* PII masking
* JSON schema
* File paths
* Sensitive information handling

Once approved:

```text
member1-data-privacy
          ↓
        main
```

---

# 9. PHASE 3 — Member 2

## AI Classification

Member 2 can develop the classifier in parallel, but should finalize against the data format provided by Member 1.

---

## Files to Push

```text
src/
└── classification.py

models/
├── classifier.joblib
└── vectorizer.joblib
```

Optional:

```text
tests/
└── test_classification.py
```

Optional evaluation file:

```text
data/
└── classification_results.json
```

---

## Before Push

Verify:

```text
☐ Dataset loads
☐ Text preprocessing works
☐ TF-IDF works
☐ Model trains
☐ Model saves
☐ Model loads
☐ Prediction works
☐ Evaluation metrics are generated
☐ Metrics are real
☐ Model output format is documented
```

---

## Commit

```bash
git add src/classification.py
git add models/classifier.joblib
git add models/vectorizer.joblib
git commit -m "feat: add complaint classification model"
```

Push:

```bash
git push origin member2-classification
```

---

# 10. Member 2 Pull Request

## PR Title

```text
Add complaint classification model
```

## PR Description

```text
Summary:
- Added text preprocessing
- Added TF-IDF vectorization
- Added classification model
- Added saved model artifacts
- Added model evaluation

Testing:
- Training completed successfully
- Model reload tested
- Sample predictions tested

Dependencies:
- Uses protected/clean complaint data from Member 1
```

---

# 11. PHASE 4 — Member 3

## Indicator Extraction

Member 3 can work in parallel with Member 2 but must finalize the output schema before Member 4 begins integration.

---

## Files to Push

```text
src/
└── indicator_extraction.py

data/
└── extracted_indicators.json
```

Optional:

```text
tests/
└── test_indicator_extraction.py
```

---

## Expected Structure

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

The actual structure may differ, but it must be documented and kept consistent.

---

## Before Push

Verify:

```text
☐ Phone extraction works
☐ Email extraction works
☐ URL extraction works
☐ UPI extraction works
☐ Missing indicators are handled
☐ Case IDs are preserved
☐ JSON is valid
☐ Sensitive values are appropriately protected
```

---

## Commit

```bash
git add src/indicator_extraction.py
git add data/extracted_indicators.json
git commit -m "feat: add complaint indicator extraction"
```

Push:

```bash
git push origin member3-indicators
```

---

# 12. Member 3 Pull Request

## PR Title

```text
Add complaint indicator extraction
```

## PR Description

```text
Summary:
- Added structured indicator extraction
- Added supported indicator types
- Added JSON output

Testing:
- Tested phone extraction
- Tested email extraction
- Tested URL extraction
- Tested UPI extraction
- Tested missing indicators

Dependencies:
- Consumes complaint text from the prepared dataset
- Provides structured indicators to correlation module
```

---

# 13. PHASE 5 — Member 4

## Case Correlation

Member 4 should integrate only after the indicator format is stable.

---

## Files to Push

```text
src/
└── correlation.py

data/
└── case_clusters.json
```

Optional:

```text
tests/
└── test_correlation.py
```

---

## Correlation Output

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

## Before Push

Verify:

```text
☐ Cases can be compared
☐ Shared indicators are detected
☐ Similarity calculation works
☐ Self-comparisons are excluded
☐ Duplicate relationships are handled
☐ Threshold is documented
☐ Output JSON is valid
☐ Relationship language is cautious
```

Use:

```text
Potential relationship
```

rather than:

```text
Confirmed criminal connection
```

---

## Commit

```bash
git add src/correlation.py
git add data/case_clusters.json
git commit -m "feat: add case correlation pipeline"
```

Push:

```bash
git push origin member4-correlation
```

---

# 14. Member 4 Pull Request

## PR Title

```text
Add case correlation and similarity analysis
```

## PR Description

```text
Summary:
- Added case comparison
- Added shared-indicator matching
- Added similarity analysis
- Added correlation output

Testing:
- Shared indicators tested
- Similarity tested
- Duplicate relationships tested
- Self-comparisons tested

Dependencies:
- Uses indicator output from Member 3
```

---

# 15. PHASE 6 — Member 5

## Dashboard + Integration

Member 5 should integrate the outputs after Members 1–4 have stable formats.

---

## Files to Push

```text
frontend/
├── dashboard.html
├── dashboard_template.html
├── caseintel_data_flow.svg
└── caseintel_system_architecture.svg
```

If actually used:

```text
data/
└── dashboard_data.json
```

Optional:

```text
tests/
└── test_integration.py
```

---

# 16. Dashboard Integration Order

Member 5 should connect data in this order:

```text
1. Protected complaints
        ↓
2. Classification output
        ↓
3. Extracted indicators
        ↓
4. Correlation results
        ↓
5. Investigation leads
        ↓
6. dashboard_data.json
        ↓
7. dashboard.html
```

---

# 17. Dashboard Commit

Example:

```bash
git add frontend/
git add data/dashboard_data.json
git commit -m "feat: integrate CaseIntel dashboard"
```

Push:

```bash
git push origin member5-dashboard-integration
```

---

# 18. Member 5 Pull Request

## PR Title

```text
Integrate CaseIntel dashboard
```

## PR Description

```text
Summary:
- Integrated classification results
- Integrated extracted indicators
- Integrated case correlations
- Added investigation-lead display
- Added dashboard data layer
- Updated architecture/data-flow diagrams

Testing:
- Dashboard loading tested
- Case search tested
- Sample case tested
- End-to-end data display tested
```

---

# 19. PHASE 7 — Integration Testing

After all major branches have been merged, perform a complete integration test.

---

## Test Flow

```text
Complaint
   ↓
Data Processing
   ↓
PII Protection
   ↓
Classification
   ↓
Indicator Extraction
   ↓
Case Correlation
   ↓
Investigation Lead
   ↓
Dashboard
```

---

# 20. Integration Test Checklist

```text
☐ Dataset loads
☐ PII module runs
☐ Classification module runs
☐ Indicator extraction runs
☐ Correlation runs
☐ JSON files are generated
☐ Dashboard reads generated data
☐ Case search works
☐ Classification appears correctly
☐ Indicators appear correctly
☐ Related cases appear correctly
☐ Investigation lead appears correctly
☐ No sensitive information is unnecessarily displayed
```

---

# 21. End-to-End Test Commit

If changes are required:

```bash
git checkout -b integration-testing
```

After fixing issues:

```bash
git add .
git commit -m "test: validate end-to-end CaseIntel pipeline"
git push origin integration-testing
```

---

# 22. Final Merge Order

The recommended final merge sequence is:

```text
1. Base project structure
        ↓
2. Member 1 — Data + PII
        ↓
3. Member 2 — Classification
        ↓
4. Member 3 — Indicators
        ↓
5. Member 4 — Correlation
        ↓
6. Member 5 — Dashboard
        ↓
7. Integration testing
        ↓
8. Documentation
        ↓
9. Final main branch
```

---

# 23. Documentation Push

After the implementation stabilizes, update:

```text
README.md
references.md
team_work_division.md
review2_slide_content.md
```

Documentation should describe the actual implementation, not an intended future architecture.

---

## Commit

```bash
git add README.md
git add references.md
git add team_work_division.md
git add review2_slide_content.md

git commit -m "docs: finalize CaseIntel documentation"
```

---

# 24. Final Cleanup

Before the final push, check:

```bash
git status
```

Look for:

```text
.env
__pycache__/
*.pyc
.DS_Store
.vscode/
.idea/
temporary files
debug output
personal datasets
private credentials
```

These should normally not be committed.

---

# 25. `.gitignore`

The project should have a `.gitignore`.

Example:

```text id="3i6s1o"
__pycache__/
*.pyc
.env
.venv/
venv/
.DS_Store
.idea/
.vscode/
*.log
```

If model files are required for the demo, do **not** blindly ignore `*.joblib`. Keep the specific required model artifacts versioned if they are small enough and permitted.

---

# 26. Sensitive Data Check

Before every push:

```text
☐ No real phone numbers
☐ No real email addresses
☐ No passwords
☐ No API keys
☐ No authentication tokens
☐ No confidential case information
☐ No private government identifiers
☐ No private user data
```

Use synthetic or appropriately anonymized data.

---

# 27. Commit Order by Member

## Member 1

```text
1. data_processing.py
2. pii_protection.py
3. combined_dataset.csv
4. pii_protected_complaints.json
5. tests
```

---

## Member 2

```text
1. classification.py
2. classifier.joblib
3. vectorizer.joblib
4. evaluation output
5. tests
```

---

## Member 3

```text
1. indicator_extraction.py
2. extracted_indicators.json
3. tests
```

---

## Member 4

```text
1. correlation.py
2. case_clusters.json
3. tests
```

---

## Member 5

```text
1. dashboard.html
2. dashboard_template.html
3. dashboard_data.json
4. architecture SVG
5. data-flow SVG
6. integration tests
```

---

# 28. What Should NOT Be Pushed Early

Avoid pushing incomplete or temporary files such as:

```text
test.py
abc.py
final.py
demo2.py
temp.json
output_new.json
model_final_final.joblib
screenshot.png
```

unless they are genuinely part of the project.

---

# 29. If a Member Changes a Shared JSON Format

This is a critical rule.

Suppose Member 3 changes:

```json
{
  "phone_numbers": []
}
```

to:

```json
{
  "indicators": {
    "phone_numbers": []
  }
}
```

They must notify Member 4 and Member 5 before merging.

The process should be:

```text
Proposed Change
      ↓
Notify Dependent Members
      ↓
Update Dependent Code
      ↓
Run Tests
      ↓
Merge
```

Never silently introduce breaking changes.

---

# 30. If a Merge Conflict Occurs

Do not randomly overwrite files.

First:

```bash
git status
```

Identify the conflicting files.

Then coordinate with the owner of the file.

For example:

```text
dashboard.html conflict
        ↓
Member 5 owns file
        ↓
Member 5 resolves conflict
        ↓
Team reviews result
```

---

# 31. If a Push Breaks the Main Branch

Do not continue adding features.

Immediately:

```text
Stop
 ↓
Identify broken commit
 ↓
Fix issue
 ↓
Run tests
 ↓
Push fix
 ↓
Retest
```

If necessary, use Git history to revert the problematic merge rather than making unrelated emergency changes.

---

# 32. Daily Push Policy

Do not keep all work locally for several days.

Recommended:

```text
Small working change
        ↓
Test
        ↓
Commit
        ↓
Push
```

At least one meaningful push should happen on active development days.

---

# 33. 10-Day GitHub Push Schedule

## Day 1

```text
Base repository
Project structure
Documentation skeleton
```

---

## Day 2

```text
Member 1:
Initial dataset processing

Member 2:
Initial classification code

Member 3:
Initial extraction code

Member 4:
Initial correlation code

Member 5:
Dashboard skeleton
```

These can remain on separate branches.

---

## Day 3

```text
Member 1:
Protected dataset

Member 2:
Baseline model

Member 3:
Indicator extraction

Member 4:
Correlation prototype

Member 5:
Dashboard sample data
```

---

## Day 4

Merge stable module versions.

```text
Member 1 → main
Member 2 → main
Member 3 → main
```

Member 4 begins against stable indicator output.

---

## Day 5

```text
Member 4 → main
Member 5 → integration
```

---

## Day 6

Full pipeline integration.

```text
Data
 ↓
Classification
 ↓
Extraction
 ↓
Correlation
 ↓
Dashboard
```

---

## Day 7

Bug fixes.

```text
fix: correct JSON parsing
fix: handle missing indicators
fix: correct dashboard case lookup
```

---

## Day 8

Testing and UI improvements.

---

## Day 9

Final integration and documentation.

---

## Day 10

Freeze the main branch.

Only critical fixes should be merged after this point.

---

# 34. Final Repository Freeze

Before presentation:

```text
MAIN BRANCH FREEZE
        ↓
No unnecessary features
        ↓
Only critical bug fixes
        ↓
Final test
        ↓
Final demo
```

Do not introduce a large new feature one hour before the presentation.

---

# 35. Final Repository Checklist

```text
☐ main branch builds/runs
☐ Dataset available or reproducible
☐ PII protection works
☐ Classifier works
☐ Model artifacts available
☐ Indicator extraction works
☐ Correlation works
☐ Dashboard works
☐ JSON files are valid
☐ Tests pass
☐ README is complete
☐ references.md is complete
☐ team_work_division.md is complete
☐ review2_slide_content.md is complete
☐ .gitignore exists
☐ No secrets committed
☐ No unnecessary PII committed
☐ No temporary files committed
☐ Final demo case works
```

---

# 36. Final Git History Goal

The repository history should tell a clear development story:

```text
chore: initialize CaseIntel project structure

feat: add dataset processing and PII protection

feat: add complaint classification model

feat: add complaint indicator extraction

feat: add case correlation pipeline

feat: integrate CaseIntel dashboard

test: validate end-to-end CaseIntel pipeline

docs: finalize CaseIntel documentation

fix: resolve final integration issues
```

This is much better than a history containing:

```text
final
final2
final3
last
last2
new
changes
```

---

# 37. Final Workflow

The complete team workflow is:

```text
                 CASEINTEL REPOSITORY
                         │
                         ▼
                  Project Structure
                         │
                         ▼
                 ┌───────────────┐
                 │    MEMBER 1   │
                 │ Data + Privacy│
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    MEMBER 2   │
                 │ Classification│
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    MEMBER 3   │
                 │  Indicators   │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    MEMBER 4   │
                 │  Correlation  │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    MEMBER 5   │
                 │   Dashboard   │
                 └───────┬───────┘
                         │
                         ▼
                  Integration Test
                         │
                         ▼
                    Documentation
                         │
                         ▼
                    MAIN BRANCH
                         │
                         ▼
                  FINAL DEMO
```

---

# 38. Golden Rules for the Team

## Rule 1

**Never push untested code to `main`.**

## Rule 2

**Never commit real confidential PII.**

## Rule 3

**Never silently change another module's data format.**

## Rule 4

**Never fabricate model metrics or correlation results.**

## Rule 5

**Commit small, meaningful changes.**

## Rule 6

**Pull the latest `main` before starting major integration work.**

## Rule 7

**Test the complete pipeline before the final presentation.**

## Rule 8

**Keep the final `main` branch reproducible.**

## Rule 9

**The dashboard must consume actual outputs wherever possible.**

## Rule 10

**Freeze the repository before the final demo except for critical fixes.**

---

# 39. Final Definition of Done

CaseIntel is ready for final submission when:

```text
             ALL MODULES WORK
                    +
             DATA FORMATS MATCH
                    +
             MODELS LOAD
                    +
             JSON OUTPUTS VALID
                    +
             CORRELATION WORKS
                    +
             DASHBOARD WORKS
                    +
             END-TO-END TEST PASSES
                    +
             DOCUMENTATION COMPLETE
                    +
             NO SENSITIVE DATA
                    ↓
             CASEINTEL READY
```

The objective of the GitHub workflow is not simply to get every member's code into the repository. The objective is to ensure that **all five members' work becomes one reproducible, working CaseIntel system**.
