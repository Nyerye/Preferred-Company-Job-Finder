
import json
import os
import tkinter as tk
from tkinter import messagebox, Listbox

# Set up the app directory
APP_DIR = "C:/MunicipalJobTracker"
os.makedirs(APP_DIR, exist_ok=True)
JOB_TITLES_FILE = os.path.join(APP_DIR, "job_titles.json")

# Load existing job titles or create a new list if the file doesn't exist
def load_job_titles():
    if os.path.exists(JOB_TITLES_FILE):
        with open(JOB_TITLES_FILE, "r") as file:
            return json.load(file)
    return []

# Save the job titles to a JSON file
def save_job_titles(titles):
    with open(JOB_TITLES_FILE, "w") as file:
        json.dump(titles, file, indent=4)

# Add a new job title to the list
def add_title():
    title = title_entry.get().strip()
    if title:
        if title not in job_titles:
            job_titles.append(title)
            save_job_titles(job_titles)
            update_listbox()
            title_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Duplicate", f"'{title}' is already in the list.")
    else:
        messagebox.showwarning("Empty Input", "Please enter a job title.")

# Remove the selected job title from the list
def remove_title():
    try:
        selected_index = listbox.curselection()[0]
        removed_title = job_titles.pop(selected_index)
        save_job_titles(job_titles)
        update_listbox()
        messagebox.showinfo("Removed", f"'{removed_title}' has been removed.")
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a job title to remove.")

# Update the listbox with current job titles
def update_listbox():
    listbox.delete(0, tk.END)
    for title in job_titles:
        listbox.insert(tk.END, title)

# Set up the main window
root = tk.Tk()
root.title("Job Titles Manager")
root.geometry("400x500")

title_label = tk.Label(root, text="Enter a Job Title:")
title_label.pack(pady=10)

title_entry = tk.Entry(root, width=40)
title_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Job Title", command=add_title)
add_button.pack(pady=5)

listbox = Listbox(root, width=50, height=15)
listbox.pack(pady=20)

remove_button = tk.Button(root, text="Remove Selected Title", command=remove_title)
remove_button.pack(pady=5)

# Load existing job titles on startup
job_titles = load_job_titles()
update_listbox()

root.mainloop()
