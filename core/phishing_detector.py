import re
from typing import Dict, Any, List
from config import PHISHING_KEYWORDS, SUSPICIOUS_URL_KEYWORDS

class PhishingDetector:
    def __init__(self):
        self.urgency_phrases = [
            r"within \d+ hours?", r"immediately", r"urgent action", r"account will be suspended",
            r"immediate response", r"last warning", r"failure to respond", r"expire in \d+ mins?"
        ]
        self.credential_cues = [
            r"enter your password", r"confirm your pin", r"verify your ssn", r"update credentials",
            r"security verification code", r"send your login", r"verify account details",
            r"verify your password", r"confirm your password", r"log in now"
        ]
        self.financial_cues = [
            r"wire transfer", r"crypto deposit", r"bitcoin", r"gift card", r"tax refund",
            r"bank account frozen", r"unauthorized charge", r"claim \$?\d+"
        ]

    def analyze(self, text: str) -> Dict[str, Any]:
        text_clean = text.strip()
        if not text_clean:
            return {"error": "Input text cannot be empty."}

        score = 100
        indicators = []
        text_lower = text_clean.lower()

        # 1. Check keyword triggers
        matched_keywords = [kw for kw in PHISHING_KEYWORDS if kw in text_lower]
        if matched_keywords:
            penalty = min(40, len(matched_keywords) * 10)
            score -= penalty
            indicators.append({
                "category": "Suspicious Keywords",
                "severity": "High" if len(matched_keywords) >= 3 else "Medium",
                "description": f"Found {len(matched_keywords)} phishing triggers: {', '.join(matched_keywords[:5])}"
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
                "category": "High Pressure & Urgency Tactics",
                "severity": "High",
                "description": f"Psychological urgency cues detected: '{', '.join(urgency_matches[:3])}'"
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
                "category": "Credential Solicitation",
                "severity": "High",
                "description": f"Direct requests for sensitive account data: '{', '.join(cred_matches[:3])}'"
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
                "category": "Financial Fraud & Wire Cues",
                "severity": "High",
                "description": f"Financial solicitation keywords detected: '{', '.join(fin_matches[:3])}'"
            })

        # 5. Link Extractor & Deceptive URL Check
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text_clean)
        if urls:
            suspicious_urls = []
            for u in urls:
                if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', u) or any(sk in u.lower() for sk in SUSPICIOUS_URL_KEYWORDS):
                    suspicious_urls.append(u)
            
            if suspicious_urls:
                score -= 30
                indicators.append({
                    "category": "Deceptive Links",
                    "severity": "High",
                    "description": f"Contains suspicious/unverified hyperlinks: {', '.join(suspicious_urls[:2])}"
                })
            else:
                score -= 10
                indicators.append({
                    "category": "Embedded Links",
                    "severity": "Low",
                    "description": f"Contains {len(urls)} external hyperlink(s). Exercise caution before clicking."
                })

        score = max(0, min(100, score))
        phishing_risk_score = 100 - score  # Invert so 100 = High Phishing Threat

        if phishing_risk_score >= 60:
            risk_level = "High Risk"
            verdict = "PHISHING / SOCIAL ENGINEERING ATTACK DETECTED"
        elif phishing_risk_score >= 30:
            risk_level = "Medium Risk"
            verdict = "SUSPICIOUS MESSAGE - EXERCISE EXTREME CAUTION"
        else:
            risk_level = "Low Risk"
            verdict = "LIKELY LEGITIMATE / LOW PHISHING RISK"

        return {
            "risk_score": score,
            "phishing_risk_score": phishing_risk_score,
            "risk_level": risk_level,
            "verdict": verdict,
            "extracted_urls": urls,
            "indicators": indicators,
            "word_count": len(text_clean.split())
        }
