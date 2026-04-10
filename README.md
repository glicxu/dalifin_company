# dalifin_company

Public-facing Dalifin company website.

Current scope:

- homepage
- about page
- contact page
- `/app` portal redirect
- downloads index
- per-product download pages
- presentation-only catalog content
- release data read from `app_server`
- stage/prod env templates
- runtime wrapper and smoke-verification tooling
- ini-driven startup compatible with the current `5003` website slot

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Or with the runtime wrapper on Linux:

```bash
./scripts/run_site.sh start --env-file ./env/stage.env.example
```

Or from the current prod-style config model:

```bash
python ./dalifin_company.py -c /data/dali/prod/config/app_dalifin_company.ini
```

Or deploy the repo tree on a Linux host:

```bash
./check_and_deploy.sh
```

Environment variables:

- `DALIFIN_API_BASE_URL`
  - default: `http://127.0.0.1:8000/account/api`
- `DALIFIN_SITE_NAME`
  - default: `Dalifin`
- `DALIFIN_PORTAL_URL`
  - default: `https://server.dalifin.com/sso`
- `DALIFIN_CONTACT_EMAIL`
  - default: `gli@dalifin.com`
- `DALIFIN_CONTACT_NAME`
  - default: `Gang Li`

`dalifin_company.py -c <config.ini>` can derive:

- bind host/port from `[dalifin_company]` and fall back to `[dali_user]` for compatibility
- `DALIFIN_API_BASE_URL` from `[app_server]`

## Routes

- `/healthz`
- `/version`
- `/`
- `/sso`
- `/about`
- `/contact`
- `/app`
- `/downloads`
- `/downloads/{product_key}`

## Notes

- The website does not compute artifact URLs.
- Download metadata comes from `app_server` JSON APIs.
- Product marketing copy in this repo is presentation-only.
- The intended production cutover is to replace the website process behind the existing Apache proxy target `127.0.0.1:5003`.
- Runtime/deploy helpers live in:
  - `dalifin_company.py`
  - `scripts/run_site.sh`
  - `scripts/verify_deploy.py`
  - `env/*.env.example`
  - `deploy/apache/dalifin_company_vhost.conf.example`
