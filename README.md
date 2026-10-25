🚜 Loader Store - Management System
<img width="1084" height="650" alt="image" src="https://github.com/user-attachments/assets/e8fc82f7-a347-4f05-be32-3e3bb79412ce" />

A Comprehensive Inventory & Point of Sale (POS) System for Loader Spare Parts

📝 Overview

Loader Store is a lightweight, blazing-fast, and fully self-contained web-based management system tailored for heavy machinery and loader spare parts stores. Built with a clean architecture without relying on heavy external frameworks, it features a Python standard-library backend and a Vanilla JavaScript Single Page Application (SPA) frontend.

✨ Key Features

🔐 Security & Authentication

Role-Based Access Control (RBAC): Distinct privileges for "Managers" (Full Access) and "Employees" (Sales & Inventory only).

Secure Login/Registration: Passwords are encrypted using PBKDF2 hashing with unique salts.

Pending Approvals: New accounts remain in a 'pending' state until approved by an administrator.

📦 Inventory & Sales Management

Smart POS System: Quick invoice generation with automatic stock deduction and 14% tax calculation.

Low Stock Alerts: Automatic visual highlighting and dashboard alerts when items fall below their minimum threshold.

Dynamic Categories: Organize spare parts efficiently with real-time filtering.

🤖 Advanced AI Features

🎙️ Voice Assistant: Integrated smart assistant supporting Egyptian Arabic voice commands (e.g., "ضيف اتنين فلتر زيت", "خصم خمسين").

📷 Visual Image Search: Upload or capture a photo of a spare part to find its match in the database using built-in HOG and Color Histogram analysis.

💰 Financials & Reporting

Comprehensive Dashboards: Track sales, expenses, and purchases in real-time.

🕌 Zakat Calculator: Specialized module to calculate standard 2.5% Zakat based on live inventory valuation, cash, and active debts.

🏗️ Technology Stack

Backend: Python (Standard http.server), SQLite3, Hashlib (PBKDF2).

Frontend: HTML5, CSS3 (Custom variables, responsive design), Vanilla JavaScript (ES6+).

Architecture: RESTful API, Single Page Application (SPA).

🚀 Installation & Usage

Prerequisites

Python 3.8 or higher installed on your machine.

Running the Server

Clone the repository:

git clone https://github.com/Team-Loader-Store/Agile-project-.git
cd Agile-project-


Start the backend server:

python server.py


(Alternatively, run desktop.py to launch as a standalone desktop application).

Open your web browser and navigate to:

http://127.0.0.1:8000


📂 Project Structure

📦 Loader-Store
 ┣ 📂 static             # Frontend assets
 ┃ ┣ 📜 index.html       # The main Single Page Application (UI + Logic)
 ┃ ┗ 🖼️ logo.png         # System Logo
 ┣ 📂 data               # Database storage (created on first run)
 ┃ ┗ 🛢️ loader.db        # SQLite database
 ┣ 📜 server.py          # Python Backend API & Database Handlers
 ┣ 📜 desktop.py         # Script to run the app as a desktop window
 ┗ 📜 README.md          # Project documentation


🔄 Agile Development

This project was developed using Agile (Scrum) methodologies.

Task Tracking: Jira was used to track User Stories, Bugs, and Tasks (e.g., SCRUM-142, SCRUM-143, SCRUM-111).

Version Control: Managed via GitHub with structured Branching and Pull Request workflows.
