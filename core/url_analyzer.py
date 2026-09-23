import re
import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime
import requests
from typing import Dict, Any, List
from config import SUSPICIOUS_URL_KEYWORDS

# Attempt to import dnspython, with graceful fallback
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

class URLAnalyzer:
    def __init__(self, timeout: int = 6):
        self.timeout = timeout

    def analyze(self, raw_url: str) -> Dict[str, Any]:
        url = raw_url.strip()
        if not url:
            return {"error": "URL cannot be empty."}

        # Normalize URL scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed = urlparse(url)
        domain = parsed.netloc.split(':')[0]
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)

        score = 100
        issues = []
        remediations = []
        header_results = {}
        dns_records = {}
        ssl_details = {
            "valid": False,
            "issuer": "N/A",
            "subject": "N/A",
            "expiry": "N/A",
            "version": "N/A",
            "days_remaining": "N/A",
            "details": "Not checked"
        }
        dns_ip = None

        # 1. SSL/HTTPS & Certificate Inspection
        is_https = parsed.scheme == 'https'
        if not is_https:
            score -= 30
            issues.append("Missing HTTPS encryption (Insecure HTTP plaintext connection).")
            remediations.append("Enforce HTTPS with a trusted SSL/TLS certificate to secure data in transit.")
            ssl_details["details"] = "Insecure HTTP connection — no SSL/TLS certificate detected."
        else:
            try:
                ctx = ssl.create_default_context()
                with socket.create_connection((domain, port), timeout=self.timeout) as sock:
                    with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        
                        issuer_dict = dict(x[0] for x in cert.get('issuer', ()))
                        subject_dict = dict(x[0] for x in cert.get('subject', ()))
                        not_after_str = cert.get('notAfter', '')
                        
                        issuer_name = issuer_dict.get('organizationName') or issuer_dict.get('commonName') or 'Trusted CA'
                        subject_name = subject_dict.get('commonName') or domain
                        
                        days_left = "N/A"
                        if not_after_str:
                            try:
                                exp_dt = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                                days_left = (exp_dt - datetime.utcnow()).days
                                if days_left < 15:
                                    score -= 15
                                    issues.append(f"SSL Certificate is expiring soon ({days_left} days remaining).")
                                    remediations.append("Renew the SSL/TLS certificate before expiration to avoid browser warnings.")
                            except Exception:
                                pass

                        ssl_details = {
                            "valid": True,
                            "issuer": issuer_name,
                            "subject": subject_name,
                            "expiry": not_after_str,
                            "version": f"TLSv{ssock.version() if hasattr(ssock, 'version') else cert.get('version', '1.3')}",
                            "days_remaining": days_left,
                            "cipher": ssock.cipher()[0] if ssock.cipher() else "AES-GCM",
                            "details": "Certificate valid and signed by recognized Certificate Authority."
                        }
            except Exception as e:
                score -= 25
                ssl_details = {
                    "valid": False,
                    "issuer": "N/A",
                    "subject": "N/A",
                    "expiry": "N/A",
                    "version": "N/A",
                    "days_remaining": "N/A",
                    "error": str(e),
                    "details": f"SSL/TLS handshake failed: {str(e)}"
                }
                issues.append(f"SSL/TLS handshake error ({str(e)}).")
                remediations.append("Verify your web server SSL/TLS certificate installation and chain.")

        # 2. DNS Resolution & Record Lookup
        try:
            dns_ip = socket.gethostbyname(domain)
            dns_records["A"] = [dns_ip]
        except Exception as e:
            score -= 20
            issues.append(f"DNS Resolution failed for host '{domain}'.")
            remediations.append("Check DNS A record propagation and domain registration status.")

        if DNS_AVAILABLE and domain and not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            resolver = dns.resolver.Resolver()
            resolver.timeout = 2.5
            resolver.lifetime = 2.5
            for rtype in ["MX", "TXT", "NS", "AAAA"]:
                try:
                    answers = resolver.resolve(domain, rtype)
                    dns_records[rtype] = [str(rdata) for rdata in answers][:3]
                except Exception:
                    dns_records[rtype] = []

        # 3. Raw IP Address in URL
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            score -= 30
            issues.append("Raw IPv4 address used directly in domain host (Frequent phishing/malware signature).")
            remediations.append("Use a registered domain name with valid DNS records rather than a direct IP address.")

        # 4. URL Length & Subdomain Anomaly Detection
        if len(url) > 85:
            score -= 10
            issues.append(f"Excessively long URL ({len(url)} characters). Phishing links often use long paths to obscure destinations.")
            remediations.append("Avoid excessively nested or query-heavy URL paths for primary entry points.")

        subdomains = domain.split('.')
        if len(subdomains) > 3 and not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            score -= 15
            issues.append(f"High subdomain depth detected ({len(subdomains)} levels). Possible domain impersonation.")
            remediations.append("Keep domain structure clear and avoid misleading multi-level subdomains.")

        # 5. Suspicious Banking / Security Keywords in Path
        path_lower = parsed.path.lower()
        found_keywords = [kw for kw in SUSPICIOUS_URL_KEYWORDS if kw in path_lower]
        if found_keywords:
            score -= 15
            issues.append(f"Suspicious sensitive keywords found in URL path: {', '.join(found_keywords)}.")
            remediations.append("Confirm domain ownership and verify HTTPS certificate before submitting credentials.")

        # 6. HTTP Security Headers Audit
        req_headers = {
            "Strict-Transport-Security": "Protects against SSL-stripping and MITM downgrade attacks",
            "Content-Security-Policy": "Mitigates Cross-Site Scripting (XSS) and unauthorized script injection",
            "X-Frame-Options": "Protects users against Clickjacking and iframe embedding attacks",
            "X-Content-Type-Options": "Prevents MIME-sniffing vulnerabilities (nosniff)",
            "Referrer-Policy": "Protects user privacy by restricting referrer leakages",
            "Permissions-Policy": "Restricts browser feature access (geolocation, camera, microphone)"
        }

        try:
            resp = None
            try:
                resp = requests.head(url, timeout=self.timeout, allow_redirects=True, headers={'User-Agent': 'CyberGuard-Security-Auditor/3.0'})
            except Exception:
                resp = None

            if resp is None or resp.status_code == 405:
                resp = requests.get(url, timeout=self.timeout, allow_redirects=True, headers={'User-Agent': 'CyberGuard-Security-Auditor/3.0'}, stream=True)
            
            headers = resp.headers if resp is not None else {}

            missing_headers = []
            for h_name, h_desc in req_headers.items():
                present = (h_name in headers) or (h_name.lower() in headers)
                val = headers.get(h_name, headers.get(h_name.lower(), ""))
                header_results[h_name] = {
                    "present": present,
                    "value": str(val)[:60] + "..." if len(str(val)) > 60 else str(val),
                    "description": h_desc
                }
                if not present:
                    missing_headers.append(h_name)

            if missing_headers:
                penalty = min(25, len(missing_headers) * 5)
                score -= penalty
                issues.append(f"Missing essential security headers: {', '.join(missing_headers[:4])}.")
                remediations.append("Configure web server (Nginx/Apache/Cloudflare) to send HSTS, CSP, and X-Content-Type-Options headers.")

        except Exception as req_err:
            header_results = {h: {"present": False, "value": "N/A", "description": d} for h, d in req_headers.items()}
            issues.append(f"HTTP header inspection timed out or unreachable ({str(req_err)}).")

        score = max(5, min(100, score))
        if score >= 75:
            risk_level = "Low Risk"
        elif score >= 45:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        return {
            "target": url,
            "domain": domain,
            "ip_address": dns_ip or "Unresolved",
            "is_https": is_https,
            "dns_records": dns_records,
            "risk_score": score,
            "risk_level": risk_level,
            "ssl_details": ssl_details,
            "header_audit": header_results,
            "issues": issues,
            "remediations": remediations
        }
