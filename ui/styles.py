"""
CyberGuard 3.0 Pro - Custom QSS Stylesheet
Modern Glassmorphism Obsidian Dark Theme (#0F172A),
Subtle Rounded Glass Borders (12px), Electric Cyan Accents (#38BDF8),
Frameless Window Control Styling, and Glowing Badges.
"""

DARK_CYBER_STYESHEET = """
/* Global Application Styling */
QMainWindow, QDialog {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: 'Segoe UI', -apple-system, Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
}

QWidget {
    color: #f8fafc;
    font-family: 'Segoe UI', -apple-system, Roboto, Helvetica, Arial, sans-serif;
}

/* Frameless Window Custom Title Bar */
#CustomTitleBar {
    background-color: #0b1329;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

#WinControlMin, #WinControlMax {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

#WinControlMin:hover, #WinControlMax:hover {
    background-color: #334155;
    color: #38bdf8;
}

#WinControlClose {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

#WinControlClose:hover {
    background-color: #ef4444;
    color: #ffffff;
}

/* Sidebar & Navigation */
#SidebarFrame {
    background-color: #0b1329;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    min-width: 240px;
    max-width: 240px;
}

#NavButton {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
}

#NavButton:hover {
    background-color: rgba(51, 65, 85, 0.6);
    color: #38bdf8;
}

#NavButton:checked, #NavButton[active="true"] {
    background-color: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    font-weight: 800;
    border-left: 4px solid #38bdf8;
}

#AppTitleLabel {
    color: #38bdf8;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
}

#AppSubtitleLabel {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 500;
}

/* Cards & Content Containers */
.QFrame, #CardContainer {
    background-color: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}

#CardHeader {
    color: #f8fafc;
    font-size: 15px;
    font-weight: 700;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 8px;
}

/* Typography Header Tags */
#Header1 {
    font-size: 22px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.5px;
}

#Header2 {
    font-size: 16px;
    font-weight: 700;
    color: #38bdf8;
}

#TextMuted {
    color: #94a3b8;
    font-size: 13px;
}

/* Tooltips */
QToolTip {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #38bdf8;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
}

/* Info Icon Widget */
#InfoIconLabel {
    background-color: #334155;
    color: #38bdf8;
    border-radius: 10px;
    font-weight: bold;
    font-size: 11px;
    padding: 2px 6px;
}

#InfoIconLabel:hover {
    background-color: #38bdf8;
    color: #0f172a;
}

/* Snippet Code Boxes */
#SnippetBox {
    background-color: #090d16;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    color: #38bdf8;
}

#SnippetCopyBtn {
    background-color: #334155;
    color: #f8fafc;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
}

#SnippetCopyBtn:hover {
    background-color: #38bdf8;
    color: #0f172a;
}

/* Drag and Drop Box */
#DropZone {
    background-color: #090d16;
    border: 2px dashed #38bdf8;
    border-radius: 12px;
    padding: 30px;
    text-align: center;
}

#DropZone:hover, #DropZone[dragOver="true"] {
    background-color: rgba(16, 185, 129, 0.1);
    border-color: #10b981;
}

/* Input Fields & Text Edits */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
    background-color: #090d16;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: #38bdf8;
    selection-color: #0f172a;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
    border: 1px solid #38bdf8;
    background-color: #090d16;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    color: #f8fafc;
    selection-background-color: #38bdf8;
    selection-color: #0f172a;
    border: 1px solid #334155;
}

/* Radio Buttons & Checkboxes */
QRadioButton, QCheckBox {
    color: #f8fafc;
    font-size: 13px;
    spacing: 8px;
}

QRadioButton::indicator, QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #334155;
    background-color: #090d16;
}

QRadioButton::indicator:checked {
    background-color: #38bdf8;
    border-color: #38bdf8;
}

QCheckBox::indicator {
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #38bdf8;
    border-color: #38bdf8;
}

/* Sliders */
QSlider::groove:horizontal {
    border: 1px solid #334155;
    height: 8px;
    background: #090d16;
    border-radius: 4px;
}

QSlider::sub-page:horizontal {
    background: #38bdf8;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #f8fafc;
    border: 2px solid #38bdf8;
    width: 18px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #38bdf8;
    border-color: #f8fafc;
}

/* Buttons */
QPushButton {
    background-color: #38bdf8;
    color: #0f172a;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 700;
}

QPushButton:hover {
    background-color: #7dd3fc;
}

QPushButton:pressed {
    background-color: #0284c7;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
}

#SecondaryButton {
    background-color: #334155;
    color: #f8fafc;
    border: 1px solid #475569;
}

#SecondaryButton:hover {
    background-color: #475569;
    color: #38bdf8;
}

#DangerButton {
    background-color: #ef4444;
    color: #ffffff;
}

#DangerButton:hover {
    background-color: #f87171;
}

#SuccessButton {
    background-color: #10b981;
    color: #ffffff;
}

#SuccessButton:hover {
    background-color: #34d399;
}

/* Progress Bars */
QProgressBar {
    background-color: #090d16;
    border: 1px solid #334155;
    border-radius: 8px;
    text-align: center;
    color: #f8fafc;
    font-weight: bold;
    height: 22px;
}

QProgressBar::chunk {
    background-color: #38bdf8;
    border-radius: 7px;
}

/* Table Views */
QTableWidget, QTableView {
    background-color: #1e293b;
    color: #f8fafc;
    gridline-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    selection-background-color: #334155;
    selection-color: #38bdf8;
}

QHeaderView::section {
    background-color: #0b1329;
    color: #94a3b8;
    padding: 10px;
    font-weight: bold;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

/* List Widgets */
QListWidget {
    background-color: #090d16;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 6px;
    color: #f8fafc;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1e293b;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #0b1329;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #38bdf8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Status Bar */
QStatusBar {
    background-color: #0b1329;
    color: #94a3b8;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}
"""
