from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from ui.components.stat_card import StatCard
from ui.components.chart_widget import AnalyticsChartWidget
from ui.components.info_tooltip import InfoIcon
from ui.components.circular_gauge import CircularProgressWidget
from ui.components.terminal_log import TerminalLogWidget
from database.db_manager import DatabaseManager
from config import COLOR_ACCENT_CYAN, COLOR_ACCENT_BLUE, COLOR_RISK_HIGH, COLOR_RISK_LOW

class DashboardView(QWidget):
    """
    Security Operations & Threat Analytics Dashboard for CyberGuard 3.0 Pro.
    Integrates Circular Score Gauge, Glassmorphic KPI cards, PyQtGraph Threat Charts,
    and Live Monospaced Terminal Feed.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header Title
        header_layout = QHBoxLayout()
        title = QLabel("Security Operations & Threat Analytics")
        title.setObjectName("Header1")

        info_icon = InfoIcon("Overview of system scan logs, threat level distributions, and database historical records.")

        refresh_btn = QPushButton("🔄 Refresh Analytics")
        refresh_btn.setObjectName("SecondaryButton")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_data)

        header_layout.addWidget(title)
        header_layout.addWidget(info_icon)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        layout.addLayout(header_layout)

        # KPI Section: Circular Gauge + Stat Cards Row
        top_kpi_layout = QHBoxLayout()
        top_kpi_layout.setSpacing(16)

        # Circular Gauge Widget Card
        gauge_card = QFrame()
        gauge_card.setObjectName("CardContainer")
        gauge_layout = QVBoxLayout(gauge_card)
        gauge_layout.setContentsMargins(12, 12, 12, 12)
        gauge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.health_gauge = CircularProgressWidget(100, "HEALTH SCORE")
        gauge_layout.addWidget(self.health_gauge)
        top_kpi_layout.addWidget(gauge_card)

        # Stat Cards Grid
        self.kpi_grid_layout = QHBoxLayout()
        self.card_total = StatCard("Total Scans Run", "0", "All modules", COLOR_ACCENT_CYAN)
        self.card_avg = StatCard("Average Score", "100%", "Overall status", COLOR_RISK_LOW)
        self.card_high_risk = StatCard("High Risk Threats", "0", "Action required", COLOR_RISK_HIGH)
        self.card_recent = StatCard("Last Target Scanned", "None", "System active", COLOR_ACCENT_BLUE)

        self.kpi_grid_layout.addWidget(self.card_total)
        self.kpi_grid_layout.addWidget(self.card_avg)
        self.kpi_grid_layout.addWidget(self.card_high_risk)
        self.kpi_grid_layout.addWidget(self.card_recent)

        top_kpi_layout.addLayout(self.kpi_grid_layout, stretch=1)
        layout.addLayout(top_kpi_layout)

        # Middle Section: Interactive Chart & Live Terminal Log Feed
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(20)

        self.chart_widget = AnalyticsChartWidget("Threat Level Distribution (Low / Med / High)")
        middle_layout.addWidget(self.chart_widget, stretch=5)

        self.terminal_log = TerminalLogWidget("Live AI Audit Stream")
        self.terminal_log.setMinimumHeight(240)
        middle_layout.addWidget(self.terminal_log, stretch=4)

        layout.addLayout(middle_layout)

        # Bottom Section: Recent Scan Logs Table
        table_header = QHBoxLayout()
        table_title = QLabel("Recent Security Scan Log History")
        table_title.setObjectName("Header2")
        table_header.addWidget(table_title)
        table_header.addWidget(InfoIcon("Logs are stored permanently in local database cyberguard_desktop.db."))
        table_header.addStretch()
        layout.addLayout(table_header)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Target / Subject", "Scan Type", "Risk Score", "Risk Level", "Timestamp"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        stats = self.db.get_dashboard_stats()

        self.card_total.update_value(str(stats["total_scans"]), "Logged scans")
        
        avg_score_int = int(round(stats['avg_score'] or 100))
        self.card_avg.update_value(f"{stats['avg_score']}/100", "Health score")
        self.health_gauge.set_value(avg_score_int, "HEALTH SCORE")

        self.card_high_risk.update_value(str(stats["high_risk_count"]), "Critical issues")

        recent_scans = stats.get("recent_scans", [])
        if recent_scans:
            last_target = recent_scans[0]["target"]
            if len(last_target) > 20:
                last_target = last_target[:20] + "..."
            self.card_recent.update_value(last_target, recent_scans[0]["scan_type"])
        else:
            self.card_recent.update_value("No scans yet", "System idle")

        # Update Chart
        self.chart_widget.update_risk_bar_chart(
            stats["low_risk_count"],
            stats["medium_risk_count"],
            stats["high_risk_count"]
        )

        # Update Table
        self.table.setRowCount(len(recent_scans))
        for row, scan in enumerate(recent_scans):
            self.table.setItem(row, 0, QTableWidgetItem(str(scan["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(scan["target"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(scan["scan_type"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{scan['risk_score']}/100"))

            level_item = QTableWidgetItem(f"[ {str(scan['risk_level']).upper()} ]")
            if scan["risk_level"] == "High Risk":
                level_item.setForeground(Qt.GlobalColor.red)
            elif scan["risk_level"] == "Medium Risk":
                level_item.setForeground(Qt.GlobalColor.yellow)
            else:
                level_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(row, 4, level_item)

            self.table.setItem(row, 5, QTableWidgetItem(str(scan["scanned_at"] or "")))

        # Add terminal log entry for refresh
        self.terminal_log.log(f"Analytics refreshed. Total scans: {stats['total_scans']}, Avg Score: {stats['avg_score']}/100.", "INFO")
