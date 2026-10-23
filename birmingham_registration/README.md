# Birmingham interest registration

Separate Flask service for the Birmingham register-interest form. It has its own database and does not use the dashboard API.

## Run

1. Create a Postgres database, for example `createdb birmingham_registration`.
2. Copy `.env.example` to `.env` and set `DATABASE_URL`, `RESEND_API_KEY`, `RESEND_FROM`, `ADMIN_PASSWORD`, `SECRET_KEY`, `PUBLIC_BASE_URL`, and `PRIVACY_CONTACT_EMAIL`.
3. In production behind one HTTPS proxy, set `TRUSTED_PROXY_HOPS=1`, `DATABASE_SSLMODE=require`, and use an HTTPS `PUBLIC_BASE_URL`. Rate limits and admin lockout are in-memory and assume one process.
4. From `TMA_backend`, run `./run-birmingham`.

The service listens on port 5051. Health: `GET /api/health`. Admin: `/admin/login`.

Set both artwork stocks in the admin before opening the form. Stock starts at zero, so both artworks stay hidden until then.

## Tests

Copy `.env.test.example` to `.env.test` and point it at a database that is not the development database.

```bash
.venv-birmingham/bin/pytest birmingham_registration/tests -v
```

## Check by hand

Submit the Birmingham form, open the Resend link within 5 minutes, and sign in to the admin page.
