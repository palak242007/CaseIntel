# CaseIntel — References

This document contains the references, technologies, datasets, algorithms, and supporting resources used during the development of the CaseIntel project.

---

## 1. Project Overview

**CaseIntel** is an AI-assisted cybercrime complaint analysis and case-correlation system.

The project combines:

* Privacy/PII protection
* Natural Language Processing (NLP)
* Crime-category classification
* Indicator/entity extraction
* Similarity-based case correlation
* Investigation-lead generation
* Investigator-oriented dashboard visualization

The system is intended as a decision-support prototype. Its outputs should be treated as potential leads and should not be considered definitive evidence or proof of criminal activity.

---

# 2. Python

Python is the primary programming language used for the CaseIntel backend, data processing, machine-learning pipeline, indicator extraction, and integration components.

Official documentation:

* Python Documentation: https://docs.python.org/3/

Python is used for:

* Dataset processing
* Text preprocessing
* PII protection
* Machine-learning model training
* Feature extraction
* Indicator extraction
* Case similarity calculations
* JSON generation
* Backend integration

---

# 3. Pandas

Pandas is used for loading, cleaning, transforming, and analyzing structured complaint data.

Official documentation:

https://pandas.pydata.org/docs/

Typical uses in CaseIntel include:

* Reading CSV datasets
* Cleaning complaint records
* Selecting relevant columns
* Handling missing values
* Preparing training data
* Generating analysis outputs

Example:

```python
import pandas as pd

df = pd.read_csv("data/combined_dataset.csv")
```

---

# 4. NumPy

NumPy provides numerical and array-processing functionality used by the machine-learning and data-processing components.

Official documentation:

https://numpy.org/doc/

Typical uses include:

* Numerical calculations
* Array manipulation
* Feature processing
* Similarity calculations

---

# 5. Scikit-learn

Scikit-learn is used for machine-learning tasks such as text vectorization, classification, evaluation, and similarity analysis.

Official documentation:

https://scikit-learn.org/stable/

Relevant components include:

* `TfidfVectorizer`
* Classification algorithms
* Train/test splitting
* Accuracy and evaluation metrics
* Cosine similarity

Example:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(text_data)
```

---

# 6. TF-IDF

Term Frequency–Inverse Document Frequency (TF-IDF) is used to convert complaint text into numerical features that can be processed by machine-learning algorithms.

TF-IDF assigns higher importance to terms that are useful for distinguishing documents while reducing the importance of terms that occur frequently across many documents.

Scikit-learn implementation:

https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

In CaseIntel, TF-IDF can be used for:

```text
Complaint Text
      ↓
Text Preprocessing
      ↓
TF-IDF Vectorization
      ↓
Numerical Feature Matrix
      ↓
Classification / Similarity Analysis
```

---

# 7. Cosine Similarity

Cosine similarity is used to compare text or feature vectors and estimate how similar two complaint records are.

Scikit-learn documentation:

https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

The general formula is:

```text
cosine_similarity(A, B) =
(A · B) / (||A|| × ||B||)
```

A value closer to `1` indicates greater similarity between the vectors, while a value closer to `0` indicates lower similarity.

In CaseIntel, similarity can be used as one signal for identifying potentially related complaints.

---

# 8. Natural Language Processing

Natural Language Processing (NLP) techniques are used to process complaint descriptions and extract useful information.

The NLP pipeline may include:

```text
Raw Complaint
      ↓
Cleaning
      ↓
Normalization
      ↓
Tokenization / Vectorization
      ↓
Classification
      ↓
Indicator Extraction
```

NLP is used primarily for:

* Complaint classification
* Text representation
* Keyword/entity identification
* Similarity analysis

---

# 9. Regular Expressions

Python regular expressions (`re`) are used for rule-based identification of structured indicators within complaint text.

Python documentation:

https://docs.python.org/3/library/re.html

Potential indicator types include:

* Phone numbers
* Email addresses
* URLs
* UPI-style identifiers
* Other structured identifiers supported by the implementation

Example:

```python
import re

emails = re.findall(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    text
)
```

Regular expressions should be treated as extraction rules rather than definitive proof that an extracted value is malicious or belongs to a particular person.

---

# 10. Joblib

Joblib is used for saving and loading trained machine-learning models and vectorizers.

Official documentation:

https://joblib.readthedocs.io/

CaseIntel may store artifacts such as:

```text
classifier.joblib
vectorizer.joblib
```

Typical workflow:

```text
Training
   ↓
Trained Model
   ↓
joblib.dump()
   ↓
classifier.joblib
```

Then during prediction:

```text
classifier.joblib
       ↓
joblib.load()
       ↓
Prediction
```

---

# 11. JSON

JSON is used as a structured interchange format between processing modules and the dashboard.

Reference:

https://www.json.org/

Example CaseIntel outputs include:

```text
data/pii_protected_complaints.json
data/extracted_indicators.json
data/case_clusters.json
data/dashboard_data.json
```

The use of structured JSON allows different project components to exchange information without directly depending on each other's internal implementation

12. Data Privacy and PII Protection

Personally Identifiable Information (PII) should be protected before information is displayed in the dashboard or used where unnecessary.

Examples of potentially sensitive information include:

Phone numbers
Email addresses
Account numbers
Addresses
Government identifiers
Other information capable of identifying an individual

The CaseIntel prototype should use techniques such as:

Raw Data
   ↓
PII Detection
   ↓
Masking / Redaction
   ↓
Protected Data
   ↓
Analysis / Dashboard

Example:

Original:
9876543210

Dashboard:
XXXXXX3210

The exact masking strategy should follow the implementation used by the project.

13. Cybercrime Complaint Data

CaseIntel uses structured complaint information for demonstrating classification, indicator extraction, and correlation.

The project dataset should be stored under the project's data/ directory.

Example:

data/
├── combined_dataset.csv
├── pii_protected_complaints.json
├── extracted_indicators.json
├── case_clusters.json
└── dashboard_data.json

If an external dataset is used, its:

Dataset name
Provider
URL
License
Download date
Version

should be recorded here before final submission.

Important: Do not commit real complainant PII or confidential case information to the repository.

14. Machine Learning Classification

The classification module predicts a crime/category label from complaint text.

General workflow:

Complaint Text
      ↓
Preprocessing
      ↓
TF-IDF Vectorization
      ↓
Trained Classifier
      ↓
Predicted Category

Example output:

Input:
Suspicious message containing a fraudulent login URL

Predicted Category:
Phishing

The exact classification algorithm should match the model actually implemented by Member 2.

Possible algorithms include:

Logistic Regression
Linear Support Vector Machine
Naive Bayes
Random Forest

Only the algorithm actually used in the final implementation should be described as the project's final model.

15. Case Correlation

Case correlation compares complaints to identify potentially related cases.

Possible signals include:

Shared phone number
Shared email address
Shared URL
Shared UPI identifier
Similar complaint text
Similar crime category

General workflow:

Case A ─────┐
            ├── Indicator Matching ──┐
Case B ─────┘                        │
                                     ↓
                              Similarity Score
                                     ↓
                              Potential Relationship

The system should describe these results as potential relationships, not confirmed links.

16. Investigation Leads

Investigation leads are generated when the system identifies potentially useful relationships or patterns.

Example:

Case C001
   ↓
Shared phone number
   ↓
Case C004
   ↓
Potential relationship

A dashboard message may therefore state:

Potential relationship detected — manual investigation recommended.

The system does not independently establish criminal responsibility, identity, or guilt.

17. HTML

The CaseIntel dashboard uses HTML for the structure of the investigator-facing interface.

Reference:

https://developer.mozilla.org/en-US/docs/Web/HTML

Primary dashboard file:

frontend/dashboard.html

HTML is used to define:

Dashboard sections
Case information
Tables
Cards
Navigation
Forms
Result containers
18. CSS

CSS is used to control the visual presentation of the CaseIntel dashboard.

Reference:

https://developer.mozilla.org/en-US/docs/Web/CSS

CSS may be used for:

Layout
Colors
Typography
Cards
Tables
Responsive design
Status indicators
Dashboard styling
19. JavaScript

JavaScript is used to add client-side functionality to the dashboard.

Reference:

https://developer.mozilla.org/en-US/docs/Web/JavaScript

Possible uses include:

Loading JSON data
Searching cases
Filtering results
Updating dashboard cards
Displaying selected-case information
Rendering correlation results

Example flow:

dashboard_data.json
        ↓
JavaScript
        ↓
HTML Dashboard
20. SVG

Scalable Vector Graphics (SVG) are used for project architecture and data-flow diagrams.

Reference:

https://developer.mozilla.org/en-US/docs/Web/SVG

CaseIntel diagrams include:

frontend/caseintel_system_architecture.svg
frontend/caseintel_data_flow.svg

These diagrams communicate:

System components
Module relationships
Data flow
User interaction
21. Git

Git is used for source-code version control and collaborative development.

Official documentation:

https://git-scm.com/doc

The team can maintain separate branches for each member, for example:

main
member1-data-privacy
member2-classification
member3-indicators
member4-correlation
member5-dashboard-integration

Changes should be reviewed before merging into the main branch.

22. GitHub

GitHub is used to host the CaseIntel repository and coordinate team development.

Official documentation:

https://docs.github.com/

The repository contains the project source code, data-processing scripts, dashboard files, documentation, and other project artifacts.

Sensitive or confidential information should not be committed to the repository.

23. Suggested Project Structure
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

The exact structure should reflect the files actually present in the final repository.

24. Development and Testing References

The team should use the official documentation for the libraries used in the implementation.

Python

https://docs.python.org/3/

Pandas

https://pandas.pydata.org/docs/

NumPy

https://numpy.org/doc/

Scikit-learn

https://scikit-learn.org/stable/

Joblib

https://joblib.readthedocs.io/

MDN Web Docs

https://developer.mozilla.org/

Git

https://git-scm.com/doc

GitHub Documentation

https://docs.github.com/

25. Responsible Use

CaseIntel is an academic/prototype system intended to demonstrate how AI and data-processing techniques can assist with cybercrime complaint analysis.

The system:

Does not establish guilt.
Does not independently identify a criminal.
Does not replace investigators.
Does not guarantee that correlated cases are connected.
Does not guarantee that a classification is correct.
Should not expose unnecessary personal information.
Should not be used as the sole basis for enforcement action.

Similarity scores and extracted indicators should be interpreted as analytical signals requiring human verification.

26. Reference Management Notes

Before final submission, the team should update this document with the exact sources actually used.

For every external dataset, model, paper, API, or major technical resource, record:

Name:
Author / Organization:
URL:
Version:
License:
Access / Download Date:
How it was used:

This prevents the references file from claiming that the project used resources that were not actually used.

27. Final Reference Checklist

Before submitting the project, verify:

Every external dataset is documented.

Dataset license is documented.

Dataset source URL is documented.

ML libraries are documented.

Important algorithms are documented.

External APIs are documented if used.

Frontend technologies are documented.

Git/GitHub usage is documented.

No fake references are included.

No confidential case information is included.

No real PII is included unnecessarily.

URLs have been checked.

References match the actual final implementation.

28. Summary

CaseIntel combines established technologies for text processing, machine learning, structured information extraction, similarity analysis, privacy protection, and dashboard visualization.

The principal technical stack is:

Python
  ↓
Pandas / NumPy
  ↓
NLP + TF-IDF
  ↓
Scikit-learn Classification
  ↓
Indicator Extraction
  ↓
Similarity / Correlation
  ↓
JSON Data
  ↓
HTML + CSS + JavaScript
  ↓
CaseIntel Dashboard

The references in this document provide the technical foundation for understanding and reproducing the major components of the CaseIntel prototype.
