# 🛡️ CyberGuard 3.0 Pro — Enterprise Threat Intelligence Suite

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**CyberGuard 3.0 Pro** is a modern cybersecurity threat intelligence and cyber hygiene platform. It offers comprehensive defensive security tooling, real-time cryptographic verification, social engineering detection, and interactive educational workflows.

---

## 🚀 Live Web Dashboard Deployment (Streamlit)

### Running Locally
```bash
# Install pure-Python web dependencies
pip install -r requirements.txt

# Launch Streamlit web dashboard
streamlit run app.py
```

### Streamlit Community Cloud Configuration
* **Streamlit Cloud Entry Point / Main file path:** `app.py`
* **Python Version:** 3.9+

---

## 📸 Core Modules (7-Tab Dashboard)

1. **📊 Dashboard & Analytics:** Primary landing interface featuring high-level threat metrics, scan distribution charts (Altair), risk severity breakdown, and live audit logs.
2. **🌐 Website Security:** SSL/TLS certificate verification, DNS records inspection, HTTP security headers audit, and vulnerability checks.
3. **🎣 Phishing Detector:** Natural language and indicator-based social engineering detection with actionable guidance.
4. **🔑 Password Entropy:** Shannon entropy calculations, character pool analysis, and multi-tier brute-force crack time estimates (with zero persistence of raw passwords).
5. **📁 File Integrity:** In-memory SHA-256, SHA-1, and MD5 cryptographic hashing, magic byte verification, and checksum verification tool.
6. **📈 Awareness Survey:** Cyber awareness questionnaire with interactive demographic benchmark analytics.
7. **🎮 Cyber Security Quiz:** 8-question knowledge challenge with scoring badges, educational explanations, and global leaderboard.

---

## 🏗️ Repository Architecture

```text
cyberguard/
├── .streamlit/
│   └── config.toml              # Hardened Streamlit server & dark theme configuration
├── core/                        # Pure-Python Defensive Security Engines
│   ├── __init__.py
│   ├── url_analyzer.py          # Domain, SSL, DNS & Security Header Inspector
│   ├── phishing_detector.py     # Social Engineering & NLP Trigger Parser
│   ├── password_analyzer.py     # Mathematical Shannon Entropy & Cracking Simulator
│   └── file_integrity.py        # In-Memory SHA-256/SHA-1/MD5 & Magic Byte Checker
├── database/                    # SQLite Persistence Layer
│   ├── __init__.py
│   └── db_manager.py            # Thread-Safe Database Manager with Seeded Benchmarks
├── app.py                       # Single Entry Point for Streamlit Web Cloud
├── config.py                    # Unified Configuration & Design Tokens
├── requirements.txt             # Pinned Pure-Python Web Dependencies
├── Procfile                     # PaaS Process Definition
└── README.md
```

---

## 🔒 Security & Privacy by Design
* **Zero Credential Storage:** Raw passwords and full message bodies are processed ephemerally in-memory and never written to SQLite database logs.
* **In-Memory File Processing:** Uploaded files for integrity auditing are read directly from memory streams and never saved to the hosting filesystem.
