
# Secure SDLC Midterm — QuickNotes API (Starter Package)

This folder contains drafts, templates, and CI configs you can drop into your repo.

## How to use (5‑minute setup)
1) Copy **everything** in this folder into your project repo root.
2) Commit & push:
   ```bash
   git add .github workflows *.md threats
   git commit -m "chore: add reports + CI security workflows"
   git push
   ```
3) On GitHub → **Actions**: enable workflows if prompted and let CodeQL, pip-audit, ZAP, and Trivy run.
4) Open `MIDTERM_REPORT_DRAFT.md` and paste your screenshots where marked.
5) Export `MIDTERM_REPORT_DRAFT.md` to PDF (e.g., via VS Code “Markdown PDF” or print to PDF).

## Files
- `MIDTERM_REPORT_DRAFT.md` — full paper scaffold with placeholders.
- `SECURITY_TEST_REPORT_DRAFT.md` — table-driven test report to paste screenshots.
- `SECURITY_PLAN.md` — one-page plan (Phase 1).
- `threats/STRIDE_TABLE.md` — template for Phase 2.
- `.github/workflows/*.yml` — CodeQL (SAST), pip-audit (SCA), ZAP baseline (DAST), Trivy (image scan).
- `DEMO_SCRIPT.md` — 5–7 minute demo script to follow.

## Pro tips
- Keep repo name: **SecureApp_Midterm_TeamName**.
- Record your demo after all workflows turn green.
- Make sure your code implements ≥5 controls (rate limit, RBAC, headers, validation, logging, secrets).

