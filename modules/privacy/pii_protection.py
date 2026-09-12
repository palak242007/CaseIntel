"""
CaseIntel — Module 1: PII Protection (Detect + Mask)
Detects and redacts personally identifiable information from raw
complaint text BEFORE it moves downstream to classification/extraction,
per the Review-1 architecture (Complaint -> PII Protection -> AI/NLP layer).

Uses regex patterns for structured PII (phone, email, bank account, UPI,
IP) which is fast, explainable, and demo-friendly. Can be upgraded to
spaCy NER for unstructured PII (names, addresses) as a stretch goal.
"""
import re
import json

PII_PATTERNS = {
    "PHONE": re.compile(r"(?:\+?91[-\s]?)?[6-9]\d{9}\b|\+91-\d{5}\d{5}"),
    "EMAIL": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "UPI_ID": re.compile(r"\b[\w.\-]{2,}@(?:ybl|okaxis|paytm|oksbi|okhdfcbank|ibl)\b"),
    "BANK_ACCOUNT": re.compile(r"\b\d{9,18}\b"),
    "IP_ADDRESS": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "URL": re.compile(r"https?://[^\s]+"),
}

# Order matters: check more specific patterns (UPI, email, url) before
# generic ones (bank account is just digits, would over-match otherwise)
PATTERN_ORDER = ["URL", "EMAIL", "UPI_ID", "PHONE", "IP_ADDRESS", "BANK_ACCOUNT"]


def detect_pii(text: str) -> list[dict]:
    """Return list of {type, value, start, end} for every PII match found."""
    found = []
    masked_spans = []  # track already-claimed character ranges

    def overlaps(start, end):
        return any(not (end <= s or start >= e) for s, e in masked_spans)

    for pii_type in PATTERN_ORDER:
        pattern = PII_PATTERNS[pii_type]
        for m in pattern.finditer(text):
            if overlaps(m.start(), m.end()):
                continue
            found.append({
                "type": pii_type,
                "value": m.group(),
                "start": m.start(),
                "end": m.end(),
            })
            masked_spans.append((m.start(), m.end()))
    found.sort(key=lambda x: x["start"])
    return found


def redact_text(text: str) -> tuple[str, list[dict]]:
    """Replace each detected PII span with a [TYPE_REDACTED] tag.
    Returns (redacted_text, list_of_findings)."""
    findings = detect_pii(text)
    redacted = text
    # Replace from the end of the string backwards so earlier offsets
    # stay valid as we edit.
    for f in sorted(findings, key=lambda x: x["start"], reverse=True):
        tag = f"[{f['type']}_REDACTED]"
        redacted = redacted[: f["start"]] + tag + redacted[f["end"] :]
    return redacted, findings


def process_complaint(complaint_text: str) -> dict:
    """Full module output: redacted text + structured PII inventory,
    matching the 'Detect + mask' box in the architecture diagram."""
    redacted, findings = redact_text(complaint_text)
    return {
        "original_text": complaint_text,
        "redacted_text": redacted,
        "pii_found": findings,
        "pii_count": len(findings),
    }


if __name__ == "__main__":
    # Demo against a few complaints from the generated dataset
    import csv

    with open("data/complaints_dataset.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print("=" * 70)
    print("CaseIntel — Module 1: PII Protection — Demo on 3 sample complaints")
    print("=" * 70)
    for row in rows[:3]:
        result = process_complaint(row["complaint_text"])
        print(f"\nComplaint {row['complaint_id']}:")
        print(f"  ORIGINAL : {result['original_text']}")
        print(f"  REDACTED : {result['redacted_text']}")
        print(f"  PII FOUND: {[(p['type'], p['value']) for p in result['pii_found']]}")

    # Batch-process the whole dataset and save output for the next module
    all_results = []
    for row in rows:
        result = process_complaint(row["complaint_text"])
        all_results.append({"complaint_id": row["complaint_id"], **result})

    with open("data/complaints_dataset.csv", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    total_pii = sum(r["pii_count"] for r in all_results)
    print(f"\n\nProcessed {len(all_results)} complaints, found {total_pii} PII instances total.")
    print("Output saved to data/pii_protected_complaints.json")
