
# FILE            : gui.py
# PROJECT         : Preferred Job Finder
# PROGRAMMER      : Nicholas Reilly
# FIRST VERSION   : 2025-04-10
# DESCRIPTION     : This script creates a GUI for tracking job postings from various employers. 
#                   It allows users to add employers, scrape job postings, and manage job titles.

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Listbox
import json
import os
import sys
from pathlib import Path
import pandas as pd
from job_scraper import scrape_jobs
from emailer import send_email

APP_DIR = Path(os.getenv("APPDATA")) / "MunicipalJobTracker"
APP_DIR.mkdir(parents=True, exist_ok=True)
EMPLOYER_FILE = APP_DIR / "employers.json"
JOBS_FILE = APP_DIR / "jobs.csv"
JOB_TITLES_FILE = APP_DIR / "job_titles.json"

def load_job_titles():
    if JOB_TITLES_FILE.exists():
        with open(JOB_TITLES_FILE, "r") as file:
            return json.load(file)
    return []

def save_job_titles(titles):
    with open(JOB_TITLES_FILE, "w") as file:
        json.dump(titles, file, indent=4)

def load_employers():
    if EMPLOYER_FILE.exists():
        with open(EMPLOYER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_employers(employers):
    with open(EMPLOYER_FILE, "w") as file:
        json.dump(employers, file, indent=4)

class JobTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("🌇️ Preferred Job Tracker")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.style = ttk.Style("flatly")

        self.employer_frame = ttk.Labelframe(root, text="Tracked Employers", padding=10)
        self.employer_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.employer_frame, columns=("Name", "URL"), show="headings", height=10)
        self.tree.heading("Name", text="Employer Name")
        self.tree.heading("URL", text="Job Board URL")
        self.tree.column("Name", width=300)
        self.tree.column("URL", width=800)
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

        self.remove_employer_button = ttk.Button(
            self.employer_frame, 
            text="Remove Selected Employer", 
            command=self.remove_employer, 
            bootstyle=DANGER
        )
        self.remove_employer_button.pack(pady=5)

        self.title_frame = ttk.Labelframe(root, text="🔍 Manage Job Titles", padding=10)
        self.title_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        ttk.Label(self.title_frame, text="Enter Job Title").grid(row=0, column=0, sticky=W, padx=5)
        self.title_entry = ttk.Entry(self.title_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        self.add_title_button = ttk.Button(
            self.title_frame, 
            text="Add Job Title", 
            command=self.add_job_title, 
            bootstyle=SUCCESS
        )
        self.add_title_button.grid(row=0, column=2, padx=5)

        self.remove_title_button = ttk.Button(
            self.title_frame, 
            text="Remove Selected", 
            command=self.remove_job_title, 
            bootstyle=DANGER
        )
        self.remove_title_button.grid(row=0, column=3, padx=5)

        self.title_listbox = Listbox(self.title_frame, width=70, height=10)
        self.title_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=10)

        self.refresh_job_title_list()

        self.scrape_button = ttk.Button(
            root, 
            text="🔍 Run Scraper + Email", 
            command=self.run_scraper_and_email, 
            bootstyle=PRIMARY
        )
        self.scrape_button.pack(pady=10)

        self.refresh_employer_list()

    def run_scraper_and_email(self):
        self.scrape_button.config(text="Running...", state=DISABLED)
        self.root.update()

        all_jobs = scrape_jobs()

        if all_jobs:
            df = pd.DataFrame(all_jobs)
            df.to_csv(JOBS_FILE, index=False)
            try:
                send_email(all_jobs)
                messagebox.showinfo("Success", f"{len(all_jobs)} total jobs found and emailed successfully.")
            except Exception as e:
                messagebox.showerror("Email Error", f"Jobs saved but failed to send email:\n{e}")
        else:
            messagebox.showinfo("No Matches", "No matching jobs found.")

        self.scrape_button.config(text="🔍 Run Scraper + Email", state=NORMAL)

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

    def refresh_job_title_list(self):
        self.title_listbox.delete(0, END)
        for title in load_job_titles():
            self.title_listbox.insert(END, title)

    def add_job_title(self):
        title = self.title_entry.get().strip()
        if title:
            titles = load_job_titles()
            if title not in titles:
                titles.append(title)
                save_job_titles(titles)
                self.refresh_job_title_list()
                self.title_entry.delete(0, END)
                messagebox.showinfo("Added", f"'{title}' was added to job titles.")
            else:
                messagebox.showinfo("Duplicate", f"'{title}' is already in the list.")
        else:
            messagebox.showwarning("Empty Input", "Please enter a job title.")

    def remove_job_title(self):
        try:
            selected_index = self.title_listbox.curselection()[0]
            titles = load_job_titles()
            removed_title = titles.pop(selected_index)
            save_job_titles(titles)
            self.refresh_job_title_list()
            messagebox.showinfo("Removed", f"'{removed_title}' was removed from job titles.")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a job title to remove.")

    def remove_employer(self):
        try:
            selected_item = self.tree.selection()[0]
            name, url = self.tree.item(selected_item, "values")
            employers = load_employers()
            if name in employers:
                del employers[name]
                save_employers(employers)
                self.refresh_employer_list()
                messagebox.showinfo("Removed", f"'{name}' has been removed from the tracked employers.")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select an employer to remove.")

def launch():
    root = ttk.Window(themename="flatly")
    app = JobTrackerApp(root)
    root.mainloop()
