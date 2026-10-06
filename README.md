<div align="center">

# 🛡️ CyberGuard 3.0 Pro
### Enterprise Threat Intelligence & Defensive Cyber Hygiene Suite

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Zero--Persistence-emerald.svg)](#-security--privacy-by-design)

An ultra-modern, dark-obsidian threat intelligence dashboard engineered for real-time URL inspection, NLP-driven social engineering analysis, cryptographic file verification, and security awareness analytics.

[🚀 Explore Core Features](#-core-modules-7-tab-dashboard) • [🛠️ Quickstart Guide](#-installation--quickstart) • [🏗️ Repository Architecture](#%EF%B8%8F-repository-architecture)

---

</div>

## 🌟 Key Highlights & Cyberpunk UI Design

* **⚡ Real-Time Telemetry & Radar FX:** Dynamic CSS keyframe animations, glowing radar pulses, glassmorphism cards, and interactive live status indicators.
* **🔒 Zero-Trust Privacy Architecture:** All raw passwords, analyzed email contents, and uploaded file streams are processed purely in-memory with zero persistence.
* **📊 Live Security Operations Center (SOC) Analytics:** Integrated with Altair interactive data visualizations for scan frequency, risk distribution, and historical threat logs.

---

## 📸 Core Modules (7-Tab Dashboard)

| Tab | Feature Module | Technical Highlights |
| :--- | :--- | :--- |
| **📊 01** | **Dashboard & Analytics** | Real-time threat feeds, Altair scan distribution charts, severity risk counters, and live database audit logs. |
| **🌐 02** | **Website Security** | Direct SSL/TLS certificate chain verification, DNS record inspection, HTTP security header audits (`HSTS`, `CSP`), and vulnerability tagging. |
| **🎣 03** | **Phishing Detector** | Natural language processing (NLP) and rule-based heuristic trigger engine for identifying social engineering attempts. |
| **🔑 04** | **Password Entropy** | Mathematical Shannon Entropy calculations, character space pool analysis, and multi-tier brute-force crack time estimations. |
| **📁 05** | **File Integrity Audit** | Direct stream SHA-256, SHA-1, and MD5 cryptographic hashing with magic byte verification and checksum comparisons. |
| **📈 06** | **Awareness Survey** | Interactive cyber hygiene questionnaire featuring aggregated demographic benchmark visualizations. |
| **🎮 07** | **Cyber Security Quiz** | Gamified 8-question knowledge assessment with real-time scoring badges, detailed remediation answers, and global leaderboard ranking. |

---

## 🛠️ Installation & Quickstart

### Prerequisites
* **Python 3.9+** installed on your system.
* `git` version control.

### 1. Local Setup
```bash
# Clone the repository
git clone [https://github.com/your-username/cyberguard.git](https://github.com/your-username/cyberguard.git)
cd cyberguard

# Create and activate virtual environment (Optional but recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install pure-Python dependencies
pip install -r requirements.txt

# Launch the Streamlit web app
streamlit run app.py
```
### Repository Architecture

 cyberguard/
├── .streamlit/
│   └── config.toml           # Streamlit theme and execution parameters
├── core/                     # Defensive analysis engines
│   ├── __init__.py
│   ├── url_analyzer.py       # Domain, SSL, DNS, and header verification
│   ├── phishing_detector.py # NLP heuristics and threat keyword parser
│   ├── password_analyzer.py # Entropy evaluation and cracking time estimates
│   └── file_integrity.py    # In-memory checksum computation and file-type analysis
├── database/                 # Persistence layer
│   ├── __init__.py
│   └── db_manager.py         # Thread-safe SQLite logging and benchmark metrics
├── app.py                    # Application orchestration and view routes
├── style.py                  # UI stylesheets and dashboard styling tokens
├── config.py                 # Application settings and threshold definitions
├── requirements.txt          # Python runtime dependencies
├── Procfile                  # Deployment configuration (e.g., PaaS)
└── README.md                 # Project documentation


###🔒 Security & Privacy by Design
[!IMPORTANT]
CyberGuard 3.0 Pro is architected around privacy-first defensive security standards:

🛑 Zero Password Persistence: Password inputs evaluated in the Password Entropy module are analyzed solely in transient memory. Raw password strings are never saved to disk, logged to SQLite, or transmitted externally.

🛡️ Streamlined In-Memory File Processing: Uploaded files for hash generation and magic byte inspection are read directly from RAM memory streams (io.BytesIO) and discarded immediately after inspection without touching the hosting file system.

🔑 Sanitized Audit Logging: Database logs store only anonymized execution metadata (e.g., timestamps, risk levels, domain names, hash checksums) to maintain a clean operational history.

Made with ❤️ for Cybersecurity Enthusiasts & Security Operations Centers.
