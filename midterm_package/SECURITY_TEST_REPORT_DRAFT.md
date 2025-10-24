
# Security Test Report (Phase 4)

## Tools & Config
- **SAST:** GitHub CodeQL (Python)
- **SCA:** pip-audit (requirements.txt)
- **DAST:** OWASP ZAP Baseline → target `http://127.0.0.1:8000/docs`
- **Container:** Trivy on `notes-api:latest`

## Findings
> Paste screenshots into each subsection and summarize fixes.

### 1) SAST — CodeQL
- [PASTE: screenshot of Actions run]
- Findings summary: [fill]
- Fixes: [fill]
- Re-test result: [fill]

### 2) SCA — pip-audit
- [PASTE: screenshot]
- Vulnerabilities: [list]
- Remediation: pin/upgrade to versions: [list]
- Re-test: [fill]

### 3) DAST — OWASP ZAP Baseline
- [PASTE: screenshot]
- Alerts: [list]
- Mitigations: [list]
- Re-test: [fill]

### 4) Container Scan — Trivy
- [PASTE: screenshot]
- Critical/High: [count] → [resolved]
- Remediation: [fill]

## CVSS-Based Risk Analysis
| Issue | CVSS | Before | After | Notes |
|------|------|--------|-------|-------|
| Dep vuln (pkg) | 8.8 | High | Low | Upgraded |
| Missing HSTS | - | Med | Low | Added headers |
| ... | ... | ... | ... | ... |

## Conclusion
All critical/high findings addressed; pipeline enforces regression checks.
