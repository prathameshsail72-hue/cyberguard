import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cyberguard.db"

# App Metadata
APP_NAME = "CyberGuard 3.0 Pro"
APP_VERSION = "v3.0.0"
ORGANIZATION_NAME = "CEP Group 5 - Cyber Security Initiative"
TEAM_LEADER = "Prathamesh Sail"
GROUP_NAME = "CEP Group 5"

# Theme Color Palette - CyberGuard 3.0 Obsidian Glassmorphism
COLOR_BG_DARK = "#0b1120"
COLOR_CARD_BG = "#1e293b"
COLOR_CARD_HOVER = "#334155"
COLOR_BORDER = "rgba(255, 255, 255, 0.08)"
COLOR_TEXT_PRIMARY = "#f8fafc"
COLOR_TEXT_MUTED = "#94a3b8"

# Accent Colors
COLOR_ACCENT_CYAN = "#38bdf8"
COLOR_ACCENT_BLUE = "#60a5fa"
COLOR_ACCENT_PURPLE = "#818cf8"

# Risk Colors
COLOR_RISK_HIGH = "#ef4444"
COLOR_RISK_MEDIUM = "#f59e0b"
COLOR_RISK_LOW = "#10b981"

# Phishing Risk Keywords
PHISHING_KEYWORDS = [
    "urgent", "immediately", "account suspended", "verify your account", "update billing",
    "unauthorized login", "password reset", "claim prize", "wire transfer", "bank alert",
    "social security", "tax refund", "limited time", "security breach", "action required",
    "log in now", "confirm password", "verify pin", "gift card", "crypto deposit",
    "suspended access", "payment declined", "click here immediately", "irs notification"
]

# Suspicious URL Keywords
SUSPICIOUS_URL_KEYWORDS = [
    "login", "verify", "update", "banking", "secure", "account", "paypal", "free",
    "signin", "webscr", "ebayisapi", "authorization", "credential", "security-update",
    "wallet", "crypto", "blockchain", "airdrop", "bonus", "claim"
]
