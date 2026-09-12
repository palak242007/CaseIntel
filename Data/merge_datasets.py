"""
CaseIntel — Merge Real + Synthetic Data
Combines:
  1) Synthetic cybercrime complaints (complaints_dataset.csv) — full narrative
     complaints with embedded correlation indicators (phone/UPI/bank), used
     for classification, correlation, and PII testing.
  2) Real India SMS fraud/spam dataset (real_india_sms_raw.csv) — genuine
     scam message text (KYC/OTP/loan/job scams, RBI/UIDAI advisories) used
     to ground the classifier's "fraud signal" patterns in real language,
     not just synthetic phrasing.

Output: combined_dataset.csv with a `source` column so you can always show
your reviewer exactly which rows are real vs synthetic (this is the
transparency point that satisfies "bring more datasets" without pretending
everything is real).
"""
import csv

def load_synthetic(path="complaints_dataset.csv"):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append({
            "id": r["complaint_id"],
            "text": r["complaint_text"],
            "label": r["crime_type"],
            "sub_label": r["sub_type"],
            "source": "synthetic",
        })
    return out

def load_real_sms(path="real_india_sms_raw.csv"):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    n = 0
    for r in rows:
        if r["Label"].strip().lower() != "spam":
            continue  # only keep real fraud/spam text as positive fraud signal
        n += 1
        text = r["Msg"]
        # light heuristic sub-labeling from real message content, so it's
        # usable for classifier training rather than one giant "spam" bucket
        low = text.lower()
        if "otp" in low or "aadhaar" in low or "kyc" in low or "biometric" in low:
            label, sub = "Financial Fraud", "KYC/OTP/Aadhaar Scam"
        elif "job" in low or "earn" in low or "recruit" in low or "part-time" in low or "part time" in low:
            label, sub = "Employment Scam", "Fake Job Offer"
        elif "loan" in low or "credit card" in low or "cashback" in low:
            label, sub = "Financial Fraud", "Loan/Credit Card Scam"
        elif "click" in low or "http" in low or "bit.ly" in low:
            label, sub = "Phishing", "Malicious Link"
        else:
            label, sub = "Phishing", "General Scam Message"
        out.append({
            "id": f"R{n:04d}",
            "text": text,
            "label": label,
            "sub_label": sub,
            "source": "real",
        })
    return out

if __name__ == "__main__":
    synthetic = load_synthetic()
    real = load_real_sms()
    combined = synthetic + real

    fields = ["id", "text", "label", "sub_label", "source"]
    with open("combined_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(combined)

    print(f"Synthetic complaints : {len(synthetic)}")
    print(f"Real SMS fraud msgs  : {len(real)}")
    print(f"Combined total       : {len(combined)}")
    print("\nLabel distribution:")
    from collections import Counter
    counts = Counter(r["label"] for r in combined)
    for label, c in counts.most_common():
        print(f"  {label:20s} {c}")
    print("\nSaved -> combined_dataset.csv")
