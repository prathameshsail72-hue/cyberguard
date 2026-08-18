from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QFrame, QCheckBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from core.password_analyzer import PasswordAnalyzer
from database.db_manager import DatabaseManager
from ui.components.risk_badge import RiskBadge
from ui.components.snippet_box import CopySnippetBox
from ui.components.badge_pill import BadgePill
from ui.components.info_tooltip import InfoIcon

class PasswordView(QWidget):
    """
    Password Security & Mathematical Entropy Analyzer Module for CyberGuard 3.0 Pro.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.analyzer = PasswordAnalyzer()
        self.log_timer = QTimer(self)
        self.log_timer.setSingleShot(True)
        self.log_timer.timeout.connect(self._log_password_audit)
        self.last_result = None
        self.last_text = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title with Tooltips
        header_top = QHBoxLayout()
        title = QLabel("Password Security & Entropy Analyzer")
        title.setObjectName("Header1")

        info_icon = InfoIcon(
            "Mathematical Entropy calculates theoretical randomness bits (E = L * log2(R)) to estimate "
            "resistance against offline GPU brute-force dictionary attacks."
        )

        header_top.addWidget(title)
        header_top.addWidget(info_icon)
        header_top.addStretch()
        layout.addLayout(header_top)

        subtitle = QLabel("Evaluate mathematical entropy (E = L * log2(R)), dictionary pattern risks, and estimated brute-force times.")
        subtitle.setObjectName("TextMuted")
        layout.addWidget(subtitle)

        # Input Card
        input_card = QFrame()
        input_card.setObjectName("CardContainer")
        input_layout = QVBoxLayout(input_card)
        input_layout.setContentsMargins(16, 16, 16, 16)
        input_layout.setSpacing(12)

        pwd_top = QHBoxLayout()
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setPlaceholderText("Enter password to test in real-time...")
        self.pwd_input.textChanged.connect(self.on_text_changed)

        self.toggle_show = QCheckBox("Show Password")
        self.toggle_show.toggled.connect(self.toggle_echo_mode)

        pwd_top.addWidget(self.pwd_input, stretch=1)
        pwd_top.addWidget(self.toggle_show)
        input_layout.addLayout(pwd_top)

        # Dynamic Real-time Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        input_layout.addWidget(self.progress)

        layout.addWidget(input_card)

        # Results Container
        self.results_card = QFrame()
        self.results_card.setObjectName("CardContainer")
        results_layout = QVBoxLayout(self.results_card)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(16)

        top_res = QHBoxLayout()
        self.status_lbl = QLabel("Strength: Enter password")
        self.status_lbl.setObjectName("Header2")

        self.risk_badge = RiskBadge("Low Risk", 100)

        top_res.addWidget(self.status_lbl)
        top_res.addStretch()
        top_res.addWidget(self.risk_badge)
        results_layout.addLayout(top_res)

        # Status Badge Pills Row
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(12)

        dict_label_box = QHBoxLayout()
        dict_label_box.addWidget(QLabel("Dictionary Risk:"))
        dict_label_box.addWidget(InfoIcon("Dictionary checks search for top 100,000 common passwords used in credential stuffing attacks."))
        self.dict_badge = BadgePill("CLEAN", "safe")
        badges_layout.addLayout(dict_label_box)
        badges_layout.addWidget(self.dict_badge)

        badges_layout.addSpacing(20)

        entropy_label_box = QHBoxLayout()
        entropy_label_box.addWidget(QLabel("Entropy Status:"))
        entropy_label_box.addWidget(InfoIcon("Passwords exceeding 60 bits of entropy are resilient against modern multi-GPU cracking rigs."))
        self.entropy_badge = BadgePill("HIGH ENTROPY", "safe")
        badges_layout.addLayout(entropy_label_box)
        badges_layout.addWidget(self.entropy_badge)

        badges_layout.addStretch()
        results_layout.addLayout(badges_layout)

        # Copyable Snippets Grid (Entropy & Crack Times)
        snippets_layout = QHBoxLayout()
        snippets_layout.setSpacing(16)

        # Left Snippet Column: Entropy & Charset
        ent_col = QVBoxLayout()
        ent_header = QHBoxLayout()
        ent_header.addWidget(QLabel("Entropy Formula Metrics"))
        ent_header.addWidget(InfoIcon("Charset Pool (R) expands by mixing lowercase (26), uppercase (26), numbers (10), and symbols (32)."))
        ent_header.addStretch()
        ent_col.addLayout(ent_header)

        self.bits_snippet = CopySnippetBox("Entropy Bits", "-")
        self.charset_snippet = CopySnippetBox("Charset Pool (R)", "-")
        ent_col.addWidget(self.bits_snippet)
        ent_col.addWidget(self.charset_snippet)
        snippets_layout.addLayout(ent_col, stretch=1)

        # Right Snippet Column: Estimated Crack Times
        crack_col = QVBoxLayout()
        crack_header = QHBoxLayout()
        crack_header.addWidget(QLabel("Estimated Brute-Force Crack Times"))
        crack_header.addWidget(InfoIcon("GPU Clusters calculate up to 100 billion hash combinations per second."))
        crack_header.addStretch()
        crack_col.addLayout(crack_header)

        self.cpu_snippet = CopySnippetBox("Desktop CPU (10k/s)", "-")
        self.gpu_snippet = CopySnippetBox("Fast GPU Cluster (100B/s)", "-")
        crack_col.addWidget(self.cpu_snippet)
        crack_col.addWidget(self.gpu_snippet)
        snippets_layout.addLayout(crack_col, stretch=1)

        results_layout.addLayout(snippets_layout)

        # Improvements List
        imp_lbl = QLabel("Actionable Strength Improvements & Feedback")
        imp_lbl.setStyleSheet("color: #f8fafc; font-weight: bold; font-size: 14px;")
        results_layout.addWidget(imp_lbl)

        self.improvements_list = QListWidget()
        self.improvements_list.setMaximumHeight(140)
        results_layout.addWidget(self.improvements_list)

        layout.addWidget(self.results_card)
        layout.addStretch()

    def toggle_echo_mode(self, checked: bool):
        if checked:
            self.pwd_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)

    def on_text_changed(self, text: str):
        if not text:
            self.progress.setValue(0)
            self.status_lbl.setText("Strength: Enter password")
            self.improvements_list.clear()
            self.dict_badge.set_badge("NO INPUT", "info")
            self.entropy_badge.set_badge("NO INPUT", "info")
            self.bits_snippet.set_snippet("Entropy Bits", "-")
            self.charset_snippet.set_snippet("Charset Pool (R)", "-")
            self.cpu_snippet.set_snippet("Desktop CPU", "-")
            self.gpu_snippet.set_snippet("Fast GPU Cluster", "-")
            return

        result = self.analyzer.analyze(text)
        score = result["score"]
        self.progress.setValue(score)

        status = result["status"]
        risk_level = result["risk_level"]
        self.status_lbl.setText(f"Strength: {status}")
        self.risk_badge.set_risk(risk_level, score)

        # Update Badge Pills
        if result["is_common"]:
            self.dict_badge.set_badge("COMMON WEAK WORD", "danger")
        else:
            self.dict_badge.set_badge("DICTIONARY CLEAN", "safe")

        entropy_bits = result["entropy_bits"]
        if entropy_bits < 36:
            self.entropy_badge.set_badge(f"CRITICAL ENTROPY ({entropy_bits}b)", "danger")
        elif entropy_bits < 60:
            self.entropy_badge.set_badge(f"MODERATE ENTROPY ({entropy_bits}b)", "warning")
        else:
            self.entropy_badge.set_badge(f"HIGH ENTROPY ({entropy_bits}b)", "safe")

        # Update Copy Snippets
        self.bits_snippet.set_snippet("Entropy Bits", f"{entropy_bits} bits (L={result['password_length']})")
        self.charset_snippet.set_snippet("Charset Pool (R)", f"{result['charset_size']} symbols")

        ct = result.get("crack_times", {})
        self.cpu_snippet.set_snippet("Desktop CPU (10k/s)", str(ct.get('cpu', 'N/A')))
        self.gpu_snippet.set_snippet("Fast GPU Cluster (100B/s)", str(ct.get('gpu_cluster', 'N/A')))

        # Update Improvements
        self.improvements_list.clear()
        improvements = result.get("improvements", [])
        feedback = result.get("feedback", [])

        for fb in feedback:
            item = QListWidgetItem(f"WARN: {fb}")
            item.setForeground(Qt.GlobalColor.yellow)
            self.improvements_list.addItem(item)

        for imp in improvements:
            item = QListWidgetItem(f"TIP: {imp}")
            item.setForeground(Qt.GlobalColor.cyan)
            self.improvements_list.addItem(item)

        if not improvements and not feedback:
            item = QListWidgetItem("EXCELLENT: Highly secure, high-entropy password formulation!")
            item.setForeground(Qt.GlobalColor.green)
            self.improvements_list.addItem(item)

        # Trigger debounced DB logging (500ms delay) to prevent log spam
        self.last_result = result
        self.last_text = text
        self.log_timer.stop()
        self.log_timer.start(500)

    def _log_password_audit(self):
        if self.last_result and self.last_text:
            masked_pwd = "*" * len(self.last_text)
            self.db.save_scan_log(
                target=masked_pwd,
                scan_type="Password Entropy",
                risk_score=self.last_result["score"],
                risk_level=self.last_result["risk_level"],
                details={"entropy_bits": self.last_result["entropy_bits"], "status": self.last_result["status"]}
            )
