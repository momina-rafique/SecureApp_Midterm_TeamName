
# Security Plan — QuickNotes API (Phase 1)
**Objectives:** Protect confidentiality, integrity, availability; minimize PII exposure; secure tokens; least privilege.
**Assets:** Accounts, JWTs, notes DB, logs.
**Users/Roles:** Anonymous, User, Admin.
**Data Flows:** Auth → JWT → CRUD Notes; Admin → Stats.
**Controls to Implement (≥5):**
1. Rate limiting on login + write endpoints.
2. RBAC with route-level guards.
3. Security headers (HSTS, CSP, XFO, XCTO) + HTTPS redirect in prod.
4. Validation (Pydantic field bounds) + request body size caps.
5. Audit logging (sanitized JSON); error handling without stack traces.
6. Secret/config hardening; pinned deps.
**Testing Plan:** CodeQL (SAST), pip-audit (SCA), ZAP baseline (DAST), Trivy (container).
**Deliverables:** Proposal, overview diagram, repo bootstrap.
