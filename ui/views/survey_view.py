from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QFrame, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from ui.components.chart_widget import AnalyticsChartWidget
from ui.components.info_tooltip import InfoIcon
from ui.components.badge_pill import BadgePill

DEMOGRAPHIC_OPTIONS = [
    ("Student / Educator", "Schools, universities, and academic research institutions"),
    ("Corporate Employee", "Enterprise workplaces, financial services, and commercial sectors"),
    ("IT Professional", "Software engineers, system administrators, and security specialists"),
    ("Senior Citizen", "Retired individuals and digital literacy program participants"),
    ("General Public", "Independent consumers, freelancers, and home network users")
]

class SurveyView(QWidget):
    """
    Revamped Awareness Survey Module with Radio Demographics, Custom Sliders, and Live Benchmark Charting.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title with Tooltip
        header_top = QHBoxLayout()
        title = QLabel("Cybersecurity Awareness & Community Benchmark Survey")
        title.setObjectName("Header1")

        info_icon = InfoIcon(
            "Community benchmarks aggregate self-reported security habits to highlight vulnerability gaps "
            "across demographic user categories."
        )

        header_top.addWidget(title)
        header_top.addWidget(info_icon)
        header_top.addStretch()
        layout.addLayout(header_top)

        subtitle = QLabel("Submit your security habits metrics to benchmark awareness levels against community averages in real time.")
        subtitle.setObjectName("TextMuted")
        layout.addWidget(subtitle)

        # Form & Live Graph Side-by-Side
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # Left Column: Dynamic Multi-Step Survey Form Container
        form_card = QFrame()
        form_card.setObjectName("CardContainer")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(22, 22, 22, 22)
        form_layout.setSpacing(16)

        form_title = QLabel("1. Demographic Selection & Self-Assessment")
        form_title.setObjectName("CardHeader")
        form_layout.addWidget(form_title)

        # Demographic Radio Selection
        demo_lbl_layout = QHBoxLayout()
        demo_lbl_layout.addWidget(QLabel("Select Demographic Group:"))
        demo_lbl_layout.addWidget(InfoIcon("Select your primary workplace or personal user category for community comparison."))
        demo_lbl_layout.addStretch()
        form_layout.addLayout(demo_lbl_layout)

        self.demo_group = QButtonGroup(self)
        self.radio_list = []

        demo_options_layout = QVBoxLayout()
        demo_options_layout.setSpacing(8)

        for idx, (label_text, tooltip_text) in enumerate(DEMOGRAPHIC_OPTIONS):
            radio = QRadioButton(label_text)
            radio.setToolTip(tooltip_text)
            radio.setCursor(Qt.CursorShape.PointingHandCursor)
            if idx == 0:
                radio.setChecked(True)
            self.demo_group.addButton(radio, idx)
            demo_options_layout.addWidget(radio)
            self.radio_list.append(radio)

        form_layout.addLayout(demo_options_layout)
        form_layout.addSpacing(10)

        # Phishing Awareness Slider
        phish_lbl_layout = QHBoxLayout()
        phish_lbl_layout.addWidget(QLabel("2. Phishing Awareness Score:"))
        phish_lbl_layout.addWidget(InfoIcon("How confident are you in identifying phishing links and social engineering emails? (0 = Low, 100 = Expert)"))
        phish_lbl_layout.addStretch()

        self.phish_val_lbl = QLabel("75 / 100")
        self.phish_val_lbl.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 14px;")
        phish_lbl_layout.addWidget(self.phish_val_lbl)
        form_layout.addLayout(phish_lbl_layout)

        self.phish_slider = QSlider(Qt.Orientation.Horizontal)
        self.phish_slider.setRange(0, 100)
        self.phish_slider.setValue(75)
        self.phish_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.phish_slider.valueChanged.connect(lambda v: self.phish_val_lbl.setText(f"{v} / 100"))
        form_layout.addWidget(self.phish_slider)

        form_layout.addSpacing(10)

        # Password Hygiene Slider
        pass_lbl_layout = QHBoxLayout()
        pass_lbl_layout.addWidget(QLabel("3. Password Hygiene Score:"))
        pass_lbl_layout.addWidget(InfoIcon("How strictly do you follow unique high-entropy password habits and use password managers? (0 = Weak, 100 = Expert)"))
        pass_lbl_layout.addStretch()

        self.pass_val_lbl = QLabel("80 / 100")
        self.pass_val_lbl.setStyleSheet("color: #60a5fa; font-weight: bold; font-size: 14px;")
        pass_lbl_layout.addWidget(self.pass_val_lbl)
        form_layout.addLayout(pass_lbl_layout)

        self.pass_slider = QSlider(Qt.Orientation.Horizontal)
        self.pass_slider.setRange(0, 100)
        self.pass_slider.setValue(80)
        self.pass_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pass_slider.valueChanged.connect(lambda v: self.pass_val_lbl.setText(f"{v} / 100"))
        form_layout.addWidget(self.pass_slider)

        form_layout.addSpacing(14)

        # Submit Button
        self.submit_btn = QPushButton("🚀 Submit Survey Response & Update Chart")
        self.submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self.submit_survey)
        form_layout.addWidget(self.submit_btn)
        form_layout.addStretch()

        main_layout.addWidget(form_card, stretch=1)

        # Right Column: Live Benchmark Graph Widget
        self.chart_widget = AnalyticsChartWidget("Community Benchmark Scores by User Category")
        main_layout.addWidget(self.chart_widget, stretch=2)

        layout.addLayout(main_layout)
        self.load_analytics()

    def submit_survey(self):
        selected_id = self.demo_group.checkedId()
        category = DEMOGRAPHIC_OPTIONS[selected_id][0] if selected_id != -1 else "General Public"

        phish_score = self.phish_slider.value()
        pass_score = self.pass_slider.value()

        # Save to SQLite DB
        self.db.save_survey_response(category, phish_score, pass_score)

        # Immediately Update Live Benchmark Chart
        self.load_analytics()

        QMessageBox.information(
            self,
            "Survey Submitted",
            f"✅ Survey Response Recorded Successfully!\n\nCategory: {category}\nPhishing Awareness: {phish_score}/100\nPassword Hygiene: {pass_score}/100\n\nThe community benchmark graph has been updated."
        )

    def load_analytics(self):
        analytics = self.db.get_survey_analytics()
        categories = [item["user_category"] for item in analytics]
        phishing_scores = [item["avg_phishing"] for item in analytics]
        password_scores = [item["avg_password"] for item in analytics]

        self.chart_widget.update_survey_chart(categories, phishing_scores, password_scores)
