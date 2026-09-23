# 🛡️ CYBERGUARD — Desktop Cybersecurity Operations & Threat Analytics

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**CYBERGUARD** is a native, cross-platform desktop application designed to evaluate security threats, analyze digital artifacts, and foster cybersecurity awareness. Powered by **Python 3** and **PyQt6**, it combines real-time security auditing engines with interactive gamification and local data analytics in a sleek, dark-themed operations dashboard.

---

## 📸 Overview & Key Features

CYBERGUARD brings multiple defensive security analysis tools together under a single, unified desktop dashboard:

### 1. 📊 Security Operations & Threat Analytics Dashboard
* **Aggregated Threat Metrics:** Displays total logged scans, average health scores, and critical threat counts in real time.
* **Risk Distribution Charts:** Visualizes threat levels (*Low Risk*, *Medium Risk*, *High Risk*) using embedded data visualization components.
* **Scan History Audit Trail:** Automatically logs every security audit into a local, embedded SQLite database.

### 2. 🌐 Website & Domain Security Analyzer
* **SSL/HTTPS Auditing:** Checks domain connection protocols and flags non-encrypted HTTP configurations.
* **URL Structural Analysis:** Detects raw IP address routing, excessive subdomains, long URL paths ($>75$ characters), and suspicious phishing keywords.
* **Security Header Verification:** Evaluates HTTP security headers (e.g., CSP, HSTS, X-Frame-Options) to calculate a overall risk score ($0–100$).

### 3. 🎣 Phishing Email & Message Detector
* **NLP & Pattern Analysis:** Scans raw text, emails, or SMS bodies for psychological manipulation, financial fraud indicators, and credential harvesting patterns.
* **Threat Classification:** Highlights specific risk indicators and generates categorical safety assessments.

### 4. 🔐 Password Security & Entropy Analyzer
* **Mathematical Entropy Calculation:** Measures password randomness in bits ($E = L \cdot \log_2(R)$).
* **Brute-Force Time Estimation:** Simulates cracking times across CPU and GPU hardware clusters.
* **Dictionary Attack Defense:** Cross-references inputs against common dictionary terms and sequential keyboard patterns.

### 5. 📁 File Integrity & Cryptographic Fingerprint Inspector
* **Cryptographic Hashing:** Computes exact **SHA-256** and **MD5** digital signatures for file integrity verification.
* **Anomalous Extension Detection:** Uncovers double-extension masking (e.g., `document.pdf.exe`) and magic header byte mismatches.

### 6. 🎮 Cyber Quiz & Community Awareness Survey
* **Interactive Challenges:** Features scenario-based cybersecurity quizzes to test awareness of social engineering and cyber hygiene.
* **Demographic Benchmarking:** Collects community awareness metrics to benchmark scores across user demographics.

---

## 🏗️ System Architecture & Tech Stack

* **Frontend / GUI:** PyQt6 (Custom QSS Glassmorphic Dark Theme)
* **Backend Logic:** Python 3 (Native Regex, Math, and Hashlib Engine)
* **Database Layer:** SQLite3 (`cyberguard_desktop.db`)
* **Visualization:** PyQtGraph / Chart.js Data Visuals

```text
cyberguard/
│
├── main.py                      # Application Entry Point & PyQt6 Main Window
├── cyberguard_desktop.db        # Embedded SQLite Database (Auto-generated)
│
├── core/                        # Security Analysis Modules
│   ├── url_analyzer.py          # Domain & SSL Inspection Logic
│   ├── phishing_detector.py     # Social Engineering & NLP Parser
│   ├── password_entropy.py      # Entropy Calculations & Dictionary Checks
│   └── file_inspector.py        # SHA-256 Hashing & Magic Byte Verification
│
├── database/
│   └── db_manager.py            # SQLite Connection & Query Handlers
│
└── assets/                      # Icons, Stylesheets (.qss), and Images
