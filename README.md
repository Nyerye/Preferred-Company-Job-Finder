# 🏙️ Municipality Job Tracker

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Made with ❤️ by Nicholas Reilly](https://img.shields.io/badge/made%20by-Nicholas%20Reilly-orange.svg)](https://github.com/yourusername)
[![Status](https://img.shields.io/badge/status-active-brightgreen)]()

# Preferred Company Job Finder

### 🌟 Overview
The **Preferred Company Job Finder** is a Python-based desktop application designed to streamline job tracking from multiple employers. It features a modern graphical user interface (GUI) and automated email notifications for new job postings.

---

### ⚙️ Technologies Used
- **Python 3.11**: Core scripting language
- **ttkbootstrap**: Modern GUI styling
- **tkinter**: GUI framework
- **Pandas**: Data processing and export
- **BeautifulSoup**: Web scraping
- **Requests**: HTTP requests for web content
- **PyInstaller**: Packaging the application into an executable
- **Inno Setup**: Creating the Windows installer

---

### 📝 Features
- Add and manage tracked employers and job titles
- Automated email notifications for new job postings
- Modern GUI with ttkbootstrap styling
- Persistent data storage in **AppData**
- Professional Windows installer with desktop and start menu shortcuts

---

### 🚀 Installation Guide

1. **Download the Installer:**
   - Visit the [GitHub Releases page](https://github.com/Nyerye/Preferred-Company-Job-Finder/releases/tag/v2.1.9).
   - Extract the contents of the downloaded archive.

2. **Run the Installer:**
   - Run the `PreferredCompanyJobFinderInstaller.exe` and **accept all defaults**.

---

### 📧 Setting Up Email Notifications

Since the application uses Gmail to send notifications, follow these steps to configure your email:

1. **Create a Gmail Account:**
   - If you don’t want to use your personal email, create a dedicated Gmail account for this application.
   - You can set up mail forwarding to your preferred email.

2. **Enable App Passwords:**
   - Visit [Google App Passwords](https://myaccount.google.com/apppasswords).
   - Generate an **app password** for "Mail" on "Windows".
   - Copy the 16-character password (no spaces or dashes).

3. **Configure the `.env` File:**
   - Press **`Win + R`** to open the Run dialog.
   - Enter **`%APPDATA%\MunicipalJobTracker`** and press **Enter**.
   - Create a new file named **`.env`** with the following content:
     ```plaintext
     SENDER_EMAIL=your_gmail_address_here
     SENDER_PASSWORD=your_16_character_app_password_here
     RECIPIENT_EMAIL=your_gmail_address_here
     ```
   - **Important:** Make sure the file has no `.txt` extension and is named exactly **`.env`**.

4. **Launch the Application:**
   - Use the desktop shortcut or start menu entry to open the application.
   - Enjoy automated job tracking and notifications!

---

### 🛠️ Troubleshooting

- **App Not Launching:** Make sure all required files are present in the installation directory.
- **Emails Not Sending:** Double-check your **`.env`** file for typos and ensure **App Passwords** are enabled in your Gmail settings.
- **Updating the App:** Simply run the latest installer to update to the newest version.

---

### 📬 Feedback and Issues

If you encounter any bugs or have feature requests, please create an **Issue** in the [GitHub repository](https://github.com/Nyerye/Preferred-Company-Job-Finder/issues).

---

### 📃 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.


## 💼 About the Author

**Nicholas Reilly**  
Software Engineering Technology Student – Conestoga College  

