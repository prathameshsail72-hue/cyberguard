from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QProgressBar, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from core.url_analyzer import URLAnalyzer
from database.db_manager import DatabaseManager
from ui.components.risk_badge import RiskBadge
from ui.components.snippet_box import CopySnippetBox
from ui.components.badge_pill import BadgePill
from ui.components.info_tooltip import InfoIcon

class URLScanWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            analyzer = URLAnalyzer()
            result = analyzer.analyze(self.url)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class URLView(QWidget):
    """
    Website & Domain Security Analyzer Module for CyberGuard 3.0 Pro.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.scan_timer = QTimer(self)
        self.scan_timer.timeout.connect(self.update_progress_bar)
        self.scan_progress_val = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title with Tooltips
        header_top = QHBoxLayout()
        title = QLabel("Website & Domain Security Analyzer")
        title.setObjectName("Header1")

        info_icon = InfoIcon(
            "Performs real-time TLS/SSL handshake analysis, IP DNS resolution, HTTP security header auditing, "
            "and domain threat pattern evaluation."
        )

        header_top.addWidget(title)
        header_top.addWidget(info_icon)
        header_top.addStretch()
        layout.addLayout(header_top)

        subtitle = QLabel("Audit target domains for SSL certificate validity, DNS resolution, HTTP security headers, and phishing cues.")
        subtitle.setObjectName("TextMuted")
        layout.addWidget(subtitle)

        # Input Card
        input_card = QFrame()
        input_card.setObjectName("CardContainer")
        input_layout = QHBoxLayout(input_card)
        input_layout.setContentsMargins(16, 16, 16, 16)
        input_layout.setSpacing(12)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter target domain or URL (e.g. https://example.com)...")
        self.url_input.returnPressed.connect(self.start_scan)

        self.scan_btn = QPushButton("Scan Website Security")
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.clicked.connect(self.start_scan)

        input_layout.addWidget(self.url_input, stretch=1)
        input_layout.addWidget(self.scan_btn)
        layout.addWidget(input_card)

        # Dynamic Action Animated Progress Bar & Timer
        self.progress_container = QFrame()
        self.progress_container.setVisible(False)
        prog_layout = QVBoxLayout(self.progress_container)
        prog_layout.setContentsMargins(0, 0, 0, 0)
        
        self.prog_lbl = QLabel("🔍 Initiating domain handshake & Security Audit...")
        self.prog_lbl.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 12px;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        prog_layout.addWidget(self.prog_lbl)
        prog_layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_container)

        # Results Display Card
        self.results_card = QFrame()
        self.results_card.setObjectName("CardContainer")
        self.results_card.setVisible(False)
        results_layout = QVBoxLayout(self.results_card)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(16)

        # Top Result Bar (Target & Risk Badge)
        res_top_layout = QHBoxLayout()
        self.target_lbl = QLabel("Target: -")
        self.target_lbl.setObjectName("Header2")

        self.risk_badge = RiskBadge("Low Risk", 100)

        res_top_layout.addWidget(self.target_lbl)
        res_top_layout.addStretch()
        res_top_layout.addWidget(self.risk_badge)
        results_layout.addLayout(res_top_layout)

        # Status Badge Pills Row
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(12)

        ssl_label_box = QHBoxLayout()
        ssl_label_box.addWidget(QLabel("SSL Certificate:"))
        ssl_label_box.addWidget(InfoIcon("TLS/SSL encryption protects data in transit between web browsers and servers."))
        self.ssl_badge = BadgePill("VALID", "safe")
        badges_layout.addLayout(ssl_label_box)
        badges_layout.addWidget(self.ssl_badge)

        badges_layout.addSpacing(20)

        headers_label_box = QHBoxLayout()
        headers_label_box.addWidget(QLabel("Security Headers:"))
        headers_label_box.addWidget(InfoIcon("HTTP Security Headers (HSTS, CSP, X-Frame-Options) protect against XSS and clickjacking."))
        self.headers_badge = BadgePill("AUDITED", "safe")
        badges_layout.addLayout(headers_label_box)
        badges_layout.addWidget(self.headers_badge)

        badges_layout.addStretch()
        results_layout.addLayout(badges_layout)

        # Copyable Snippets Grid (IP Address & SSL Details)
        snippets_layout = QHBoxLayout()
        snippets_layout.setSpacing(16)

        ip_col = QVBoxLayout()
        ip_header = QHBoxLayout()
        ip_header.addWidget(QLabel("Network Details"))
        ip_header.addWidget(InfoIcon("DNS resolution maps friendly domain names to network IP address targets."))
        ip_header.addStretch()
        ip_col.addLayout(ip_header)

        self.ip_snippet = CopySnippetBox("IP Address", "-")
        self.domain_snippet = CopySnippetBox("Target Domain", "-")
        ip_col.addWidget(self.ip_snippet)
        ip_col.addWidget(self.domain_snippet)
        snippets_layout.addLayout(ip_col, stretch=1)

        ssl_col = QVBoxLayout()
        ssl_header = QHBoxLayout()
        ssl_header.addWidget(QLabel("SSL / Certificate Issuer"))
        ssl_header.addWidget(InfoIcon("Certificate Authorities (CA) digitally sign SSL certificates to establish identity trust."))
        ssl_header.addStretch()
        ssl_col.addLayout(ssl_header)

        self.issuer_snippet = CopySnippetBox("SSL Issuer", "-")
        self.expiry_snippet = CopySnippetBox("Expiration", "-")
        ssl_col.addWidget(self.issuer_snippet)
        ssl_col.addWidget(self.expiry_snippet)
        snippets_layout.addLayout(ssl_col, stretch=1)

        results_layout.addLayout(snippets_layout)

        # Security Audit Findings List
        issues_lbl = QLabel("Security Audit Findings & Remediations")
        issues_lbl.setStyleSheet("color: #f8fafc; font-weight: bold; font-size: 14px;")
        results_layout.addWidget(issues_lbl)

        self.issues_list = QListWidget()
        self.issues_list.setMaximumHeight(150)
        results_layout.addWidget(self.issues_list)

        layout.addWidget(self.results_card)
        layout.addStretch()

    def start_scan(self):
        target_url = self.url_input.text().strip()
        if not target_url:
            return

        self.scan_btn.setEnabled(False)
        self.results_card.setVisible(False)
        self.progress_container.setVisible(True)
        self.progress_bar.setValue(0)
        self.scan_progress_val = 0

        # Start timer animation
        self.scan_timer.start(50)

        self.worker = URLScanWorker(target_url)
        self.worker.finished.connect(self.handle_scan_result)
        self.worker.error.connect(self.handle_scan_error)
        self.worker.start()

    def update_progress_bar(self):
        if self.scan_progress_val < 90:
            self.scan_progress_val += 3
            self.progress_bar.setValue(self.scan_progress_val)
            if self.scan_progress_val > 60:
                self.prog_lbl.setText("🔒 Auditing HTTP Security Headers & TLS Certificates...")
            elif self.scan_progress_val > 30:
                self.prog_lbl.setText("🌐 Resolving DNS Records & IP Target...")

    def handle_scan_result(self, result: dict):
        self.scan_timer.stop()
        self.progress_bar.setValue(100)
        self.scan_btn.setEnabled(True)
        self.progress_container.setVisible(False)

        if "error" in result:
            self.handle_scan_error(result["error"])
            return

        self.results_card.setVisible(True)
        self.target_lbl.setText(f"Target: {result.get('target', '')}")
        
        score = result.get("risk_score", 100)
        risk_level = result.get("risk_level", "Low Risk")
        self.risk_badge.set_risk(risk_level, score)

        # Update Badge Pills
        ssl_info = result.get("ssl_details", {})
        if ssl_info.get("valid"):
            self.ssl_badge.set_badge("PASSED / VALID", "safe")
        else:
            self.ssl_badge.set_badge("INVALID / EXPIRED", "danger")

        headers_audit = result.get("header_audit", {})
        missing_headers = [h for h, present in headers_audit.items() if not present] if isinstance(headers_audit, dict) else []
        if not missing_headers:
            self.headers_badge.set_badge("ALL HEADERS PRESENT", "safe")
        elif len(missing_headers) <= 2:
            self.headers_badge.set_badge(f"{len(missing_headers)} HEADERS MISSING", "warning")
        else:
            self.headers_badge.set_badge(f"{len(missing_headers)} HEADERS MISSING", "danger")

        # Update Copy Snippet Boxes
        self.ip_snippet.set_snippet("IP Address", result.get("ip_address", "N/A"))
        self.domain_snippet.set_snippet("Target Domain", result.get("domain", "N/A"))
        self.issuer_snippet.set_snippet("SSL Issuer", ssl_info.get("issuer", {}).get("organizationName", "Unknown CA"))
        self.expiry_snippet.set_snippet("Expiration", str(ssl_info.get("notAfter", "N/A")))

        # Update Issues List
        self.issues_list.clear()
        issues = result.get("issues", [])
        remediations = result.get("remediations", [])

        if not issues:
            item = QListWidgetItem("SAFE: SSL/TLS handshakes, DNS resolution, and security header configurations verified.")
            item.setForeground(Qt.GlobalColor.green)
            self.issues_list.addItem(item)
        else:
            for idx, issue in enumerate(issues):
                item_text = f"ISSUE: {issue}"
                if idx < len(remediations):
                    item_text += f"\n   REMEDIATION: {remediations[idx]}"
                item = QListWidgetItem(item_text)
                item.setForeground(Qt.GlobalColor.yellow if score > 40 else Qt.GlobalColor.red)
                self.issues_list.addItem(item)

        # Log to Database
        self.db.save_scan_log(
            target=result.get("target"),
            scan_type="URL Security",
            risk_score=score,
            risk_level=risk_level,
            details=result
        )

    def handle_scan_error(self, err_msg: str):
        self.scan_timer.stop()
        self.scan_btn.setEnabled(True)
        self.progress_container.setVisible(False)
        self.results_card.setVisible(True)
        self.target_lbl.setText("Scan Error")
        self.ip_snippet.set_snippet("Error", err_msg)
