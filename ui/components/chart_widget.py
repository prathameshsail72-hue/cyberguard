import pyqtgraph as pg
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from config import COLOR_CARD_BG, COLOR_BORDER

# Configure global PyQtGraph Dark Theme for CyberGuard 3.0 Pro
pg.setConfigOption('background', '#1e293b')
pg.setConfigOption('foreground', '#94a3b8')
pg.setConfigOptions(antialias=True)

class AnalyticsChartWidget(QFrame):
    """
    Real-Time Analytics Bar Chart Widget using PyQtGraph.
    """
    def __init__(self, title: str = "Scan History & Risk Distribution"):
        super().__init__()
        self.init_ui(title)

    def init_ui(self, title: str):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 10px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #f8fafc; font-size: 14px; font-weight: bold; border: none;")
        layout.addWidget(title_lbl)

        # Plot Widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True, alpha=0.15)
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen('#334155'))
        self.plot_widget.getAxis('left').setPen(pg.mkPen('#334155'))
        
        layout.addWidget(self.plot_widget)

    def update_risk_bar_chart(self, low: int, medium: int, high: int):
        self.plot_widget.clear()
        
        # Color bars: Low (Green #10b981), Medium (Amber #f59e0b), High (Red #ef4444)
        bg1 = pg.BarGraphItem(x=[1], height=[low], width=0.55, brush='#10b981', pen='#10b981')
        bg2 = pg.BarGraphItem(x=[2], height=[medium], width=0.55, brush='#f59e0b', pen='#f59e0b')
        bg3 = pg.BarGraphItem(x=[3], height=[high], width=0.55, brush='#ef4444', pen='#ef4444')

        self.plot_widget.addItem(bg1)
        self.plot_widget.addItem(bg2)
        self.plot_widget.addItem(bg3)

        ax = self.plot_widget.getAxis('bottom')
        ticks = [list(zip([1, 2, 3], ['Low Risk', 'Medium Risk', 'High Risk']))]
        ax.setTicks(ticks)

    def update_survey_chart(self, categories: list, phishing_scores: list, password_scores: list):
        self.plot_widget.clear()
        if not categories:
            return

        x = list(range(1, len(categories) + 1))
        
        bg_phish = pg.BarGraphItem(x=[i - 0.15 for i in x], height=phishing_scores, width=0.3, brush='#38bdf8', pen='#38bdf8', name='Phishing Awareness')
        bg_pass = pg.BarGraphItem(x=[i + 0.15 for i in x], height=password_scores, width=0.3, brush='#60a5fa', pen='#60a5fa', name='Password Habits')

        self.plot_widget.addItem(bg_phish)
        self.plot_widget.addItem(bg_pass)

        ax = self.plot_widget.getAxis('bottom')
        ticks = [list(zip(x, categories))]
        ax.setTicks(ticks)
