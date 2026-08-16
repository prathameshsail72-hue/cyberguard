import re
import math
from typing import Dict, Any, List

COMMON_WEAK_PASSWORDS = {
    "password", "123456", "12345678", "123456789", "qwerty", "12345", "dragon",
    "p@ssword", "admin", "welcome", "letmein", "sunshine", "iloveyou", "master",
    "cyberguard", "password123", "abc123", "000000", "111111", "charlie"
}

class PasswordAnalyzer:
    def analyze(self, password: str) -> Dict[str, Any]:
        pwd = password.strip()
        length = len(pwd)
        if length == 0:
            return {"error": "Password cannot be empty."}

        # Calculate character set pool size (R)
        charset_size = 0
        has_lower = bool(re.search(r'[a-z]', pwd))
        has_upper = bool(re.search(r'[A-Z]', pwd))
        has_digit = bool(re.search(r'[0-9]', pwd))
        has_symbol = bool(re.search(r'[^a-zA-Z0-9]', pwd))

        if has_lower: charset_size += 26
        if has_upper: charset_size += 26
        if has_digit: charset_size += 10
        if has_symbol: charset_size += 32

        # Calculate Shannon / Mathematical Entropy (E = L * log2(R))
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        entropy = round(entropy, 2)

        # Base score out of 100
        score = min(100, int((entropy / 100.0) * 100))

        feedback = []
        improvements = []

        # Check weak password dictionary
        is_common = pwd.lower() in COMMON_WEAK_PASSWORDS
        if is_common:
            score = min( score, 15)
            feedback.append("CRITICAL: Password found in common weak password dictionaries!")
            improvements.append("Avoid generic terms, dictionary words, and common default passwords.")

        # Check length
        if length < 8:
            score -= 30
            feedback.append("Password length is dangerously short (< 8 characters).")
            improvements.append("Use at least 12-16 characters for robust protection.")
        elif length < 12:
            score -= 10
            feedback.append("Password length is moderate (8-11 characters).")
            improvements.append("Increasing length to 14+ characters exponentially increases security.")

        # Check character diversity
        types_used = sum([has_lower, has_upper, has_digit, has_symbol])
        if types_used < 3:
            score -= 15
            feedback.append("Limited character set diversity.")
            improvements.append("Mix uppercase, lowercase, numbers, and special symbols (@, #, $, %).")

        # Check repeating or sequential characters
        if re.search(r'(.)\1{2,}', pwd):
            score -= 15
            feedback.append("Contains repeated characters (e.g. 'aaa' or '111').")
            improvements.append("Avoid repeated character sequences.")

        if re.search(r'(1234|2345|3456|4567|5678|6789|abcd|bcde|cdef|qwerty|asdf)', pwd.lower()):
            score -= 15
            feedback.append("Contains simple keyboard sequential patterns.")
            improvements.append("Avoid standard keyboard rows and numerical sequences.")

        score = max(0, min(100, score))

        if score >= 80:
            status = "Very Strong"
            risk_level = "Low Risk"
        elif score >= 60:
            status = "Strong"
            risk_level = "Low Risk"
        elif score >= 40:
            status = "Moderate"
            risk_level = "Medium Risk"
        elif score >= 20:
            status = "Weak"
            risk_level = "High Risk"
        else:
            status = "Very Weak"
            risk_level = "High Risk"

        # Calculate total combinations (R^L)
        total_combinations = charset_size ** length if charset_size > 0 else 0

        # Estimate Crack Times
        crack_times = self.estimate_crack_times(total_combinations)

        return {
            "password_length": length,
            "charset_size": charset_size,
            "entropy_bits": entropy,
            "score": score,
            "status": status,
            "risk_level": risk_level,
            "has_lower": has_lower,
            "has_upper": has_upper,
            "has_digit": has_digit,
            "has_symbol": has_symbol,
            "is_common": is_common,
            "crack_times": crack_times,
            "feedback": feedback,
            "improvements": improvements
        }

    def estimate_crack_times(self, combinations: float) -> Dict[str, str]:
        if combinations <= 0:
            return {"online": "Instant", "cpu": "Instant", "gpu_cluster": "Instant"}

        # Rates:
        # Online web rate limited: 10 guesses / sec
        # Desktop CPU: 10,000 guesses / sec
        # Fast GPU cluster: 100,000,000,000 (10^11) guesses / sec
        online_sec = combinations / 10.0
        cpu_sec = combinations / 10000.0
        gpu_sec = combinations / 1e11

        return {
            "online": self.format_time(online_sec),
            "cpu": self.format_time(cpu_sec),
            "gpu_cluster": self.format_time(gpu_sec)
        }

    @staticmethod
    def format_time(seconds: float) -> str:
        if seconds < 1:
            return "Instantaneous (< 1 sec)"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds // 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds // 86400)} days"
        elif seconds < 31536000 * 1000:
            years = int(seconds // 31536000)
            return f"{years:,} years"
        else:
            return "Centuries (Unbreakable by current hardware)"
