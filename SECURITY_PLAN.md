# Security Plan — QuickNotes API (Phase 1)
Objectives: CIA + privacy; token safety; least privilege.
Assets: accounts, JWTs, notes DB, logs.
Users/Roles: Anonymous, User, Admin.
Data Flows: Auth→JWT; CRUD notes; Admin stats.
Controls (≥5): rate limiting; RBAC; security headers; validation & size cap; audit logs; secrets hardening.
Testing: CodeQL (SAST), pip-audit (SCA), ZAP baseline (DAST), Trivy (container).
