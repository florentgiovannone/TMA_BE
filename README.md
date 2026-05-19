# TMA Backend API

Flask API for the Take Me Around dashboard (`poise_log` → JSON).

## Local development

```bash
./run
```

API: `http://127.0.0.1:5050` — health: `/api/health`, data: `/api/items` (header `X-Dashboard-Password`).

Optional tunnel:

```bash
./ngrok-tunnel   # in another terminal, after ./run
```

Copy `.env.example` → `.env` and set Postgres + `DASHBOARD_PASSWORD`.

## Deploy

**Start here:** **[deploy/DEPLOYMENT-GUIDE.md](deploy/DEPLOYMENT-GUIDE.md)** — step-by-step for **Windows VM + AWS + Netlify**.

| Target | Guide |
|--------|--------|
| **Full walkthrough** | [deploy/DEPLOYMENT-GUIDE.md](deploy/DEPLOYMENT-GUIDE.md) |
| **AWS only** (details) | [deploy/aws/README.md](deploy/aws/README.md) |
| **Windows VM only** | [deploy/windows/README.md](deploy/windows/README.md) |
| **Sample DB table** | [deploy/sql/poise_log.example.sql](deploy/sql/poise_log.example.sql) |

Quick push image:

```bash
./deploy/aws/push-ecr.sh
```

Then create an **App Runner** service from that ECR image and set DB env vars.

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/api/health` | none |
| GET | `/api/items` | `X-Dashboard-Password` |
| GET | `/api/secure/items` | same as `/api/items` |
