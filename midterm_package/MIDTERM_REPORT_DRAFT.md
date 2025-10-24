
# Midterm Report — Secure Software Design & Development
> Replace bracketed sections and paste screenshots where indicated. Keep within your instructor’s format.

## 1) Title Page
- **Title:** Secure REST API for QuickNotes
- **Team:** <Team Name> — <Member 1, Member 2, Member 3>
- **Repo:** <https://github.com/<org>/SecureApp_Midterm_TeamName>
- **Date:** <YYYY-MM-DD>

## 2) Abstract (100–150 words)
[Write a concise summary of what you built, the security controls, test types, and outcome.]

## 3) Introduction & Project Overview
- Stack: FastAPI + SQLite + JWT
- Why this project: small, realistic, covers auth + CRUD
- Architecture summary diagram: [PASTE: system overview diagram]

## 4) Security Objectives & Architecture
- Objectives (CIA + privacy): [fill]
- Assets & trust boundaries: [fill]
- Data Flow Diagram (DFD): [PASTE: DFD image]
- Security headers & HTTPS policy: [fill]

## 5) Threat Model (DFD + STRIDE + CVSS)
- Method: STRIDE per component; CVSS v3.1 for top risks
- Tables: see `threats/STRIDE_TABLE.md`
- Attack tree / abuse case: [PASTE: diagram or brief tree]
- [PASTE: screenshots from Threat Dragon / FIRST CVSS]

## 6) Secure Implementation Summary (≥5 controls)
- Rate limiting (SlowAPI) — login, POST/PUT endpoints
- RBAC (admin/user) — route guard `require_role()`
- Security headers (HSTS, CSP, XFO, X-Content-Type-Options)
- Input validation & body size caps (Pydantic + middleware)
- Audit logging (structured JSON, no secrets)
- Secrets/config hardening (.env, no debug in prod)
- [ADD any others you implemented]

> Include short code refs (file:line) and [PASTE: diffs or screenshots].

## 7) Testing Results (Automated)
- **SAST** (CodeQL): [PASTE: screenshot + summary]
- **SCA** (pip-audit): [PASTE: screenshot + fixed versions]
- **DAST** (ZAP baseline): [PASTE: screenshot + fixed warnings]
- **Container Scan** (Trivy): [PASTE: screenshot; ensure no criticals]

## 8) Risk Assessment (CVSS Table)
| ID | Threat | CVSS (Base) | Before | After | Mitigation |
|----|--------|-------------|--------|-------|------------|
| R1 | Brute-force login | 7.5 | High | Low | Rate limit + lockout |
| R2 | Missing HSTS/headers | n/a | Med | Low | Added middleware |
| R3 | Dependency vuln (libX) | 8.8 | High | Low | Pin + upgrade |
[Add/adjust rows]

## 9) Conclusion & Lessons Learned
[Summarize impact and what you’d improve next.]

## 10) References
- OWASP ASVS, Threat Dragon, CodeQL, ZAP, Trivy, pip-audit, FastAPI docs
