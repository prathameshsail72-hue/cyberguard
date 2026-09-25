import streamlit as st
import os
import json
import inspect
import pandas as pd
import altair as alt
from datetime import datetime

# =============================================================================
# STREAMLIT PAGE CONFIGURATION (Must be the very first Streamlit call)
# =============================================================================
st.set_page_config(
    page_title="CyberGuard 3.0 Pro - Cyber Threat Intelligence Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Core Security Engines & Database Manager
from core.url_analyzer import URLAnalyzer
from core.phishing_detector import PhishingDetector
from core.password_analyzer import PasswordAnalyzer
from core.file_integrity import FileIntegrityAnalyzer
from database.db_manager import DatabaseManager
from config import (
    APP_NAME, APP_VERSION, COLOR_BG_DARK, COLOR_CARD_BG,
    COLOR_ACCENT_CYAN, COLOR_RISK_HIGH, COLOR_RISK_MEDIUM, COLOR_RISK_LOW
)

# =============================================================================
# DATABASE CACHING
# =============================================================================
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# =============================================================================
# NAVIGATION SYSTEM (STATE MANAGEMENT WITH IMMEDIATE RERUN)
# =============================================================================
NAV_TABS = [
    "📊 Dashboard & Analytics",
    "🌐 Website Security",
    "🎣 Phishing Detector",
    "🔑 Password Entropy",
    "📁 File Integrity",
    "📈 Awareness Survey",
    "🎮 Cyber Security Quiz"
]

def switch_tab_callback(target_tab: str):
    st.session_state["nav_radio_bar"] = target_tab
    st.query_params["tab"] = target_tab
    st.rerun()

# Sync query params and session state safely before rendering UI
query_tab = st.query_params.get("tab", None)
if "nav_radio_bar" not in st.session_state:
    st.session_state["nav_radio_bar"] = query_tab if query_tab in NAV_TABS else NAV_TABS[0]

# =============================================================================
# CYBERPUNK / DARK OBSIDIAN GLASSMORPHISM DESIGN SYSTEM
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    :root {
        --bg-base: #020617;
        --bg-surface: rgba(15, 23, 42, 0.75);
        --bg-surface-solid: #0f172a;
        --bg-card: #1e293b;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(56, 189, 248, 0.3);
        --text-primary: #f8fafc;
        --text-muted: #94a3b8;
        --primary: #38bdf8;
        --primary-glow: rgba(56, 189, 248, 0.35);
        --success: #22c55e;
        --warning: #f59e0b;
        --critical: #ef4444;
        --font-ui: 'Inter', system-ui, -apple-system, sans-serif;
        --font-mono: 'JetBrains Mono', 'Consolas', monospace;
    }

    .stApp {
        background-color: var(--bg-base);
        color: var(--text-primary);
        font-family: var(--font-ui);
    }

    /* Header Banner */
    .header-banner {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e293b 100%);
        border: 1px solid var(--border-strong);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 20px;
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

    /* Metric Cards */
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
        transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
        box-shadow: 0 12px 28px rgba(56, 189, 248, 0.15);
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

    /* Feature Cards */
    .guide-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid var(--border-strong);
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .feature-card {
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
        transition: all 0.2s ease;
    }
    .feature-card:hover {
        border-color: var(--primary);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.2);
        transform: translateY(-2px);
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

    /* Status Badges */
    .badge-high, .badge-med, .badge-low {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.82rem;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.16);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-med {
        background-color: rgba(245, 158, 11, 0.16);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-low {
        background-color: rgba(34, 197, 94, 0.16);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }

    .content-box {
        background: #0f172a;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* Cyberpunk Navigation Radio Bar */
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
        transform: translateY(-1px);
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(30, 41, 59, 0.9) 100%) !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.4);
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] input[type="radio"] {
        display: none;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* Buttons & Inputs */
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
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.45);
        transform: translateY(-2px);
        color: #38bdf8;
    }
    .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="header-banner">
    <div class="header-title">🛡️ {APP_NAME} <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 400;">{APP_VERSION}</span></div>
    <div class="header-subtitle">Futuristic AI Cybersecurity Operations & Real-Time Threat Intelligence Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(f"### 🛡️ {APP_NAME}")
st.sidebar.markdown(f"**Version:** `{APP_VERSION}`")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ System Status")
st.sidebar.markdown(f"""
- 🟢 **Core Engine:** Active
- 💾 **Database:** `{os.path.basename(db.db_path)}`
- ☁️ **Deployment:** Streamlit Cloud Ready
""")
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Click navigation buttons or the Return button to switch views.")

# Render Navigation Bar
selected_tab = st.radio(
    "Navigation",
    NAV_TABS,
    key="nav_radio_bar",
    horizontal=True,
    label_visibility="collapsed"
)

if st.query_params.get("tab") != selected_tab:
    st.query_params["tab"] = selected_tab

# =============================================================================
# VIEW 1: 📊 DASHBOARD & ANALYTICS
# =============================================================================
if selected_tab == "📊 Dashboard & Analytics":
    st.markdown("""
    <div class="guide-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h3 style="color: #38bdf8; margin:0; font-size: 1.25rem; font-weight: 800;">⚡ Features & Quick-Launch Guide</h3>
                <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 0.9rem;">
                    Instant access to active defensive security engines, cryptographic auditing, and awareness suites.
                </p>
            </div>
            <span class="badge-low">All Engines Operational</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    qcol1, qcol2, qcol3 = st.columns(3)

    with qcol1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🌐 Website Security</div>
            <div class="feature-desc">Analyze domain safety, verify SSL/TLS certificates, query DNS records, and audit HTTP security headers.</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🚀 Audit URL Security", key="qbtn_web", use_container_width=True, on_click=switch_tab_callback, args=("🌐 Website Security",))

    with qcol2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎣 Phishing Detector</div>
            <div class="feature-desc">Scan emails, SMS alerts, or suspicious messages for psychological urgency tactics and credential harvesting links.</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🔍 Scan Phishing Message", key="qbtn_phish", use_container_width=True, on_click=switch_tab_callback, args=("🎣 Phishing Detector",))

    with qcol3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔑 Password Entropy</div>
            <div class="feature-desc">Calculate mathematical Shannon entropy in bits, analyze character diversity, and estimate brute-force cracking resistance.</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🔐 Evaluate Password", key="qbtn_pwd", use_container_width=True, on_click=switch_tab_callback, args=("🔑 Password Entropy",))

    st.write("")
    qcol4, qcol5, qcol6 = st.columns(3)

    with qcol4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📁 File Integrity</div>
            <div class="feature-desc">Compute in-memory cryptographic hashes (SHA-256/SHA-1/MD5), inspect magic bytes, and detect double-extension spoofing.</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🛡️ Audit File Integrity", key="qbtn_file", use_container_width=True, on_click=switch_tab_callback, args=("📁 File Integrity",))

    with qcol5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📈 Awareness Survey</div>
            <div class="feature-desc">Assess your cyber hygiene habits, contribute to community benchmarks, and explore interactive demographic analytics.</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("📊 Take Cyber Survey", key="qbtn_survey", use_container_width=True, on_click=switch_tab_callback, args=("📈 Awareness Survey",))

    with qcol6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎮 Cyber Security Quiz</div>
            <div class="feature-desc">Challenge your defensive cybersecurity knowledge across 8 domains, earn skill badges, and join the global leaderboard.</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🎯 Start Security Quiz", key="qbtn_quiz", use_container_width=True, on_click=switch_tab_callback, args=("🎮 Cyber Security Quiz",))

    st.markdown("---")
    st.subheader("📊 Security Analytics & Threat Operations Overview")
    
    stats = db.get_dashboard_stats()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Security Audits</div>
            <div class="metric-val" style="color: #38bdf8;">{stats.get('total_scans', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        avg_score = stats.get('avg_score', 0)
        score_color = "#22c55e" if avg_score >= 75 else "#f59e0b" if avg_score >= 45 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Health Score</div>
            <div class="metric-val" style="color: {score_color};">{avg_score} <span style="font-size: 1rem; color: #94a3b8;">/ 100</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Risk / Critical Findings</div>
            <div class="metric-val" style="color: #ef4444;">{stats.get('high_risk_count', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Clean / Low Risk Audits</div>
            <div class="metric-val" style="color: #22c55e;">{stats.get('low_risk_count', 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 🔍 Security Scans by Module")
        by_type_data = stats.get('by_type', {})
        if by_type_data:
            df_types = pd.DataFrame(list(by_type_data.items()), columns=["Module", "Scan Count"])
            bar_chart = (
                alt.Chart(df_types)
                .mark_bar(cornerRadiusEnd=6, size=24, color="#38bdf8")
                .encode(
                    x=alt.X("Scan Count:Q", title="Number of Audits"),
                    y=alt.Y("Module:N", sort="-x", title=None),
                    tooltip=["Module", "Scan Count"]
                )
                .properties(height=240, background="transparent")
                .configure_view(strokeWidth=0)
            )
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.info("No security audits recorded yet.")

    with col_chart2:
        st.markdown("#### 🎯 Threat Risk Level Distribution")
        risk_counts = [
            {"Risk Level": "High Risk", "Count": stats.get('high_risk_count', 0)},
            {"Risk Level": "Medium Risk", "Count": stats.get('medium_risk_count', 0)},
            {"Risk Level": "Low Risk", "Count": stats.get('low_risk_count', 0)}
        ]
        df_risk = pd.DataFrame(risk_counts)
        if df_risk["Count"].sum() > 0:
            pie_chart = (
                alt.Chart(df_risk)
                .mark_arc(innerRadius=45, stroke="#020617", strokeWidth=2)
                .encode(
                    theta=alt.Theta("Count:Q"),
                    color=alt.Color(
                        "Risk Level:N",
                        scale=alt.Scale(
                            domain=["High Risk", "Medium Risk", "Low Risk"],
                            range=["#ef4444", "#f59e0b", "#22c55e"]
                        ),
                        legend=alt.Legend(orient="right", title="Risk Category")
                    ),
                    tooltip=["Risk Level", "Count"]
                )
                .properties(height=240, background="transparent")
            )
            st.altair_chart(pie_chart, use_container_width=True)
        else:
            st.info("No risk distribution data available.")

    st.markdown("---")
    st.markdown("#### 📜 Live Security Audit History Log")
    recent = stats.get("recent_scans", [])
    if recent:
        df_recent = pd.DataFrame(recent)[["target", "scan_type", "risk_score", "risk_level", "scanned_at"]]
        df_recent.columns = ["Target / Artifact", "Module", "Score", "Risk Level", "Scanned At"]
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No historical scan logs found.")

# =============================================================================
# VIEW 2: 🌐 WEBSITE SECURITY
# =============================================================================
elif selected_tab == "🌐 Website Security":
    st.button("⬅️ Return to Dashboard", key="back_web", on_click=switch_tab_callback, args=("📊 Dashboard & Analytics",))
    st.subheader("🌐 Website Security & SSL Audit Inspector")
    st.write("Perform real-time SSL/TLS certificate verification, DNS record lookup, and HTTP security header analysis.")

    col_in, col_btn = st.columns([4, 1])
    with col_in:
        target_url = st.text_input("Enter Target Domain or URL to Inspect:", placeholder="https://example.com", label_visibility="collapsed")
    with col_btn:
        scan_btn = st.button("🚀 Audit URL Security", use_container_width=True)

    if scan_btn:
        if not target_url.strip():
            st.warning("Please enter a valid domain or URL to audit.")
        else:
            with st.spinner("Analyzing domain DNS records, SSL/TLS handshake, and HTTP security headers..."):
                analyzer = URLAnalyzer()
                res = analyzer.analyze(target_url)

                db.save_scan_log(
                    target=res.get("target", target_url),
                    scan_type="URL Audit",
                    risk_score=res.get("risk_score", 0),
                    risk_level=res.get("risk_level", "Unknown"),
                    details=res
                )

                score = res.get("risk_score", 0)
                level = res.get("risk_level", "Unknown")
                badge_class = "badge-low" if level == "Low Risk" else "badge-med" if level == "Medium Risk" else "badge-high"

                st.markdown("### 📋 Audit Findings")
                m1, m2, m3 = st.columns(3)
                m1.metric("Safety Score", f"{score} / 100")
                m2.markdown(f"**Risk Level:** <br><span class='{badge_class}'>{level}</span>", unsafe_allow_html=True)
                m3.metric("Resolved IP Address", res.get("ip_address") or "N/A")

                st.markdown("---")
                c_ssl, c_dns = st.columns(2)

                with c_ssl:
                    st.markdown("#### 🔒 SSL/TLS Certificate Status")
                    ssl_info = res.get("ssl_details", {})
                    if ssl_info.get("valid"):
                        st.success(f"✅ Valid SSL/TLS Certificate ({ssl_info.get('version', 'TLS')})")
                        st.markdown(f"- **Issuer:** `{ssl_info.get('issuer')}`")
                        st.markdown(f"- **Subject / Domain:** `{ssl_info.get('subject')}`")
                        st.markdown(f"- **Expires:** `{ssl_info.get('expiry')}` ({ssl_info.get('days_remaining')} days left)")
                        st.markdown(f"- **Cipher Suite:** `{ssl_info.get('cipher')}`")
                    else:
                        st.error(f"❌ SSL/TLS Warning: {ssl_info.get('details', ssl_info.get('error', 'Invalid or absent certificate'))}")

                with c_dns:
                    st.markdown("#### 🌐 DNS Records")
                    dns_recs = res.get("dns_records", {})
                    if dns_recs:
                        for rtype, rvals in dns_recs.items():
                            if rvals:
                                st.markdown(f"**{rtype} Records:** `{', '.join(rvals)}`")
                            else:
                                st.markdown(f"**{rtype} Records:** *None configured*")
                    else:
                        st.write(f"Primary A Record: `{res.get('ip_address')}`")

                st.markdown("---")
                st.markdown("#### 🛡️ HTTP Security Headers Audit")
                headers = res.get("header_audit", {})
                if headers:
                    h_cols = st.columns(2)
                    for i, (h_name, h_data) in enumerate(headers.items()):
                        col = h_cols[i % 2]
                        if isinstance(h_data, dict):
                            present = h_data.get("present")
                            desc = h_data.get("description")
                            if present:
                                col.markdown(f"✅ **{h_name}**: Present <br><span style='color: #94a3b8; font-size: 0.85rem;'>{desc}</span>", unsafe_allow_html=True)
                            else:
                                col.markdown(f"❌ **{h_name}**: Missing <br><span style='color: #94a3b8; font-size: 0.85rem;'>{desc}</span>", unsafe_allow_html=True)

                if res.get("issues"):
                    st.markdown("---")
                    st.markdown("#### ⚠️ Identified Security Vulnerabilities")
                    for issue in res.get("issues", []):
                        st.warning(f"• {issue}")

                if res.get("remediations"):
                    st.markdown("#### 💡 Recommended Security Hardening")
                    for rem in res.get("remediations", []):
                        st.info(f"👉 {rem}")

# =============================================================================
# VIEW 3: 🎣 PHISHING DETECTOR
# =============================================================================
elif selected_tab == "🎣 Phishing Detector":
    st.button("⬅️ Return to Dashboard", key="back_phish", on_click=switch_tab_callback, args=("📊 Dashboard & Analytics",))
    st.subheader("🎣 Phishing & Social Engineering Analyzer")
    st.write("Inspect email messages, SMS alerts, or communications for psychological urgency tactics, credential harvesting cues, and spoofed links.")

    preset = st.selectbox("Load Sample Test Payload:", [
        "Custom Input",
        "🚨 High Risk: Banking Account Suspension Notice",
        "⚠️ Medium Risk: Crypto Airdrop / Lottery Claim",
        "✅ Low Risk: Standard Security Meeting Invitation"
    ])

    preset_texts = {
        "🚨 High Risk: Banking Account Suspension Notice": "URGENT: Your bank account has been suspended due to unauthorized login attempts. You must confirm your password and verify your SSN within 24 hours at http://192.168.1.1/login-banking or your account will be permanently closed.",
        "⚠️ Medium Risk: Crypto Airdrop / Lottery Claim": "Congratulations! You have been selected for a 500 USDT crypto deposit bonus. Claim your prize immediately by connecting your wallet at http://free-crypto-airdrop-claim.net",
        "✅ Low Risk: Standard Security Meeting Invitation": "Hi Team, please join our quarterly cybersecurity awareness review this Thursday at 2 PM in the main conference room. We will discuss MFA rollouts and password manager adoption."
    }

    initial_text = preset_texts.get(preset, "")
    sample_text = st.text_area("Paste Message Content to Scan:", value=initial_text, height=160, placeholder="Paste suspicious email text, SMS, or message body here...")

    if st.button("🔍 Scan Payload for Phishing Indicators", use_container_width=True):
        if not sample_text.strip():
            st.warning("Please enter or select message content to analyze.")
        else:
            with st.spinner("Scanning message for social engineering cues and deceptive URLs..."):
                detector = PhishingDetector()
                res = detector.analyze(sample_text)

                db.save_scan_log(
                    target=f"[Message: {res.get('word_count', 0)} words]",
                    scan_type="Phishing Scan",
                    risk_score=res.get("risk_score", 0),
                    risk_level=res.get("risk_level", "Unknown"),
                    details={"phishing_risk_score": res.get("phishing_risk_score"), "indicators_count": len(res.get("indicators", []))}
                )

                st.markdown("### 📊 Phishing Threat Assessment")
                p_score = res.get("phishing_risk_score", 0)
                level = res.get("risk_level", "Unknown")
                verdict = res.get("verdict", "")

                if level == "High Risk":
                    st.error(f"**{verdict}** (Threat Score: {p_score}%)")
                elif level == "Medium Risk":
                    st.warning(f"**{verdict}** (Threat Score: {p_score}%)")
                else:
                    st.success(f"**{verdict}** (Threat Score: {p_score}%)")

                st.markdown(f"**Defensive Guidance:** {res.get('recommendation')}")

                indicators = res.get("indicators", [])
                if indicators:
                    st.markdown("---")
                    st.markdown("#### 🚩 Triggered Security Indicators")
                    for ind in indicators:
                        sev = ind.get("severity", "Medium")
                        badge = "badge-high" if sev == "High" else "badge-med" if sev == "Medium" else "badge-low"
                        st.markdown(f"""
                        <div class="content-box">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <strong style="color: #f8fafc;">{ind.get('category')}</strong>
                                <span class="{badge}">{sev} Severity</span>
                            </div>
                            <div style="margin-top: 6px; color: #cbd5e1;">{ind.get('description')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                if res.get("extracted_urls"):
                    st.markdown("---")
                    st.markdown("#### 🔗 Extracted Hyperlinks")
                    for u in res.get("extracted_urls"):
                        st.code(u, language="text")

# =============================================================================
# VIEW 4: 🔑 PASSWORD ENTROPY
# =============================================================================
elif selected_tab == "🔑 Password Entropy":
    st.button("⬅️ Return to Dashboard", key="back_pwd", on_click=switch_tab_callback, args=("📊 Dashboard & Analytics",))
    st.subheader("🔑 Mathematical Password Entropy & Strength Analyzer")
    st.write("Calculate Shannon entropy in bits, analyze character set diversity, and estimate brute-force cracking resistance across various attacker computing speeds.")

    pwd_input = st.text_input("Enter Password to Test (Masked):", type="password", placeholder="Type a password or passphrase...")

    if st.button("🔐 Analyze Password Strength", use_container_width=True):
        if not pwd_input:
            st.warning("Please enter a password to evaluate.")
        else:
            analyzer = PasswordAnalyzer()
            res = analyzer.analyze(pwd_input)

            db.save_scan_log(
                target=f"****** ({res.get('password_length')} chars)",
                scan_type="Password Entropy",
                risk_score=res.get("score", 0),
                risk_level=res.get("risk_level", "Unknown"),
                details={
                    "entropy_bits": res.get("entropy_bits"),
                    "status": res.get("status"),
                    "length": res.get("password_length")
                }
            )

            score = res.get("score", 0)
            status = res.get("status", "")
            entropy = res.get("entropy_bits", 0)

            st.markdown("### 📊 Password Security Metrics")
            p1, p2, p3 = st.columns(3)
            p1.metric("Strength Rating", status)
            p2.metric("Shannon Entropy", f"{entropy} bits")
            p3.metric("Length", f"{res.get('password_length')} characters")

            st.progress(min(100, max(0, score)) / 100.0)

            st.markdown("---")
            st.markdown("#### ⏱️ Brute-Force Crack Time Estimates")
            crack = res.get("crack_times", {})
            ct1, ct2, ct3 = st.columns(3)
            ct1.metric("Online Attack (10 req/sec)", crack.get("online", "N/A"))
            ct2.metric("Desktop CPU (10k/sec)", crack.get("offline_slow", "N/A"))
            ct3.metric("GPU Cluster (100 Billion/sec)", crack.get("offline_fast", "N/A"))

            if res.get("feedback"):
                st.markdown("---")
                st.markdown("#### 💡 Password Strength Feedback")
                for tip in res.get("feedback", []):
                    st.info(f"👉 {tip}")

# =============================================================================
# VIEW 5: 📁 FILE INTEGRITY
# =============================================================================
elif selected_tab == "📁 File Integrity":
    st.button("⬅️ Return to Dashboard", key="back_file", on_click=switch_tab_callback, args=("📊 Dashboard & Analytics",))
    st.subheader("📁 In-Memory Cryptographic File Integrity & Extension Inspector")
    st.write("Upload suspicious files to calculate SHA-256, SHA-1, and MD5 hashes, verify file magic headers, and flag extension spoofing.")

    uploaded_file = st.file_uploader("Choose a file to analyze", type=None)

    if uploaded_file is not None:
        if st.button("🛡️ Audit File Integrity", use_container_width=True):
            with st.spinner("Calculating cryptographic hashes and inspecting magic headers..."):
                file_bytes = uploaded_file.getvalue()
                filename = uploaded_file.name
                
                analyzer = FileIntegrityAnalyzer()
                
                # Robust argument signature resolution for FileIntegrityAnalyzer.analyze()
                try:
                    res = analyzer.analyze(filename, file_bytes)
                except TypeError:
                    try:
                        res = analyzer.analyze(file_bytes, filename)
                    except TypeError:
                        res = analyzer.analyze(file_bytes)

                db.save_scan_log(
                    target=filename,
                    scan_type="File Integrity",
                    risk_score=res.get("risk_score", 0),
                    risk_level=res.get("risk_level", "Unknown"),
                    details={
                        "sha256": res.get("sha256"),
                        "file_size": res.get("file_size"),
                        "mime_type": res.get("mime_type")
                    }
                )

                st.markdown("### 📋 Cryptographic Hashes")
                st.code(f"SHA-256: {res.get('sha256')}\nSHA-1:   {res.get('sha1')}\nMD5:     {res.get('md5')}", language="text")

                f1, f2, f3 = st.columns(3)
                f1.metric("File Size", res.get("file_size_human", "N/A"))
                f2.metric("MIME Type", res.get("mime_type", "Unknown"))
                f3.metric("Risk Level", res.get("risk_level", "Unknown"))

                if res.get("warnings"):
                    st.markdown("---")
                    st.markdown("#### ⚠️ Anomalies Detected")
                    for warn in res.get("warnings", []):
                        st.warning(f"• {warn}")

# =============================================================================
# VIEW 6: 📈 AWARENESS SURVEY
# =============================================================================
elif selected_tab == "📈 Awareness Survey":
    st.button("⬅️ Return to Dashboard", key="back_survey", on_click=switch_tab_callback, args=("📊 Dashboard & Analytics",))
    st.subheader("📈 Cybersecurity Hygiene Awareness Survey")
    st.write("Assess your personal cybersecurity habits and compare your hygiene score against community benchmarks.")

    with st.form("survey_form"):
        q1 = st.selectbox("1. How often do you use unique passwords across accounts?", ["Always", "Frequently", "Rarely", "Never"])
        q2 = st.selectbox("2. Do you enable Multi-Factor Authentication (MFA) on critical accounts?", ["On all accounts", "On important accounts only", "Rarely", "Never"])
        q3 = st.selectbox("3. How do you handle links in unexpected or urgent emails?", ["Verify sender first", "Hover over link", "Click directly", "Ignore email"])
        
        submitted = st.form_submit_button("Submit Survey Response")
        if submitted:
            db.save_survey_response({"q1": q1, "q2": q2, "q3": q3})
            st.success("Thank you! Your responses have been safely recorded.")

# =============================================================================
# VIEW 7: 🎮 CYBER SECURITY QUIZ
# =============================================================================
elif selected_tab == "🎮 Cyber Security Quiz":
    st.button("⬅️ Return to Dashboard", key="back_quiz", on_click=switch_tab_callback, args=("📊 Dashboard & Analytics",))
    st.subheader("🎮 Interactive Cybersecurity Knowledge Challenge")
    st.write("Test your knowledge on common security risks, phishing traps, and best practices.")

    score = 0
    q1_ans = st.radio("1. What does 'HTTPS' stand for in a web address?", ["HyperText Transfer Protocol Secure", "High Transfer Protocol Service", "HyperText Technical Protocol System"])
    if q1_ans == "HyperText Transfer Protocol Secure":
        score += 1

    q2_ans = st.radio("2. Which of the following is an example of Multi-Factor Authentication (MFA)?", ["Entering password + SMS OTP", "Entering password + username", "Using the same password twice"])
    if q2_ans == "Entering password + SMS OTP":
        score += 1

    if st.button("Submit Answers"):
        st.balloons()
        st.success(f"🎉 You scored {score}/2!")
