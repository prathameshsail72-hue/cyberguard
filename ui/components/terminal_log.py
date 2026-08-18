from datetime import datetime
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor

class TerminalLogWidget(QFrame):
    """
    Monospaced Live Security Terminal Audit Log Feed.
    Features dark background (#090D16), glowing HTML text output, timestamping, and clear control.
    """
    def __init__(self, title: str = "LIVE CYBERGUARD AUDIT TERMINAL STREAM"):
        super().__init__()
        self.setObjectName("TerminalCard")
        self.init_ui(title)
        self.seed_initial_logs()

    def init_ui(self, title: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        # Header Bar
        top_bar = QHBoxLayout()
        icon_lbl = QLabel("💻")
        icon_lbl.setStyleSheet("font-size: 14px;")
        
        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 800; letter-spacing: 1px;")

        clear_btn = QPushButton("Clear Output")
        clear_btn.setObjectName("SecondaryButton")
        clear_btn.setFixedSize(90, 24)
        clear_btn.setStyleSheet("font-size: 11px; padding: 2px 6px;")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_logs)

        top_bar.addWidget(icon_lbl)
        top_bar.addWidget(title_lbl)
        top_bar.addStretch()
        top_bar.addWidget(clear_btn)
        layout.addLayout(top_bar)

        # Terminal Output Box
        self.terminal_edit = QTextEdit()
        self.terminal_edit.setReadOnly(True)
        self.terminal_edit.setObjectName("TerminalTextEdit")
        self.terminal_edit.setFont(QFont("Consolas", 10))
        self.terminal_edit.setStyleSheet("""
            QTextEdit#TerminalTextEdit {
                background-color: #050b14;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 10px;
                color: #f8fafc;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)

        layout.addWidget(self.terminal_edit)

    def log(self, text: str, level: str = "INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        level_upper = level.upper()

        if level_upper == "ALERT" or level_upper == "CRITICAL" or level_upper == "HIGH":
            color = "#ef4444"  # Red
            tag = "ALERT"
        elif level_upper == "WARN" or level_upper == "MEDIUM":
            color = "#f59e0b"  # Amber
            tag = "WARN "
        elif level_upper == "SUCCESS" or level_upper == "LOW" or level_upper == "SAFE":
            color = "#10b981"  # Emerald
            tag = "PASS "
        else:
            color = "#38bdf8"  # Cyan
            tag = "INFO "

        html_line = f"<span style='color:#64748b;'>[{now}]</span> <b style='color:{color};'>[{tag}]</b> <span style='color:#f8fafc;'>{text}</span><br>"
        self.terminal_edit.append(html_line)
        self.terminal_edit.moveCursor(QTextCursor.MoveOperation.End)

    def clear_logs(self):
        self.terminal_edit.clear()
        self.log("Terminal output buffer cleared by operator.", "INFO")

    def seed_initial_logs(self):
        self.log("CyberGuard 3.0 Pro Security Operations Kernel Initialized.", "SUCCESS")
        self.log("SQLite Embedded DB 'cyberguard_desktop.db' connected successfully.", "INFO")
        self.log("Real-time threat monitoring engines & heuristic rulesets active.", "INFO")
