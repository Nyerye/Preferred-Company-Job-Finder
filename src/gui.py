# FILE		    : gui.py
# PROJECT	    : Preffered Job Finder
# PROGRAMMER	: Nicholas Reilly
# FIRST VERSION	: 2025-04-10
# DESCRIPTION	: This script creates a GUI for tracking job postings from various employers. It allows users to add employers, scrape job postings, and send them via email. The GUI is built using the ttkbootstrap library for a modern look and feel.

# Import all the required modules and libraries.
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
import os
import sys
from pathlib import Path
import pandas as pd
from job_scraper import scrape_jobs
from emailer import send_email

# Use persistent location in user's AppData
APP_DIR = Path(os.getenv("APPDATA")) / "MunicipalJobTracker"
APP_DIR.mkdir(parents=True, exist_ok=True)
EMPLOYER_FILE = APP_DIR / "employers.json"
JOBS_FILE = APP_DIR / "jobs.csv"

# Fallback to bundled file (read-only)
def resource_path(relative_path: str) -> Path:
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return Path(base_path) / relative_path

# Copy default data from bundled folder if not already present
if not EMPLOYER_FILE.exists():
    default_employer = resource_path("data/employers.json")
    if default_employer.exists():
        with open(default_employer, "r") as src, open(EMPLOYER_FILE, "w") as dst:
            dst.write(src.read())

# FUNCTION NAME: load_employers
# DESCRIPTION: This function loads the employers from the JSON file.
# PARAMETERS: None
# RETURNS: A dictionary of employers where the key is the employer name and the value is the job board URL.
def load_employers():
    if EMPLOYER_FILE.exists():
        with open(EMPLOYER_FILE, "r") as f:
            return json.load(f)
    return {}

# FUNCTION NAME: save_employers
# DESCRIPTION: This function saves the employers to the JSON file.
# PARAMETERS: data: A dictionary of employers where the key is the employer name and the value is the job board URL.
# RETURNS: None
def save_employers(data):
    with open(EMPLOYER_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Class: JobTrackerApp
# DESCRIPTION: This class creates the GUI for the job tracker application. It allows users to add employers, view tracked employers, and run the job scraper and email functionality.
# METHODS:
#   - __init__: Initializes the GUI components and layout.
#   - refresh_employer_list: Refreshes the list of tracked employers in the GUI.
#   - add_employer: Adds a new employer to the tracked list and updates the GUI.
#   - run_scraper_and_email: Runs the job scraper and sends an email with the job postings.
#   - launch: Launches the GUI application.
#   - resource_path: Returns the absolute path to a resource file, handling both bundled and non-bundled cases.
#   - load_employers: Loads the employers from the JSON file.
#   - save_employers: Saves the employers to the JSON file.
#   - scrape_jobs: Scrapes job postings from the tracked employers.
#   - send_email: Sends an email with the job postings using the yagmail library.

class JobTrackerApp:

    # FUNCTION NAME: __init__
    # DESCRIPTION: This function initializes the GUI components and layout.
    # PARAMETERS: root: The root window of the application.
    # RETURNS: None
    def __init__(self, root):
        self.root = root
        self.root.title("🌇️ Municipality Job Tracker")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        self.style = ttk.Style("flatly")

        self.employer_frame = ttk.Labelframe(root, text="Tracked Employers", padding=10)
        self.employer_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.employer_frame, columns=("Name", "URL"), show="headings", height=12)
        self.tree.heading("Name", text="Employer Name")
        self.tree.heading("URL", text="Job Board URL")
        self.tree.column("Name", width=200)
        self.tree.column("URL", width=600)
        self.tree.pack(fill=BOTH, expand=True)

        self.add_frame = ttk.Labelframe(root, text="➕ Add New Employer", padding=10)
        self.add_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(self.add_frame, text="Employer Name").grid(row=0, column=0, sticky=W, padx=5)
        self.name_entry = ttk.Entry(self.add_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.add_frame, text="Job Board URL").grid(row=0, column=2, sticky=W, padx=5)
        self.url_entry = ttk.Entry(self.add_frame, width=50)
        self.url_entry.grid(row=0, column=3, padx=5)

        self.add_button = ttk.Button(self.add_frame, text="Add Employer", command=self.add_employer, bootstyle=SUCCESS)
        self.add_button.grid(row=1, column=0, columnspan=5, pady=(10, 0))

        self.scrape_button = ttk.Button(root, text="🔍 Run Scraper + Email", command=self.run_scraper_and_email, bootstyle=PRIMARY)
        self.scrape_button.pack(pady=10)

        self.refresh_employer_list()

    # FUNCTION NAME: refresh_employer_list
    # DESCRIPTION: This function refreshes the list of tracked employers in the GUI.
    # PARAMETERS: None
    # RETURNS: None
    def refresh_employer_list(self):
        self.tree.delete(*self.tree.get_children())
        employers = load_employers()
        for name, url in employers.items():
            self.tree.insert("", END, values=(name, url))

    # FUNCTION NAME: add_employer
    # DESCRIPTION: This function adds a new employer to the tracked list and updates the GUI.
    # PARAMETERS: None
    # RETURNS: None
    def add_employer(self):
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        if not name or not url:
            messagebox.showwarning("Missing Info", "Both name and URL are required.")
            return
        employers = load_employers()
        if name in employers:
            messagebox.showerror("Duplicate", "This employer already exists.")
            return
        employers[name] = url
        save_employers(employers)
        self.name_entry.delete(0, END)
        self.url_entry.delete(0, END)
        self.refresh_employer_list()
        messagebox.showinfo("Added", f"{name} was added to tracking.")

    # FUNCTION NAME: run_scraper_and_email
    # DESCRIPTION: This function runs the job scraper and sends an email with the job postings.
    # PARAMETERS: None
    # RETURNS: None
    def run_scraper_and_email(self):
        self.scrape_button.config(text="Running...", state=DISABLED)
        self.root.update()

        jobs = scrape_jobs()
        if jobs:
            df = pd.DataFrame(jobs)
            df.to_csv(JOBS_FILE, index=False)
            try:
                send_email(jobs)
                messagebox.showinfo("Success", f"{len(jobs)} jobs found and emailed successfully.")
            except Exception as e:
                messagebox.showerror("Email Error", f"Jobs saved but failed to send email:\n{e}")
        else:
            messagebox.showinfo("No Matches", "No matching jobs found.")

        self.scrape_button.config(text="🔍 Run Scraper + Email", state=NORMAL)

# FUNCTION NAME: launch
# DESCRIPTION: This function launches the GUI application.
# PARAMETERS: None
# RETURNS: None
def launch():
    root = ttk.Window(themename="flatly")
    app = JobTrackerApp(root)
    root.mainloop()
