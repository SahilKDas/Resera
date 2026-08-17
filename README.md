# RESERA

RESERA is a student-led research collective with 1,050+ members and growing. This repository contains the public Svelte site and the Django account/opportunity service.

## Architecture

- `src/` — Svelte frontend, built with Bun and Vite
- `backend/` — Django session authentication, CSRF protection, opportunity submissions, and staff moderation
- `.github/workflows/deploy-pages.yml` — static frontend deployment to GitHub Pages

GitHub Pages cannot execute Python. The frontend can stay on Pages, while Django runs on a server controlled by RESERA. The two are connected with the `VITE_API_BASE_URL` repository variable.

## Frontend

```powershell
bun install
bun run dev
```

## Backend

See [`backend/README.md`](backend/README.md) for local setup and production environment settings. New opportunities are pending by default; staff approve or reject them through Django Admin.

## Verification

```powershell
bun run build
.\.venv\Scripts\python.exe backend\manage.py check
.\.venv\Scripts\python.exe backend\manage.py test core
```
