import re
import socket
import ssl
from urllib.parse import urlparse
import requests
from typing import Dict, Any, List
from config import SUSPICIOUS_URL_KEYWORDS

class URLAnalyzer:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def analyze(self, raw_url: str) -> Dict[str, Any]:
        url = raw_url.strip()
        if not url:
            return {"error": "URL cannot be empty."}

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        parsed = urlparse(url)
        domain = parsed.netloc.split(':')[0]
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)

        score = 100
        issues = []
        remediations = []
        header_results = {}
        ssl_details = {"valid": False, "details": "Not checked"}
        dns_ip = None

        # 1. SSL/HTTPS Check
        if parsed.scheme != 'https':
            score -= 25
            issues.append("Missing HTTPS encryption (Insecure HTTP standard connection).")
            remediations.append("Enforce HTTPS with an SSL/TLS certificate to encrypt data in transit.")
        else:
            # Check SSL Certificate validity
            try:
                ctx = ssl.create_default_context()
                with socket.create_connection((domain, port), timeout=self.timeout) as sock:
                    with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        ssl_details = {
                            "valid": True,
                            "subject": dict(x[0] for x in cert.get('subject', ())),
                            "issuer": dict(x[0] for x in cert.get('issuer', ())),
                            "version": cert.get('version'),
                            "notAfter": cert.get('notAfter')
                        }
            except Exception as e:
                score -= 20
                ssl_details = {"valid": False, "error": str(e)}
                issues.append(f"SSL/TLS handshake failed or certificate is invalid ({str(e)}).")
                remediations.append("Ensure a valid SSL certificate signed by a trusted Certificate Authority is installed.")

        # 2. DNS & IP resolution check
        try:
            dns_ip = socket.gethostbyname(domain)
        except Exception as e:
            score -= 15
            issues.append(f"DNS Resolution failed for host: {domain}.")
            remediations.append("Verify domain name resolution and DNS A record configuration.")

        # 3. Raw IP Address in URL
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            score -= 30
            issues.append("Raw IP address used instead of domain name (Common phishing indicator).")
            remediations.append("Use legitimate domain names instead of bare IP addresses.")

        # 4. URL Length check
        if len(url) > 75:
            score -= 15
            issues.append(f"URL length is unusually long ({len(url)} chars > 75 chars).")
            remediations.append("Avoid excessively long URLs which may be obscuring target destinations.")

        # 5. Excessive Subdomains
        subdomains = domain.split('.')
        if len(subdomains) > 3:
            score -= 15
            issues.append(f"Excessive subdomains detected ({len(subdomains)} levels).")
            remediations.append("Simplify domain hierarchy to prevent deceptive domain spoofing.")

        # 6. Suspicious Keywords in Path
        path_lower = parsed.path.lower()
        found_keywords = [kw for kw in SUSPICIOUS_URL_KEYWORDS if kw in path_lower]
        if found_keywords:
            score -= 20
            issues.append(f"Suspicious security/banking keywords in path: {', '.join(found_keywords)}.")
            remediations.append("Inspect page content closely to confirm identity before entering credentials.")

        # 7. HTTP Headers Audit
        try:
            headers = None
            try:
                response = requests.head(url, timeout=self.timeout, allow_redirects=True, headers={'User-Agent': 'CyberGuard/2.0'})
                if response.status_code != 405:
                    headers = response.headers
            except Exception:
                headers = None

            if headers is None:
                response = requests.get(url, timeout=self.timeout, allow_redirects=True, headers={'User-Agent': 'CyberGuard/2.0'}, stream=True)
                headers = response.headers
                response.close()
            
            req_headers = {
                "Strict-Transport-Security": "Protects against MITM downgrade attacks",
                "Content-Security-Policy": "Prevents XSS and unauthorized data injection",
                "X-Frame-Options": "Protects against Clickjacking",
                "X-Content-Type-Options": "Prevents MIME-type sniffing",
                "Referrer-Policy": "Controls referrer privacy"
            }

            missing_headers = []
            for h_name, h_desc in req_headers.items():
                present = h_name in headers or h_name.lower() in headers
                header_results[h_name] = present
                if not present:
                    missing_headers.append(h_name)

            if missing_headers:
                score -= len(missing_headers) * 5
                issues.append(f"Missing recommended security headers: {', '.join(missing_headers)}.")
                remediations.append("Configure web server to emit modern HTTP security headers (HSTS, CSP, X-Frame-Options).")

        except Exception as req_err:
            header_results = {"error": f"Header fetch failed: {str(req_err)}"}

        score = max(0, min(100, score))
        if score >= 76:
            risk_level = "Low Risk"
        elif score >= 41:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        return {
            "target": url,
            "domain": domain,
            "ip_address": dns_ip,
            "risk_score": score,
            "risk_level": risk_level,
            "ssl_details": ssl_details,
            "header_audit": header_results,
            "issues": issues,
            "remediations": remediations
        }
