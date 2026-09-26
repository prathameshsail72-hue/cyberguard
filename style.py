"""
style.py
================================================================================
CyberGuard 3.0 Pro — Design System Module
--------------------------------------------------------------------------------
Centralizes all CSS (Cyberpunk / Dark Obsidian Glassmorphism) and reusable
HTML component renderers (live telemetry bar, radar-scan loader, pulse
badges) so app.py can stay focused on application logic.

Usage in app.py:

    from style import (
        load_css,
        render_system_status_bar,
        render_telemetry_pills,
        radar_scan_html,
        pulse_badge_html,
    )

    load_css()                        # inject once, near the top
    render_system_status_bar()        # under the header banner
    render_telemetry_pills()          # live-feed / latency / engine pills
================================================================================
"""

import random
import time
import streamlit as st

# =============================================================================
# CSS DESIGN TOKENS + FULL STYLE SHEET
# =============================================================================
CSS_STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        --bg-base: #020617;
        --bg-surface: rgba(15, 23, 42, 0.75);
        --bg-surface-solid: #0f172a;
        --bg-surface-hover: rgba(30, 41, 59, 0.85);
        --bg-card: #1e293b;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.16);
        --border-glow: rgba(56, 189, 248, 0.4);
        --text-primary: #f8fafc;
        --text-muted: #94a3b8;
        --text-faint: #64748b;
        --primary: #38bdf8;
        --primary-glow: rgba(56, 189, 248, 0.35);
        --accent-violet: #818cf8;
        --success: #22c55e;
        --warning: #f59e0b;
        --critical: #ef4444;
        --font-ui: 'Inter', system-ui, -apple-system, sans-serif;
        --font-mono: 'JetBrains Mono', 'Consolas', monospace;
    }

    /* -------------------------------------------------------------------
       Base app surface + animated cyber-grid background
       ------------------------------------------------------------------- */
    .stApp {
        background-color: var(--bg-base);
        color: var(--text-primary);
        font-family: var(--font-ui);
        background-image:
            linear-gradient(rgba(56, 189, 248, 0.055) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.055) 1px, transparent 1px),
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(56, 189, 248, 0.12), transparent),
            radial-gradient(ellipse 60% 40% at 85% 65%, rgba(129, 140, 248, 0.08), transparent);
        background-size: 42px 42px, 42px 42px, 100% 100%, 100% 100%;
        animation: gridDrift 18s linear infinite;
    }

    @keyframes gridDrift {
        0%   { background-position: 0 0, 0 0, 0 0, 0 0; }
        100% { background-position: 42px 42px, 42px 42px, 0 0, 0 0; }
    }

    @keyframes pulseGreen {
        0%   { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.65); }
        70%  { box-shadow: 0 0 0 9px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    @keyframes pulseRed {
        0%   { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.65); }
        70%  { box-shadow: 0 0 0 9px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    @keyframes pulseAmber {
        0%   { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.65); }
        70%  { box-shadow: 0 0 0 9px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes sheen {
        0%   { transform: translateX(-160%) skewX(-15deg); }
        100% { transform: translateX(220%) skewX(-15deg); }
    }
    @keyframes radarSpin {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }
    @keyframes radarPing {
        0%   { transform: scale(0.25); opacity: 0.85; }
        100% { transform: scale(1.7); opacity: 0; }
    }
    @keyframes blinkCursor {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0; }
    }

    /* -------------------------------------------------------------------
       Header Banner
       ------------------------------------------------------------------- */
    .header-banner {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e293b 100%);
        border: 1px solid var(--border-glow);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 14px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .header-title {
        color: var(--primary);
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        text-shadow: 0 0 20px var(--primary-glow);
    }
    .header-subtitle {
        color: var(--text-muted);
        font-size: 1rem;
        margin-top: 6px;
        letter-spacing: 0.2px;
    }

    /* -------------------------------------------------------------------
       Live System Status Bar + Telemetry Pills
       ------------------------------------------------------------------- */
    .system-status-bar {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(2, 6, 23, 0.7);
        border: 1px solid rgba(34, 197, 94, 0.35);
        border-radius: 10px;
        padding: 9px 16px;
        margin-bottom: 14px;
        font-family: var(--font-mono);
        font-size: 0.8rem;
        font-weight: 700;
        color: #4ade80;
        letter-spacing: 0.4px;
        box-shadow: 0 0 18px rgba(34, 197, 94, 0.08);
    }
    .status-beacon {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--success);
        animation: pulseGreen 1.8s infinite;
        flex-shrink: 0;
    }
    .status-cursor {
        display: inline-block;
        width: 7px;
        margin-left: 2px;
        color: #4ade80;
        animation: blinkCursor 1s steps(1) infinite;
    }

    .telemetry-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 22px;
    }
    .telemetry-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 6px 14px;
        font-family: var(--font-mono);
        font-size: 0.76rem;
        font-weight: 600;
        color: var(--text-muted);
        backdrop-filter: blur(10px);
        transition: all 0.2s ease;
    }
    .telemetry-pill:hover {
        border-color: var(--border-glow);
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.18);
    }
    .telemetry-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .telemetry-dot.green  { background: var(--success); box-shadow: 0 0 8px var(--success); animation: pulseGreen 2s infinite; }
    .telemetry-dot.red    { background: var(--critical); box-shadow: 0 0 8px var(--critical); animation: pulseRed 2s infinite; }
    .telemetry-dot.amber  { background: var(--warning); box-shadow: 0 0 8px var(--warning); animation: pulseAmber 2s infinite; }
    .telemetry-dot.cyan   { background: var(--primary); box-shadow: 0 0 8px var(--primary); }

    /* -------------------------------------------------------------------
       Metric Cards (animated glow sheen on hover)
       ------------------------------------------------------------------- */
    .metric-card {
        position: relative;
        background: var(--bg-surface);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        margin-bottom: 12px;
        overflow: hidden;
        transition: transform 200ms ease, border-color 200ms ease, box-shadow 200ms ease;
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 60%; height: 100%;
        background: linear-gradient(100deg, transparent, rgba(56, 189, 248, 0.12), transparent);
        transform: translateX(-160%) skewX(-15deg);
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--primary);
        box-shadow: 0 0 22px rgba(56, 189, 248, 0.4), 0 12px 28px rgba(0, 0, 0, 0.35);
    }
    .metric-card:hover::before {
        animation: sheen 1s ease forwards;
    }
    .metric-label {
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-val {
        font-family: var(--font-mono);
        font-size: 2.1rem;
        font-weight: 800;
        margin-top: 4px;
    }

    /* -------------------------------------------------------------------
       Feature Cards
       ------------------------------------------------------------------- */
    .guide-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid var(--border-glow);
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .feature-card {
        position: relative;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
        transition: all 0.22s ease;
    }
    .feature-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 55%; height: 100%;
        background: linear-gradient(100deg, transparent, rgba(56, 189, 248, 0.1), transparent);
        transform: translateX(-160%) skewX(-15deg);
        pointer-events: none;
    }
    .feature-card:hover {
        border-color: var(--primary);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.35), 0 6px 20px rgba(56, 189, 248, 0.15);
        transform: translateY(-3px);
    }
    .feature-card:hover::before {
        animation: sheen 1s ease forwards;
    }
    .feature-title {
        color: #f8fafc;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .feature-desc {
        color: #94a3b8;
        font-size: 0.88rem;
        line-height: 1.45;
        margin-bottom: 12px;
        flex-grow: 1;
    }

    /* -------------------------------------------------------------------
       Status / Risk Badges (static + pulsing variants)
       ------------------------------------------------------------------- */
    .badge-high, .badge-med, .badge-low {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.82rem;
    }
    .badge-high { background-color: rgba(239, 68, 68, 0.16); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-med  { background-color: rgba(245, 158, 11, 0.16); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-low  { background-color: rgba(34, 197, 94, 0.16); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }

    .badge-pulse-red, .badge-pulse-green, .badge-pulse-amber {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 4px 13px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.82rem;
        font-family: var(--font-mono);
        letter-spacing: 0.3px;
    }
    .badge-pulse-red   { background-color: rgba(239, 68, 68, 0.14); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.5); }
    .badge-pulse-green { background-color: rgba(34, 197, 94, 0.14); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.5); }
    .badge-pulse-amber { background-color: rgba(245, 158, 11, 0.14); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); }
    .badge-pulse-red .dot   { width: 7px; height: 7px; border-radius: 50%; background: var(--critical); animation: pulseRed 1.6s infinite; }
    .badge-pulse-green .dot{ width: 7px; height: 7px; border-radius: 50%; background: var(--success); animation: pulseGreen 1.6s infinite; }
    .badge-pulse-amber .dot{ width: 7px; height: 7px; border-radius: 50%; background: var(--warning); animation: pulseAmber 1.6s infinite; }

    .content-box {
        background: #0f172a;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* -------------------------------------------------------------------
       Threat Intel & Helpline Cards
       ------------------------------------------------------------------- */
    .threat-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid var(--critical);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }
    .threat-card:hover { transform: translateX(3px); box-shadow: 0 0 18px rgba(56, 189, 248, 0.18), 0 8px 22px rgba(0, 0, 0, 0.4); }
    .threat-card.major { border-left-color: var(--warning); }
    .threat-card.alert { border-left-color: #facc15; }
    .threat-meta-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-top: 10px; }
    .threat-meta-item { background: rgba(2, 6, 23, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; padding: 8px 12px; }
    .threat-meta-label { color: #64748b; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .threat-meta-val { color: #e2e8f0; font-size: 0.85rem; font-weight: 600; margin-top: 2px; }
    .sev-critical { display: inline-block; background-color: rgba(239, 68, 68, 0.18); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.45); padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; }
    .sev-major    { display: inline-block; background-color: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.45); padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; }
    .sev-alert    { display: inline-block; background-color: rgba(250, 204, 21, 0.18); color: #fde047; border: 1px solid rgba(250, 204, 21, 0.45); padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; }

    .helpline-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .helpline-number { font-family: var(--font-mono); font-size: 2.4rem; font-weight: 800; color: #4ade80; letter-spacing: 1px; }
    .golden-hour-box { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 10px; padding: 14px 18px; margin-top: 10px; }

    /* -------------------------------------------------------------------
       Radar Scan Loader (shown while a scan/audit is running)
       ------------------------------------------------------------------- */
    .radar-scan-wrap {
        display: flex;
        align-items: center;
        gap: 22px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid var(--border-glow);
        border-radius: 14px;
        padding: 18px 24px;
        margin: 12px 0 18px 0;
        box-shadow: 0 0 24px rgba(56, 189, 248, 0.15);
    }
    .radar-scope {
        position: relative;
        width: 64px;
        height: 64px;
        flex-shrink: 0;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, rgba(2, 6, 23, 0.9) 70%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        overflow: hidden;
    }
    .radar-ring {
        position: absolute;
        top: 50%; left: 50%;
        width: 10px; height: 10px;
        margin: -5px 0 0 -5px;
        border-radius: 50%;
        border: 1px solid rgba(56, 189, 248, 0.7);
        animation: radarPing 2s cubic-bezier(0, 0.2, 0.8, 1) infinite;
    }
    .radar-ring.d2 { animation-delay: 0.6s; }
    .radar-ring.d3 { animation-delay: 1.2s; }
    .radar-sweep {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: conic-gradient(from 0deg, rgba(56, 189, 248, 0.55), transparent 35%);
        animation: radarSpin 1.4s linear infinite;
        border-radius: 50%;
    }
    .radar-copy { display: flex; flex-direction: column; gap: 4px; }
    .radar-title { font-family: var(--font-mono); font-weight: 700; color: var(--primary); font-size: 0.95rem; letter-spacing: 0.4px; }
    .radar-sub { color: var(--text-muted); font-size: 0.8rem; font-family: var(--font-mono); }

    /* -------------------------------------------------------------------
       Streamlit-native element overrides (progress bar, tables, tabs)
       ------------------------------------------------------------------- */
    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #0284c7, #38bdf8, #818cf8, #38bdf8, #0284c7);
        background-size: 300% 100%;
        animation: gradientShift 2.5s ease infinite;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.6);
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border-glow) !important;
        border-radius: 10px !important;
        overflow: hidden;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.08);
    }
    button[data-baseweb="tab"] {
        font-family: var(--font-mono) !important;
        font-weight: 700 !important;
    }

    /* -------------------------------------------------------------------
       Cyberpunk Navigation Radio Bar
       ------------------------------------------------------------------- */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 22px;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 8px 16px !important;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.92rem;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        margin: 0;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.25);
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(30, 41, 59, 0.9) 100%) !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.5);
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] input[type="radio"] { display: none; }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child { display: none; }

    /* -------------------------------------------------------------------
       Buttons & Inputs
       ------------------------------------------------------------------- */
    .stButton > button {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(30, 41, 59, 0.8) 100%);
        color: #f8fafc;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.22s ease-in-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .stButton > button:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
        color: #38bdf8;
    }
    .stLinkButton > a {
        transition: all 0.22s ease-in-out;
    }
    .stLinkButton > a:hover {
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
    }
    .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.45) !important;
    }
</style>
"""


def load_css() -> None:
    """Inject the full CyberGuard design system stylesheet. Call once, early."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


# =============================================================================
# REUSABLE HTML COMPONENTS
# =============================================================================
def render_system_status_bar() -> None:
    """Pulsing 'SYSTEM ONLINE' beacon bar, meant to sit under the header."""
    st.markdown(
        """
        <div class="system-status-bar">
            <span class="status-beacon"></span>
            SYSTEM ONLINE // REAL-TIME MONITORING ACTIVE
            <span class="status-cursor">▍</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_telemetry_pills(latency_ms: int | None = None) -> None:
    """
    Row of simulated live-status pills: threat feed, latency, engine state.
    latency_ms: pass a value to keep it stable across a rerun; otherwise a
    plausible value is generated for display purposes only.
    """
    if latency_ms is None:
        latency_ms = random.randint(8, 26)

    st.markdown(
        f"""
        <div class="telemetry-row">
            <span class="telemetry-pill"><span class="telemetry-dot red"></span> Live Threat Feed: Active</span>
            <span class="telemetry-pill"><span class="telemetry-dot green"></span> Latency: {latency_ms}ms</span>
            <span class="telemetry-pill"><span class="telemetry-dot cyan"></span> Engine: Operational</span>
            <span class="telemetry-pill"><span class="telemetry-dot amber"></span> Sync: {time.strftime('%H:%M:%S')}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def radar_scan_html(title: str = "SCANNING TARGET", subtitle: str = "Running security analysis engine...") -> str:
    """Returns the HTML for a radar-scan loader card (render via st.markdown)."""
    return f"""
    <div class="radar-scan-wrap">
        <div class="radar-scope">
            <div class="radar-sweep"></div>
            <div class="radar-ring"></div>
            <div class="radar-ring d2"></div>
            <div class="radar-ring d3"></div>
        </div>
        <div class="radar-copy">
            <div class="radar-title">{title}</div>
            <div class="radar-sub">{subtitle}</div>
        </div>
    </div>
    """


def pulse_badge_html(text: str, kind: str = "green") -> str:
    """
    Returns an inline pulsing badge span. kind: 'green' | 'red' | 'amber'.
    Embed directly inside an f-string / st.markdown block.
    """
    kind = kind if kind in ("green", "red", "amber") else "green"
    return f'<span class="badge-pulse-{kind}"><span class="dot"></span>{text}</span>'


def risk_level_to_pulse_kind(level: str) -> str:
    """Maps a 'High/Medium/Low Risk' style string to a pulse badge kind."""
    level = (level or "").lower()
    if "high" in level or "critical" in level:
        return "red"
    if "medium" in level or "major" in level:
        return "amber"
    return "green"
