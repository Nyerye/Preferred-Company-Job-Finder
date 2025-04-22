# src/emailer.py

import yagmail
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from %APPDATA%\MunicipalJobTracker
APPDATA_ENV_PATH = Path(os.getenv("APPDATA")) / "MunicipalJobTracker" / ".env"

if not APPDATA_ENV_PATH.exists():
    print(f"[ERROR] .env not found at: {APPDATA_ENV_PATH}")
else:
    load_dotenv(dotenv_path=APPDATA_ENV_PATH)
    print(f"[DEBUG] .env loaded from: {APPDATA_ENV_PATH}")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Show basic config status
print(f"[DEBUG] SENDER_EMAIL: {SENDER_EMAIL or '❌ MISSING'}")
print(f"[DEBUG] PASSWORD FOUND: {'✅' if SENDER_PASSWORD else '❌'}")
print(f"[DEBUG] RECIPIENT_EMAIL: {RECIPIENT_EMAIL or '❌ MISSING'}")

def send_email(jobs):
    if not (SENDER_EMAIL and SENDER_PASSWORD and RECIPIENT_EMAIL):
        print("[ERROR] Missing email config in .env")
        return

    if not jobs:
        print("[INFO] No jobs to send.")
        return

    subject = "New IT Job Postings Found"
    body_lines = ["Here are the new job postings:\n"]

    for job in jobs:
        body_lines.append(f"{job['city']} - {job['title']}\n{job['url']}\n")

    try:
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        yag.send(to=RECIPIENT_EMAIL, subject=subject, contents="\n".join(body_lines))
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
