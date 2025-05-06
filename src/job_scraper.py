# FILE		    : job_scarper.py
# PROJECT	    : Preffered Job Finder
# PROGRAMMER	: Nicholas Reilly
# FIRST VERSION	: 2025-04-10
# DESCRIPTION	: This script scrapes job postings from various employers' websites based on specific job titles. It uses BeautifulSoup for web scraping and regex for keyword matching. The scraped jobs are stored in a JSON file in the user's AppData directory. The script also includes functions to load employer URLs and scrape jobs from them.

# Import the libraries required for web scraping and data handling.
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from pathlib import Path


__all__ = ["scrape_jobs", "load_employer_urls"]

# Actual path to data/employers.json for both development and exe
APP_DIR = Path(os.getenv("APPDATA")) / "MunicipalJobTracker"
APP_DIR.mkdir(parents=True, exist_ok=True)
EMPLOYER_FILE = APP_DIR / "employers.json"

# Job title keywords
job_titles = [
    "IT Support Specialist", "IT Support Technician", "Service Desk Analyst", "Help Desk Analyst",
    "Desktop Support Technician", "Technical Support Specialist", "End User Support Technician",
    "IT Operations Analyst", "Systems Analyst", "Business Systems Analyst", "IT Analyst",
    "Network Analyst", "Network Administrator", "Network Engineer", "Infrastructure Analyst",
    "Infrastructure Specialist", "System Administrator", "Linux Administrator", "Windows Administrator",
    "Cloud Administrator", "Cloud Engineer", "Cloud Solutions Architect", "Cybersecurity Analyst",
    "Security Analyst", "Information Security Analyst", "Security Engineer", "Security Administrator",
    "DevOps Engineer", "Site Reliability Engineer", "Software Developer", "Software Engineer",
    "Application Developer", "Web Developer", "Frontend Developer", "Backend Developer",
    "Full Stack Developer", "Embedded Systems Developer", "Database Administrator", "Data Analyst",
    "Data Engineer", "Data Scientist", "IT Project Manager", "IT Manager", "IT Coordinator",
    "IT Consultant", "Solutions Architect", "Enterprise Architect", "QA Analyst",
    "Test Automation Engineer", "Technical Business Analyst", "IT Compliance Analyst",
    "Technical Account Manager", "Field Support Technician", "IT Trainer", "IT Asset Manager",
    "IT Procurement Specialist", "Incident Response Analyst", "Vulnerability Analyst",
    "Penetration Tester", "SOC Analyst", "IT Auditor", "IT Generalist", "Integration Specialist",
    "CRM Developer", "ERP Analyst", "IT Systems Engineer", "IT Change Manager", "IT Release Manager",
    "Application Support Analyst", "IT Monitoring Specialist", "IT Governance Analyst", "Infrastructure Engineer"
]

# Precompiled regex
pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, job_titles)) + r')\b', flags=re.IGNORECASE)

#FUNCTION NAME: keyword_match
# DESCRIPTION: This function checks if the given text contains any of the specified job titles.
# PARAMETERS:
#   - text: A string containing the text to be checked.
# RETURNS: True if any job title is found in the text, False otherwise.
def keyword_match(text: str) -> bool:
    return bool(pattern.search(text))

# FUNCTION NAME: load_employer_urls
# DESCRIPTION: This function loads the employer URLs from the JSON file.
# PARAMETERS: None
# RETURNS: A dictionary of employers where the key is the employer name and the value is the job board URL.
def load_employer_urls() -> dict:
    if os.path.exists(EMPLOYER_FILE):
        with open(EMPLOYER_FILE, "r") as f:
            return json.load(f)
    return {}

# FUNCTION NAME: save_employer_urls
# DESCRIPTION: This function saves the employer URLs to the JSON file.
# PARAMETERS: data: A dictionary of employers where the key is the employer name and the value is the job board URL.
# RETURNS: None
def scrape_city(city: str, url: str) -> list:
    jobs = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            href = link.get("href", "")
            if keyword_match(text):
                full_url = href if href.startswith("http") else f"{url.rstrip('/')}/{href.lstrip('/')}"
                jobs.append({
                    "city": city,
                    "title": text,
                    "url": full_url
                })
    except Exception as e:
        print(f"[ERROR] Could not scrape {city}: {e}")
    return jobs

# FUNCTION NAME: scrape_jobs
# DESCRIPTION: This function scrapes job postings from the tracked employers.
# PARAMETERS: None
# RETURNS: A list of job postings, where each job is a dictionary containing 'city', 'title', and 'url'.
def scrape_jobs() -> list:
    all_jobs = []
    for city, url in load_employer_urls().items():
        print(f"Scraping {city}...")
        all_jobs.extend(scrape_city(city, url))
    return all_jobs
