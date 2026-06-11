# Deploy TMA Backend to AWS

Recommended path: **Docker → ECR → App Runner** (HTTPS URL included, minimal ops).

## What you need

| Piece | AWS service |
|--------|-------------|
| API (Flask) | **App Runner** (or ECS Fargate) |
| PostgreSQL | **RDS** (or your existing DB reachable from VPC) |
| Image registry | **ECR** |
| Frontends (Netlify) | Set `VITE_API_PROXY_TARGET` to the App Runner URL |

## 1. Database (RDS)

1. Create a **PostgreSQL** RDS instance (or use an existing server).
2. Note: **endpoint**, **port**, **database name**, **user**, **password**.
3. Security group: allow **inbound 5432** from the App Runner VPC connector (or same VPC as the API).
4. Ensure table **`poise_log`** exists with your columns.

App Runner env vars (step 3):

```text
PGHOST=your-db.xxxx.eu-west-1.rds.amazonaws.com
PGPORT=5432
PGDATABASE=aba_cards
PGUSER=poise
PGPASSWORD=...
DASHBOARD_PASSWORD=choose-a-strong-password
DASHBOARD_PASSWORD_ARKIN=rodin-dashboard
```

## 2. Push the Docker image to ECR

From the `Backend` folder:

```bash
chmod +x deploy/aws/push-ecr.sh
export AWS_REGION=eu-west-1   # your region
./deploy/aws/push-ecr.sh
```

Copy the printed image URI (e.g. `123456789.dkr.ecr.eu-west-1.amazonaws.com/tma-be-api:latest`).

## 3. Create App Runner service

In **AWS Console → App Runner → Create service**:

1. **Source**: Container registry → **Amazon ECR** → select `tma-be-api:latest`.
2. **Deployment**: Automatic (optional: connect GitHub later).
3. **Port**: `8080`.
4. **Health check**: path `/api/health`, protocol HTTP.
5. **Environment variables**: copy from `.env.example` / RDS (see above).
6. **VPC connector** (if RDS is private): attach a connector in the same VPC/subnets as RDS.

After deploy, copy the **App Runner URL** (e.g. `https://xxxxx.eu-west-1.awsapprunner.com`).

Test:

```bash
curl -sS "https://YOUR-APP-RUNNER-URL/api/health"
curl -sS -H "X-Dashboard-Password: YOUR_PASSWORD" \
  "https://YOUR-APP-RUNNER-URL/api/items"
```

## 4. Point Netlify frontends at AWS

For **museum** and **gallery** sites, in Netlify → **Environment variables** (build time):

```text
VITE_API_PROXY_TARGET=https://YOUR-APP-RUNNER-URL
```

Redeploy both sites. The dashboard will call `/api/...` on the same Netlify host; Netlify proxies to App Runner (no browser CORS to AWS).

Do **not** set `VITE_API_BASE_URL` to the App Runner URL in production unless you intentionally want cross-origin calls.

## 5. CORS (only if calling AWS URL directly from the browser)

Allowed origins are already in `app.py` (`takemearound.museum`, `.gallery`, Netlify previews). Add more with:

```text
CORS_EXTRA_ORIGINS=https://something-else.com
```

## Local Docker test

```bash
docker build -t tma-be-api .
docker run --rm -p 8080:8080 --env-file .env tma-be-api
curl http://127.0.0.1:8080/api/health
```

## Alternatives

- **ECS Fargate** + ALB: same ECR image, more control, more setup.
- **Elastic Beanstalk** (Docker): upload `Dockerrun.aws.json` pointing at ECR.
- **EC2**: run `docker run` with `.env`; you manage TLS (nginx + Let’s Encrypt).

## Costs (rough)

App Runner and RDS both bill while running. Use the smallest RDS instance for dev; stop App Runner service when not needed.
