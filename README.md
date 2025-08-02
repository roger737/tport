# Vulnerability Labs

This is a deliberately vulnerable Flask web application for practicing web security testing. The labs roughly correspond to the OWASP Top 10 categories and include intentionally insecure code examples.

## Installation

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000` to view the list of labs.

## Included Labs

- Broken Access Control (`/broken_access/login?role=admin`)
- Cryptographic Failures (`/crypto/login`)
- SQL Injection (`/sqli?id=1`)
- Insecure Design (`/redirect?url=http://example.com`)
- Security Misconfiguration (`/config/env`)
- Vulnerable and Outdated Components (`/components`)
- Identification and Authentication Failures (`/auth/login`)
- Software and Data Integrity Failures (`/pickle/load`)
- Security Logging and Monitoring Failures (`/logging/login`)
- Server-Side Request Forgery (`/ssrf?url=http://example.com`)

The application is simplified for educational use and does not cover the full OWASP Web Security Testing Guide checklist.
