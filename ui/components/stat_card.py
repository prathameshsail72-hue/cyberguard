from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from config import COLOR_ACCENT_CYAN, COLOR_TEXT_MUTED, COLOR_TEXT_PRIMARY, COLOR_CARD_BG, COLOR_BORDER

class StatCard(QFrame):
    """
    Glassmorphism KPI Analytics Card Widget for CyberGuard 3.0 Pro.
    """
    def __init__(self, title: str, value: str, subtitle: str = "", accent_color: str = COLOR_ACCENT_CYAN):
        super().__init__()
        self.accent_color = accent_color
        self.init_ui(title, value, subtitle)

    def init_ui(self, title: str, value: str, subtitle: str):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-left: 5px solid {self.accent_color};
                border-radius: 10px;
                padding: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 11px; font-weight: 800; letter-spacing: 1px;")

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 26px; font-weight: 800;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet(f"color: {self.accent_color}; font-size: 12px; font-weight: 600;")
            layout.addWidget(self.subtitle_label)

    def update_value(self, new_value: str, new_subtitle: str = ""):
        self.value_label.setText(new_value)
        if new_subtitle and hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(new_subtitle)
