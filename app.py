import streamlit as st
import os
import json
import inspect
import time
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

# Design system module (CSS + live-telemetry / radar-scan / pulse-badge components)
from style import (
    load_css,
    render_system_status_bar,
    render_telemetry_pills,
    radar_scan_html,
    pulse_badge_html,
    risk_level_to_pulse_kind,
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
load_css()

# Header
st.markdown(f"""
<div class="header-banner">
    <div class="header-title">🛡️ {APP_NAME} <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 400;">{APP_VERSION}</span></div>
    <div class="header-subtitle">Futuristic AI Cybersecurity Operations & Real-Time Threat Intelligence Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Live "system online" beacon + simulated telemetry pills
render_system_status_bar()
render_telemetry_pills()

# Sidebar
st.sidebar.markdown(f"### 🛡️ {APP_NAME}")
st.sidebar.markdown(f"**Version:** `{APP_VERSION}`")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ System Status")
st.sidebar.markdown(f"""
- 🟢 **Core Engine:** Active
- 💾 **Database:** `{os.path.basename(db.db_path)}`
- ☁️ **Deployment:** Streamlit Cloud Ready
- 🕒 **Session Started:** `{datetime.now().strftime('%H:%M:%S')}`
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
    st.markdown(f"#### 📜 Live Security Audit History Log <span style='font-size:0.75rem; color:#64748b; font-family: JetBrains Mono, monospace;'>&nbsp;&nbsp;last refreshed {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_allow_html=True)
    recent = stats.get("recent_scans", [])
    if recent:
        df_recent = pd.DataFrame(recent)[["target", "scan_type", "risk_score", "risk_level", "scanned_at"]]
        df_recent.columns = ["Target / Artifact", "Module", "Score", "Risk Level", "Scanned At"]
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No historical scan logs found.")

    # =========================================================================
    # SECTION A: 🌐 GLOBAL & INDIAN MAJOR CYBER ATTACK TIMELINE & CASE STUDIES
    # =========================================================================
    st.markdown("---")
    st.markdown("""
    <div class="guide-banner">
        <h3 style="color: #38bdf8; margin:0; font-size: 1.25rem; font-weight: 800;">🌐 Global & Indian Major Cyber Attack Timeline & Case Studies</h3>
        <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 0.9rem;">
            A curated threat-intelligence archive of landmark incidents that reshaped global and national cybersecurity posture.
        </p>
    </div>
    """, unsafe_allow_html=True)

    GLOBAL_INCIDENTS = [
        {
            "title": "WannaCry Ransomware (2017)",
            "sev": "critical",
            "sev_label": "🔴 Critical",
            "desc": "A self-propagating ransomware worm that exploited the EternalBlue SMB vulnerability, encrypting files across unpatched Windows systems worldwide.",
            "sector": "Healthcare, Telecom, Logistics (Global)",
            "vector": "EternalBlue SMBv1 Exploit (Worm)",
            "impact": "200,000+ computers in 150 countries, $4B+ in damages",
            "takeaway": "Timely OS patching and disabling legacy SMBv1 could have prevented the vast majority of infections."
        },
        {
            "title": "SolarWinds Cyber Espionage (2020)",
            "sev": "critical",
            "sev_label": "🔴 Critical",
            "desc": "A nation-state-grade supply chain compromise that inserted a backdoor (SUNBURST) into Orion software updates, granting long-term covert access to victim networks.",
            "sector": "Government, Defense, Fortune 500 (Global)",
            "vector": "Compromised Software Supply Chain Update",
            "impact": "18,000+ public/private organizations affected",
            "takeaway": "Verify software build integrity and monitor for anomalous outbound traffic from trusted vendor updates."
        },
        {
            "title": "MOVEit Transfer Zero-Day Exploit (2023)",
            "sev": "major",
            "sev_label": "🟠 Major Breach",
            "desc": "Attackers exploited an SQL injection zero-day in the MOVEit managed file transfer software to mass-exfiltrate sensitive data from client organizations.",
            "sector": "Enterprise File Transfer / Multi-Industry",
            "vector": "SQL Injection Zero-Day",
            "impact": "2,000+ enterprises and millions of individual records exposed",
            "takeaway": "Apply emergency vendor patches immediately and minimize exposure of file-transfer infrastructure to the public internet."
        },
    ]

    INDIA_INCIDENTS = [
        {
            "title": "AIIMS New Delhi Cyber Attack (2022)",
            "sev": "critical",
            "sev_label": "🔴 Critical",
            "desc": "A ransomware assault crippled digital hospital systems, forcing manual patient registration and outpatient handling for weeks.",
            "sector": "Healthcare / Critical Public Infrastructure",
            "vector": "Ransomware (server-side compromise)",
            "impact": "Outpatient services & core servers down for ~2 weeks",
            "takeaway": "Segment critical healthcare networks and maintain offline backups for continuity of patient care."
        },
        {
            "title": "Kudankulam Nuclear Power Plant Breach (2019)",
            "sev": "critical",
            "sev_label": "🔴 Critical",
            "desc": "DTrack malware was identified on an administrative (non-critical) network at India's largest nuclear power plant, raising alarms over critical infrastructure security.",
            "sector": "Energy / Critical Infrastructure",
            "vector": "DTrack Malware (spear-phishing entry point)",
            "impact": "Administrative network compromise; operational systems reported unaffected",
            "takeaway": "Strict air-gapping between administrative IT and operational technology (OT) networks is essential."
        },
        {
            "title": "Cosmos Bank Cyber Heist, Pune (2018)",
            "sev": "major",
            "sev_label": "🟠 Major Breach",
            "desc": "A coordinated malware attack on the bank's switching system enabled simultaneous fraudulent ATM withdrawals across multiple countries in a tightly synchronized window.",
            "sector": "Banking & Financial Services",
            "vector": "Malware on Payment Switch / Card Cloning",
            "impact": "₹94+ Crore (~$13.5M) siphoned via 28 countries in under 2 hours",
            "takeaway": "Real-time transaction anomaly detection and payment-switch isolation are critical for fraud containment."
        },
        {
            "title": "Power Grid Ransomware / Mumbai Blackout Analysis (2020)",
            "sev": "alert",
            "sev_label": "🟡 High Alert",
            "desc": "Security researchers identified malware targeting Maharashtra's state electricity transmission utility, coinciding with a major Mumbai power outage investigation.",
            "sector": "Energy / Power Grid Infrastructure",
            "vector": "Suspected State-Sponsored Malware Intrusion",
            "impact": "Investigation into grid utility systems; heightened critical-infra scrutiny",
            "takeaway": "Continuous OT network monitoring and incident-response drills are vital for power-grid resilience."
        },
    ]

    def render_incident_card(item):
        card_class = "threat-card" if item["sev"] == "critical" else f"threat-card {item['sev']}"
        sev_class = f"sev-{item['sev']}"
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap: wrap; gap: 8px;">
                <strong style="color:#f8fafc; font-size:1.05rem;">{item['title']}</strong>
                <span class="{sev_class}">{item['sev_label']}</span>
            </div>
            <div style="color:#cbd5e1; margin-top:8px; font-size:0.9rem; line-height:1.5;">{item['desc']}</div>
            <div class="threat-meta-grid">
                <div class="threat-meta-item">
                    <div class="threat-meta-label">Target Sector</div>
                    <div class="threat-meta-val">{item['sector']}</div>
                </div>
                <div class="threat-meta-item">
                    <div class="threat-meta-label">Attack Vector</div>
                    <div class="threat-meta-val">{item['vector']}</div>
                </div>
                <div class="threat-meta-item">
                    <div class="threat-meta-label">Estimated Impact</div>
                    <div class="threat-meta-val">{item['impact']}</div>
                </div>
                <div class="threat-meta-item">
                    <div class="threat-meta-label">Primary Defense Takeaway</div>
                    <div class="threat-meta-val">{item['takeaway']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    tab_global, tab_india = st.tabs(["🌍 Global High-Impact Incidents", "🇮🇳 India-Specific Case Studies"])

    with tab_global:
        for item in GLOBAL_INCIDENTS:
            render_incident_card(item)

    with tab_india:
        for item in INDIA_INCIDENTS:
            render_incident_card(item)

    # =========================================================================
    # SECTION B: 🇮🇳 OFFICIAL INDIAN CYBERCRIME REPORTING & EMERGENCY HUB
    # =========================================================================
    st.markdown("---")
    st.markdown("""
    <div class="guide-banner">
        <h3 style="color: #38bdf8; margin:0; font-size: 1.25rem; font-weight: 800;">🇮🇳 Official Indian Cybercrime Reporting & Emergency Assistance Hub</h3>
        <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 0.9rem;">
            Verified national helplines, nodal agencies, and reporting protocols for citizens and enterprises facing cyber incidents in India.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        hc1, hc2 = st.columns([1, 2])
        with hc1:
            st.markdown("""
            <div class="helpline-card" style="text-align:center;">
                <div class="metric-label">National Cyber Crime Helpline</div>
                <div class="helpline-number">1930</div>
                <div style="color:#94a3b8; font-size:0.85rem; margin-top:4px;">Toll-Free · 24/7 Citizen Assistance</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("📞 Report at cybercrime.gov.in", "https://www.cybercrime.gov.in", use_container_width=True)

        with hc2:
            st.markdown("""
            <div class="helpline-card">
                <div class="metric-label">Operating Authority</div>
                <div style="color:#f8fafc; font-weight:700; font-size:1.05rem; margin-top:4px;">
                    Ministry of Home Affairs (MHA), Government of India<br>
                    Indian Cyber Crime Coordination Centre (I4C)
                </div>
                <div class="golden-hour-box">
                    <strong style="color:#f87171;">⏱️ The "Golden Hour" Rule</strong>
                    <div style="color:#cbd5e1; font-size:0.88rem; margin-top:4px;">
                        Report unauthorized financial transactions within <strong>1–2 hours</strong> of occurrence via the
                        1930 helpline or the portal to trigger inter-bank freeze protocols and maximize fund-recovery chances.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("#### 🏛️ Key Indian Incident Reporting Bodies & Nodal Agencies")
    ac1, ac2, ac3 = st.columns(3)

    with ac1:
        st.markdown("""
        <div class="content-box">
            <div class="feature-title">🛰️ CERT-In</div>
            <div class="feature-desc">
                Indian Computer Emergency Response Team — the national nodal agency for cyber incident response and advisories.<br><br>
                <strong>Web:</strong> www.cert-in.org.in<br>
                <strong>Incident Email:</strong> incident@cert-in.org.in
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 Visit CERT-In", "https://www.cert-in.org.in", use_container_width=True)

    with ac2:
        st.markdown("""
        <div class="content-box">
            <div class="feature-title">🏭 NCIIPC</div>
            <div class="feature-desc">
                National Critical Information Infrastructure Protection Centre — safeguards national critical assets across
                power, banking, telecom, and government sectors.<br><br>
                <strong>Web:</strong> www.nciipc.gov.in
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 Visit NCIIPC", "https://www.nciipc.gov.in", use_container_width=True)

    with ac3:
        st.markdown("""
        <div class="content-box">
            <div class="feature-title">🏦 RBI Cyber Fraud & Ombudsman</div>
            <div class="feature-desc">
                Reserve Bank of India guidelines provide a <strong>zero-liability policy</strong> on unauthorized electronic
                banking transactions if reported to your bank within <strong>3 days</strong>.<br><br>
                Escalate unresolved banking fraud via the RBI Ombudsman Portal.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 RBI Ombudsman Portal", "https://cms.rbi.org.in", use_container_width=True)

    st.info("💡 **Reminder:** Always preserve transaction IDs, screenshots, and sender details before reporting — these are essential for law-enforcement follow-up.")

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
            radar_slot = st.empty()
            radar_slot.markdown(
                radar_scan_html("SCANNING TARGET", f"Inspecting {target_url.strip()} — DNS, TLS & headers"),
                unsafe_allow_html=True,
            )
            analyzer = URLAnalyzer()
            res = analyzer.analyze(target_url)
            radar_slot.empty()

            db.save_scan_log(
                target=res.get("target", target_url),
                scan_type="URL Audit",
                risk_score=res.get("risk_score", 0),
                risk_level=res.get("risk_level", "Unknown"),
                details=res
            )

            score = res.get("risk_score", 0)
            level = res.get("risk_level", "Unknown")
            pulse_html = pulse_badge_html(level, risk_level_to_pulse_kind(level))

            st.markdown("### 📋 Audit Findings")
            m1, m2, m3 = st.columns(3)
            m1.metric("Safety Score", f"{score} / 100")
            m2.markdown(f"**Risk Level:** <br>{pulse_html}", unsafe_allow_html=True)
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
            radar_slot = st.empty()
            radar_slot.markdown(
                radar_scan_html("ANALYZING PAYLOAD", "Scanning for social engineering cues & deceptive URLs"),
                unsafe_allow_html=True,
            )
            detector = PhishingDetector()
            res = detector.analyze(sample_text)
            radar_slot.empty()

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
            pulse_html = pulse_badge_html(f"{verdict} · {p_score}%", risk_level_to_pulse_kind(level))
            st.markdown(pulse_html, unsafe_allow_html=True)

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
            level = res.get("risk_level", "Unknown")

            st.markdown("### 📊 Password Security Metrics")
            st.markdown(pulse_badge_html(status, risk_level_to_pulse_kind(level)), unsafe_allow_html=True)
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
            radar_slot = st.empty()
            radar_slot.markdown(
                radar_scan_html("HASHING FILE", f"Computing checksums for {uploaded_file.name}"),
                unsafe_allow_html=True,
            )
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
            radar_slot.empty()

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

            level = res.get("risk_level", "Unknown")
            st.markdown("### 📋 Cryptographic Hashes")
            st.markdown(pulse_badge_html(level, risk_level_to_pulse_kind(level)), unsafe_allow_html=True)
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
    st.subheader("📈 Cybersecurity Awareness & Hygiene Assessment")
    st.write("Complete this quick survey to measure your personal security posture and contribute to global community benchmark metrics.")

    with st.form("survey_form"):
        role = st.selectbox("Your Organizational Role:", ["Student", "IT Professional", "Developer / Engineer", "Management / Executive", "General Consumer"])
        q1 = st.radio("Do you use a dedicated password manager?", ["Yes, always", "Sometimes", "No, I reuse/memorize passwords"])
        q2 = st.radio("Is Multi-Factor Authentication (MFA) enabled on your primary accounts?", ["Enforced on all accounts", "Only on critical accounts (Email/Bank)", "No"])
        q3 = st.radio("How frequently do you audit software updates and security patches?", ["Automatically installed / Immediately", "Monthly", "Rarely / Never"])
        comments = st.text_area("Additional Security Feedback or Comments (Optional):", value="", placeholder="Share any specific security challenges or thoughts...")
        
        submitted = st.form_submit_button("📊 Submit Assessment")
        
        if submitted:
            score = 100
            if q1 == "Sometimes": score -= 20
            elif q1 == "No, I reuse/memorize passwords": score -= 40
            
            if q2 == "Only on critical accounts (Email/Bank)": score -= 15
            elif q2 == "No": score -= 35
            
            if q3 == "Monthly": score -= 10
            elif q3 == "Rarely / Never": score -= 25

            risk_level = "Low Risk" if score >= 80 else "Medium Risk" if score >= 50 else "High Risk"

            # Check if save_survey_response is present and call it with required signature
            if hasattr(db, "save_survey_response"):
                db.save_survey_response(
                    role=role,
                    q1=q1,
                    q2=q2,
                    q3=q3,
                    score=score,
                    risk_level=risk_level,
                    comments=comments if comments.strip() else "None"
                )
            
            # Log to general scan history for dashboard integration
            db.save_scan_log(
                target=f"Survey: {role}",
                scan_type="Awareness Survey",
                risk_score=score,
                risk_level=risk_level,
                details={"role": role, "q1": q1, "q2": q2, "q3": q3, "comments": comments}
            )

            st.success(f"✅ Survey submitted successfully! Your Hygiene Index Score is **{score} / 100**.")

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
