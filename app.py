import streamlit as st
import os
import json
import pandas as pd
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

# Apply Glassmorphism Dark Theme Styling
st.markdown("""
<style>
    /* Dark Obsidian Base Theme */
    .stApp {
        background-color: #0b1120;
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Styling */
    .header-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    .header-title {
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 6px;
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        margin-bottom: 12px;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 4px;
    }

    /* Badges */
    .badge-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid #ef4444;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-med {
        background-color: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid #f59e0b;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    /* Buttons */
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
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status**")
st.sidebar.markdown("🟢 **Engine**: CyberGuard 3.0 Core")
st.sidebar.markdown(f"💾 **Storage**: `{os.path.basename(db.db_path)}`")
st.sidebar.markdown("☁️ **Deployment**: Dual-Target Ready")

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
            <div class="metric-label">Total Security Audits</div>
            <div class="metric-val" style="color: #38bdf8;">{stats['total_scans']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        avg_score = stats['avg_score']
        score_color = "#10b981" if avg_score >= 75 else "#f59e0b" if avg_score >= 40 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Health Score</div>
            <div class="metric-val" style="color: {score_color};">{avg_score} <span style="font-size: 1rem;">/ 100</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Risk Threats</div>
            <div class="metric-val" style="color: #ef4444;">{stats['high_risk_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
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
        st.bar_chart(risk_data.set_index("Risk Level"))

    with col_right:
        st.markdown("#### 🔍 Audits by Scanner Type")
        by_type_data = stats.get('by_type', {})
        if by_type_data:
            type_df = pd.DataFrame(list(by_type_data.items()), columns=["Scan Type", "Count"])
            st.bar_chart(type_df.set_index("Scan Type"))
        else:
            st.info("No security scans logged yet. Perform a scan in one of the tool tabs!")

    st.markdown("---")
    st.markdown("#### 📜 Live Security Audit History")
    recent = stats.get("recent_scans", [])
    if recent:
        df_recent = pd.DataFrame(recent)
        df_display = df_recent[["target", "scan_type", "risk_score", "risk_level", "scanned_at"]]
        st.dataframe(df_display, use_container_width=True)
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
    ])
    
    q2 = st.radio("2. What indicator strongly suggests an email is a phishing attempt?", [
        "Email sent from official company domain",
        "Psychological urgency tactics (e.g. 'Account suspended in 1 hour!')",
        "Personalized greeting with full name"
    ])
    
    q3 = st.radio("3. Why is raw IP address usage in a URL suspicious?", [
        "IP addresses load faster",
        "Raw IPs bypass domain name verification and hide illegitimate host identity",
        "IP addresses enforce HTTPS encryption"
    ])

    if st.button("Submit Quiz Answers"):
        score = 0
        if q1 == "Using unique, complex passphrases managed in a password manager": score += 1
        if q2 == "Psychological urgency tactics (e.g. 'Account suspended in 1 hour!')": score += 1
        if q3 == "Raw IPs bypass domain name verification and hide illegitimate host identity": score += 1

        total = 3
        badge = "🛡️ Cyber Guardian Gold" if score == 3 else "🥈 Security Apprentice Silver" if score == 2 else "🥉 Security Novice"
        
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