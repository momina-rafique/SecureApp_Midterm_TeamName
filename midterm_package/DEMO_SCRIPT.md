
# Demo Script (5–7 minutes)

1) **Intro (30s):** Team, project, stack.
2) **App Tour (1m):** Open `/docs`; show login, notes CRUD.
3) **Security Controls (2m):**
   - Rate limit: show 429 after 5 rapid login attempts.
   - RBAC: call `/admin/stats` as user (403), then as admin (200).
   - Headers: `curl -I http://127.0.0.1:8000 | grep -Ei 'strict|frame|content-security|x-content'`.
4) **Testing (1.5m):** Open GitHub **Actions**; show green runs for CodeQL, pip-audit, ZAP, Trivy. Open each summary.
5) **Threat Model (30s):** Show Threat Dragon DFD + STRIDE table.
6) **Wrap (30s):** What improved; future work.
