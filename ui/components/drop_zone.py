import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal

class FileDropZone(QFrame):
    """
    Interactive Drag & Drop File Zone supporting dragEnterEvent, dragLeaveEvent, dropEvent, and click to browse.
    """
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_label = QLabel("📁")
        self.icon_label.setStyleSheet("font-size: 38px; color: #38bdf8;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Drag & Drop File Here or Click to Browse")
        self.title_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sub_label = QLabel("Supports binary executables, documents, archives, and scripts for cryptographic auditing")
        self.sub_label.setStyleSheet("font-size: 12px; color: #94a3b8;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.sub_label)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select File for Security Audit",
                "",
                "All Files (*.*)"
            )
            if file_path:
                self.file_selected.emit(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragOver", "true")
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("dragOver", "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event):
        self.setProperty("dragOver", "false")
        self.style().unpolish(self)
        self.style().polish(self)

        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.exists(file_path):
                self.file_selected.emit(file_path)

    def set_file_name(self, file_path: str):
        file_name = os.path.basename(file_path)
        self.title_label.setText(f"Selected File: {file_name}")
        self.sub_label.setText(f"Full Path: {file_path}")
        self.icon_label.setText("📄")
