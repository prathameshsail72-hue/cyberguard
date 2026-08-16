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
from ui.views import (
    DashboardView, URLView, PhishingView,
    PasswordView, FileView, SurveyView, QuizView
)

class CyberGuardMainWindow(QMainWindow):
    """
    CYBERGUARD 3.0 Pro - Principal Desktop Application Window
    """
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME} - {APP_VERSION}")
        self.resize(1320, 840)
        self.setMinimumSize(1024, 680)

        # Apply Global CyberGuard 3.0 Pro Glassmorphism QSS Theme
        self.setStyleSheet(DARK_CYBER_STYESHEET)

        # Central Widget & Root Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ----------------------------------------------------
        # 1. Left Navigation Sidebar Frame
        # ----------------------------------------------------
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(8)

        # App Logo & Branding
        logo_label = QLabel("🛡️ " + APP_NAME)
        logo_label.setObjectName("AppTitleLabel")
        
        version_label = QLabel(APP_VERSION)
        version_label.setObjectName("AppSubtitleLabel")

        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addWidget(version_label)
        sidebar_layout.addSpacing(24)

        # Navigation Buttons List
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

        # System Status Indicator in Sidebar Bottom
        sys_status_card = QFrame()
        sys_status_card.setStyleSheet("background-color: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 10px;")
        sys_layout = QVBoxLayout(sys_status_card)
        sys_layout.setContentsMargins(8, 8, 8, 8)
        
        db_lbl = QLabel("DB: cyberguard_desktop.db")
        db_lbl.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: bold;")
        sec_lbl = QLabel("Engine: CyberGuard 3.0 / PyQt6")
        sec_lbl.setStyleSheet("color: #94a3b8; font-size: 10px;")

        sys_layout.addWidget(db_lbl)
        sys_layout.addWidget(sec_lbl)

        sidebar_layout.addWidget(sys_status_card)

        root_layout.addWidget(sidebar)

        # ----------------------------------------------------
        # 2. Main Content View Container (QStackedWidget)
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

        root_layout.addWidget(self.stacked_widget, stretch=1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("CyberGuard 3.0 Pro Security Engine Active. Database loaded successfully.")

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
