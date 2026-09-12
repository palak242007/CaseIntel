"""
CaseIntel — Module 2: AI Classification (Classify)
Trains a text classifier to label complaints by crime type, using the
combined real + synthetic dataset. TF-IDF + Logistic Regression is used
as a strong, fast, explainable baseline (Review-2 appropriate); a
transformer fine-tune is the natural "future work" upgrade for Review-3.

Per the architecture: this module receives REDACTED text from Module 1
(PII Protection) — never raw text — so it never trains on or predicts
using personal identifiers.
"""
import csv
import json
import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "privacy"))
from pii_protection import redact_text  # reuse Module 1 for redaction


def load_data(path="../../data/combined_dataset.csv"):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    texts, labels = [], []
    for r in rows:
        redacted, _ = redact_text(r["text"])  # PII protection BEFORE classification
        texts.append(redacted)
        labels.append(r["label"])
    return texts, labels


def train_and_evaluate():
    texts, labels = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words="english")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=0)

    print("=" * 70)
    print("CaseIntel — Module 2: Classification — Evaluation")
    print("=" * 70)
    print(f"\nTest set accuracy: {acc:.2%}\n")
    print(report)

    # Save model + vectorizer for reuse in the demo / API
    os.makedirs("../../data/models", exist_ok=True)
    joblib.dump(clf, "../../data/models/classifier.joblib")
    joblib.dump(vectorizer, "../../data/models/vectorizer.joblib")
    print("\nModel saved -> data/models/classifier.joblib")

    return clf, vectorizer


def classify_complaint(text: str, clf, vectorizer) -> dict:
    """Full module output for a single new complaint: redact -> classify."""
    redacted, pii_findings = redact_text(text)
    vec = vectorizer.transform([redacted])
    pred = clf.predict(vec)[0]
    proba = clf.predict_proba(vec)[0]
    classes = clf.classes_
    confidence = dict(zip(classes, proba))
    top_confidence = max(confidence.values())
    return {
        "redacted_text": redacted,
        "predicted_crime_type": pred,
        "confidence": round(top_confidence, 3),
        "all_scores": {k: round(v, 3) for k, v in confidence.items()},
        "pii_redacted_count": len(pii_findings),
    }


if __name__ == "__main__":
    clf, vectorizer = train_and_evaluate()

    print("\n" + "=" * 70)
    print("Demo: classifying 3 brand-new (unseen) complaint texts")
    print("=" * 70)
    demo_complaints = [
        "Someone called me from an unknown number pretending to be from my bank and asked for my OTP to update KYC, then Rs.40000 was debited.",
        "I clicked a suspicious link sent via SMS and my UPI account was compromised, lost Rs.15000.",
        "A stranger is threatening to leak my private photos unless I pay him through UPI immediately.",
    ]
    for text in demo_complaints:
        result = classify_complaint(text, clf, vectorizer)
        print(f"\nComplaint: {text}")
        print(f"  -> Predicted: {result['predicted_crime_type']} (confidence: {result['confidence']:.1%})")
        print(f"  -> PII redacted: {result['pii_redacted_count']} item(s)")
