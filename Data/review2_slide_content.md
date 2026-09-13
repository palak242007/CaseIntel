# CaseIntel — Review 2 Slide Content

## Project Title

# CaseIntel

### AI-Assisted Cybercrime Complaint Analysis and Case Correlation System

**Second Project Review**

---

# Slide 1 — Title Slide

## CaseIntel

### AI-Assisted Cybercrime Complaint Analysis and Case Correlation System

**Presented by:**
Team CaseIntel

**Project Type:**
AI / Machine Learning / NLP / Cybercrime Analysis

**Review:**
Review 2

---

# Slide 2 — Problem Statement

## Problem Statement

Cybercrime complaint data can contain large amounts of unstructured text and useful investigative indicators.

Manually analyzing every complaint can make it difficult to:

* Categorize complaints consistently
* Identify important indicators
* Detect relationships between different complaints
* Prioritize potentially useful investigation leads
* Present analytical results in a unified format

### Our Goal

Develop an AI-assisted system that processes cybercrime complaints and helps investigators identify:

* Crime category
* Important indicators
* Potentially related cases
* Investigation leads

---

# Slide 3 — Proposed Solution

## CaseIntel Solution

CaseIntel provides an end-to-end pipeline for analyzing cybercrime complaints.

```text
Complaint Data
      ↓
PII Protection
      ↓
AI Classification
      ↓
Indicator Extraction
      ↓
Case Correlation
      ↓
Investigation Leads
      ↓
Dashboard
```

### Key Idea

Instead of manually inspecting every complaint independently, CaseIntel combines multiple analytical modules into one workflow.

---

# Slide 4 — Project Objectives

## Objectives

### 1. Protect sensitive information

Detect and mask unnecessary personally identifiable information (PII).

### 2. Classify complaints

Use NLP and machine learning to predict the category of a complaint.

### 3. Extract investigation indicators

Identify structured information such as:

* Phone numbers
* Email addresses
* URLs
* UPI identifiers
* Other supported indicators

### 4. Correlate cases

Compare cases using shared indicators and similarity measures.

### 5. Generate investigation leads

Highlight potentially related complaints for human investigation.

### 6. Provide a unified dashboard

Present the outputs of all modules through an investigator-friendly interface.

---

# Slide 5 — System Architecture

## CaseIntel System Architecture

```text
                  USER / INVESTIGATOR
                         │
                         ▼
                 ┌───────────────┐
                 │   Dashboard   │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Integration   │
                 │    Layer      │
                 └───────┬───────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   PII Protection   Classification   Extraction
    Member 1         Member 2        Member 3
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  ┌───────────────┐
                  │     Case      │
                  │  Correlation  │
                  │   Member 4    │
                  └───────┬───────┘
                          │
                          ▼
                  Investigation Leads
                          │
                          ▼
                      Dashboard
```

---

# Slide 6 — Data Flow

## Data Flow

```text
Raw Complaint
      │
      ▼
Data Cleaning
      │
      ▼
PII Protection
      │
      ▼
Protected Complaint
      │
      ├──────────────► Classification
      │                       │
      │                       ▼
      │                Crime Category
      │
      └──────────────► Indicator Extraction
                              │
                              ▼
                         Indicators
                              │
                              ▼
                       Case Correlation
                              │
                              ▼
                     Related Cases / Leads
                              │
                              ▼
                         Dashboard
```

---

# Slide 7 — Team Contribution

## Division of Work

| Member   | Module                  | Main Responsibility                        |
| -------- | ----------------------- | ------------------------------------------ |
| Member 1 | Data + PII Protection   | Dataset preparation and privacy protection |
| Member 2 | AI Classification       | Crime-category prediction                  |
| Member 3 | Indicator Extraction    | Extract useful structured indicators       |
| Member 4 | Case Correlation        | Identify potentially related cases         |
| Member 5 | Dashboard + Integration | Combine outputs and visualize results      |

### Integration Principle

Each member produces a structured output that can be consumed by the next module.

---

# Slide 8 — Member 1: Data + PII Protection

## Data Processing and Privacy

### Responsibilities

* Prepare complaint dataset
* Clean inconsistent records
* Handle missing values
* Identify sensitive information
* Mask or redact unnecessary PII
* Generate protected complaint data

### Example

```text
Original:
My phone number is 9876543210

Protected:
My phone number is XXXXXX3210
```

### Output

```text
combined_dataset.csv
pii_protected_complaints.json
```

---

# Slide 9 — Member 2: AI Classification

## Complaint Classification

The classification module predicts the crime category from complaint text.

### Pipeline

```text
Complaint Text
      ↓
Text Preprocessing
      ↓
TF-IDF Vectorization
      ↓
Machine Learning Classifier
      ↓
Predicted Category
```

### Example

```text
Input:
Victim received a suspicious message
containing a fraudulent login link.

Output:
Phishing
```

### Model Artifacts

```text
classifier.joblib
vectorizer.joblib
```

---

# Slide 10 — NLP and TF-IDF

## Text Representation

The system converts complaint text into numerical features using TF-IDF.

### Why TF-IDF?

TF-IDF helps identify words that are useful for distinguishing complaint categories.

```text
Complaint
    ↓
Tokenization / Preprocessing
    ↓
TF-IDF
    ↓
Numerical Vector
    ↓
ML Classifier
```

### Benefit

The classifier can work with textual complaint data after it has been converted into numerical features.

---

# Slide 11 — Member 3: Indicator Extraction

## Investigation Indicator Extraction

The indicator extraction module identifies structured information contained in complaint text.

### Indicators

```text
📱 Phone Number
📧 Email Address
🔗 URL
💳 UPI Identifier
🏦 Other Supported Identifiers
```

### Example

```text
Complaint:
Contacted from 9876543210
and asked to pay using demo@upi.

Extracted:

Phone:
XXXXXX3210

UPI:
demo@upi
```

### Output

```text
extracted_indicators.json
```

---

# Slide 12 — Member 4: Case Correlation

## Case Correlation

The correlation module compares complaints to identify potentially related cases.

### Signals

* Shared phone number
* Shared email address
* Shared URL
* Shared UPI identifier
* Similar complaint text
* Other supported indicators

### Example

```text
Case C001
   │
   ├── Phone: XXXXXX4321
   └── URL: example-phishing.test
             │
             ▼
          Case C004
```

### Result

```text
Potential relationship detected
```

---

# Slide 13 — Similarity Analysis

## Similarity Score

Text or feature vectors can be compared using cosine similarity.

```text
Case A ──► Vector A
              │
              │
              ▼
       Cosine Similarity
              ▲
              │
              │
Case B ──► Vector B
```

### Interpretation

```text
Score closer to 1
        ↓
Higher similarity

Score closer to 0
        ↓
Lower similarity
```

Similarity is an analytical signal and does not prove that two cases are connected.

---

# Slide 14 — Investigation Leads

## Investigation Lead Generation

CaseIntel converts correlation results into potential investigation leads.

### Example

```text
Case C001
    ↓
Shared phone number
    ↓
Case C004
    ↓
Potential relationship
    ↓
Manual investigation recommended
```

### Lead Priority

The prototype can classify leads as:

* High
* Medium
* Low

based on the implemented correlation rules and signals.

---

# Slide 15 — Dashboard

## CaseIntel Dashboard

The dashboard combines the outputs of all analytical modules.

### Dashboard Components

```text
┌───────────────────────────────────┐
│          CASEINTEL                │
├─────────┬─────────┬───────────────┤
│ Cases   │ Leads   │ Relationships │
├─────────┴─────────┴───────────────┤
│ Case Search                        │
├───────────────────────────────────┤
│ Crime Classification              │
├───────────────────────────────────┤
│ Extracted Indicators              │
├───────────────────────────────────┤
│ Related Cases                     │
├───────────────────────────────────┤
│ Investigation Lead                │
└───────────────────────────────────┘
```

### Main File

```text
frontend/dashboard.html
```

---

# Slide 16 — Dashboard Data Integration

## Integration Layer

The dashboard consumes structured outputs from the backend modules.

```text
PII Module
     │
     ▼
pii_protected_complaints.json
     │
     ├──────────────┐
     ▼              ▼
Classification   Extraction
     │              │
     ▼              ▼
Model Output    Indicators
     │              │
     └──────┬───────┘
            ▼
       Correlation
            │
            ▼
      case_clusters.json
            │
            ▼
    dashboard_data.json
            │
            ▼
       Dashboard
```

The integration layer ensures that the frontend displays structured results rather than raw intermediate processing output.

---

# Slide 17 — Project File Structure

## Current Project Structure

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
└── references.md
```

The final structure should be updated to match the actual repository.

---

# Slide 18 — Technology Stack

## Technologies Used

### Programming

* Python
* HTML
* CSS
* JavaScript

### Data Processing

* Pandas
* NumPy
* JSON

### Machine Learning

* Scikit-learn
* TF-IDF
* Classification algorithms
* Cosine similarity

### Model Persistence

* Joblib

### Development

* Git
* GitHub

---

# Slide 19 — Privacy and Security

## Privacy by Design

Because complaint information may contain sensitive data, privacy is considered throughout the pipeline.

### Measures

* PII identification
* Masking/redaction
* Avoiding unnecessary exposure of personal information
* Protected dashboard display
* No real confidential complaint information in the public repository

### Principle

```text
Use only the information necessary
for the analytical task.
```

---

# Slide 20 — Testing Strategy

## Testing

Testing is performed at both module and integration levels.

### Module Testing

```text
PII Protection
      ↓
Classification
      ↓
Indicator Extraction
      ↓
Correlation
```

Each module is tested independently.

### Integration Testing

```text
Input Complaint
      ↓
Complete Pipeline
      ↓
Dashboard Output
```

### Key Checks

* Correct file paths
* Valid JSON
* Correct data formats
* Model loading
* Correct classification output
* Correct indicator extraction
* Correct case relationships
* Dashboard displays actual generated data

---

# Slide 21 — Sample End-to-End Result

## Example Case

### Input

```text
A victim received a suspicious message
from an unknown number containing a
fraudulent login URL.
```

### Classification

```text
Category:
Phishing
```

### Extracted Indicators

```text
Phone:
XXXXXX4321

URL:
example-phishing.test
```

### Correlation

```text
Potentially related:

C004
Similarity: 0.87

C007
Similarity: 0.79
```

### Investigation Lead

```text
Priority:
High

Reason:
Shared indicators detected across complaints.
```

---

# Slide 22 — Current Progress

## Review 2 Progress

### Completed / In Progress

```text
✓ Dataset preparation
✓ PII protection
✓ NLP preprocessing
✓ Classification pipeline
✓ Indicator extraction
✓ Case correlation
✓ JSON data exchange
✓ Dashboard development
✓ System architecture
✓ Data-flow documentation
✓ Initial integration testing
```

### Remaining Work

```text
→ Final integration
→ End-to-end testing
→ UI refinement
→ Model evaluation
→ Error handling
→ Documentation
→ Final presentation/demo preparation
```

Update the checkmarks to match the team's actual status before presenting.

---

# Slide 23 — Evaluation Metrics

## Model Evaluation

The classification module should be evaluated using appropriate metrics.

### Metrics

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

### Example Format

```text
Accuracy:   XX.XX%
Precision:  XX.XX%
Recall:     XX.XX%
F1-score:   XX.XX%
```

**Important:** Replace `XX.XX%` with the actual values obtained from the trained model. Do not present assumed or fabricated metrics.

---

# Slide 24 — Advantages

## Advantages of CaseIntel

### Faster Analysis

Automates repetitive complaint-processing tasks.

### Structured Information

Converts unstructured complaint text into structured indicators.

### Cross-Case Analysis

Makes potentially related complaints easier to identify.

### Privacy Awareness

Reduces unnecessary exposure of sensitive information.

### Unified Dashboard

Combines multiple analytical outputs in one interface.

### Human-in-the-Loop

Provides leads rather than automatically making enforcement decisions.

---

# Slide 25 — Limitations

## Current Limitations

### Data Quality

Model performance depends on the quality and representativeness of the dataset.

### Classification Errors

Predictions may be incorrect for ambiguous complaints.

### Extraction Errors

Regular expressions and NLP methods may miss indicators or produce false positives.

### Correlation Does Not Equal Proof

Shared indicators or textual similarity do not prove that two cases originate from the same source.

### Prototype Scale

The current system is a prototype and may require additional engineering for large-scale production deployment.

---

# Slide 26 — Future Scope

## Future Enhancements

### 1. Advanced NLP

Use transformer-based language models for improved complaint understanding.

### 2. Improved Entity Recognition

Use dedicated NER models for extracting entities from unstructured complaints.

### 3. Graph-Based Correlation

Represent cases and indicators as a graph.

```text
Case ── Phone
 │        │
 │        │
URL ── Case
 │
UPI
```

### 4. Real-Time Processing

Process new complaints as they arrive.

### 5. Explainable AI

Provide reasons behind classification and correlation results.

### 6. Role-Based Access

Restrict sensitive information according to investigator roles.

### 7. Scalable Backend

Deploy the processing pipeline through an API and scalable backend architecture.

---

# Slide 27 — Responsible AI

## Responsible Use

CaseIntel is an AI-assisted decision-support system.

### Important Principle

```text
AI Output ≠ Final Decision
```

The system can provide:

```text
Prediction
+
Indicators
+
Similarity
+
Potential Relationships
```

But:

```text
Human Investigator
        ↓
Verification
        ↓
Final Decision
```

### Therefore

The system should not be used as the sole basis for determining guilt, identity, or enforcement action.

---

# Slide 28 — Demonstration Flow

## Live Demo

### Step 1

Open CaseIntel dashboard.

### Step 2

Select a sample case.

### Step 3

Display the predicted crime category.

### Step 4

Display extracted indicators.

### Step 5

Display potentially related cases.

### Step 6

Show similarity/correlation information.

### Step 7

Display investigation lead.

### Step 8

Explain how the result travelled through the pipeline.

```text
Complaint
   ↓
Privacy
   ↓
Classification
   ↓
Extraction
   ↓
Correlation
   ↓
Investigation Lead
   ↓
Dashboard
```

---

# Slide 29 — Team Contribution Summary

## Team Contribution

### Member 1

Data preparation and PII protection.

### Member 2

NLP classification and model development.

### Member 3

Indicator/entity extraction.

### Member 4

Case correlation and similarity analysis.

### Member 5

Dashboard development and system integration.

### Combined Result

```text
5 Modules
    ↓
1 Integrated Pipeline
    ↓
1 Investigator Dashboard
```

---

# Slide 30 — Conclusion

## Conclusion

CaseIntel demonstrates how AI, NLP, structured information extraction, and similarity analysis can be combined to assist with cybercrime complaint analysis.

The system provides:

* Automated complaint classification
* Privacy-aware data processing
* Indicator extraction
* Cross-case correlation
* Investigation leads
* Unified dashboard visualization

### Final Concept

> **CaseIntel helps investigators move from individual complaints toward structured, connected, and actionable analytical leads.**

---

# Slide 31 — References

## Technical References

### Python

https://docs.python.org/3/

### Pandas

https://pandas.pydata.org/docs/

### NumPy

https://numpy.org/doc/

### Scikit-learn

https://scikit-learn.org/stable/

### TF-IDF Vectorizer

https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

### Cosine Similarity

https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

### Joblib

https://joblib.readthedocs.io/

### Python Regular Expressions

https://docs.python.org/3/library/re.html

### MDN Web Docs

https://developer.mozilla.org/

### Git

https://git-scm.com/doc

### GitHub Documentation

https://docs.github.com/

---

# Slide 32 — Thank You

# Thank You

## Questions?

### CaseIntel

**AI-Assisted Cybercrime Complaint Analysis and Case Correlation System**

```text
Data
  +
AI
  +
Indicators
  +
Correlation
  +
Dashboard
  =
CaseIntel
```
