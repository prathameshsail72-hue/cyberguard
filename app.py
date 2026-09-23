import streamlit as st
import os
import json
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
    APP_NAME, APP_VERSION, ORGANIZATION_NAME, TEAM_LEADER, GROUP_NAME,
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_ACCENT_CYAN, COLOR_RISK_HIGH,
    COLOR_RISK_MEDIUM, COLOR_RISK_LOW
)

# =============================================================================
# DATABASE CACHING
# =============================================================================
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# =============================================================================
# CUSTOM CSS / GLASSMORPHISM OBSIDIAN DESIGN SYSTEM
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    :root {
        --bg-base: #0b1120;
        --bg-surface: rgba(30, 41, 59, 0.65);
        --bg-surface-solid: #141b2d;
        --bg-card: #1e293b;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(56, 189, 248, 0.3);
        --text-primary: #f8fafc;
        --text-muted: #94a3b8;
        --primary: #38bdf8;
        --primary-2: #818cf8;
        --success: #10b981;
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
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid var(--border-strong);
        border-radius: 16px;
        padding: 22px 30px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .header-title {
        color: var(--primary);
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .header-subtitle {
        color: var(--text-muted);
        font-size: 1.02rem;
        margin-top: 4px;
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        position: relative;
        background: var(--bg-surface);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        margin-bottom: 12px;
        transition: transform 180ms ease, border-color 180ms ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: var(--border-strong);
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
        font-size: 2rem;
        font-weight: 800;
        margin-top: 4px;
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
        background-color: rgba(16, 185, 129, 0.16);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Content Cards */
    .content-box {
        background: #141b2d;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 8px 8px 0px 0px;
        padding: 10px 18px;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: var(--primary) !important;
        border-bottom: 2px solid var(--primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Header Banner
st.markdown(f"""
<div class="header-banner">
    <div class="header-title">🛡️ {APP_NAME} <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 400;">{APP_VERSION}</span></div>
    <div class="header-subtitle">Futuristic AI Cybersecurity Operations & Real-Time Threat Intelligence Dashboard | {GROUP_NAME}</div>
</div>
""", unsafe_allow_html=True)

# Sidebar System Status Overview
st.sidebar.markdown(f"### 🛡️ {APP_NAME}")
st.sidebar.markdown(f"**Version:** `{APP_VERSION}`")
st.sidebar.markdown(f"**Leader:** `{TEAM_LEADER}`")
st.sidebar.markdown(f"**Project:** `{GROUP_NAME}`")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ System Status")
st.sidebar.markdown(f"""
- 🟢 **Core Engine:** Active
- 💾 **Database:** `{os.path.basename(db.db_path)}`
- ☁️ **Deployment:** Streamlit Cloud / Render Ready
""")
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Navigate through the 8 tabs above to perform real-time security audits, analyze credentials, and test cyber awareness.")

# =============================================================================
# 8-TAB STREAMLIT LAYOUT (Phase 2 Requirement)
# =============================================================================
tab_home, tab_dash, tab_web, tab_phish, tab_pwd, tab_file, tab_survey, tab_quiz = st.tabs([
    "🏠 Home",
    "📊 Dashboard & Analytics",
    "🌐 Website Security",
    "🎣 Phishing Detector",
    "🔑 Password Entropy",
    "📁 File Integrity",
    "📈 Awareness Survey",
    "🎮 Cyber Security Quiz"
])

# -----------------------------------------------------------------------------
# TAB 1: 🏠 HOME
# -----------------------------------------------------------------------------
with tab_home:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                padding: 28px; border-radius: 14px; border: 1px solid rgba(56, 189, 248, 0.3);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); margin-bottom: 24px;">
        <h2 style="color: #38bdf8; font-weight: 800; margin-bottom: 6px;">
            🛡️ Community Engagement Project — CyberGuard 3.0 Pro
        </h2>
        <h4 style="color: #f8fafc; font-weight: 600; margin-top: 0;">
            Enterprise Cyber Threat Intelligence & Responsible Digital Literacy Operations
        </h4>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin-top: 12px;">
            CyberGuard 3.0 Pro is an advanced cybersecurity defensive operations platform engineered for comprehensive threat auditing, cryptographic verification, social engineering detection, and interactive community cyber hygiene education.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_proj, col_mission = st.columns(2)
    with col_proj:
        st.markdown(f"""
        <div style="background-color: #141b2d; padding: 22px; border-radius: 12px; border-left: 5px solid #38bdf8; height: 100%;">
            <h3 style="color: #38bdf8; margin-top: 0; font-weight: 700;">📌 PROJECT DIRECTORY</h3>
            <p style="color: #f8fafc; font-size: 1.05rem; line-height: 1.8;">
                • <strong>Program:</strong> Community Engagement Project (CEP)<br>
                • <strong>Group:</strong> <span style="color: #38bdf8; font-weight: 700;">{GROUP_NAME}</span><br>
                • <strong>Team Leader:</strong> <span style="color: #10b981; font-weight: 700;">{TEAM_LEADER}</span><br>
                • <strong>Core Initiative:</strong> Cyber Ethics & Responsible Internet Usage
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_mission:
        st.markdown("""
        <div style="background-color: #141b2d; padding: 22px; border-radius: 12px; border-left: 5px solid #10b981; height: 100%;">
            <h3 style="color: #10b981; margin-top: 0; font-weight: 700;">🎯 MISSION & PURPOSE</h3>
            <p style="color: #f8fafc; font-size: 1rem; line-height: 1.6;">
                Equip individuals, students, and organizations with proactive defensive capabilities to identify phishing vectors, evaluate SSL/TLS infrastructure, quantify password entropy, verify digital file integrity, and uphold ethical standards in digital safety.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚖️ Core Cyber-Ethics Principles")
    
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown("""
        <div class="content-box" style="border-top: 3px solid #38bdf8;">
            <h4 style="color: #38bdf8; margin-top: 0;">1. Consent & Authorization</h4>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">
                Security audits and vulnerability assessments must strictly occur on systems, domains, and files owned or explicitly authorized for testing.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="content-box" style="border-top: 3px solid #818cf8;">
            <h4 style="color: #818cf8; margin-top: 0;">4. Digital Empathy</h4>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">
                Focus on constructive education, empathetic remediation, and empowerment rather than punitive fault-finding when incidents occur.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown("""
        <div class="content-box" style="border-top: 3px solid #10b981;">
            <h4 style="color: #10b981; margin-top: 0;">2. Privacy by Design</h4>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">
                Zero persistent storage of sensitive secrets or raw passwords. User communications and inputs are processed ephemerally.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="content-box" style="border-top: 3px solid #f59e0b;">
            <h4 style="color: #f59e0b; margin-top: 0;">5. Continuous Learning</h4>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">
                Cyber threats evolve dynamically; staying educated on emerging vectors and maintaining active cyber hygiene is fundamental.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with e3:
        st.markdown("""
        <div class="content-box" style="border-top: 3px solid #ef4444;">
            <h4 style="color: #ef4444; margin-top: 0;">3. Responsible Disclosure</h4>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">
                Vulnerabilities discovered in digital systems should be reported responsibly to affected organizations prior to public release.
            </p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: 📊 DASHBOARD & ANALYTICS
# -----------------------------------------------------------------------------
with tab_dash:
    st.subheader("📊 Security Analytics & Threat Operations Overview")
    
    stats = db.get_dashboard_stats()
    
    # 4 Top-line Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Security Audits</div>
            <div class="metric-val" style="color: #38bdf8;">{stats['total_scans']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        avg_score = stats['avg_score']
        score_color = "#10b981" if avg_score >= 75 else "#f59e0b" if avg_score >= 45 else "#ef4444"
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
            <div class="metric-val" style="color: #ef4444;">{stats['high_risk_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Clean / Low Risk Audits</div>
            <div class="metric-val" style="color: #10b981;">{stats['low_risk_count']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Altair Charts: Bar Chart of Scans by Module & Arc/Pie Chart of Risk Distribution
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
            {"Risk Level": "High Risk", "Count": stats['high_risk_count'], "Color": "#ef4444"},
            {"Risk Level": "Medium Risk", "Count": stats['medium_risk_count'], "Color": "#f59e0b"},
            {"Risk Level": "Low Risk", "Count": stats['low_risk_count'], "Color": "#10b981"}
        ]
        df_risk = pd.DataFrame(risk_counts)
        if df_risk["Count"].sum() > 0:
            pie_chart = (
                alt.Chart(df_risk)
                .mark_arc(innerRadius=45, stroke="#0b1120", strokeWidth=2)
                .encode(
                    theta=alt.Theta("Count:Q"),
                    color=alt.Color(
                        "Risk Level:N",
                        scale=alt.Scale(
                            domain=["High Risk", "Medium Risk", "Low Risk"],
                            range=["#ef4444", "#f59e0b", "#10b981"]
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

# -----------------------------------------------------------------------------
# TAB 3: 🌐 WEBSITE SECURITY
# -----------------------------------------------------------------------------
with tab_web:
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

                # Persist to database audit log
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

# -----------------------------------------------------------------------------
# TAB 4: 🎣 PHISHING DETECTOR
# -----------------------------------------------------------------------------
with tab_phish:
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

                # Persist to database log (Never persist full body, only non-sensitive summary)
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

# -----------------------------------------------------------------------------
# TAB 5: 🔑 PASSWORD ENTROPY
# -----------------------------------------------------------------------------
with tab_pwd:
    st.subheader("🔑 Mathematical Password Entropy & Strength Analyzer")
    st.write("Calculate Shannon entropy in bits, analyze character set diversity, and estimate brute-force cracking resistance across various attacker computing speeds.")

    pwd_input = st.text_input("Enter Password to Test (Masked):", type="password", placeholder="Type a password or passphrase...")

    if st.button("🔐 Analyze Password Strength", use_container_width=True):
        if not pwd_input:
            st.warning("Please enter a password to evaluate.")
        else:
            analyzer = PasswordAnalyzer()
            res = analyzer.analyze(pwd_input)

            # Persist only non-sensitive derived metrics (RAW PASSWORD IS NEVER PERSISTED)
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
            ct1.metric("Online (10 req/sec)", crack.get("online", "N/A"))
            ct2.metric("Desktop CPU (10k req/sec)", crack.get("cpu", "N/A"))
            ct3.metric("GPU Cluster (100B req/sec)", crack.get("gpu_cluster", "N/A"))

            st.markdown("---")
            col_comp, col_tips = st.columns(2)

            with col_comp:
                st.markdown("#### 🔣 Character Composition")
                st.markdown(f"- Lowercase Letters (a-z): {'✅ Present' if res.get('has_lower') else '❌ Missing'}")
                st.markdown(f"- Uppercase Letters (A-Z): {'✅ Present' if res.get('has_upper') else '❌ Missing'}")
                st.markdown(f"- Numbers (0-9): {'✅ Present' if res.get('has_digit') else '❌ Missing'}")
                st.markdown(f"- Special Symbols (@, #, $, %): {'✅ Present' if res.get('has_symbol') else '❌ Missing'}")
                if res.get("is_common"):
                    st.error("🚨 Found in Common Breached Password Lists!")

            with col_tips:
                st.markdown("#### 💡 Hardening Guidance")
                if res.get("feedback"):
                    for fb in res.get("feedback"):
                        st.warning(f"• {fb}")
                if res.get("improvements"):
                    for imp in res.get("improvements"):
                        st.info(f"👉 {imp}")

# -----------------------------------------------------------------------------
# TAB 6: 📁 FILE INTEGRITY
# -----------------------------------------------------------------------------
with tab_file:
    st.subheader("📁 In-Memory File Integrity & Extension Spoofing Inspector")
    st.write("Compute cryptographic SHA-256, SHA-1, and MD5 hashes in-memory, inspect magic byte file headers, and detect double-extension disguises.")

    uploaded_file = st.file_uploader("Upload a file to inspect (Processed entirely in-memory — never saved to disk):", type=None)

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        analyzer = FileIntegrityAnalyzer()
        res = analyzer.analyze_bytes(file_bytes, uploaded_file.name)

        # Log non-sensitive file metadata
        db.save_scan_log(
            target=uploaded_file.name,
            scan_type="File Integrity",
            risk_score=res.get("risk_score", 0),
            risk_level=res.get("risk_level", "Unknown"),
            details={
                "sha256": res.get("sha256"),
                "file_size": res.get("file_size_formatted"),
                "magic_matched": res.get("magic_matched")
            }
        )

        score = res.get("risk_score", 100)
        level = res.get("risk_level", "Unknown")
        badge_class = "badge-low" if level == "Low Risk" else "badge-med" if level == "Medium Risk" else "badge-high"

        st.markdown("### 📋 File Analysis Report")
        fc1, fc2, fc3 = st.columns(3)
        fc1.metric("Integrity Score", f"{score} / 100")
        fc2.markdown(f"**Risk Level:** <br><span class='{badge_class}'>{level}</span>", unsafe_allow_html=True)
        fc3.metric("File Size", res.get("file_size_formatted"))

        st.markdown("---")
        st.markdown("#### 🔑 Cryptographic Hashes")
        st.code(
            f"SHA-256: {res.get('sha256')}\n"
            f"SHA-1:   {res.get('sha1')}\n"
            f"MD5:     {res.get('md5')}",
            language="text"
        )

        # Hash Verification Tool
        st.markdown("#### 🔍 Verify Known Hash Match")
        expected_hash = st.text_input("Paste Expected Hash to Compare (SHA-256, SHA-1, or MD5):", placeholder="Paste known checksum here...").strip().lower()
        if expected_hash:
            computed_hashes = [res.get('sha256', '').lower(), res.get('sha1', '').lower(), res.get('md5', '').lower()]
            if expected_hash in computed_hashes:
                st.success("✅ HASH MATCH VERIFIED: The uploaded file matches the expected cryptographic checksum exactly.")
            else:
                st.error("❌ HASH MISMATCH: The file checksum does not match the expected hash. Possible file corruption or tampering.")

        st.markdown("---")
        col_hdr, col_ext = st.columns(2)
        with col_hdr:
            st.markdown("#### 🔬 Header Magic Bytes")
            st.markdown(f"**Header Hex:** `{res.get('header_hex')}`")
            if res.get("magic_matched"):
                st.success("✅ File header magic bytes match the reported file extension.")
            else:
                st.error("❌ Header Mismatch: Byte signature does not match the file extension!")

        with col_ext:
            st.markdown("#### 🎭 Extension Masking Audit")
            if res.get("is_double_ext"):
                st.error("🚨 Double Extension Spoofing Detected! (e.g. filename.pdf.exe)")
            else:
                st.success("✅ No double-extension spoofing detected.")

        if res.get("anomalies"):
            st.markdown("---")
            st.markdown("#### ⚠️ Identified Anomalies")
            for an in res.get("anomalies"):
                st.warning(f"• {an}")

# -----------------------------------------------------------------------------
# TAB 7: 📈 AWARENESS SURVEY
# -----------------------------------------------------------------------------
with tab_survey:
    st.subheader("📈 Community Cybersecurity Awareness Survey")
    st.write("Participate in the community cyber hygiene assessment. Your responses help measure digital literacy benchmarks and shape training programs.")

    with st.form("awareness_survey_form"):
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            name_input = st.text_input("Name (Optional):", placeholder="Anonymous / Your Name")
            age_group = st.selectbox("Age Group:", ["<18", "18-24", "25-34", "35-50", "50+"])
            role = st.selectbox("Primary Role:", [
                "Student / Educator", "IT / Security Professional", "Corporate Employee", "General Public", "Senior Citizen"
            ])
            awareness_val = st.slider("Self-Rated Cybersecurity Awareness Level (1 = Novice, 5 = Expert):", 1, 5, 3)

        with s_col2:
            mfa_usage = st.selectbox("Multi-Factor Authentication (2FA/MFA) Usage:", [
                "Always on all accounts", "Only on banking/work", "Rarely", "Never"
            ])
            pwd_habits = st.selectbox("Password Reuse Habits:", [
                "Unique passphrase per account (Password Manager)", "A few variations reused across accounts", "Same password everywhere"
            ])
            training_int = st.selectbox("Interest in Free Cyber Defense Training Workshops:", [
                "Yes, strongly interested", "Maybe in future", "No"
            ])
            comments_text = st.text_area("Feedback or Comments (Optional):", placeholder="Share your thoughts on digital safety...", height=70)

        submit_survey = st.form_submit_button("📩 Submit Survey Response", use_container_width=True)

        if submit_survey:
            db.save_survey_response(
                name=name_input,
                age_group=age_group,
                role=role,
                awareness_rating=awareness_val,
                two_factor_auth=mfa_usage,
                password_reuse=pwd_habits,
                training_interest=training_int,
                comments=comments_text
            )
            st.success("🎉 Thank you! Your survey response has been recorded successfully.")

    st.markdown("---")
    st.markdown("### 📊 Aggregated Community Benchmark Analytics")
    survey_stats = db.get_survey_analytics()
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### 🎓 Average Awareness Rating by Role (1-5 Scale)")
        by_role_data = survey_stats.get("by_role", [])
        if by_role_data:
            df_role = pd.DataFrame(by_role_data)
            chart_role = (
                alt.Chart(df_role)
                .mark_bar(cornerRadiusEnd=6, size=22, color="#38bdf8")
                .encode(
                    x=alt.X("avg_rating:Q", title="Average Rating (1-5)", scale=alt.Scale(domain=[0, 5])),
                    y=alt.Y("role:N", title=None, sort="-x"),
                    tooltip=["role", "avg_rating", "response_count"]
                )
                .properties(height=220, background="transparent")
            )
            st.altair_chart(chart_role, use_container_width=True)
        else:
            st.info("No survey records yet.")

    with col_s2:
        st.markdown("#### 🔐 2FA / MFA Adoption Distribution")
        by_2fa_data = survey_stats.get("by_2fa", [])
        if by_2fa_data:
            df_2fa = pd.DataFrame(by_2fa_data)
            chart_2fa = (
                alt.Chart(df_2fa)
                .mark_arc(innerRadius=40, stroke="#0b1120", strokeWidth=2)
                .encode(
                    theta=alt.Theta("count:Q"),
                    color=alt.Color("two_factor_auth:N", legend=alt.Legend(orient="right", title="2FA Habit")),
                    tooltip=["two_factor_auth", "count"]
                )
                .properties(height=220, background="transparent")
            )
            st.altair_chart(chart_2fa, use_container_width=True)
        else:
            st.info("No 2FA distribution data yet.")

    st.markdown("#### 📋 Recent Community Survey Submissions")
    recent_surveys = survey_stats.get("recent_responses", [])
    if recent_surveys:
        df_surv_table = pd.DataFrame(recent_surveys)[["name", "age_group", "role", "awareness_rating", "two_factor_auth", "password_reuse", "submitted_at"]]
        df_surv_table.columns = ["Name", "Age Group", "Role", "Awareness (1-5)", "2FA Habit", "Password Habit", "Submitted At"]
        st.dataframe(df_surv_table, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 8: 🎮 CYBER SECURITY QUIZ
# -----------------------------------------------------------------------------
with tab_quiz:
    st.subheader("🎮 Interactive Cyber Security Knowledge Challenge")
    st.write("Test your cyber defense knowledge across 8 core domains and earn your verified security badge on the community leaderboard.")

    quiz_name = st.text_input("Player Name / Nickname for Leaderboard:", value="Cyber Explorer")

    quiz_questions = [
        {
            "q": "1. What is the most secure method for managing complex passwords across multiple services?",
            "options": [
                "Reusing a strong password with a few minor variations",
                "Using unique, high-entropy passphrases stored in an encrypted password manager",
                "Writing down passwords in a physical notebook kept beside the computer",
                "Saving all passwords in an unencrypted spreadsheet on the desktop"
            ],
            "correct": "Using unique, high-entropy passphrases stored in an encrypted password manager",
            "explanation": "Password managers allow users to generate and securely store unique, long, and complex passwords for every single service without risking credential-stuffing attacks."
        },
        {
            "q": "2. Which psychological trigger is most commonly exploited in phishing and social engineering attacks?",
            "options": [
                "Artificial urgency, high-pressure threats of immediate suspension, or fake financial deadlines",
                "Long detailed technical documentation",
                "Formal verified legal contracts delivered via certified mail",
                "Scheduled quarterly maintenance notices"
            ],
            "correct": "Artificial urgency, high-pressure threats of immediate suspension, or fake financial deadlines",
            "explanation": "Attackers induce cognitive panic with artificial urgency (e.g. 'Account suspended in 24 hours!') to compel victims to act before critically evaluating the message."
        },
        {
            "q": "3. Why is using Multi-Factor Authentication (2FA/MFA) critically important?",
            "options": [
                "It speeds up your internet connection",
                "It requires a secondary verification factor, preventing unauthorized access even if passwords are leaked",
                "It automatically changes passwords every 24 hours",
                "It replaces the need for antivirus software"
            ],
            "correct": "It requires a secondary verification factor, preventing unauthorized access even if passwords are leaked",
            "explanation": "MFA combines something you know (password) with something you have (authenticator app/security key), blocking up to 99% of automated credential theft attempts."
        },
        {
            "q": "4. What security danger does an email attachment named 'Invoice_March.pdf.exe' represent?",
            "options": [
                "The file will take twice as much disk storage",
                "Double-extension spoofing designed to trick users into launching malicious executable code",
                "It converts your operating system into a virtual machine",
                "It is a legitimate compressed PDF archive"
            ],
            "correct": "Double-extension spoofing designed to trick users into launching malicious executable code",
            "explanation": "Operating systems often hide known extensions by default; attackers exploit this by appending '.exe' or '.scr' after '.pdf' so victims click on executable malware."
        },
        {
            "q": "5. What is the primary purpose of HTTPS and SSL/TLS encryption?",
            "options": [
                "To speed up webpage loading times",
                "To encrypt data in transit and authenticate the web server's identity to prevent eavesdropping and MITM tampering",
                "To prevent all types of malware from running on the client computer",
                "To block pop-up ads automatically"
            ],
            "correct": "To encrypt data in transit and authenticate the web server's identity to prevent eavesdropping and MITM tampering",
            "explanation": "HTTPS encrypts the communication channel between browser and server, safeguarding session tokens, passwords, and sensitive information from interception on untrusted networks."
        },
        {
            "q": "6. How does Shannon mathematical entropy measure password resilience?",
            "options": [
                "It counts how many vowel letters exist in the word",
                "It quantifies the bits of unpredictability based on length and character set pool size, determining resistance to brute-force guessing",
                "It tests whether the password matches your username",
                "It calculates how fast the user can type the password"
            ],
            "correct": "It quantifies the bits of unpredictability based on length and character set pool size, determining resistance to brute-force guessing",
            "explanation": "Entropy (E = L * log2(R)) calculates the total theoretical search space an attacker must exhaust during brute-force or dictionary cracking."
        },
        {
            "q": "7. What is a cryptographic hash function (e.g. SHA-256) primarily used for in file integrity?",
            "options": [
                "To compress large files into smaller zip archives",
                "To generate a deterministic, irreversible digital fingerprint that changes if even a single byte is altered",
                "To decrypt passwords automatically",
                "To run antivirus scans on memory"
            ],
            "correct": "To generate a deterministic, irreversible digital fingerprint that changes if even a single byte is altered",
            "explanation": "Cryptographic hashes produce unique fixed-length digests; any alteration in the underlying file completely changes the hash, proving data integrity or tampering."
        },
        {
            "q": "8. Why is entering confidential credentials over unencrypted public Wi-Fi hazardous?",
            "options": [
                "Public Wi-Fi discharges laptop batteries faster",
                "Attackers on the same local network can intercept unencrypted session packets or deploy Evil Twin spoofing",
                "Public Wi-Fi voids your computer manufacturer warranty",
                "It reduces screen resolution"
            ],
            "correct": "Attackers on the same local network can intercept unencrypted session packets or deploy Evil Twin spoofing",
            "explanation": "Open networks lack client isolation; attackers can eavesdrop on plaintext communications or spoof legitimate access points to capture user data."
        }
    ]

    with st.form("quiz_form"):
        user_responses = []
        for idx, item in enumerate(quiz_questions):
            st.markdown(f"**{item['q']}**")
            ans = st.radio(
                f"Question {idx+1}",
                item["options"],
                index=None,
                key=f"quiz_q_{idx}",
                label_visibility="collapsed"
            )
            user_responses.append(ans)
            st.write("")

        submit_quiz = st.form_submit_button("🎯 Submit Quiz Answers", use_container_width=True)

    if submit_quiz:
        if None in user_responses:
            st.warning("⚠️ Please answer all 8 questions before submitting!")
        else:
            score = 0
            for i, item in enumerate(quiz_questions):
                if user_responses[i] == item["correct"]:
                    score += 1

            total_q = len(quiz_questions)
            pct = int((score / total_q) * 100)

            if score == 8:
                badge = "🛡️ Cyber Guardian Gold"
            elif score >= 6:
                badge = "🥈 Security Apprentice Silver"
            elif score >= 4:
                badge = "🥉 Cyber Defender Bronze"
            else:
                badge = "🔰 Security Recruit"

            # Save score to SQLite database
            db.save_quiz_score(score, total_q, badge, player_name=quiz_name)

            if score >= 6:
                st.balloons()

            st.markdown(f"### 🏆 Result: {score} / {total_q} ({pct}%)")
            st.markdown(f"**Badge Earned:** `{badge}`")

            st.markdown("---")
            st.markdown("### 📝 Detailed Answer Review & Explanations")
            for i, item in enumerate(quiz_questions):
                user_ans = user_responses[i]
                is_correct = user_ans == item["correct"]
                if is_correct:
                    st.success(f"**{item['q']}**\n\n✅ **Your Answer:** {user_ans}\n\n💡 **Explanation:** {item['explanation']}")
                else:
                    st.error(f"**{item['q']}**\n\n❌ **Your Answer:** {user_ans}\n\n👉 **Correct Answer:** {item['correct']}\n\n💡 **Explanation:** {item['explanation']}")

    st.markdown("---")
    st.markdown("#### 🏆 Global Quiz Leaderboard")
    q_stats = db.get_quiz_stats()
    qc1, qc2, qc3 = st.columns(3)
    qc1.metric("Total Quiz Attempts", q_stats.get("total_attempts", 0))
    qc2.metric("Average Score", f"{q_stats.get('avg_percentage', 0)}%")
    qc3.metric("Highest Score", f"{q_stats.get('high_score', 0)} / 8")

    leaderboard = q_stats.get("leaderboard", [])
    if leaderboard:
        df_lead = pd.DataFrame(leaderboard)[["player_name", "score", "percentage", "badge_earned", "completed_at"]]
        df_lead.columns = ["Player", "Score (out of 8)", "Accuracy %", "Badge Earned", "Completed At"]
        st.dataframe(df_lead, use_container_width=True)
    else:
        st.info("No quiz scores recorded yet. Be the first to take the quiz!")
