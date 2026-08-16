from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from config import COLOR_RISK_HIGH, COLOR_RISK_MEDIUM, COLOR_RISK_LOW

class RiskBadge(QFrame):
    """
    Color-coded Risk Level Indicator Badge Pill for CyberGuard 3.0 Pro.
    """
    def __init__(self, risk_level: str = "Low Risk", score: int = 100):
        super().__init__()
        self.init_ui(risk_level, score)

    def init_ui(self, risk_level: str, score: int):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(6)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label)
        self.set_risk(risk_level, score)

    def set_risk(self, risk_level: str, score: int):
        if risk_level == "High Risk" or score <= 40:
            bg_color = "rgba(239, 68, 68, 0.2)"
            border_color = COLOR_RISK_HIGH
            text_color = COLOR_RISK_HIGH
            icon = "🚨 "
        elif risk_level == "Medium Risk" or score <= 75:
            bg_color = "rgba(245, 158, 11, 0.2)"
            border_color = COLOR_RISK_MEDIUM
            text_color = COLOR_RISK_MEDIUM
            icon = "⚠️ "
        else:
            bg_color = "rgba(16, 185, 129, 0.2)"
            border_color = COLOR_RISK_LOW
            text_color = COLOR_RISK_LOW
            icon = "🛡️ "

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
        """)
        self.label.setStyleSheet(f"color: {text_color}; font-weight: 800; font-size: 12px; letter-spacing: 0.5px;")
        self.label.setText(f"{icon}{risk_level.upper()} ({score}/100)")
