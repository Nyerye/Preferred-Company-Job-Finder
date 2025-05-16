# FILE            : job_scraper.py
# PROJECT         : Preferred Job Finder
# PROGRAMMER      : Nicholas Reilly
# FIRST VERSION   : 2025-04-10
# DESCRIPTION     : This script scrapes job postings from various employers' websites based on specific job titles. 
#                   It uses BeautifulSoup for web scraping and regex for keyword matching. 
#                   The scraped jobs are stored in a JSON file in the user's AppData directory.

import os
import json
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from urllib.parse import urljoin


__all__ = ["scrape_jobs", "load_employer_urls"]

# Set the directory for persistent data
APP_DIR = Path(os.getenv("APPDATA")) / "MunicipalJobTracker"
APP_DIR.mkdir(parents=True, exist_ok=True)
EMPLOYER_FILE = APP_DIR / "employers.json"
JOB_TITLES_FILE = APP_DIR / "job_titles.json"

# FUNCTION NAME: load_job_titles
# DESCRIPTION: Loads job titles from a JSON file. If the file doesn't exist or is empty, it returns an empty list.
# INPUT: None
# OUTPUT: A list of job titles.
def load_job_titles():
    if JOB_TITLES_FILE.exists():
        with open(JOB_TITLES_FILE, "r") as file:
            titles = json.load(file)
            if titles:
                print(f"[INFO] Loaded {len(titles)} job titles.")
                return titles
            else:
                print("[WARNING] No job titles found in job_titles.json. Please add some using the Job Titles Manager.")
                return []
    else:
        print("[ERROR] job_titles.json not found. Please add job titles using the Job Titles Manager.")
        return []

# FUNCTION NAME: build_title_pattern
# DESCRIPTION: Builds a regex pattern from a list of job titles for case-insensitive matching.
# INPUT: A list of job titles.
# OUTPUT: A compiled regex pattern.
def build_title_pattern(titles):
    if titles:
        return re.compile(r'\b(?:' + '|'.join(map(re.escape, titles)) + r')\b', flags=re.IGNORECASE)
    else:
        return None

# FUNCTION NAME: load_employer_urls
# DESCRIPTION: Loads employer URLs from a JSON file. If the file doesn't exist, it returns an empty dictionary.
# INPUT: None
# OUTPUT: A dictionary of employer URLs.
def load_employer_urls() -> dict:
    if EMPLOYER_FILE.exists():
        with open(EMPLOYER_FILE, "r") as f:
            return json.load(f)
    else:
        print("[ERROR] employers.json not found. Please add employers.")
        return {}

# FUNCTION NAME: keyword_match
# DESCRIPTION: Checks if a given text matches any of the job titles using regex.
# INPUT: A string of text and a compiled regex pattern.
# OUTPUT: True if a match is found, False otherwise.
def keyword_match(text: str, pattern) -> bool:
    return bool(pattern.search(text))


# FUNCTION NAME: scrape_city
# DESCRIPTION: Scrapes job postings from a given city URL. It looks for links that match the job titles.
# INPUT: A city name, a URL to scrape, and a compiled regex pattern.
# OUTPUT: A list of dictionaries containing unique job titles and URLs.
def scrape_city(city: str, url: str, pattern) -> list:
    jobs = []
    seen_jobs = set()  # Track unique title-URL pairs to prevent duplicates
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            href = link.get("href", "")
            
            #Proper appending of the URL for both relative and absolute paths so they send correctly 
            full_url = urljoin(url, href)

            # Use a unique key to prevent duplicate entries
            unique_key = f"{city}|{text}|{full_url}"
            if keyword_match(text, pattern) and unique_key not in seen_jobs:
                seen_jobs.add(unique_key)
                jobs.append({
                    "city": city,
                    "title": text,
                    "url": full_url
                })
    except Exception as e:
        print(f"[ERROR] Could not scrape {city}: {e}")
    return jobs

# FUNCTION NAME: scrape_jobs
# DESCRIPTION: Main function to scrape jobs from all employers. It loads job titles, builds a regex pattern,
#              loads employer URLs, and scrapes each city
# INPUT: None
# OUTPUT: A list of dictionaries containing job titles and URLs.
def scrape_jobs() -> list:
    # Load job titles and build the search pattern
    job_titles = load_job_titles()
    if not job_titles:
        print("[ERROR] No job titles to search for. Exiting.")
        return []

    pattern = build_title_pattern(job_titles)

    # Load employer URLs
    employers = load_employer_urls()
    if not employers:
        print("[ERROR] No employers to scrape. Exiting.")
        return []

    # Scrape jobs for each employer
    all_jobs = []
    for city, url in employers.items():
        print(f"[INFO] Scraping {city}...")
        all_jobs.extend(scrape_city(city, url, pattern))

    print(f"[INFO] Found {len(all_jobs)} jobs.")
    return all_jobs

# Run the scraper if executed directly
if __name__ == "__main__":
    scrape_jobs()
