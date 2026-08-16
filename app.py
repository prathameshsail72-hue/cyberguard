import re
import math
import hashlib
import requests
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SUSPICIOUS_KEYWORDS = ['login', 'verify', 'update', 'banking', 'secure', 'account', 'paypal', 'free']

def analyze_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    domain = parsed.netloc
    
    score = 100
    reasons = []

    if parsed.scheme != 'https':
        score -= 25
        reasons.append("Missing HTTPS encryption (HTTP only).")

    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
        score -= 30
        reasons.append("Raw IP address used instead of domain name.")

    if len(url) > 75:
        score -= 15
        reasons.append("URL length is unusually long (>75 chars).")

    subdomains = domain.split('.')
    if len(subdomains) > 3:
        score -= 15
        reasons.append(f"Excessive subdomains detected ({len(subdomains)} levels).")

    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in parsed.path.lower()]
    if found_keywords:
        score -= 20
        reasons.append(f"Suspicious keywords detected in URL path: {', '.join(found_keywords)}")

    score = max(0, score)
    level = "Low Risk" if score > 75 else "Medium Risk" if score > 40 else "High Risk"

    return {
        "url": url,
        "score": score,
        "risk_level": level,
        "issues": reasons
    }

def analyze_password(password):
    length = len(password)
    charset_size = 0

    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset_size += 32

    if charset_size == 0 or length == 0:
        return {"score": 0, "entropy": 0, "status": "Very Weak"}

    entropy = length * math.log2(charset_size)
    
    if entropy < 28:
        status = "Very Weak"
    elif entropy < 36:
        status = "Weak"
    elif entropy < 60:
        status = "Moderate"
    elif entropy < 128:
        status = "Strong"
    else:
        status = "Very Strong"

    return {
        "entropy": round(entropy, 2),
        "status": status,
        "length": length
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze-url', methods=['POST'])
def api_analyze_url():
    data = request.json
    target_url = data.get('url', '')
    if not target_url:
        return jsonify({"error": "URL is required"}), 400
    
    result = analyze_url(target_url)
    return jsonify(result)

@app.route('/api/check-password', methods=['POST'])
def api_check_password():
    data = request.json
    pwd = data.get('password', '')
    result = analyze_password(pwd)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)