"""
CyberGuard 3.0 Pro - Custom QSS Stylesheet (v2 — Elevated)
Modern Glassmorphism Obsidian Dark Theme, Token-Driven Design System,
Electric Cyan Primary Accent, Gradient CTAs, Status Pills, Redaction
Styling, Frameless Window Controls, and Glow-Ready Card Surfaces.

NOTE ON QSS LIMITS: Qt Style Sheets do not support backdrop-filter/blur,
box-shadow, or CSS transitions. True "glow" and blur effects are added
on the Python side via QGraphicsDropShadowEffect (helper provided at the
bottom of this file) and QPropertyAnimation for hover/press motion.
Apply those to widgets that need to visually pop (primary buttons,
active nav item, critical alert cards) — the stylesheet alone gets you
~80% of the way there; the helpers close the gap.
"""

# ---------------------------------------------------------------------------
# DESIGN TOKENS — single source of truth. Change a value here and every
# widget that references it updates. Keeps the whole app visually coherent
# instead of hex codes scattered through 400 lines of QSS.
# ---------------------------------------------------------------------------

PALETTE = {
    # Base surfaces
    "bg_base":        "#0B1120",   # app background — deeper than card surfaces
    "bg_sidebar":      "#0B1120",
    "bg_surface":       "#141B2D",   # cards, panels
    "bg_surface_alt":     "#1A2438",   # hover / elevated surface
    "bg_input":       "#0A0F1C",
    "bg_titlebar":       "#0A0E1A",

    # Borders
    "border":         "rgba(255, 255, 255, 0.08)",
    "border_strong":     "#334155",
    "border_focus":       "#38BDF8",

    # Text
    "text_primary":     "#F8FAFC",
    "text_muted":       "#8B99B0",
    "text_faint":       "#5B6B85",

    # Accents
    "primary":         "#38BDF8",   # electric cyan — informational / brand
    "primary_hover":     "#7DD3FC",
    "primary_press":     "#0284C7",
    "primary_tint":       "rgba(56, 189, 248, 0.12)",

    "success":         "#10B981",   # clean / low risk
    "success_tint":       "rgba(16, 185, 129, 0.14)",

    "warning":         "#F59E0B",   # medium risk
    "warning_tint":       "rgba(245, 158, 11, 0.14)",

    "critical":        "#EF4444",   # high risk / danger
    "critical_tint":      "rgba(239, 68, 68, 0.14)",
}

FONT_UI = "'Inter', 'Segoe UI', -apple-system, Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Cascadia Code', 'Consolas', 'Courier New', monospace"

P = PALETTE  # short alias for the f-string below


DARK_CYBER_STYESHEET = f"""
/* =========================================================
   GLOBAL
   ========================================================= */
QMainWindow, QDialog {{
    background-color: {P['bg_base']};
    color: {P['text_primary']};
    font-family: {FONT_UI};
    font-size: 13px;
}}

QWidget {{
    color: {P['text_primary']};
    font-family: {FONT_UI};
}}

/* =========================================================
   FRAMELESS WINDOW / TITLE BAR
   ========================================================= */
#CustomTitleBar {{
    background-color: {P['bg_titlebar']};
    border-bottom: 1px solid {P['border']};
}}

#WinControlMin, #WinControlMax {{
    background-color: transparent;
    color: {P['text_muted']};
    border: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}}

#WinControlMin:hover, #WinControlMax:hover {{
    background-color: {P['bg_surface_alt']};
    color: {P['primary']};
}}

#WinControlClose {{
    background-color: transparent;
    color: {P['text_muted']};
    border: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}}

#WinControlClose:hover {{
    background-color: {P['critical']};
    color: #ffffff;
}}

/* =========================================================
   SIDEBAR & NAVIGATION
   ========================================================= */
#SidebarFrame {{
    background-color: {P['bg_sidebar']};
    border-right: 1px solid {P['border']};
    min-width: 248px;
    max-width: 248px;
}}

#NavButton {{
    background-color: transparent;
    color: {P['text_muted']};
    border: none;
    border-left: 3px solid transparent;
    border-radius: 8px;
    padding: 11px 16px 11px 13px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
}}

#NavButton:hover {{
    background-color: {P['bg_surface_alt']};
    color: {P['primary']};
}}

#NavButton:checked, #NavButton[active="true"] {{
    background-color: {P['primary_tint']};
    color: {P['primary']};
    font-weight: 800;
    border-left: 3px solid {P['primary']};
}}

#AppTitleLabel {{
    color: {P['primary']};
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
}}

#AppSubtitleLabel {{
    color: {P['text_muted']};
    font-size: 11px;
    font-weight: 500;
}}

/* Sidebar status footer */
#StatusCard {{
    background-color: {P['bg_surface']};
    border: 1px solid {P['border']};
    border-radius: 10px;
    padding: 10px 12px;
}}

#StatusDotOnline {{
    background-color: {P['success']};
    border-radius: 4px;
    min-width: 8px;
    max-width: 8px;
    min-height: 8px;
    max-height: 8px;
}}

#StatusDotOffline {{
    background-color: {P['critical']};
    border-radius: 4px;
    min-width: 8px;
    max-width: 8px;
    min-height: 8px;
    max-height: 8px;
}}

/* =========================================================
   CARDS & CONTENT CONTAINERS
   (scoped to explicit names, NOT every QFrame in the app —
   this avoids accidentally styling nested layout frames)
   ========================================================= */
#CardContainer, .GlassCard {{
    background-color: {P['bg_surface']};
    border: 1px solid {P['border']};
    border-radius: 14px;
}}

#CardContainer:hover, .GlassCard:hover {{
    border: 1px solid {P['border_strong']};
    background-color: {P['bg_surface_alt']};
}}

#CardHeader {{
    color: {P['text_primary']};
    font-size: 15px;
    font-weight: 700;
    border-bottom: 1px solid {P['border']};
    padding-bottom: 8px;
}}

/* Stat card — big number + label pairing */
#StatCardValue {{
    color: {P['text_primary']};
    font-family: {FONT_MONO};
    font-size: 40px;
    font-weight: 700;
    letter-spacing: -1px;
}}

#StatCardLabel {{
    color: {P['text_muted']};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

#StatCardDeltaUp {{
    color: {P['success']};
    font-family: {FONT_MONO};
    font-size: 12px;
    font-weight: 700;
}}

#StatCardDeltaDown {{
    color: {P['critical']};
    font-family: {FONT_MONO};
    font-size: 12px;
    font-weight: 700;
}}

/* =========================================================
   TYPOGRAPHY
   ========================================================= */
#Header1 {{
    font-size: 24px;
    font-weight: 800;
    color: {P['text_primary']};
    letter-spacing: -0.5px;
}}

#Header2 {{
    font-size: 16px;
    font-weight: 700;
    color: {P['primary']};
}}

#TextMuted {{
    color: {P['text_muted']};
    font-size: 13px;
}}

#TextFaint {{
    color: {P['text_faint']};
    font-size: 11px;
}}

/* =========================================================
   TOOLTIPS
   ========================================================= */
QToolTip {{
    background-color: {P['bg_surface']};
    color: {P['text_primary']};
    border: 1px solid {P['primary']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
}}

/* =========================================================
   INFO ICON
   ========================================================= */
#InfoIconLabel {{
    background-color: {P['bg_surface_alt']};
    color: {P['primary']};
    border-radius: 10px;
    font-weight: bold;
    font-size: 11px;
    padding: 2px 6px;
}}

#InfoIconLabel:hover {{
    background-color: {P['primary']};
    color: {P['bg_base']};
}}

/* =========================================================
   STATUS / RISK PILLS — use these instead of plain text
   labels for "High Risk" / "Medium Risk" / "Low Risk" / "Clean"
   ========================================================= */
#BadgeCritical {{
    background-color: {P['critical_tint']};
    color: {P['critical']};
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 11px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

#BadgeWarning {{
    background-color: {P['warning_tint']};
    color: {P['warning']};
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 11px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

#BadgeSuccess {{
    background-color: {P['success_tint']};
    color: {P['success']};
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 11px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

#BadgeInfo {{
    background-color: {P['primary_tint']};
    color: {P['primary']};
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 11px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

/* Redacted / masked value styling — for hidden targets (********) */
#RedactedLabel {{
    background-color: {P['bg_input']};
    color: {P['text_faint']};
    border: 1px solid {P['border']};
    border-radius: 6px;
    padding: 2px 8px;
    font-family: {FONT_MONO};
    font-size: 11px;
    letter-spacing: 2px;
}}

/* =========================================================
   SNIPPET / CODE BOXES
   ========================================================= */
#SnippetBox {{
    background-color: {P['bg_input']};
    border: 1px solid {P['border']};
    border-radius: 8px;
    padding: 10px;
    font-family: {FONT_MONO};
    color: {P['primary']};
}}

#SnippetCopyBtn {{
    background-color: {P['bg_surface_alt']};
    color: {P['text_primary']};
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
}}

#SnippetCopyBtn:hover {{
    background-color: {P['primary']};
    color: {P['bg_base']};
}}

/* =========================================================
   DRAG & DROP
   ========================================================= */
#DropZone {{
    background-color: {P['bg_input']};
    border: 2px dashed {P['primary']};
    border-radius: 14px;
    padding: 30px;
}}

#DropZone[dragOver="true"] {{
    background-color: {P['success_tint']};
    border-color: {P['success']};
}}

/* =========================================================
   INPUTS
   ========================================================= */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
    background-color: {P['bg_input']};
    color: {P['text_primary']};
    border: 1px solid {P['border_strong']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: {P['primary']};
    selection-color: {P['bg_base']};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
    border: 1.5px solid {P['border_focus']};
    background-color: {P['bg_input']};
}}

QLineEdit:disabled, QComboBox:disabled {{
    color: {P['text_faint']};
    border-color: {P['border']};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {P['bg_surface']};
    color: {P['text_primary']};
    selection-background-color: {P['primary']};
    selection-color: {P['bg_base']};
    border: 1px solid {P['border_strong']};
    outline: none;
}}

/* Search / command-bar style input */
#SearchInput {{
    background-color: {P['bg_input']};
    border: 1px solid {P['border']};
    border-radius: 20px;
    padding: 8px 16px;
    color: {P['text_primary']};
    font-size: 13px;
}}

#SearchInput:focus {{
    border: 1.5px solid {P['primary']};
}}

/* =========================================================
   RADIO / CHECKBOX
   ========================================================= */
QRadioButton, QCheckBox {{
    color: {P['text_primary']};
    font-size: 13px;
    spacing: 8px;
}}

QRadioButton::indicator, QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid {P['border_strong']};
    background-color: {P['bg_input']};
}}

QRadioButton::indicator:hover, QCheckBox::indicator:hover {{
    border-color: {P['primary']};
}}

QRadioButton::indicator:checked {{
    background-color: {P['primary']};
    border-color: {P['primary']};
}}

QCheckBox::indicator {{
    border-radius: 4px;
}}

QCheckBox::indicator:checked {{
    background-color: {P['primary']};
    border-color: {P['primary']};
}}

/* =========================================================
   SLIDERS
   ========================================================= */
QSlider::groove:horizontal {{
    border: 1px solid {P['border_strong']};
    height: 6px;
    background: {P['bg_input']};
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: {P['primary']};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {P['text_primary']};
    border: 2px solid {P['primary']};
    width: 16px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {P['primary']};
    border-color: {P['text_primary']};
}}

/* =========================================================
   BUTTONS
   ========================================================= */
QPushButton {{
    background-color: {P['primary']};
    color: {P['bg_base']};
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 700;
}}

QPushButton:hover {{
    background-color: {P['primary_hover']};
}}

QPushButton:pressed {{
    background-color: {P['primary_press']};
}}

QPushButton:disabled {{
    background-color: {P['bg_surface_alt']};
    color: {P['text_faint']};
}}

#SecondaryButton {{
    background-color: {P['bg_surface_alt']};
    color: {P['text_primary']};
    border: 1px solid {P['border_strong']};
}}

#SecondaryButton:hover {{
    background-color: {P['border_strong']};
    color: {P['primary']};
}}

#DangerButton {{
    background-color: {P['critical']};
    color: #ffffff;
}}

#DangerButton:hover {{
    background-color: #f87171;
}}

#SuccessButton {{
    background-color: {P['success']};
    color: #ffffff;
}}

#SuccessButton:hover {{
    background-color: #34d399;
}}

#GhostButton {{
    background-color: transparent;
    color: {P['text_muted']};
    border: 1px solid {P['border']};
}}

#GhostButton:hover {{
    color: {P['primary']};
    border-color: {P['primary']};
}}

/* =========================================================
   PROGRESS BARS — reuse per risk state via object name
   ========================================================= */
QProgressBar {{
    background-color: {P['bg_input']};
    border: 1px solid {P['border_strong']};
    border-radius: 8px;
    text-align: center;
    color: {P['text_primary']};
    font-weight: bold;
    height: 20px;
}}

QProgressBar::chunk {{
    background-color: {P['primary']};
    border-radius: 7px;
}}

#GaugeCritical::chunk {{ background-color: {P['critical']}; }}
#GaugeWarning::chunk  {{ background-color: {P['warning']}; }}
#GaugeSuccess::chunk  {{ background-color: {P['success']}; }}

/* =========================================================
   TABLES
   ========================================================= */
QTableWidget, QTableView {{
    background-color: {P['bg_surface']};
    color: {P['text_primary']};
    gridline-color: rgba(255, 255, 255, 0.04);
    border: 1px solid {P['border']};
    border-radius: 14px;
    selection-background-color: {P['bg_surface_alt']};
    selection-color: {P['primary']};
    alternate-background-color: rgba(255, 255, 255, 0.015);
}}

QTableView::item {{
    padding: 6px 4px;
    border-bottom: 1px solid {P['border']};
}}

QTableView::item:hover {{
    background-color: {P['bg_surface_alt']};
}}

QTableView::item:selected {{
    background-color: {P['primary_tint']};
    color: {P['primary']};
}}

QHeaderView::section {{
    background-color: {P['bg_titlebar']};
    color: {P['text_muted']};
    padding: 10px;
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    border: none;
    border-bottom: 1px solid {P['border']};
}}

/* =========================================================
   LISTS
   ========================================================= */
QListWidget {{
    background-color: {P['bg_input']};
    border: 1px solid {P['border']};
    border-radius: 8px;
    padding: 6px;
    color: {P['text_primary']};
}}

QListWidget::item {{
    padding: 8px;
    border-radius: 6px;
}}

QListWidget::item:hover {{
    background-color: {P['bg_surface_alt']};
}}

QListWidget::item:selected {{
    background-color: {P['primary_tint']};
    color: {P['primary']};
}}

/* =========================================================
   SCROLLBARS
   ========================================================= */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: {P['border_strong']};
    min-height: 24px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background: {P['primary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: {P['border_strong']};
    min-width: 24px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {P['primary']};
}}

/* =========================================================
   TOASTS / NOTIFICATIONS
   ========================================================= */
#ToastSuccess {{
    background-color: {P['bg_surface']};
    border: 1px solid {P['success']};
    border-left: 4px solid {P['success']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {P['text_primary']};
}}

#ToastCritical {{
    background-color: {P['bg_surface']};
    border: 1px solid {P['critical']};
    border-left: 4px solid {P['critical']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {P['text_primary']};
}}

#ToastWarning {{
    background-color: {P['bg_surface']};
    border: 1px solid {P['warning']};
    border-left: 4px solid {P['warning']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {P['text_primary']};
}}

#ToastInfo {{
    background-color: {P['bg_surface']};
    border: 1px solid {P['primary']};
    border-left: 4px solid {P['primary']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {P['text_primary']};
}}

/* =========================================================
   STATUS BAR
   ========================================================= */
QStatusBar {{
    background-color: {P['bg_titlebar']};
    color: {P['text_muted']};
    border-top: 1px solid {P['border']};
}}
"""


# ---------------------------------------------------------------------------
# PYTHON-SIDE COMPANIONS
# QSS can't do blur/glow/shadow or eased motion — these two tiny helpers
# cover the gap for the handful of elements that should visually "pop"
# (primary CTA buttons, the active nav item, critical-risk cards).
# Call them once after constructing the widget.
# ---------------------------------------------------------------------------

def apply_glow(widget, color: str = PALETTE["primary"], blur_radius: int = 24, y_offset: int = 0):
    """Attach a soft colored glow to a widget (button, card, badge).

    Usage:
        from styles import apply_glow, PALETTE
        apply_glow(self.scan_button, PALETTE["primary"])
        apply_glow(self.critical_alert_card, PALETTE["critical"], blur_radius=32)
    """
    from PyQt6.QtWidgets import QGraphicsDropShadowEffect
    from PyQt6.QtGui import QColor

    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur_radius)
    effect.setOffset(0, y_offset)
    qc = QColor(color)
    qc.setAlpha(160)
    effect.setColor(qc)
    widget.setGraphicsEffect(effect)
    return effect


def animate_hover_lift(widget, lift_px: int = 3, duration_ms: int = 150):
    """Attach a subtle upward lift animation on hover for card-like widgets.

    Requires the widget to have a `pos()`-animatable geometry (i.e. it's
    inside a layout that won't fight the animation, or use it on absolutely
    positioned widgets). For layout-managed widgets, animate a `contentsMargins`
    or swap in a QGraphicsEffect-based approach instead — geometry animation
    inside a QLayout will be immediately overridden on the next layout pass.

    Usage:
        from styles import animate_hover_lift
        animate_hover_lift(self.stat_card)
    """
    from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration_ms)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    widget._hover_anim = anim  # keep a reference so it isn't garbage collected

    original_enter = widget.enterEvent
    original_leave = widget.leaveEvent

    def enterEvent(event):
        start = widget.pos()
        anim.stop()
        anim.setStartValue(start)
        anim.setEndValue(start - type(start)(0, lift_px))
        anim.start()
        original_enter(event)

    def leaveEvent(event):
        start = widget.pos()
        anim.stop()
        anim.setStartValue(start)
        anim.setEndValue(start + type(start)(0, lift_px))
        anim.start()
        original_leave(event)

    widget.enterEvent = enterEvent
    widget.leaveEvent = leaveEvent