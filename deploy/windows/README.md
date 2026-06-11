# Run the API on a Windows VM

Use this if your **Postgres** (or the whole stack) already lives on a Windows server, instead of AWS App Runner.

## Option A — Docker (recommended)

Same image as AWS; needs [Docker Desktop](https://www.docker.com/products/docker-desktop/) on the VM.

```powershell
cd C:\path\to\Backend
copy .env.example .env
# Edit .env: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD, DASHBOARD_PASSWORD, DASHBOARD_PASSWORD_ARKIN

docker build -t tma-be-api .
docker run -d --name tma-api --restart unless-stopped -p 5050:8080 --env-file .env tma-be-api
```

Test on the VM: `http://localhost:5050/api/health`

Open **Windows Firewall** inbound TCP **5050** (or only allow your reverse proxy).

## Install Python first (if `py` / `python` not found)

1. https://www.python.org/downloads/windows/ → **Python 3.12**
2. Installer: enable **“Add python.exe to PATH”**
3. Close PowerShell, open a new window
4. Check: `python --version`

## Option B — Python only (no Docker)

Gunicorn does not run on Windows. Use **waitress**:

```powershell
cd C:\Backend
copy .env.example .env
# Edit .env

.\deploy\windows\run-api.ps1
```

## Expose the API to Netlify (dashboard)

The browser must reach your VM. Pick one:

| Method | Netlify `VITE_API_PROXY_TARGET` |
|--------|----------------------------------|
| **ngrok** on the VM | `https://xxxx.ngrok-free.app` |
| **Public IP** + HTTPS (IIS / Caddy / nginx) | `https://api.yourdomain.com` |
| **Cloudflare Tunnel** | your tunnel URL |

Then redeploy museum/gallery on Netlify with that URL (see main `deploy/aws/README.md` § Netlify).

Do **not** call the VM by IP from the browser without HTTPS unless you are only testing locally.

## Database on the same VM

If Postgres runs on the Windows VM:

```env
PGHOST=localhost
PGPORT=5432
PGDATABASE=aba_cards
PGUSER=poise
PGPASSWORD=...
```

If Postgres is on another machine, set `PGHOST` to that host and allow port **5432** from the API machine’s IP in the DB firewall.

## AWS vs Windows VM

| | AWS App Runner | Windows VM |
|--|----------------|--------------|
| Ops | AWS manages | You manage OS, updates, firewall |
| HTTPS | Built-in | You add (ngrok, Caddy, IIS, etc.) |
| Good when | No own server | DB/app already on Windows |

You can still use **RDS on AWS** with an API on a **Windows VM** by setting `PGHOST` to the RDS endpoint and using a **VPC / security group** that allows the VM’s IP.
