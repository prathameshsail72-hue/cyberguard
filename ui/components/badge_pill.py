from PyQt6.QtWidgets import QLabel, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt

class BadgePill(QFrame):
    """
    Visual status badge pill (e.g. [ PASSED ], [ HIGH RISK ], [ WARNING ]) with colored background pill.
    """
    def __init__(self, text: str = "PASSED", variant: str = "safe"):
        super().__init__()
        self.init_ui(text, variant)

    def init_ui(self, text: str, variant: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(0)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.set_badge(text, variant)

    def set_badge(self, text: str, variant: str = "safe"):
        """
        variant options: 'safe' (green), 'warning' (amber), 'danger' (red), 'info' (cyan)
        """
        variant = variant.lower()
        if variant in ["safe", "pass", "passed", "low risk"]:
            bg_color = "rgba(16, 185, 129, 0.2)"
            border_color = "#10b981"
            text_color = "#10b981"
            icon = "✓ "
        elif variant in ["warning", "warn", "medium risk"]:
            bg_color = "rgba(245, 158, 11, 0.2)"
            border_color = "#f59e0b"
            text_color = "#f59e0b"
            icon = "⚠️ "
        elif variant in ["danger", "high risk", "mismatch", "failed", "critical"]:
            bg_color = "rgba(239, 68, 68, 0.2)"
            border_color = "#ef4444"
            text_color = "#ef4444"
            icon = "🚨 "
        else:
            bg_color = "rgba(56, 189, 248, 0.2)"
            border_color = "#38bdf8"
            text_color = "#38bdf8"
            icon = "ℹ️ "

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
        """)
        self.label.setStyleSheet(f"color: {text_color}; font-weight: 800; font-size: 11px; letter-spacing: 0.5px;")
        self.label.setText(f"{icon}[ {text.upper()} ]")
