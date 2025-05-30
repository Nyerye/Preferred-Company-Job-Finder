# FILE		    : emailer.py
# PROJECT	    : Preffered Job Finder
# PROGRAMMER	: Nicholas Reilly
# FIRST VERSION	: 2025-04-10
# DESCRIPTION	: This script sends an email with job postings using the yagmail library.

# Import the libraries required for sending the email and laoding the env credentials.
import yagmail
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from %APPDATA%\MunicipalJobTracker
APPDATA_ENV_PATH = Path(os.getenv("APPDATA")) / "MunicipalJobTracker" / ".env"

# Check if the .env file exists and load it
if not APPDATA_ENV_PATH.exists():
    print(f"[ERROR] .env not found at: {APPDATA_ENV_PATH}")
else:
    load_dotenv(dotenv_path=APPDATA_ENV_PATH)
    print(f"[DEBUG] .env loaded from: {APPDATA_ENV_PATH}")

# Load environment variables into the script
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Show basic config status
print(f"[DEBUG] SENDER_EMAIL: {SENDER_EMAIL or '❌ MISSING'}")
print(f"[DEBUG] PASSWORD FOUND: {'✅' if SENDER_PASSWORD else '❌'}")
print(f"[DEBUG] RECIPIENT_EMAIL: {RECIPIENT_EMAIL or '❌ MISSING'}")

# FUNCTION NAME: send_email
# DESCRIPTION: This function sends an email with the first unique match for each job title.
# PARAMETERS:
#   - jobs: A list of job postings, where each job is a dictionary containing 'city', 'title', and 'url'.
# RETURNS: None
def send_email(jobs):
    if not (SENDER_EMAIL and SENDER_PASSWORD and RECIPIENT_EMAIL):
        print("[ERROR] Missing email config in .env")
        return

    if not jobs:
        print("[INFO] No jobs to send.")
        return

    # Create the email subject and body
    subject = "New IT Job Postings Found"
    body_lines = ["Here are the new job postings:<br><br>"]

    # Use a set to track unique titles and filter duplicates before counting
    unique_jobs = {}
    for job in jobs:
        title = job['title']
        if title not in unique_jobs:
            unique_jobs[title] = job  # Store the first occurrence only

    # Build the HTML email body from the unique job dictionary
    for job in unique_jobs.values():
        body_lines.append(
            f"{job['city']} - {job['title']}<br>"
            f"<a href='{job['url']}'>{job['url']}</a><br><br>"
        )

    # Wrap in HTML tags
    html_body = "<html><body>" + "".join(body_lines) + "</body></html>"

    # Try to send the email using yagmail. If it fails, send an error message.
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        yag.send(to=RECIPIENT_EMAIL, subject=subject, contents=html_body)
        print(f"✅ Email sent successfully. Jobs found will be sent to email.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
