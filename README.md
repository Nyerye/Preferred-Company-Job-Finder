# 🏙️ Municipality Job Tracker

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Made with ❤️ by Nicholas Reilly](https://img.shields.io/badge/made%20by-Nicholas%20Reilly-orange.svg)](https://github.com/yourusername)
[![Status](https://img.shields.io/badge/status-active-brightgreen)]()

A Python-based job monitoring tool that scrapes and filters **IT-related job postings** from municipality websites across Ontario, Canada. Designed to keep job seekers in the tech space informed — automatically.

---

## 🚀 Features

- ✅ Scrapes official municipal job boards from **14+ cities & regions**
- ✅ Filters jobs by **regex-matched IT titles** (e.g. Developer, Analyst, Admin, etc.)
- ✅ Sends **email alerts** when matches are found
- ✅ Saves matches to a **timestamped CSV** for offline tracking
- ✅ Built for easy extensibility (add more cities, filters, output formats)

---

## 📍 Municipalities Tracked

- City of Guelph
- City of Cambridge
- City of Kitchener
- City of Waterloo
- City of Toronto
- City of Mississauga
- Norfolk County
- City of Hamilton
- City of Brantford
- City of London
- Wellington County
- Region of Waterloo
- City of Burlington
- Halton Region

---

## 🛠️ Tech Stack

- **Python 3.11+**
- `requests`, `beautifulsoup4`, `lxml` – HTML scraping
- `yagmail`, `python-dotenv` – email automation via Gmail
- `csv`, `re`, `schedule` – filtering, storage & optional scheduling

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/municipality-job-tracker.git
cd municipality-job-tracker
python -m venv venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

---

## 🔐 Setup `.env`

Create a `.env` file in the project root:

```env
SENDER_EMAIL=your_gmail_here@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_email_or_same_as_sender
```

> ⚠️ Gmail accounts must use [App Passwords](https://myaccount.google.com/apppasswords) (2FA required).

---

## ▶️ Usage

Run the tracker manually:

```bash
python src/main.py
```

This will:
1. Scrape all job boards
2. Filter based on IT job titles
3. Save results to `data/jobs.csv`
4. Send matches via email

---

## ⏱️ Automation (Optional)

To run the script daily using Windows Task Scheduler or `cron`, simply point to `src/main.py` in a scheduled job.

---

## ✨ Sample Output

| Timestamp           | City              | Title                    | URL                            |
|---------------------|-------------------|--------------------------|--------------------------------|
| 2025-04-14 09:23:11 | City of Toronto   | Systems Analyst          | jobs.toronto.ca/...            |
| 2025-04-14 09:23:11 | City of Hamilton  | Service Desk Technician  | hamilton.ca/jobs/...           |

---

## 🤝 Contributing

I will NOT accept any changes to the code. You are more than welcome to take this and tweak it to your desires.

---

## 💼 About the Author

**Nicholas Reilly**  
Software Engineering Technology Student – Conestoga College  

