from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from core.file_integrity import FileIntegrityAnalyzer
from database.db_manager import DatabaseManager
from ui.components.risk_badge import RiskBadge
from ui.components.snippet_box import CopySnippetBox
from ui.components.badge_pill import BadgePill
from ui.components.info_tooltip import InfoIcon
from ui.components.drop_zone import FileDropZone

class FileView(QWidget):
    """
    File Integrity & Cryptographic Fingerprint Analyzer Module for CyberGuard 3.0 Pro.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.analyzer = FileIntegrityAnalyzer()
        self.selected_file_path = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title with Hover Tooltips
        header_top = QHBoxLayout()
        title = QLabel("File Integrity & Cryptographic Fingerprint Analyzer")
        title.setObjectName("Header1")
        
        info_icon = InfoIcon(
            "Cryptographic verification computes exact SHA-256 / MD5 hashes and verifies raw magic bytes "
            "headers to identify double extension spoofing or binary corruption."
        )

        header_top.addWidget(title)
        header_top.addWidget(info_icon)
        header_top.addStretch()
        layout.addLayout(header_top)

        subtitle = QLabel("Drag & drop any file to verify SHA-256 signatures, validate magic bytes headers, and detect double extension spoofing.")
        subtitle.setObjectName("TextMuted")
        layout.addWidget(subtitle)

        # Interactive Drag & Drop Target Box
        self.drop_zone = FileDropZone()
        self.drop_zone.file_selected.connect(self.on_file_selected)
        layout.addWidget(self.drop_zone)

        # Results Display Card
        self.results_card = QFrame()
        self.results_card.setObjectName("CardContainer")
        self.results_card.setVisible(False)
        results_layout = QVBoxLayout(self.results_card)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(16)

        # Top Result Bar (Filename & Risk Badge)
        top_res = QHBoxLayout()
        self.filename_lbl = QLabel("File: -")
        self.filename_lbl.setObjectName("Header2")

        self.risk_badge = RiskBadge("Low Risk", 100)

        top_res.addWidget(self.filename_lbl)
        top_res.addStretch()
        top_res.addWidget(self.risk_badge)
        results_layout.addLayout(top_res)

        # Status Badge Pills Layout
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(12)

        magic_label_box = QHBoxLayout()
        magic_label_box.addWidget(QLabel("Magic Bytes:"))
        magic_label_box.addWidget(InfoIcon("Magic Bytes are unique hex signatures embedded in the first 8-16 bytes of a file that identify its real format."))
        
        self.magic_badge = BadgePill("VERIFIED", "safe")
        badges_layout.addLayout(magic_label_box)
        badges_layout.addWidget(self.magic_badge)

        badges_layout.addSpacing(20)

        ext_label_box = QHBoxLayout()
        ext_label_box.addWidget(QLabel("Double Extension:"))
        ext_label_box.addWidget(InfoIcon("Double Extension Spoofing hides executable code (.exe, .bat) behind fake document extensions (.pdf.exe, .jpg.scr)."))
        
        self.ext_badge = BadgePill("CLEAN", "safe")
        badges_layout.addLayout(ext_label_box)
        badges_layout.addWidget(self.ext_badge)

        badges_layout.addStretch()
        results_layout.addLayout(badges_layout)

        # Copyable Hashes & Headers Snippet Boxes
        snippets_layout = QHBoxLayout()
        snippets_layout.setSpacing(16)

        # Left Snippet: Cryptographic Hashes
        hash_col = QVBoxLayout()
        hash_header = QHBoxLayout()
        hash_header.addWidget(QLabel("Cryptographic Signatures"))
        hash_header.addWidget(InfoIcon("SHA-256 is a 256-bit secure cryptographic hash algorithm used for digital fingerprinting and integrity verification."))
        hash_header.addStretch()
        hash_col.addLayout(hash_header)

        self.sha256_snippet = CopySnippetBox("SHA-256", "-")
        self.md5_snippet = CopySnippetBox("MD5", "-")
        hash_col.addWidget(self.sha256_snippet)
        hash_col.addWidget(self.md5_snippet)
        snippets_layout.addLayout(hash_col, stretch=1)

        # Right Snippet: Magic Headers & File Details
        header_col = QVBoxLayout()
        header_title_box = QHBoxLayout()
        header_title_box.addWidget(QLabel("Header Bytes & MIME Type"))
        header_title_box.addWidget(InfoIcon("MIME Type indicates the standardized internet media format recognized by operating system parsers."))
        header_title_box.addStretch()
        header_col.addLayout(header_title_box)

        self.mime_snippet = CopySnippetBox("MIME Type", "-")
        self.hex_snippet = CopySnippetBox("Header Hex", "-")
        header_col.addWidget(self.mime_snippet)
        header_col.addWidget(self.hex_snippet)
        snippets_layout.addLayout(header_col, stretch=1)

        results_layout.addLayout(snippets_layout)

        # Anomalies & Remediation List
        anom_lbl = QLabel("Detected File Anomalies & Security Warnings")
        anom_lbl.setStyleSheet("color: #f8fafc; font-weight: bold; font-size: 14px;")
        results_layout.addWidget(anom_lbl)

        self.anomalies_list = QListWidget()
        self.anomalies_list.setMaximumHeight(150)
        results_layout.addWidget(self.anomalies_list)

        layout.addWidget(self.results_card)
        layout.addStretch()

    def on_file_selected(self, file_path: str):
        self.selected_file_path = file_path
        self.drop_zone.set_file_name(file_path)
        self.analyze_file(file_path)

    def analyze_file(self, file_path: str):
        result = self.analyzer.analyze(file_path)
        if "error" in result:
            return

        self.results_card.setVisible(True)
        self.filename_lbl.setText(f"File: {result['file_name']} ({result['file_size_formatted']})")
        
        score = result["risk_score"]
        risk_level = result["risk_level"]
        self.risk_badge.set_risk(risk_level, score)

        # Update Badge Pills
        if result["magic_matched"]:
            self.magic_badge.set_badge("MATCHED / PASSED", "safe")
        else:
            self.magic_badge.set_badge("MISMATCH DETECTED", "danger")

        if result["is_double_ext"]:
            self.ext_badge.set_badge("DOUBLE EXT SPOOFING", "danger")
        else:
            self.ext_badge.set_badge("NO EXT SPOOFING", "safe")

        # Update Copy Snippet Boxes
        self.sha256_snippet.set_snippet("SHA-256", result["sha256"])
        self.md5_snippet.set_snippet("MD5", result["md5"])
        self.mime_snippet.set_snippet("MIME Type", f"{result['mime_type']} (.{result['extension']})")
        self.hex_snippet.set_snippet("Header Hex", result["header_hex"])

        # Update Anomalies List
        self.anomalies_list.clear()
        anomalies = result.get("anomalies", [])
        recommendations = result.get("recommendations", [])

        if not anomalies:
            item = QListWidgetItem("SAFE: File structure, magic bytes header, and extension signatures verified.")
            item.setForeground(Qt.GlobalColor.green)
            self.anomalies_list.addItem(item)
        else:
            for idx, anom in enumerate(anomalies):
                text = f"ANOMALY: {anom}"
                if idx < len(recommendations):
                    text += f"\n   RECOMMENDATION: {recommendations[idx]}"
                item = QListWidgetItem(text)
                item.setForeground(Qt.GlobalColor.red)
                self.anomalies_list.addItem(item)

        # Log to Database
        self.db.save_scan_log(
            target=result["file_name"],
            scan_type="File Integrity",
            risk_score=score,
            risk_level=risk_level,
            details={"sha256": result["sha256"], "mime_type": result["mime_type"]}
        )
