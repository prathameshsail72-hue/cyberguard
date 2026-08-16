from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class InfoIcon(QLabel):
    """
    Hover Tooltip Icon (?) displaying 1-sentence explanations of complex technical terms on hover.
    """
    def __init__(self, tooltip_text: str, label_text: str = "?"):
        super().__init__(label_text)
        self.setObjectName("InfoIconLabel")
        self.setToolTip(tooltip_text)
        self.setCursor(Qt.CursorShape.WhatsThisCursor)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(20, 20)
