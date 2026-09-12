"""
CaseIntel — Synthetic Cybercrime Complaint Dataset Generator
Generates realistic (but fake) cybercrime complaints modeled on
NCRP-style categories, with embedded PII and shared "scammer indicators"
so the correlation module has real clusters to find.
"""
import random
import csv
import json
from datetime import datetime, timedelta

random.seed(42)

FIRST_NAMES = ["Rohit","Priya","Ankit","Sneha","Vikram","Anjali","Rahul","Pooja",
               "Amit","Neha","Suresh","Kavita","Manoj","Divya","Arjun","Ritu",
               "Sanjay","Meera","Karan","Isha"]
LAST_NAMES = ["Sharma","Verma","Gupta","Singh","Yadav","Reddy","Nair","Iyer",
              "Patel","Joshi","Mehta","Kapoor","Chauhan","Malhotra","Rao"]
CITIES = ["Bhopal","Indore","Delhi","Mumbai","Pune","Bengaluru","Jaipur",
          "Lucknow","Nagpur","Ahmedabad"]

def rand_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def rand_phone():
    return f"+91-{random.randint(70000,99999)}{random.randint(10000,99999)}"

def rand_email(name):
    n = name.lower().replace(" ", ".")
    return f"{n}{random.randint(1,999)}@{random.choice(['gmail.com','yahoo.com','outlook.com'])}"

def rand_upi():
    return f"{random.choice(['scammer','fraud','pay','support'])}{random.randint(100,999)}@{random.choice(['ybl','okaxis','paytm','oksbi'])}"

def rand_bank_acc():
    return "".join(str(random.randint(0,9)) for _ in range(11))

def rand_ip():
    return ".".join(str(random.randint(1,255)) for _ in range(4))

def rand_url(domain_pool):
    return f"http://{random.choice(domain_pool)}.{random.choice(['xyz','info','shop','online'])}/verify"

def rand_date():
    start = datetime(2026,1,1)
    return (start + timedelta(days=random.randint(0,250))).strftime("%Y-%m-%d")

# --- Crime type templates -------------------------------------------------
# Each template is a "campaign": several complaints share the SAME indicator
# (phone/UPI/URL) so the correlation engine has real signal to detect.

CAMPAIGNS = [
    {
        "crime_type": "Financial Fraud", "sub_type": "KYC/Bank Impersonation",
        "phone": rand_phone(), "upi": rand_upi(), "bank": rand_bank_acc(),
        "domain_pool": ["kyc-verify-bank"],
        "templates": [
            "I received a call from {phone} claiming to be from my bank asking me to update my KYC. They asked for OTP and my account was debited.",
            "A person called from {phone} saying my bank account will be blocked unless I verify KYC. Transferred Rs.{amount} via UPI to {upi} on their instruction.",
            "Someone posing as a bank employee called from {phone}, asked for OTP for 'KYC update', money got deducted from my account.",
        ],
    },
    {
        "crime_type": "Phishing", "sub_type": "Fake Support Link",
        "phone": rand_phone(), "upi": rand_upi(), "bank": rand_bank_acc(),
        "domain_pool": ["fake-support-helpdesk"],
        "templates": [
            "I clicked a link {url} sent via SMS claiming to be customer support and entered my card details. Money was stolen.",
            "Received an email with link {url} asking to verify my account, after clicking I lost access and Rs.{amount} was withdrawn.",
            "A fake support website {url} asked for my login credentials, my wallet linked to {upi} was compromised.",
        ],
    },
    {
        "crime_type": "Identity Theft", "sub_type": "Social Media Impersonation",
        "phone": rand_phone(), "upi": rand_upi(), "bank": rand_bank_acc(),
        "domain_pool": ["profile-verify"],
        "templates": [
            "Someone created a fake profile using my photos and contacted my friends asking for money via {upi}.",
            "My identity was used to open a fraud account, contact number linked was {phone}.",
            "A cloned social media account impersonating me asked my relatives to send money to {upi}.",
        ],
    },
    {
        "crime_type": "Hacking", "sub_type": "Email/Account Compromise",
        "phone": rand_phone(), "upi": rand_upi(), "bank": rand_bank_acc(),
        "domain_pool": ["account-recovery"],
        "templates": [
            "My email account was hacked, attacker sent password reset link {url} to change my credentials.",
            "Unauthorized login detected from IP {ip}, my account was compromised and used for further scams.",
            "Received threat messages from hacked account, attacker demanded money to {upi} to restore access.",
        ],
    },
    {
        "crime_type": "Sextortion", "sub_type": "Blackmail via Video Call",
        "phone": rand_phone(), "upi": rand_upi(), "bank": rand_bank_acc(),
        "domain_pool": ["private-video-verify"],
        "templates": [
            "I received a video call from {phone} and was later blackmailed with a recorded video, asked to pay to {upi}.",
            "Unknown number {phone} is threatening to leak my private photos unless I pay Rs.{amount} to {upi}.",
            "Extortion attempt via WhatsApp from {phone}, demanding payment to bank account.",
        ],
    },
]

def generate_complaints(n=400):
    rows = []
    complaint_id = 1
    # Each campaign generates several *varied* complaints sharing indicators
    per_campaign = n // len(CAMPAIGNS)
    for camp in CAMPAIGNS:
        for _ in range(per_campaign):
            victim = rand_name()
            template = random.choice(camp["templates"])
            amount = random.choice([5000,10000,15000,25000,50000,75000,100000])
            url = rand_url(camp["domain_pool"])
            ip = rand_ip()
            text = template.format(
                phone=camp["phone"], upi=camp["upi"], amount=amount,
                url=url, ip=ip,
            )
            rows.append({
                "complaint_id": f"C{complaint_id:04d}",
                "date_filed": rand_date(),
                "city": random.choice(CITIES),
                "victim_name": victim,
                "victim_phone": rand_phone(),
                "victim_email": rand_email(victim),
                "complaint_text": text,
                "crime_type": camp["crime_type"],
                "sub_type": camp["sub_type"],
                "amount_lost": amount,
                # ground-truth indicators embedded in text, used to validate
                # the extraction + correlation modules
                "linked_phone": camp["phone"],
                "linked_upi": camp["upi"],
                "linked_bank_acc": camp["bank"],
                "linked_url": url if "{url}" in template else "",
                "linked_ip": ip if "{ip}" in template else "",
            })
            complaint_id += 1
    random.shuffle(rows)
    for i, r in enumerate(rows, start=1):
        r["complaint_id"] = f"C{i:04d}"
    return rows

if __name__ == "__main__":
    data = generate_complaints(400)
    fields = list(data[0].keys())
    with open("complaints_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    with open("complaints_dataset.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data)} synthetic complaints -> complaints_dataset.csv / .json")
    # quick sanity check: how many distinct correlation clusters exist
    campaigns_phones = set(r["linked_phone"] for r in data)
    print(f"Distinct scammer campaigns (ground-truth clusters): {len(campaigns_phones)}")
