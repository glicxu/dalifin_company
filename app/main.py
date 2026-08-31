from __future__ import annotations

from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.catalog import get_catalog_entry
from app.config import get_settings, resolved_portal_url
from app.download_api import DownloadApiClient, DownloadApiError, DownloadApiNotFound
from app.privacy import get_app_privacy_policy

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="dalifin_company")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def get_download_api_client() -> DownloadApiClient:
    settings = get_settings()
    return DownloadApiClient(base_url=settings.api_base_url, timeout_seconds=settings.request_timeout_seconds)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "dalifin_company"}


@app.get("/version")
def version():
    settings = get_settings()
    return {
        "service": "dalifin_company",
        "buildId": settings.build_id,
        "siteName": settings.site_name,
        "apiBaseUrl": settings.api_base_url,
    }


def _render(request: Request, template_name: str, **extra):
    settings = get_settings()
    return templates.TemplateResponse(
        request,
        template_name,
        {
            "request": request,
            "site_name": settings.site_name,
            **extra,
        },
    )


def _homepage_context() -> dict:
    settings = get_settings()
    portal_url = resolved_portal_url(settings)
    approach_cards = [
        {"icon": "P", "title": "Planners", "text": "Design strategy."},
        {"icon": "A", "title": "Analysts", "text": "Interpret signals."},
        {"icon": "C", "title": "Critics", "text": "Stress-test logic."},
        {"icon": "E", "title": "Executors", "text": "Deploy decisions."},
    ]
    trading_steps = [
        "Analysis agent defines market structure.",
        "Planning agent proposes probabilistic trade templates.",
        "Risk agent stress-tests downside.",
        "Execution layer deploys with discipline.",
    ]
    applications = [
        "AI-assisted development workflows",
        "Multi-repository orchestration",
        "Research synthesis",
        "Knowledge graph generation",
        "Enterprise automation",
    ]
    return {
        "approach_cards": approach_cards,
        "trading_steps": trading_steps,
        "applications": applications,
        "portal_url": portal_url,
        "contact_email": settings.contact_email,
        "contact_name": settings.contact_name,
    }


def _payment_api_url(path: str) -> str:
    settings = get_settings()
    return f"{settings.payment_api_base_url}{path}"


async def _forward_payment_request(path: str, payload: dict | None = None) -> JSONResponse:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            if payload is None:
                response = await client.get(_payment_api_url(path))
            else:
                response = await client.post(_payment_api_url(path), json=payload)
    except httpx.HTTPError:
        return JSONResponse(
            {"status": "error", "error": "Payment service is temporarily unavailable."},
            status_code=502,
        )

    try:
        body = response.json()
    except ValueError:
        return JSONResponse(
            {"status": "error", "error": "Payment service returned an invalid response."},
            status_code=502,
        )
    return JSONResponse(body, status_code=response.status_code)


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def homepage(request: Request):
    return _render(
        request,
        "home.html",
        **_homepage_context(),
    )


@app.api_route("/sso", methods=["GET", "HEAD"])
def legacy_sso_redirect():
    settings = get_settings()
    return RedirectResponse(resolved_portal_url(settings), status_code=307)


@app.api_route("/about", methods=["GET", "HEAD"], response_class=HTMLResponse)
def about_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "about.html",
        portal_url=resolved_portal_url(settings),
    )


@app.api_route("/contact", methods=["GET", "HEAD"], response_class=HTMLResponse)
def contact_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "contact.html",
        portal_url=resolved_portal_url(settings),
        contact_email=settings.contact_email,
        contact_name=settings.contact_name,
    )


@app.api_route("/support", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route(
    "/support/{app_name}", methods=["GET", "HEAD"], response_class=HTMLResponse
)
def support_page(request: Request, app_name: str | None = None):
    settings = get_settings()
    return _render(
        request,
        "support.html",
        contact_email=settings.contact_email,
        app_name=app_name,
    )


@app.api_route(
    "/account-deletion/daligo", methods=["GET", "HEAD"], response_class=HTMLResponse
)
def daligo_account_deletion_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "daligo_account_deletion.html",
        contact_email=settings.contact_email,
    )


@app.api_route(
    "/account-deletion/classroom",
    methods=["GET", "HEAD"],
    response_class=HTMLResponse,
)
def classroom_account_deletion_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "classroom_account_deletion.html",
        contact_email=settings.contact_email,
    )


@app.api_route("/payments", methods=["GET", "HEAD"], response_class=HTMLResponse)
def payments_page(request: Request):
    return _render(request, "payments.html")


@app.api_route("/privacy", methods=["GET", "HEAD"], response_class=HTMLResponse)
def privacy_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "privacy.html",
        contact_email=settings.contact_email,
    )


@app.api_route(
    "/privacy/{app_name}", methods=["GET", "HEAD"], response_class=HTMLResponse
)
def app_privacy_page(request: Request, app_name: str):
    policy = get_app_privacy_policy(app_name)
    if policy is None:
        raise HTTPException(status_code=404, detail="App privacy policy not found")
    settings = get_settings()
    return _render(
        request,
        "privacy/app_policy.html",
        contact_email=settings.contact_email,
        policy=policy,
    )


@app.get("/support/api/config")
async def support_payment_config():
    return await _forward_payment_request("/config")


@app.post("/support/api/create-payment-intent")
async def support_create_payment_intent(request: Request):
    payload = await request.json()
    amount = payload.get("amount")
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return JSONResponse({"status": "error", "error": "Enter a valid amount."}, status_code=400)
    if amount < 100:
        return JSONResponse({"status": "error", "error": "Minimum payment is $1."}, status_code=400)

    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    metadata = {
        **metadata,
        "site": "dalifin.com",
        "source": "dalifin_company_support",
    }
    forwarded_payload = {
        "amount": amount,
        "currency": str(payload.get("currency") or "usd").lower(),
        "metadata": metadata,
    }
    return await _forward_payment_request("/create-payment-intent", forwarded_payload)


@app.post("/support/api/create-setup-intent")
async def support_create_setup_intent(request: Request):
    payload = await request.json()
    forwarded_payload = {}
    customer_id = payload.get("customer_id")
    if customer_id:
        forwarded_payload["customer_id"] = str(customer_id)
    return await _forward_payment_request("/create-setup-intent", forwarded_payload)


@app.api_route("/app", methods=["GET", "HEAD"])
def app_portal_redirect():
    settings = get_settings()
    return RedirectResponse(resolved_portal_url(settings), status_code=307)


@app.api_route("/downloads", methods=["GET", "HEAD"], response_class=HTMLResponse)
def downloads_index(request: Request):
    client = get_download_api_client()
    products: list[dict] = []
    error_message: str | None = None
    try:
        products = client.list_products()
    except DownloadApiError:
        error_message = "Download data is temporarily unavailable. Try again shortly."
    enriched = []
    for product in products:
        catalog = get_catalog_entry(str(product.get("productKey") or ""))
        enriched.append({**product, "catalog": catalog})
    return _render(request, "downloads.html", products=enriched, error_message=error_message)


@app.api_route(
    "/downloads/{product_key}/{platform}/{channel}/{file_name}",
    methods=["GET", "HEAD"],
)
def download_artifact(product_key: str, platform: str, channel: str, file_name: str):
    settings = get_settings()
    artifact_root = Path(settings.download_artifact_root).resolve()
    artifact_path = (artifact_root / product_key / platform / channel / file_name).resolve()
    try:
        artifact_path.relative_to(artifact_root)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Artifact not found") from exc
    if not artifact_path.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")
    media_type = "application/vnd.android.package-archive" if artifact_path.suffix == ".apk" else None
    return FileResponse(artifact_path, media_type=media_type, filename=file_name)


@app.api_route(
    "/downloads/{product_key}", methods=["GET", "HEAD"], response_class=HTMLResponse
)
def downloads_product(request: Request, product_key: str):
    client = get_download_api_client()
    catalog = get_catalog_entry(product_key)
    latest_payload: dict | None = None
    releases_payload: dict | None = None
    error_message: str | None = None
    try:
        latest_payload = client.get_latest_release(product_key)
        releases_payload = client.get_product_releases(product_key)
    except DownloadApiNotFound as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc
    except DownloadApiError:
        error_message = "Release data is temporarily unavailable. The page is showing presentation content only."
    latest = (latest_payload or {}).get("latest")
    releases = (releases_payload or {}).get("releases") or []
    return _render(
        request,
        "download_product.html",
        product_key=product_key,
        catalog=catalog,
        latest=latest,
        releases=releases,
        error_message=error_message,
    )
