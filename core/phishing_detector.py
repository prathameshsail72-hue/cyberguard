import re
from typing import Dict, Any, List
from config import PHISHING_KEYWORDS, SUSPICIOUS_URL_KEYWORDS

class PhishingDetector:
    def __init__(self):
        self.urgency_phrases = [
            r"within \d+ hours?", r"immediately", r"urgent action", r"account will be suspended",
            r"immediate response", r"last warning", r"failure to respond", r"expire in \d+ mins?",
            r"action required immediately", r"24 hours to verify", r"permanent account closure",
            r"unauthorized transaction detected", r"critical security alert"
        ]
        self.credential_cues = [
            r"enter your password", r"confirm your pin", r"verify your ssn", r"update credentials",
            r"security verification code", r"send your login", r"verify account details",
            r"verify your password", r"confirm your password", r"log in now", r"unlock your account",
            r"authenticate identity", r"validate credit card", r"billing details required"
        ]
        self.financial_cues = [
            r"wire transfer", r"crypto deposit", r"bitcoin", r"gift card", r"tax refund",
            r"bank account frozen", r"unauthorized charge", r"claim \$?\d+", r"inheritance funds",
            r"western union", r"lottery winning", r"cryptocurrency wallet", r"overdue invoice"
        ]

    def analyze(self, text: str) -> Dict[str, Any]:
        text_clean = text.strip()
        if not text_clean:
            return {"error": "Input text cannot be empty."}

        score = 100
        indicators = []
        text_lower = text_clean.lower()

        # 1. Check keyword triggers
        matched_keywords = []
        for kw in PHISHING_KEYWORDS:
            if " " in kw:
                if kw in text_lower:
                    matched_keywords.append(kw)
            else:
                if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                    matched_keywords.append(kw)

        if matched_keywords:
            penalty = min(35, len(matched_keywords) * 8)
            score -= penalty
            indicators.append({
                "category": "Suspicious Social Engineering Keywords",
                "severity": "High" if len(matched_keywords) >= 3 else "Medium",
                "description": f"Detected {len(matched_keywords)} phishing triggers: '{', '.join(matched_keywords[:6])}'"
            })

        # 2. Check Urgency / High Pressure Regex Patterns
        urgency_matches = []
        for pattern in self.urgency_phrases:
            found = re.findall(pattern, text_lower)
            if found:
                urgency_matches.extend(found)
        if urgency_matches:
            score -= 25
            indicators.append({
                "category": "Psychological Urgency & Pressure Tactics",
                "severity": "High",
                "description": f"High-pressure manipulation cues detected: '{', '.join(set(urgency_matches[:3]))}'"
            })

        # 3. Check Credential Harvest Cues
        cred_matches = []
        for pattern in self.credential_cues:
            found = re.findall(pattern, text_lower)
            if found:
                cred_matches.extend(found)
        if cred_matches:
            score -= 30
            indicators.append({
                "category": "Credential Harvesting Cues",
                "severity": "High",
                "description": f"Direct solicitation of sensitive account credentials: '{', '.join(set(cred_matches[:3]))}'"
            })

        # 4. Check Financial Fraud Cues
        fin_matches = []
        for pattern in self.financial_cues:
            found = re.findall(pattern, text_lower)
            if found:
                fin_matches.extend(found)
        if fin_matches:
            score -= 25
            indicators.append({
                "category": "Financial Fraud & Wire Requests",
                "severity": "High",
                "description": f"Financial transfer or unverified payment solicitation: '{', '.join(set(fin_matches[:3]))}'"
            })

        # 5. Link Extractor & Deceptive URL Check
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text_clean)
        suspicious_urls = []
        if urls:
            for u in urls:
                if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', u) or any(sk in u.lower() for sk in SUSPICIOUS_URL_KEYWORDS):
                    suspicious_urls.append(u)
            
            if suspicious_urls:
                score -= 30
                indicators.append({
                    "category": "Deceptive & Spoofed Hyperlinks",
                    "severity": "High",
                    "description": f"Contains high-risk or IP-based destination links: {', '.join(suspicious_urls[:2])}"
                })
            else:
                score -= 10
                indicators.append({
                    "category": "Embedded Links",
                    "severity": "Low",
                    "description": f"Contains {len(urls)} external hyperlink(s). Verify the sender and domain before clicking."
                })

        score = max(0, min(100, score))
        phishing_risk_score = 100 - score  # 100 = High Phishing Threat

        if phishing_risk_score >= 60:
            risk_level = "High Risk"
            verdict = "🚨 PHISHING / SOCIAL ENGINEERING ATTACK DETECTED"
            recommendation = "Do NOT click any links, open attachments, or reply with credentials. Mark as spam and report to your organization's security team."
        elif phishing_risk_score >= 30:
            risk_level = "Medium Risk"
            verdict = "⚠️ SUSPICIOUS MESSAGE — EXERCISE CAUTION"
            recommendation = "Verify the authenticity of the sender via an independent secondary communication channel (e.g. phone or official portal)."
        else:
            risk_level = "Low Risk"
            verdict = "✅ LOW PHISHING RISK DETECTED"
            recommendation = "Message shows no obvious signs of automated social engineering. Always maintain general digital caution."

        return {
            "risk_score": score,
            "phishing_risk_score": phishing_risk_score,
            "risk_level": risk_level,
            "verdict": verdict,
            "recommendation": recommendation,
            "extracted_urls": urls,
            "indicators": indicators,
            "word_count": len(text_clean.split())
        }
