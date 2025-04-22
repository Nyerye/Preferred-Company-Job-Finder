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

def load_employers():
    if EMPLOYER_FILE.exists():
        with open(EMPLOYER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_employers(data):
    with open(EMPLOYER_FILE, "w") as f:
        json.dump(data, f, indent=2)

class JobTrackerApp:
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

    def refresh_employer_list(self):
        self.tree.delete(*self.tree.get_children())
        employers = load_employers()
        for name, url in employers.items():
            self.tree.insert("", END, values=(name, url))

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

def launch():
    root = ttk.Window(themename="flatly")
    app = JobTrackerApp(root)
    root.mainloop()
