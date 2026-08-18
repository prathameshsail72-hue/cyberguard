import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QStatusBar, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

from config import APP_NAME, APP_VERSION
from database.db_manager import DatabaseManager
from ui.styles import DARK_CYBER_STYESHEET
from ui.components import CustomTitleBar
from ui.views import (
    DashboardView, URLView, PhishingView,
    PasswordView, FileView, SurveyView, QuizView
)

class CyberGuardMainWindow(QMainWindow):
    """
    CYBERGUARD 3.0 Pro - Sleek Futuristic AI Cybersecurity Operations Dashboard.
    Features Frameless Window Chrome, Glassmorphism Obsidian Dark Theme, Custom Title Bar,
    and Real-Time Security Engines.
    """
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        # 1. Enable Frameless Window Hint for Custom Title Bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(f"{APP_NAME} - {APP_VERSION}")
        self.resize(1340, 860)
        self.setMinimumSize(1040, 700)

        # Apply Global CyberGuard 3.0 Pro Glassmorphism QSS Theme
        self.setStyleSheet(DARK_CYBER_STYESHEET)

        # Central Container Widget & Main Vertical Layout (TitleBar + Body)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_vbox = QVBoxLayout(central_widget)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        # ----------------------------------------------------
        # Top Custom Title Bar (Frameless Draggable Window Bar)
        # ----------------------------------------------------
        self.title_bar = CustomTitleBar(self)
        main_vbox.addWidget(self.title_bar)

        # Body Layout (Sidebar Left + Content Stack Right)
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # ----------------------------------------------------
        # Left Navigation Sidebar Frame
        # ----------------------------------------------------
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 20, 16, 20)
        sidebar_layout.setSpacing(8)

        # App Logo & Branding Tag
        logo_label = QLabel("🛡️ " + APP_NAME)
        logo_label.setObjectName("AppTitleLabel")
        
        version_label = QLabel(APP_VERSION)
        version_label.setObjectName("AppSubtitleLabel")

        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addWidget(version_label)
        sidebar_layout.addSpacing(20)

        # Navigation Buttons List with Icons & Hover States
        self.nav_buttons = []
        
        nav_items = [
            ("📊  Dashboard & Analytics", 0),
            ("🌐  Website Security", 1),
            ("🎣  Phishing Detector", 2),
            ("🔑  Password Entropy", 3),
            ("📁  File Integrity", 4),
            ("📈  Awareness Survey", 5),
            ("🎮  Cyber Quiz", 6)
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self.switch_view(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # System Status Indicator Box in Sidebar Bottom
        sys_status_card = QFrame()
        sys_status_card.setStyleSheet("""
            QFrame {
                background-color: #050b14;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        sys_layout = QVBoxLayout(sys_status_card)
        sys_layout.setContentsMargins(8, 8, 8, 8)
        sys_layout.setSpacing(4)
        
        db_lbl = QLabel("DB: cyberguard_desktop.db")
        db_lbl.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: bold;")
        sec_lbl = QLabel("Engine: CyberGuard 3.0 / PyQt6")
        sec_lbl.setStyleSheet("color: #94a3b8; font-size: 10px;")

        sys_layout.addWidget(db_lbl)
        sys_layout.addWidget(sec_lbl)

        sidebar_layout.addWidget(sys_status_card)

        body_layout.addWidget(sidebar)

        # ----------------------------------------------------
        # Main Content View Container (QStackedWidget)
        # ----------------------------------------------------
        self.stacked_widget = QStackedWidget()
        
        # Instantiate View Pages
        self.view_dashboard = DashboardView(self.db)
        self.view_url = URLView(self.db)
        self.view_phishing = PhishingView(self.db)
        self.view_password = PasswordView(self.db)
        self.view_file = FileView(self.db)
        self.view_survey = SurveyView(self.db)
        self.view_quiz = QuizView(self.db)

        self.stacked_widget.addWidget(self.view_dashboard)
        self.stacked_widget.addWidget(self.view_url)
        self.stacked_widget.addWidget(self.view_phishing)
        self.stacked_widget.addWidget(self.view_password)
        self.stacked_widget.addWidget(self.view_file)
        self.stacked_widget.addWidget(self.view_survey)
        self.stacked_widget.addWidget(self.view_quiz)

        body_layout.addWidget(self.stacked_widget, stretch=1)
        main_vbox.addWidget(body_widget, stretch=1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("CyberGuard 3.0 Pro AI Security Operations Engine Active. Glassmorphism dark mode loaded.")

        # Activate default tab (Dashboard)
        self.switch_view(0)

    def switch_view(self, index: int):
        self.stacked_widget.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Trigger data refresh on Dashboard or Quiz tab switch
        if index == 0:
            self.view_dashboard.load_data()
        elif index == 6:
            self.view_quiz.load_db_stats()

def main():
    app = QApplication(sys.argv)
    window = CyberGuardMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
