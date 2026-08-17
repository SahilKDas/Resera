# Resera Django service

This service owns Resera accounts, authenticated sessions, opportunity submissions, and moderation. The public Svelte site can remain on GitHub Pages; this Python process must run on a machine or server you control because GitHub Pages only serves static files.

## Local setup

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe backend\manage.py migrate
.\.venv\Scripts\python.exe backend\manage.py createsuperuser
.\.venv\Scripts\python.exe backend\manage.py runserver
```

In another terminal, run `bun run dev`. Vite proxies `/api` to Django during local development.

## Production settings

Set all values from `backend/.env.example` in the service environment. Use a long random `DJANGO_SECRET_KEY`, disable debug, list the public API hostname in `DJANGO_ALLOWED_HOSTS`, and list the exact GitHub Pages origin in both origin settings. When the frontend and backend use different sites, set `DJANGO_SESSION_COOKIE_SAMESITE=None`; HTTPS is required for secure cross-site cookies.

Set the GitHub repository variable `VITE_API_BASE_URL` to the backend's HTTPS origin, for example `https://api.resera.org`, then rerun the Pages workflow.

Moderators use `/admin/` to approve or reject submitted opportunities. Only approved records appear publicly.
