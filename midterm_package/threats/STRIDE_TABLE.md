
# STRIDE & CVSS Table (Phase 2)

| Component | STRIDE Category | Threat | Impact | Likelihood | CVSS (Base) | Mitigation |
|-----------|------------------|--------|--------|------------|-------------|------------|
| Auth (login) | S (Spoofing) | Credential stuffing | Account takeover | Medium | 7.5 | Rate limit + lockout |
| API (notes) | T (Tampering) | Body tampering | Data corruption | Medium | 6.5 | Validation + authz |
| API (headers) | I (Info Disclosure) | Missing HSTS/CSP | MITM/XSS | Medium | 6.8 | Security headers + HTTPS |
| DB | R (Repudiation) | Weak logging | Disputed actions | Medium | 4.2 | Audit log JSON |
| Platform | D (DoS) | Large payloads | Resource exhaustion | Medium | 5.0 | Body size cap |
| Admin route | E (Elevation) | Privilege bypass | Admin abuse | Low | 8.0 | RBAC guards |
[Add rows as needed]
