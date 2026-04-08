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

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:

- `DALIFIN_API_BASE_URL`
  - default: `http://127.0.0.1:8000/account/api`
- `DALIFIN_SITE_NAME`
  - default: `Dalifin`
- `DALIFIN_PORTAL_URL`
  - default: `https://server.dalifin.com/account`
- `DALIFIN_CONTACT_EMAIL`
  - default: `gli@dalifin.com`
- `DALIFIN_CONTACT_NAME`
  - default: `Gang Li`

## Routes

- `/`
- `/about`
- `/contact`
- `/app`
- `/downloads`
- `/downloads/{product_key}`

## Notes

- The website does not compute artifact URLs.
- Download metadata comes from `app_server` JSON APIs.
- Product marketing copy in this repo is presentation-only.
