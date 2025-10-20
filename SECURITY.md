# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of facebook-scraper-sdk seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue for security vulnerabilities
- Post about the vulnerability on social media or public forums

### Please DO:

1. **Email us directly**: your.email@example.com
2. Include the following information:
   - Type of vulnerability
   - Full path of the source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue (what an attacker can do with this vulnerability)

### What to expect:

- **Initial Response**: Within 48 hours, we will acknowledge receipt of your vulnerability report
- **Assessment**: Within 7 days, we will provide a detailed response indicating the next steps
- **Fix Timeline**: We aim to release a fix within 30 days for critical vulnerabilities
- **Credit**: We will publicly acknowledge your responsible disclosure (unless you prefer to remain anonymous)

## Security Best Practices

When using this SDK:

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive credentials
3. **Keep the SDK updated** to the latest version
4. **Enable logging** only in development environments
5. **Review dependencies** regularly for known vulnerabilities

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1) and announced:
- In the [GitHub Releases](https://github.com/OussemaFr/facebook-scraper-api-python/releases)
- In the [CHANGELOG.md](CHANGELOG.md)
- Via GitHub Security Advisories

Thank you for helping keep facebook-scraper-sdk and its users safe!