from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QRadioButton, QButtonGroup, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from ui.components.badge_pill import BadgePill
from ui.components.stat_card import StatCard

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Spot the Phishing URL: Which of the following URLs is MOST likely a malicious phishing domain?",
        "options": [
            "https://accounts.google.com/signin",
            "https://www.paypal.security-update-verify.com/login",
            "https://github.com/login",
            "https://portal.microsoft.com"
        ],
        "correct": 1,
        "explanation": "The domain 'security-update-verify.com' is a lookalike phishing domain attempting to spoof PayPal using a sub-domain trick."
    },
    {
        "id": 2,
        "question": "Password Hygiene: Which password strategy provides the highest cryptographic entropy against brute-force attacks?",
        "options": [
            "P@ssw0rd2026!",
            "CorrectHorseBatteryStaple#99",
            "1234567890Aa!",
            "Admin2026Secure"
        ],
        "correct": 1,
        "explanation": "Long passphrases like 'CorrectHorseBatteryStaple#99' have high character length (L), exponentially boosting entropy (E = L * log2(R)) while remaining easy to remember."
    },
    {
        "id": 3,
        "question": "File Integrity Spoofing: An attacker sends a file named 'Invoice_PDF.pdf.exe'. What risk pattern is being attempted?",
        "options": [
            "Magic Header Corruption",
            "Double Extension Masking / Executable Spoofing",
            "Zero-Day Buffer Overflow",
            "SSL Certificate Pinning Failure"
        ],
        "correct": 1,
        "explanation": "Double extension masking hides the true '.exe' extension on systems hiding known file extensions, tricking users into executing binary code thinking it's a PDF."
    },
    {
        "id": 4,
        "question": "Social Engineering: You receive an urgent email from your CEO demanding a wire transfer within 30 minutes. What should you do first?",
        "options": [
            "Immediately execute the wire transfer to avoid disciplinary action",
            "Reply to the email asking for confirmation of bank details",
            "Verify the request through an out-of-band communication channel (e.g. call the CEO)",
            "Forward the email to all company colleagues to warn them"
        ],
        "correct": 2,
        "explanation": "Social engineering attacks rely on artificial urgency and authority. Always verify suspicious requests out-of-band using verified phone numbers."
    },
    {
        "id": 5,
        "question": "HTTPS & SSL Auditing: What does an invalid SSL certificate warning in your browser usually indicate?",
        "options": [
            "Your internet router is turned off",
            "Potential Man-in-the-Middle (MITM) interception or expired certificate authority",
            "The website is downloading a virus automatically",
            "Your computer's RAM is overloaded"
        ],
        "correct": 1,
        "explanation": "Invalid SSL certificates mean the encrypted tunnel cannot be cryptographically verified, creating a risk of active eavesdropping or MITM attack."
    }
]

class QuizView(QWidget):
    """
    Gamified Cyber Quiz & Challenges Module for CyberGuard 3.0 Pro.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.current_q_idx = 0
        self.user_answers = {}
        self.submitted = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title
        title_layout = QHBoxLayout()
        title = QLabel("🎮 Cyber Quiz & Security Challenges")
        title.setObjectName("Header1")
        
        self.reset_btn = QPushButton("🔄 Restart Challenge")
        self.reset_btn.setObjectName("SecondaryButton")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.restart_quiz)

        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(self.reset_btn)
        layout.addLayout(title_layout)

        subtitle = QLabel("Test your cybersecurity threat detection skills across real-world phishing, password hygiene, file spoofing, and SSL scenarios.")
        subtitle.setObjectName("TextMuted")
        layout.addWidget(subtitle)

        # Stats Summary Cards Header
        stats_layout = QHBoxLayout()
        self.card_score = StatCard("Current Score", "0 / 5", "0% Accuracy", "#38bdf8")
        self.card_badge = StatCard("Earned Badge", "Unranked", "Take Quiz", "#c084fc")
        self.card_attempts = StatCard("Total Attempts", "0", "SQLite History", "#60a5fa")

        stats_layout.addWidget(self.card_score)
        stats_layout.addWidget(self.card_badge)
        stats_layout.addWidget(self.card_attempts)
        layout.addLayout(stats_layout)

        # Main Question Container Card
        self.q_card = QFrame()
        self.q_card.setObjectName("CardContainer")
        q_layout = QVBoxLayout(self.q_card)
        q_layout.setContentsMargins(24, 24, 24, 24)
        q_layout.setSpacing(16)

        # Question Header Bar
        q_top_bar = QHBoxLayout()
        self.q_num_lbl = QLabel("Question 1 of 5")
        self.q_num_lbl.setObjectName("Header2")

        self.q_progress = QProgressBar()
        self.q_progress.setRange(0, 5)
        self.q_progress.setValue(1)
        self.q_progress.setFixedHeight(12)

        q_top_bar.addWidget(self.q_num_lbl)
        q_top_bar.addSpacing(20)
        q_top_bar.addWidget(self.q_progress, stretch=1)
        q_layout.addLayout(q_top_bar)

        # Question Text Label
        self.q_text_lbl = QLabel()
        self.q_text_lbl.setWordWrap(True)
        self.q_text_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc; margin-top: 8px;")
        q_layout.addWidget(self.q_text_lbl)

        # Radio Group for Options
        self.button_group = QButtonGroup(self)
        self.radio_options = []
        self.options_container = QVBoxLayout()
        self.options_container.setSpacing(12)

        for i in range(4):
            radio = QRadioButton()
            radio.setCursor(Qt.CursorShape.PointingHandCursor)
            radio.setStyleSheet("font-size: 14px; padding: 8px;")
            self.button_group.addButton(radio, i)
            self.options_container.addWidget(radio)
            self.radio_options.append(radio)

        q_layout.addLayout(self.options_container)

        # Explanation Box
        self.explanation_card = QFrame()
        self.explanation_card.setStyleSheet("background-color: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px;")
        self.explanation_card.setVisible(False)
        exp_layout = QVBoxLayout(self.explanation_card)
        
        self.exp_badge = BadgePill("CORRECT", "safe")
        self.exp_text = QLabel()
        self.exp_text.setWordWrap(True)
        self.exp_text.setStyleSheet("color: #f8fafc; font-size: 13px; line-height: 1.5;")
        
        exp_top = QHBoxLayout()
        exp_top.addWidget(self.exp_badge)
        exp_top.addStretch()
        exp_layout.addLayout(exp_top)
        exp_layout.addWidget(self.exp_text)
        q_layout.addWidget(self.explanation_card)

        # Action Buttons Navigation
        nav_btn_layout = QHBoxLayout()
        self.prev_btn = QPushButton("← Previous")
        self.prev_btn.setObjectName("SecondaryButton")
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.clicked.connect(self.prev_question)

        self.next_btn = QPushButton("Next Question →")
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(self.next_question)

        self.submit_quiz_btn = QPushButton("🏆 Submit Challenge Answers")
        self.submit_quiz_btn.setObjectName("SuccessButton")
        self.submit_quiz_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_quiz_btn.clicked.connect(self.submit_quiz)
        self.submit_quiz_btn.setVisible(False)

        nav_btn_layout.addWidget(self.prev_btn)
        nav_btn_layout.addStretch()
        nav_btn_layout.addWidget(self.next_btn)
        nav_btn_layout.addWidget(self.submit_quiz_btn)
        q_layout.addLayout(nav_btn_layout)

        layout.addWidget(self.q_card)
        layout.addStretch()

        self.load_question(0)
        self.load_db_stats()

    def load_question(self, idx: int):
        self.current_q_idx = idx
        q = QUIZ_QUESTIONS[idx]

        self.q_num_lbl.setText(f"Question {idx + 1} of {len(QUIZ_QUESTIONS)}")
        self.q_progress.setValue(idx + 1)
        self.q_text_lbl.setText(q["question"])

        # Disconnect radio button signals before updating checked states
        self.button_group.blockSignals(True)
        checked_opt = self.user_answers.get(idx, -1)

        for i, option_text in enumerate(q["options"]):
            radio = self.radio_options[i]
            radio.setText(option_text)
            radio.setChecked(i == checked_opt)
            radio.setEnabled(not self.submitted)

        self.button_group.blockSignals(False)

        # Show explanation if already submitted
        if self.submitted:
            self.explanation_card.setVisible(True)
            user_ans = self.user_answers.get(idx, -1)
            correct_ans = q["correct"]

            if user_ans == correct_ans:
                self.exp_badge.set_badge("CORRECT ANSWER", "safe")
            else:
                self.exp_badge.set_badge("INCORRECT ANSWER", "danger")

            self.exp_text.setText(f"<b>Explanation:</b> {q['explanation']}")
        else:
            self.explanation_card.setVisible(False)

        # Buttons state
        self.prev_btn.setEnabled(idx > 0)
        if idx == len(QUIZ_QUESTIONS) - 1:
            self.next_btn.setVisible(False)
            self.submit_quiz_btn.setVisible(not self.submitted)
        else:
            self.next_btn.setVisible(True)
            self.submit_quiz_btn.setVisible(False)

    def save_current_answer(self):
        selected_id = self.button_group.checkedId()
        if selected_id != -1:
            self.user_answers[self.current_q_idx] = selected_id

    def next_question(self):
        self.save_current_answer()
        if self.current_q_idx < len(QUIZ_QUESTIONS) - 1:
            self.load_question(self.current_q_idx + 1)

    def prev_question(self):
        self.save_current_answer()
        if self.current_q_idx > 0:
            self.load_question(self.current_q_idx - 1)

    def submit_quiz(self):
        self.save_current_answer()
        if len(self.user_answers) < len(QUIZ_QUESTIONS):
            QMessageBox.warning(self, "Incomplete Quiz", "Please answer all 5 scenario questions before submitting!")
            return

        self.submitted = True
        correct_count = 0

        for idx, q in enumerate(QUIZ_QUESTIONS):
            if self.user_answers.get(idx) == q["correct"]:
                correct_count += 1

        total = len(QUIZ_QUESTIONS)
        pct = int((correct_count / total) * 100)

        # Assign Badge Level
        if correct_count >= 5:
            badge = "Cyber Master - Level 3"
        elif correct_count >= 3:
            badge = "Security Analyst - Level 2"
        else:
            badge = "Cyber Defender - Level 1"

        # Log to SQLite DB
        self.db.save_quiz_score(correct_count, total, badge)

        # Update KPI Cards
        self.card_score.update_value(f"{correct_count} / {total}", f"{pct}% Accuracy")
        self.card_badge.update_value(badge, "Badge Unlocked!")

        # Reload question view to display explanations
        self.load_question(self.current_q_idx)
        self.load_db_stats()

        QMessageBox.information(
            self,
            "Challenge Completed!",
            f"🎉 Quiz Submitted Successfully!\n\nScore: {correct_count}/{total} ({pct}%)\nBadge Earned: {badge}"
        )

    def restart_quiz(self):
        self.user_answers = {}
        self.submitted = False
        self.card_score.update_value("0 / 5", "0% Accuracy")
        self.card_badge.update_value("Unranked", "Take Quiz")
        self.load_question(0)

    def load_db_stats(self):
        stats = self.db.get_quiz_stats()
        self.card_attempts.update_value(str(stats["total_attempts"]), f"High: {stats['high_score']}/5")
