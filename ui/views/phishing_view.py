from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QProgressBar, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import QTimer, Qt
from core.phishing_detector import PhishingDetector
from database.db_manager import DatabaseManager
from ui.components.risk_badge import RiskBadge
from ui.components.snippet_box import CopySnippetBox
from ui.components.badge_pill import BadgePill
from ui.components.info_tooltip import InfoIcon

class PhishingView(QWidget):
    """
    Phishing Email & Social Engineering Detector Module for CyberGuard 3.0 Pro.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.detector = PhishingDetector()
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
        title = QLabel("Phishing Email & Social Engineering Detector")
        title.setObjectName("Header1")

        info_icon = InfoIcon(
            "Analyzes raw text for urgency cues, credential harvesting triggers, fraudulent banking claims, "
            "and psychological social engineering patterns."
        )

        header_top.addWidget(title)
        header_top.addWidget(info_icon)
        header_top.addStretch()
        layout.addLayout(header_top)

        subtitle = QLabel("Paste suspicious email bodies, SMS text messages, or notifications to analyze social engineering cues.")
        subtitle.setObjectName("TextMuted")
        layout.addWidget(subtitle)

        # Input Card
        input_card = QFrame()
        input_card.setObjectName("CardContainer")
        input_layout = QVBoxLayout(input_card)
        input_layout.setContentsMargins(16, 16, 16, 16)
        input_layout.setSpacing(12)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Paste raw email body, text message, or notification text here...")
        self.text_input.setMinimumHeight(130)

        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Text")
        self.clear_btn.setObjectName("SecondaryButton")
        self.clear_btn.clicked.connect(self.text_input.clear)

        self.scan_btn = QPushButton("Analyze Social Engineering Risk")
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.clicked.connect(self.analyze_text)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.scan_btn)

        input_layout.addWidget(self.text_input)
        input_layout.addLayout(btn_layout)
        layout.addWidget(input_card)

        # Dynamic Animated Progress Indicator
        self.progress_container = QFrame()
        self.progress_container.setVisible(False)
        prog_layout = QVBoxLayout(self.progress_container)
        prog_layout.setContentsMargins(0, 0, 0, 0)

        self.prog_lbl = QLabel("🎣 Inspecting text for social engineering cues & fraud patterns...")
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

        # Verdict Header
        verdict_top_layout = QHBoxLayout()
        self.verdict_lbl = QLabel("Verdict: -")
        self.verdict_lbl.setObjectName("Header2")

        self.risk_badge = RiskBadge("Low Risk", 100)

        verdict_top_layout.addWidget(self.verdict_lbl)
        verdict_top_layout.addStretch()
        verdict_top_layout.addWidget(self.risk_badge)
        results_layout.addLayout(verdict_top_layout)

        # Status Badge Pills Row
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(12)

        verdict_label_box = QHBoxLayout()
        verdict_label_box.addWidget(QLabel("Analysis Verdict:"))
        verdict_label_box.addWidget(InfoIcon("High Risk verdicts indicate urgent action cues or credential theft triggers."))
        self.verdict_badge = BadgePill("VERIFYING", "safe")
        badges_layout.addLayout(verdict_label_box)
        badges_layout.addWidget(self.verdict_badge)

        badges_layout.addSpacing(20)

        urgency_label_box = QHBoxLayout()
        urgency_label_box.addWidget(QLabel("Social Engineering:"))
        urgency_label_box.addWidget(InfoIcon("Artificial urgency (e.g. 'Account Suspended in 24 Hours') forces victims to bypass critical reasoning."))
        self.urgency_badge = BadgePill("CLEAN", "safe")
        badges_layout.addLayout(urgency_label_box)
        badges_layout.addWidget(self.urgency_badge)

        badges_layout.addStretch()
        results_layout.addLayout(badges_layout)

        # Copyable Text Snippet
        self.snippet_box = CopySnippetBox("Analyzed Message Snippet", "-")
        results_layout.addWidget(self.snippet_box)

        # Extracted Threats List
        indicators_lbl = QLabel("Detected Phishing Threats & Risk Indicators")
        indicators_lbl.setStyleSheet("color: #f8fafc; font-weight: bold; font-size: 14px;")
        results_layout.addWidget(indicators_lbl)

        self.indicators_list = QListWidget()
        self.indicators_list.setMaximumHeight(160)
        results_layout.addWidget(self.indicators_list)

        layout.addWidget(self.results_card)
        layout.addStretch()

    def analyze_text(self):
        content = self.text_input.toPlainText().strip()
        if not content:
            return

        self.scan_btn.setEnabled(False)
        self.results_card.setVisible(False)
        self.progress_container.setVisible(True)
        self.progress_bar.setValue(0)
        self.scan_progress_val = 0

        self.scan_timer.start(40)

    def update_progress_bar(self):
        self.scan_progress_val += 10
        self.progress_bar.setValue(self.scan_progress_val)
        if self.scan_progress_val >= 100:
            self.scan_timer.stop()
            self.finish_analysis()

    def finish_analysis(self):
        self.scan_btn.setEnabled(True)
        self.progress_container.setVisible(False)

        content = self.text_input.toPlainText().strip()
        result = self.detector.analyze(content)
        if "error" in result:
            return

        self.results_card.setVisible(True)
        self.verdict_lbl.setText(result["verdict"])
        
        score = result["risk_score"]
        risk_level = result["risk_level"]
        self.risk_badge.set_risk(risk_level, score)

        # Update Badge Pills
        if risk_level == "High Risk":
            self.verdict_badge.set_badge("HIGH RISK PHISHING", "danger")
            self.urgency_badge.set_badge("URGENCY CUES DETECTED", "danger")
        elif risk_level == "Medium Risk":
            self.verdict_badge.set_badge("SUSPICIOUS MESSAGE", "warning")
            self.urgency_badge.set_badge("POTENTIAL SOCIAL ENG", "warning")
        else:
            self.verdict_badge.set_badge("SAFE / BENIGN", "safe")
            self.urgency_badge.set_badge("NO SOCIAL ENG CUES", "safe")

        # Update Copy Snippet Box
        target_snippet = content[:60] + ("..." if len(content) > 60 else "")
        self.snippet_box.set_snippet("Analyzed Message Snippet", target_snippet)

        # Populate Indicators
        self.indicators_list.clear()
        indicators = result.get("indicators", [])
        
        if not indicators:
            item = QListWidgetItem("SAFE: No social engineering, urgency, or credential theft indicators detected.")
            item.setForeground(Qt.GlobalColor.green)
            self.indicators_list.addItem(item)
        else:
            for ind in indicators:
                text = f"[{ind['severity'].upper()} THREAT] {ind['category']}: {ind['description']}"
                item = QListWidgetItem(text)
                if ind['severity'] == 'High':
                    item.setForeground(Qt.GlobalColor.red)
                else:
                    item.setForeground(Qt.GlobalColor.yellow)
                self.indicators_list.addItem(item)

        # Log to DB
        self.db.save_scan_log(
            target=target_snippet,
            scan_type="Phishing Text",
            risk_score=score,
            risk_level=risk_level,
            details=result
        )
