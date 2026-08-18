from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QFont, QColor

class CustomTitleBar(QFrame):
    """
    Futuristic Custom Title Bar with Window Controls & Glowing AI Engine Indicator.
    Handles frameless window dragging, minimize, maximize/restore, and exit.
    """
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.drag_position = QPoint()
        self.setObjectName("CustomTitleBar")
        self.setFixedHeight(44)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 12, 0)
        layout.setSpacing(12)

        # 1. Branding & Logo
        self.logo_label = QLabel("🛡️ CYBERGUARD")
        self.logo_label.setStyleSheet("color: #38bdf8; font-weight: 800; font-size: 14px; letter-spacing: 1px;")

        self.title_label = QLabel("|  AI Cybersecurity Operations Suite")
        self.title_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")

        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)

        # 2. Glowing AI Engine Status Badge
        self.status_badge = QFrame()
        self.status_badge.setObjectName("AIEngineBadge")
        badge_layout = QHBoxLayout(self.status_badge)
        badge_layout.setContentsMargins(10, 4, 10, 4)
        badge_layout.setSpacing(6)

        dot = QLabel("🟢")
        dot.setStyleSheet("font-size: 9px;")
        lbl = QLabel("AI Engine: Active")
        lbl.setStyleSheet("color: #10b981; font-weight: 800; font-size: 11px;")

        badge_layout.addWidget(dot)
        badge_layout.addWidget(lbl)
        self.status_badge.setStyleSheet("""
            QFrame#AIEngineBadge {
                background-color: rgba(16, 185, 129, 0.15);
                border: 1px solid #10b981;
                border-radius: 12px;
            }
        """)

        layout.addStretch()
        layout.addWidget(self.status_badge)
        layout.addSpacing(16)

        # 3. Frameless Window Controls
        self.btn_min = QPushButton("─")
        self.btn_min.setObjectName("WinControlMin")
        self.btn_min.setFixedSize(30, 26)
        self.btn_min.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_min.clicked.connect(self.main_window.showMinimized)

        self.btn_max = QPushButton("▢")
        self.btn_max.setObjectName("WinControlMax")
        self.btn_max.setFixedSize(30, 26)
        self.btn_max.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_max.clicked.connect(self.toggle_maximize)

        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("WinControlClose")
        self.btn_close.setFixedSize(30, 26)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.clicked.connect(self.main_window.close)

        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)

    def toggle_maximize(self):
        if self.main_window.isMaximized():
            self.main_window.showNormal()
            self.btn_max.setText("▢")
        else:
            self.main_window.showMaximized()
            self.btn_max.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.main_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self.drag_position.isNull():
            self.main_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
