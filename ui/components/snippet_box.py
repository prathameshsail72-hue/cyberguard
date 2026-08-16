from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer

class CopySnippetBox(QFrame):
    """
    Copyable code/hash snippet box with dark container and quick '📋 Copy' button.
    """
    def __init__(self, title: str = "", text: str = ""):
        super().__init__()
        self.setObjectName("SnippetBox")
        self.raw_text = text
        self.init_ui(title, text)

    def init_ui(self, title: str, text: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # Snippet Text Label
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.set_snippet(title, text)
        layout.addWidget(self.label, stretch=1)

        # Copy Button
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setObjectName("SnippetCopyBtn")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_btn)

    def set_snippet(self, title: str, text: str):
        self.raw_text = text
        if title:
            formatted = f"<b>{title}:</b> <code style='color:#38bdf8;'>{text}</code>"
        else:
            formatted = f"<code style='color:#38bdf8;'>{text}</code>"
        self.label.setText(formatted)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.raw_text)
        self.copy_btn.setText("✓ Copied!")
        self.copy_btn.setStyleSheet("background-color: #10b981; color: #ffffff;")
        QTimer.singleShot(1800, self.reset_copy_btn)

    def reset_copy_btn(self):
        self.copy_btn.setText("📋 Copy")
        self.copy_btn.setStyleSheet("")
