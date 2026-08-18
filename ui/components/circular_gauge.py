import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QConicalGradient

class CircularProgressWidget(QWidget):
    """
    Futuristic Anti-Aliased Circular Score Gauge for Security Health Scores (0 - 100).
    Renders background track ring, glowing foreground score arc, and centered typography.
    """
    def __init__(self, value: int = 100, title: str = "HEALTH SCORE", parent=None):
        super().__init__(parent)
        self._value = value
        self._title = title
        self.setMinimumSize(140, 140)

    @pyqtProperty(int)
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        self._value = max(0, min(100, int(val)))
        self.update()

    def set_value(self, val: int, title: str = None):
        self._value = max(0, min(100, int(val)))
        if title:
            self._title = title
        self.update()

    def sizeHint(self):
        return QSize(160, 160)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        side = min(width, height)
        
        # Center coordinates & radius
        cx = width / 2.0
        cy = height / 2.0
        margin = 16.0
        radius = (side - margin * 2) / 2.0
        rect = QRectF(cx - radius, cy - radius, radius * 2.0, radius * 2.0)

        pen_width = 12.0

        # 1. Outer Background Track Ring
        track_pen = QPen(QColor(51, 65, 85, 120), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(track_pen)
        painter.drawEllipse(rect)

        # 2. Foreground Score Arc
        if self._value >= 76:
            accent_color = QColor(16, 185, 129)  # Emerald Green
            glow_color = QColor(16, 185, 129, 60)
        elif self._value >= 41:
            accent_color = QColor(245, 158, 11)   # Amber Yellow
            glow_color = QColor(245, 158, 11, 60)
        else:
            accent_color = QColor(239, 68, 68)    # Crimson Red
            glow_color = QColor(239, 68, 68, 60)

        # Draw Glow Ring Underlay
        glow_pen = QPen(glow_color, pen_width + 6.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(glow_pen)
        angle_span = int((-self._value / 100.0) * 360 * 16)
        start_angle = 90 * 16  # Top 12 o'clock
        painter.drawArc(rect, start_angle, angle_span)

        # Draw Main Score Arc
        score_pen = QPen(accent_color, pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(score_pen)
        painter.drawArc(rect, start_angle, angle_span)

        # 3. Center Text (Value + Title)
        font_score = QFont("Segoe UI", 20, QFont.Weight.Bold)
        painter.setFont(font_score)
        painter.setPen(QColor("#f8fafc"))
        score_text = f"{self._value}%" if "HEALTH" in self._title.upper() or "SCORE" in self._title.upper() else f"{self._value}"
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, score_text)

        font_title = QFont("Segoe UI", 8, QFont.Weight.Bold)
        painter.setFont(font_title)
        painter.setPen(QColor("#94a3b8"))
        title_rect = QRectF(rect.x(), rect.y() + radius * 0.55, rect.width(), radius * 0.6)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, self._title.upper())
