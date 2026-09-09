# System Security Audits & OWASP Mitigation (Security_audits.md)

## 1. Executive Security Strategy
This document specifies the security controls, static code auditing workflows, and OWASP Top 10 mitigation guidelines for the **Flask Python backend** and **HTML5/Tailwind/JS frontend**.

---

## 2. OWASP Top 10 Mitigation Matrix for Flask

| OWASP Vulnerability | Risk Level | Flask Mitigation Strategy |
| :--- | :--- | :--- |
| **A01: Broken Access Control** | Critical | `@jwt_required()` middleware on all non-public endpoints; verify ownership of resource IDs before mutating DB records |
| **A02: Cryptographic Failures** | High | Use `werkzeug.security` or `bcrypt` for password hashing; enforce HTTPS via Render & Neon DB TLS 1.3 |
| **A03: Injection (SQLi / Command)** | Critical | SQLAlchemy ORM parameterized queries; never concatenate user input into raw SQL |
| **A04: Insecure Design** | High | Marshmallow payload schema validation; rate limiting with `Flask-Limiter` |
| **A05: Security Misconfiguration** | High | Remove `debug=True` in production; set security headers via `Flask-Talisman` |
| **A06: Vulnerable Components** | Medium | Run `pip-audit` and `safety` in CI/CD pipeline |
| **A07: Identification & Auth Failures** | High | Enforce strong password policy; automatic token expiration; rate limit `/api/v1/auth/login` |
| **A08: Software & Data Integrity** | Medium | Subresource Integrity (SRI) for CDN assets; signed JWT algorithms (`HS256` / `RS256`) |
| **A09: Security Logging Failures** | Medium | Structured JSON logging using Python `logging` module; log all auth failures |
| **A10: Server-Side Request Forgery (SSRF)** | Medium | Restrict outbound HTTP requests to whitelisted domain endpoints |

---

## 3. Flask Security Headers Configuration (`Flask-Talisman`)

```python
from flask_talisman import Talisman

def configure_security_headers(app):
    csp = {
        'default-src': '\'self\'',
        'script-src': ['\'self\'', 'https://fonts.googleapis.com'],
        'style-src': ['\'self\'', '\'unsafe-inline\'', 'https://fonts.googleapis.com'],
        'font-src': ['\'self\'', 'https://fonts.gstatic.com'],
        'img-src': ['\'self\'', 'data:', 'https:']
    }
    Talisman(
        app,
        content_security_policy=csp,
        force_https=True,
        strict_transport_security=True,
        session_cookie_secure=True,
        session_cookie_http_only=True
    )
```

---

## 4. Static Code Analysis Workflow
Run security scans before committing code:

```bash
# Audit Python dependencies for known CVE vulnerabilities
pip-audit

# Run Bandit security linter on Flask application code
bandit -r backend/app/
```
