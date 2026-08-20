import streamlit as st
import os
import json
import pandas as pd
import altair as alt
from datetime import datetime

# Import CYBERGUARD Core Security Engines & Database Manager
from core.url_analyzer import URLAnalyzer
from core.phishing_detector import PhishingDetector
from core.password_analyzer import PasswordAnalyzer
from core.file_integrity import FileIntegrityAnalyzer
from database.db_manager import DatabaseManager
from config import APP_NAME, APP_VERSION

# Set Streamlit Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} - {APP_VERSION}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database Manager
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# ---------------------------------------------------------------------------
# ALTAIR CHART THEME — matches the design tokens below so charts stop looking
# like default library output and start looking native to the dashboard.
# ---------------------------------------------------------------------------
CHART_COLORS = {
    "primary": "#38bdf8",
    "success": "#10b981",
    "warning": "#f59e0b",
    "critical": "#ef4444",
    "grid": "#1e293b",
    "label": "#8b99b0",
    "text": "#f8fafc",
}


def styled_hbar(df: pd.DataFrame, cat_field: str, val_field: str,
                 color_domain=None, color_range=None, single_color=None, height=220):
    """Build a themed horizontal bar chart (rounded caps, dashed muted grid,
    transparent background) so it visually matches the glass card it sits in."""
    encode_kwargs = dict(
        x=alt.X(f"{val_field}:Q",
                axis=alt.Axis(grid=True, gridColor=CHART_COLORS["grid"], gridDash=[2, 3],
                               domain=False, tickColor=CHART_COLORS["grid"],
                               labelColor=CHART_COLORS["label"], titleColor=CHART_COLORS["label"])),
        y=alt.Y(f"{cat_field}:N", sort="-x",
                axis=alt.Axis(labelColor=CHART_COLORS["text"], domain=False, ticks=False, title=None)),
        tooltip=[cat_field, val_field],
    )
    if single_color:
        mark = alt.Chart(df).mark_bar(cornerRadiusEnd=6, size=22, color=single_color)
    else:
        mark = alt.Chart(df).mark_bar(cornerRadiusEnd=6, size=26)
        encode_kwargs["color"] = alt.Color(
            f"{cat_field}:N",
            scale=alt.Scale(domain=color_domain, range=color_range),
            legend=None,
        )
    chart = (
        mark.encode(**encode_kwargs)
        .properties(height=height, background="transparent")
        .configure_view(strokeWidth=0)
        .configure_axis(labelFontSize=11, titleFontSize=11)
    )
    return chart


# Apply Glassmorphism Dark Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    :root {
        --bg-base: #0b1120;
        --bg-surface: rgba(30, 41, 59, 0.55);
        --bg-surface-solid: #141b2d;
        --bg-surface-hover: rgba(30, 41, 59, 0.85);
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.18);
        --text-primary: #f8fafc;
        --text-muted: #94a3b8;
        --text-faint: #5b6b85;
        --primary: #38bdf8;
        --primary-2: #818cf8;
        --success: #10b981;
        --warning: #f59e0b;
        --critical: #ef4444;
        --font-ui: 'Inter', system-ui, -apple-system, sans-serif;
        --font-mono: 'JetBrains Mono', 'Consolas', monospace;
    }

    /* Dark Obsidian Base Theme */
    .stApp {
        background-color: var(--bg-base);
        color: var(--text-primary);
        font-family: var(--font-ui);
    }

    /* ---------------- Header Banner (with subtle animated sheen) ---------------- */
    .header-banner {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    .header-banner::after {
        content: "";
        position: absolute;
        top: 0; left: -60%;
        width: 60%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.06), transparent);
        animation: sheen 6s ease-in-out infinite;
    }
    @keyframes sheen {
        0%   { left: -60%; }
        50%  { left: 120%; }
        100% { left: 120%; }
    }
    .header-title {
        color: var(--primary);
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        position: relative;
    }
    .header-subtitle {
        color: var(--text-muted);
        font-size: 1.05rem;
        margin-top: 6px;
        position: relative;
    }

    /* ---------------- Glassmorphism Metric Cards ---------------- */
    .metric-card {
        position: relative;
        background: var(--bg-surface);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        margin-bottom: 12px;
        overflow: hidden;
        transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-strong);
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.4);
    }
    .metric-watermark {
        position: absolute;
        right: 10px;
        top: 4px;
        font-size: 2.6rem;
        opacity: 0.08;
        line-height: 1;
        pointer-events: none;
    }
    .metric-label {
        color: var(--text-muted);
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-val {
        font-family: var(--font-mono);
        font-size: 2.1rem;
        font-weight: 800;
        margin-top: 4px;
        letter-spacing: -0.5px;
    }

    /* ---------------- Radial Health Gauge (pure CSS conic-gradient) ---------------- */
    .gauge-row {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .gauge {
        --pct: 0;
        --gauge-color: #38bdf8;
        width: 96px;
        height: 96px;
        min-width: 96px;
        border-radius: 50%;
        background: conic-gradient(var(--gauge-color) calc(var(--pct) * 1%), rgba(255,255,255,0.06) 0);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    .gauge::before {
        content: "";
        position: absolute;
        inset: 9px;
        border-radius: 50%;
        background: var(--bg-surface-solid);
    }
    .gauge-value {
        position: relative;
        z-index: 1;
        font-family: var(--font-mono);
        font-weight: 800;
        font-size: 1.35rem;
    }

    /* ---------------- Status Pills / Badges ---------------- */
    .badge-high, .badge-med, .badge-low {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        white-space: nowrap;
    }
    .badge-high::before, .badge-med::before, .badge-low::before {
        content: "";
        width: 6px; height: 6px;
        border-radius: 50%;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.16);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-high::before { background: var(--critical); box-shadow: 0 0 6px var(--critical); }
    .badge-med {
        background-color: rgba(245, 158, 11, 0.16);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-med::before { background: var(--warning); box-shadow: 0 0 6px var(--warning); }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.16);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-low::before { background: var(--success); box-shadow: 0 0 6px var(--success); }

    /* ---------------- Custom Audit History Table ---------------- */
    .audit-table-wrap {
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        background: var(--bg-surface);
        backdrop-filter: blur(12px);
    }
    table.audit-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }
    table.audit-table thead th {
        background: #0a0e1a;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.72rem;
        font-weight: 700;
        text-align: left;
        padding: 12px 16px;
        border-bottom: 1px solid var(--border);
    }
    table.audit-table tbody td {
        padding: 10px 16px;
        border-bottom: 1px solid var(--border);
        color: var(--text-primary);
    }
    table.audit-table tbody tr:last-child td { border-bottom: none; }
    table.audit-table tbody tr:hover { background: rgba(255, 255, 255, 0.03); }
    .mono-cell { font-family: var(--font-mono); font-size: 0.82rem; }
    .text-faint { color: var(--text-faint); }
    .redacted-pill {
        font-family: var(--font-mono);
        font-size: 0.72rem;
        letter-spacing: 2px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border);
        color: var(--text-faint);
        border-radius: 6px;
        padding: 2px 8px;
    }

    /* ---------------- Sidebar ---------------- */
    section[data-testid="stSidebar"] {
        background-color: #0a0e1a;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .stRadio > label {
        color: var(--text-muted);
        font-weight: 700;
        font-size: 0.85rem;
    }
    section[data-testid="stSidebar"] .stRadio > div { gap: 2px; }
    section[data-testid="stSidebar"] .stRadio label {
        padding: 9px 12px;
        border-radius: 8px;
        border-left: 3px solid transparent;
        transition: background 150ms ease, border-color 150ms ease;
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.04);
    }
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: rgba(56, 189, 248, 0.12);
        border-left: 3px solid var(--primary);
    }
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) p {
        color: var(--primary) !important;
        font-weight: 800 !important;
    }
    .status-card {
        background: #050b14;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 14px;
        margin-top: 6px;
    }
    .status-row {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-bottom: 6px;
    }
    .status-row:last-child { margin-bottom: 0; }
    .status-row code {
        color: var(--primary);
        font-family: var(--font-mono);
        font-size: 0.75rem;
        background: transparent;
    }
    .status-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--success);
        box-shadow: 0 0 8px var(--success);
        flex-shrink: 0;
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ---------------- Section Headers ---------------- */
    h3, h4 { letter-spacing: -0.3px; }

    /* ---------------- Buttons ---------------- */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# App Header Banner
st.markdown(f"""
<div class="header-banner">
    <div class="header-title">🛡️ {APP_NAME} <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 400;">{APP_VERSION}</span></div>
    <div class="header-subtitle">Futuristic AI Cybersecurity Operations & Real-Time Threat Intelligence Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("### ⚙️ Navigation")
selected_tab = st.sidebar.radio(
    "Select Module",
    [
        "📊 Dashboard & Analytics",
        "🌐 Website Security",
        "🎣 Phishing Detector",
        "🔑 Password Entropy",
        "📁 File Integrity",
        "📈 Awareness Survey",
        "🎮 Cyber Security Quiz"
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status**")
st.sidebar.markdown(f"""
<div class="status-card">
    <div class="status-row"><span class="status-dot"></span> Engine: <code>CyberGuard 3.0 Core</code></div>
    <div class="status-row">💾 Storage: <code>{os.path.basename(db.db_path)}</code></div>
    <div class="status-row">☁️ Deployment: <code>Dual-Target Ready</code></div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 1: DASHBOARD & ANALYTICS
# -----------------------------------------------------------------------------
if selected_tab == "📊 Dashboard & Analytics":
    st.subheader("📊 Security Analytics & Operations Overview")

    stats = db.get_dashboard_stats()

    # 4 Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-watermark">📋</div>
            <div class="metric-label">Total Security Audits</div>
            <div class="metric-val" style="color: #38bdf8;">{stats['total_scans']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        avg_score = stats['avg_score']
        score_color = "#10b981" if avg_score >= 75 else "#f59e0b" if avg_score >= 40 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card">
            <div class="gauge-row">
                <div class="gauge" style="--pct: {avg_score}; --gauge-color: {score_color};">
                    <div class="gauge-value" style="color: {score_color};">{avg_score}</div>
                </div>
                <div>
                    <div class="metric-label">Average Health Score</div>
                    <div class="mono-cell" style="color: {score_color}; font-weight: 700; font-size: 1.1rem; margin-top: 4px;">/ 100</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-watermark">⚠️</div>
            <div class="metric-label">High Risk Threats</div>
            <div class="metric-val" style="color: #ef4444;">{stats['high_risk_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-watermark">✅</div>
            <div class="metric-label">Clean Audits</div>
            <div class="metric-val" style="color: #10b981;">{stats['low_risk_count']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🎯 Threat Risk Distribution")
        risk_data = pd.DataFrame({
            "Risk Level": ["High Risk", "Medium Risk", "Low Risk"],
            "Count": [stats['high_risk_count'], stats['medium_risk_count'], stats['low_risk_count']]
        })
        risk_chart = styled_hbar(
            risk_data, "Risk Level", "Count",
            color_domain=["High Risk", "Medium Risk", "Low Risk"],
            color_range=[CHART_COLORS["critical"], CHART_COLORS["warning"], CHART_COLORS["success"]],
        )
        st.altair_chart(risk_chart, use_container_width=True)

    with col_right:
        st.markdown("#### 🔍 Audits by Scanner Type")
        by_type_data = stats.get('by_type', {})
        if by_type_data:
            type_df = pd.DataFrame(list(by_type_data.items()), columns=["Scan Type", "Count"])
            type_chart = styled_hbar(
                type_df, "Scan Type", "Count",
                single_color=CHART_COLORS["primary"],
            )
            st.altair_chart(type_chart, use_container_width=True)
        else:
            st.info("No security scans logged yet. Perform a scan in one of the tool tabs!")

    st.markdown("---")
    st.markdown("#### 📜 Live Security Audit History")
    recent = stats.get("recent_scans", [])
    if recent:
        badge_map = {"Low Risk": "badge-low", "Medium Risk": "badge-med", "High Risk": "badge-high"}
        rows_html = ""
        for row in recent:
            risk_level = row.get("risk_level", "Unknown")
            badge_class = badge_map.get(risk_level, "badge-med")
            target = str(row.get("target", ""))
            is_redacted = bool(target) and target.strip("*") == ""
            target_cell = (
                f'<span class="redacted-pill">{target}</span>'
                if is_redacted else f'<span class="mono-cell">{target}</span>'
            )
            rows_html += f"""
            <tr>
                <td>{target_cell}</td>
                <td>{row.get('scan_type', '')}</td>
                <td class="mono-cell">{row.get('risk_score', '')}</td>
                <td><span class="{badge_class}">{risk_level}</span></td>
                <td class="mono-cell text-faint">{row.get('scanned_at', '')}</td>
            </tr>
            """
        st.markdown(f"""
        <div class="audit-table-wrap">
        <table class="audit-table">
            <thead>
                <tr><th>Target</th><th>Scan Type</th><th>Score</th><th>Risk Level</th><th>Scanned At</th></tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("No historical scan logs available.")

# -----------------------------------------------------------------------------
# TAB 2: WEBSITE SECURITY
# -----------------------------------------------------------------------------
elif selected_tab == "🌐 Website Security":
    st.subheader("🌐 Website Security & SSL Audit Inspector")
    st.write("Perform real-time SSL/TLS certificate verification, DNS lookup, security header analysis, and URL anomaly detection.")

    target_url = st.text_input("Enter Target URL to Inspect:", placeholder="https://example.com")

    if st.button("🚀 Audit URL Security"):
        if not target_url.strip():
            st.warning("Please enter a valid URL.")
        else:
            with st.spinner("Analyzing domain, SSL handshake, and security headers..."):
                analyzer = URLAnalyzer()
                res = analyzer.analyze(target_url)

                # Save scan to database
                db.save_scan_log(
                    target=res.get("target", target_url),
                    scan_type="URL Audit",
                    risk_score=res.get("risk_score", 0),
                    risk_level=res.get("risk_level", "Unknown"),
                    details=res
                )

                st.markdown("### Audit Results")

                # Risk level banner
                score = res.get("risk_score", 0)
                level = res.get("risk_level", "Unknown")
                badge_class = "badge-low" if level == "Low Risk" else "badge-med" if level == "Medium Risk" else "badge-high"

                c_a, c_b, c_c = st.columns(3)
                c_a.metric("Safety Score", f"{score} / 100")
                c_b.markdown(f"**Risk Level**: <span class='{badge_class}'>{level}</span>", unsafe_allow_html=True)
                c_c.metric("Resolved IP", res.get("ip_address") or "N/A")

                st.markdown("---")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 🔒 SSL/TLS Certificate Status")
                    ssl_info = res.get("ssl_details", {})
                    if ssl_info.get("valid"):
                        st.success("Valid SSL/TLS Certificate Detected")
                        st.json(ssl_info)
                    else:
                        st.error(f"SSL Issues: {ssl_info.get('error', ssl_info.get('details', 'Invalid'))}")

                with col2:
                    st.markdown("#### 🛡️ Security Headers Audit")
                    headers = res.get("header_audit", {})
                    for h, status in headers.items():
                        if status is True:
                            st.markdown(f"✅ **{h}**: Present")
                        elif status is False:
                            st.markdown(f"❌ **{h}**: Missing")
                        else:
                            st.write(f"ℹ️ {h}: {status}")

                st.markdown("---")
                if res.get("issues"):
                    st.markdown("#### ⚠️ Identified Security Vulnerabilities")
                    for issue in res.get("issues", []):
                        st.warning(f"• {issue}")

                if res.get("remediations"):
                    st.markdown("#### 💡 Recommended Security Hardening")
                    for rem in res.get("remediations", []):
                        st.info(f"👉 {rem}")

# -----------------------------------------------------------------------------
# TAB 3: PHISHING DETECTOR
# -----------------------------------------------------------------------------
elif selected_tab == "🎣 Phishing Detector":
    st.subheader("🎣 Phishing & Social Engineering Analyzer")
    st.write("Scan emails, messages, or text payloads for urgency tactics, credential harvesting cues, and deceptive links.")

    sample_text = st.text_area(
        "Paste Email Content or Message Body:",
        height=180,
        placeholder="URGENT: Your account has been suspended! Click http://192.168.1.1/login to verify your password within 24 hours."
    )

    if st.button("🔍 Scan Payload for Phishing"):
        if not sample_text.strip():
            st.warning("Please paste a text payload to inspect.")
        else:
            with st.spinner("Scanning for social engineering triggers..."):
                detector = PhishingDetector()
                res = detector.analyze(sample_text)

                db.save_scan_log(
                    target=sample_text[:50] + "...",
                    scan_type="Phishing Scan",
                    risk_score=res.get("risk_score", 0),
                    risk_level=res.get("risk_level", "Unknown"),
                    details=res
                )

                st.markdown("### Phishing Threat Assessment")
                p_score = res.get("phishing_risk_score", 0)
                verdict = res.get("verdict", "")
                level = res.get("risk_level", "")

                if level == "High Risk":
                    st.error(f"🚨 **VERDICT**: {verdict} (Phishing Threat Score: {p_score}%)")
                elif level == "Medium Risk":
                    st.warning(f"⚠️ **VERDICT**: {verdict} (Phishing Threat Score: {p_score}%)")
                else:
                    st.success(f"✅ **VERDICT**: {verdict} (Phishing Threat Score: {p_score}%)")

                st.markdown("---")
                indicators = res.get("indicators", [])
                if indicators:
                    st.markdown("#### 🚩 Triggered Security Indicators")
                    for ind in indicators:
                        sev = ind.get("severity", "")
                        badge = "badge-high" if sev == "High" else "badge-med" if sev == "Medium" else "badge-low"
                        st.markdown(f"""
                        <div class="metric-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <strong>{ind.get('category')}</strong>
                                <span class="{badge}">{sev} Severity</span>
                            </div>
                            <div style="margin-top: 8px; color: #cbd5e1;">{ind.get('description')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No suspicious social engineering triggers detected.")

                if res.get("extracted_urls"):
                    st.markdown("#### 🔗 Extracted Hyperlinks")
                    st.write(res.get("extracted_urls"))

# -----------------------------------------------------------------------------
# TAB 4: PASSWORD ENTROPY
# -----------------------------------------------------------------------------
elif selected_tab == "🔑 Password Entropy":
    st.subheader("🔑 Password Entropy & Strength Analyzer")
    st.write("Compute mathematical Shannon entropy (bits), character set diversity, dictionary weaknesses, and estimated brute-force crack times.")

    pwd_input = st.text_input("Enter Password to Test:", type="password", placeholder="Type password here...")

    if pwd_input:
        analyzer = PasswordAnalyzer()
        res = analyzer.analyze(pwd_input)

        score = res.get("score", 0)
        status = res.get("status", "")
        level = res.get("risk_level", "")
        entropy = res.get("entropy_bits", 0)

        st.markdown("### Password Security Analysis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Strength Rating", status)
        c2.metric("Shannon Entropy", f"{entropy} bits")
        c3.metric("Length", f"{res.get('password_length')} chars")

        st.progress(min(100, max(0, score)) / 100.0)

        st.markdown("---")
        st.markdown("#### ⏱️ Brute-Force Crack Time Estimates")
        crack = res.get("crack_times", {})
        ct1, ct2, ct3 = st.columns(3)
        ct1.metric("Online (10 req/sec)", crack.get("online", "N/A"))
        ct2.metric("Desktop CPU (10k req/sec)", crack.get("cpu", "N/A"))
        ct3.metric("GPU Cluster (100B req/sec)", crack.get("gpu_cluster", "N/A"))

        st.markdown("---")
        col_comp, col_tips = st.columns(2)

        with col_comp:
            st.markdown("#### 🔣 Character Composition")
            st.markdown(f"- Lowercase (a-z): {'✅' if res.get('has_lower') else '❌'}")
            st.markdown(f"- Uppercase (A-Z): {'✅' if res.get('has_upper') else '❌'}")
            st.markdown(f"- Numbers (0-9): {'✅' if res.get('has_digit') else '❌'}")
            st.markdown(f"- Special Symbols (@, #, $): {'✅' if res.get('has_symbol') else '❌'}")
            if res.get("is_common"):
                st.error("⚠️ Password is in Common Weak Password List!")

        with col_tips:
            st.markdown("#### 💡 Recommendations for Hardening")
            if res.get("feedback"):
                for fb in res.get("feedback"):
                    st.warning(f"• {fb}")
            if res.get("improvements"):
                for imp in res.get("improvements"):
                    st.info(f"👉 {imp}")

# -----------------------------------------------------------------------------
# TAB 5: FILE INTEGRITY
# -----------------------------------------------------------------------------
elif selected_tab == "📁 File Integrity":
    st.subheader("📁 File Integrity & Extension Spoofing Inspector")
    st.write("Calculate cryptographic SHA-256 / MD5 hashes, verify magic byte file headers, and catch double extension disguises.")

    uploaded_file = st.file_uploader("Choose a file to analyze", type=None)

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        analyzer = FileIntegrityAnalyzer()
        res = analyzer.analyze_bytes(file_bytes, uploaded_file.name)

        db.save_scan_log(
            target=uploaded_file.name,
            scan_type="File Integrity",
            risk_score=res.get("risk_score", 0),
            risk_level=res.get("risk_level", "Unknown"),
            details=res
        )

        st.markdown("### File Security Report")
        score = res.get("risk_score", 100)
        level = res.get("risk_level", "Unknown")
        badge_class = "badge-low" if level == "Low Risk" else "badge-med" if level == "Medium Risk" else "badge-high"

        fc1, fc2, fc3 = st.columns(3)
        fc1.metric("Safety Score", f"{score} / 100")
        fc2.markdown(f"**Risk Level**: <span class='{badge_class}'>{level}</span>", unsafe_allow_html=True)
        fc3.metric("File Size", res.get("file_size_formatted"))

        st.markdown("---")
        st.markdown("#### 🔑 Cryptographic Hashes")
        st.code(f"SHA-256: {res.get('sha256')}\nMD5:     {res.get('md5')}", language="text")

        st.markdown("---")
        col_hdr, col_ext = st.columns(2)

        with col_hdr:
            st.markdown("#### 🔍 Magic Bytes Header Inspection")
            st.write(f"**Header Hex**: `{res.get('header_hex')}`")
            if res.get("magic_matched"):
                st.success("File header magic bytes match reported extension.")
            else:
                st.error("Header Mismatch: Extension does not match file byte signature!")

        with col_ext:
            st.markdown("#### 🎭 Extension Masking Audit")
            if res.get("is_double_ext"):
                st.error("🚨 Double Extension Spoofing Detected!")
            else:
                st.success("No double-extension masking detected.")

        if res.get("anomalies"):
            st.markdown("#### ⚠️ Detected Anomalies")
            for an in res.get("anomalies"):
                st.warning(f"• {an}")

        if res.get("recommendations"):
            st.markdown("#### 💡 Guidance")
            for rec in res.get("recommendations"):
                st.info(f"👉 {rec}")

# -----------------------------------------------------------------------------
# TAB 6: AWARENESS SURVEY
# -----------------------------------------------------------------------------
elif selected_tab == "📈 Awareness Survey":
    st.subheader("📈 Cyber Security Awareness Survey")
    st.write("Participate in the community cybersecurity awareness study and view aggregated benchmark analytics.")

    with st.form("survey_form"):
        user_cat = st.selectbox("Select Your Primary Category:", [
            "Student / Educator", "IT Professional", "General Public", "Corporate Employee", "Senior Citizen"
        ])

        phish_score = st.slider("Rate your confidence in identifying phishing emails (0 = Low, 100 = High):", 0, 100, 75)
        pwd_score = st.slider("Rate your password security habits (unique passwords, 2FA used) (0 = Poor, 100 = Excellent):", 0, 100, 70)

        submit_survey = st.form_submit_button("Submit Survey Response")
        if submit_survey:
            db.save_survey_response(user_cat, phish_score, pwd_score)
            st.success("Thank you! Your response has been recorded.")

    st.markdown("---")
    st.markdown("#### 📊 Community Survey Benchmark Analytics")
    survey_data = db.get_survey_analytics()
    if survey_data:
        df_survey = pd.DataFrame(survey_data)
        st.dataframe(df_survey, use_container_width=True)
    else:
        st.info("No survey responses recorded yet.")

# -----------------------------------------------------------------------------
# TAB 7: CYBER SECURITY QUIZ
# -----------------------------------------------------------------------------
elif selected_tab == "🎮 Cyber Security Quiz":
    st.subheader("🎮 Interactive Cyber Security Quiz & Badge Challenge")
    st.write("Test your cyber hygiene knowledge and earn verified security badges.")

    q1 = st.radio("1. What is the most secure password practice?", [
        "Reusing a strong password across all sites",
        "Using unique, complex passphrases managed in a password manager",
        "Writing passwords in a physical notebook"
    ], index=None)

    q2 = st.radio("2. What indicator strongly suggests an email is a phishing attempt?", [
        "Email sent from official company domain",
        "Psychological urgency tactics (e.g. 'Account suspended in 1 hour!')",
        "Personalized greeting with full name"
    ], index=None)

    q3 = st.radio("3. Why is raw IP address usage in a URL suspicious?", [
        "IP addresses load faster",
        "Raw IPs bypass domain name verification and hide illegitimate host identity",
        "IP addresses enforce HTTPS encryption"
    ], index=None)

    q4 = st.radio("4. What primary security risk is posed by files like 'Invoice.pdf.exe'?", [
        "The file will take double the storage space",
        "Double extension masking tricks users into launching malicious executable code",
        "It forces the system to restart automatically"
    ], index=None)

    q5 = st.radio("5. What is the main benefit of Multi-Factor Authentication (MFA)?", [
        "It automatically updates your passwords every week",
        "It requires a secondary verification factor, rendering stolen credentials insufficient",
        "It encrypts your local hard drive against ransomware"
    ], index=None)

    q6 = st.radio("6. Why is conducting sensitive transactions over unencrypted public Wi-Fi dangerous?", [
        "Public networks slow down your browser performance",
        "Attackers on the same network can intercept unencrypted session traffic and data",
        "It voids your antivirus software license"
    ], index=None)

    q7 = st.radio("7. How does regular software patching protect system integrity?", [
        "It removes unused desktop shortcuts",
        "It closes known security vulnerabilities before attackers can exploit them",
        "It increases network bandwidth speeds"
    ], index=None)

    if st.button("Submit Quiz Answers"):
        # Check if user answered all questions
        user_answers = [q1, q2, q3, q4, q5, q6, q7]
        if None in user_answers:
            st.warning("⚠️ Please answer all 7 questions before submitting!")
        else:
            score = 0
            if q1 == "Using unique, complex passphrases managed in a password manager": score += 1
            if q2 == "Psychological urgency tactics (e.g. 'Account suspended in 1 hour!')": score += 1
            if q3 == "Raw IPs bypass domain name verification and hide illegitimate host identity": score += 1
            if q4 == "Double extension masking tricks users into launching malicious executable code": score += 1
            if q5 == "It requires a secondary verification factor, rendering stolen credentials insufficient": score += 1
            if q6 == "Attackers on the same network can intercept unencrypted session traffic and data": score += 1
            if q7 == "It closes known security vulnerabilities before attackers can exploit them": score += 1

            total = 7
            
            # Badge Hierarchy based on 7 total questions
            if score == 7:
                badge = "🛡️ Cyber Guardian Gold"
            elif score >= 5:
                badge = "🥈 Security Apprentice Silver"
            else:
                badge = "🥉 Security Novice"

            # Save results to local SQLite DB
            db.save_quiz_score(score, total, badge)

            st.balloons()
            st.markdown(f"### 🎉 Quiz Score: {score} / {total}")
            st.markdown(f"**Badge Earned**: `{badge}`")

    st.markdown("---")
    st.markdown("#### 🏆 Global Quiz Stats & Leaderboard History")
    q_stats = db.get_quiz_stats()
    qc1, qc2, qc3 = st.columns(3)
    qc1.metric("Total Quiz Attempts", q_stats.get("total_attempts", 0))
    qc2.metric("Average Score %", f"{q_stats.get('avg_percentage', 0)}%")
    qc3.metric("Highest Score", q_stats.get("high_score", 0))
    q_stats = db.get_quiz_stats()
    qc1, qc2, qc3 = st.columns(3)
    qc1.metric("Total Quiz Attempts", q_stats.get("total_attempts", 0))
    qc2.metric("Average Score %", f"{q_stats.get('avg_percentage', 0)}%")
    qc3.metric("Highest Score", q_stats.get("high_score", 0))
