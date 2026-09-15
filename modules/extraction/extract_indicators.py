"""
CaseIntel — Module 3: Indicator Extraction (Extract)
Pulls structured "scammer indicators" (phone, UPI ID, bank account, URL,
IP address) out of complaint text and stores them as structured records.

IMPORTANT — architecture note: this module runs on the ORIGINAL complaint
text (before PII redaction), because these indicators are exactly what
investigators need to correlate cases and trace scammers. PII Protection
(Module 1) still runs separately to produce a redacted version for any
public-facing / cross-team display — the two modules serve different
purposes on the same input:
  - Module 1 output -> safe to show broadly (redacted)
  - Module 3 output -> restricted to investigators (structured indicators
    used internally for case linking)

Reuses the same regex patterns as Module 1 for consistency, but here we
KEEP the values instead of masking them.
"""
import csv
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "privacy"))
from pii_protection import detect_pii  # reuse detection, not redaction


def extract_indicators(complaint_id: str, text: str) -> dict:
    """Return structured indicator record for one complaint."""
    findings = detect_pii(text)  # same detector, but we KEEP values here
    indicators = {
        "complaint_id": complaint_id,
        "phones": [],
        "emails": [],
        "upi_ids": [],
        "bank_accounts": [],
        "ips": [],
        "urls": [],
    }
    type_map = {
        "PHONE": "phones",
        "EMAIL": "emails",
        "UPI_ID": "upi_ids",
        "BANK_ACCOUNT": "bank_accounts",
        "IP_ADDRESS": "ips",
        "URL": "urls",
    }
    for f in findings:
        key = type_map.get(f["type"])
        if key and f["value"] not in indicators[key]:
            indicators[key].append(f["value"])
    indicators["total_indicators"] = sum(
        len(v) for k, v in indicators.items() if isinstance(v, list)
    )
    return indicators


def process_all(dataset_path="../../data/combined_dataset.csv"):
    with open(dataset_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    all_indicators = []
    for row in rows:
        result = extract_indicators(row["id"], row["text"])
        all_indicators.append(result)
    return all_indicators


if __name__ == "__main__":
    print("=" * 70)
    print("CaseIntel — Module 3: Indicator Extraction — Demo")
    print("=" * 70)

    # Demo on a few individual complaints
    demo_texts = [
        ("D001", "I received a call from +91-8485793320 asking for OTP, then transferred Rs.25000 to pay266@paytm."),
        ("D002", "Clicked a phishing link http://fake-bank-login.xyz/verify and lost access to my account, IP 192.168.4.21 was seen in logs."),
    ]
    for cid, text in demo_texts:
        result = extract_indicators(cid, text)
        print(f"\nComplaint {cid}: {text}")
        print(f"  Extracted: {json.dumps(result, indent=2)}")

    # Batch process the full dataset
    all_results = process_all()
    with open("../../data/extracted_indicators.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    total = sum(r["total_indicators"] for r in all_results)
    with_indicators = sum(1 for r in all_results if r["total_indicators"] > 0)
    print(f"\n\nProcessed {len(all_results)} complaints.")
    print(f"Complaints with at least one indicator: {with_indicators}")
    print(f"Total indicators extracted: {total}")
    print("Saved -> data/extracted_indicators.json")
