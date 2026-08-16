import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cyberguard_desktop.db"

# App Metadata
APP_NAME = "CYBERGUARD"
APP_VERSION = "3.0 Pro Native Desktop"
ORGANIZATION_NAME = "CyberGuard Security Team"

# Color Palette - CyberGuard 3.0 Pro Glassmorphism & Cyber Theme
COLOR_BG_DARK = "#0f172a"        # Deep Slate Navy background
COLOR_CARD_BG = "#1e293b"        # Dark Card container background
COLOR_CARD_HOVER = "#334155"     # Card hover state
COLOR_BORDER = "#334155"         # Subtle card border
COLOR_TEXT_PRIMARY = "#f8fafc"   # Bright crisp text
COLOR_TEXT_MUTED = "#94a3b8"     # Soft muted text

# Accent Colors
COLOR_ACCENT_CYAN = "#38bdf8"    # Primary Electric Cyan
COLOR_ACCENT_BLUE = "#60a5fa"    # Accent Blue
COLOR_ACCENT_PURPLE = "#c084fc"  # Accent Purple

# Risk Colors
COLOR_RISK_HIGH = "#ef4444"      # Crimson Red (Danger / Password Warnings)
COLOR_RISK_MEDIUM = "#f59e0b"    # Amber Yellow (Warning / Medium Risk)
COLOR_RISK_LOW = "#10b981"       # Emerald Green (Safe / Passed)

# Phishing Risk Keywords
PHISHING_KEYWORDS = [
    "urgent", "immediately", "account suspended", "verify your account", "update billing",
    "unauthorized login", "password reset", "claim prize", "wire transfer", "bank alert",
    "social security", "tax refund", "limited time", "security breach", "action required",
    "log in now", "confirm password", "verify pin", "gift card", "crypto deposit"
]

# Suspicious URL Keywords
SUSPICIOUS_URL_KEYWORDS = [
    "login", "verify", "update", "banking", "secure", "account", "paypal", "free",
    "signin", "webscr", "ebayisapi", "authorization", "credential", "security-update"
]
