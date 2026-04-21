from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.catalog import get_catalog_entry
from app.config import get_settings, resolved_portal_url
from app.download_api import DownloadApiClient, DownloadApiError, DownloadApiNotFound

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


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return _render(
        request,
        "home.html",
        **_homepage_context(),
    )


@app.get("/sso")
def legacy_sso_redirect():
    settings = get_settings()
    return RedirectResponse(resolved_portal_url(settings), status_code=307)


@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "about.html",
        portal_url=resolved_portal_url(settings),
    )


@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    settings = get_settings()
    return _render(
        request,
        "contact.html",
        portal_url=resolved_portal_url(settings),
        contact_email=settings.contact_email,
        contact_name=settings.contact_name,
    )


@app.get("/app")
def app_portal_redirect():
    settings = get_settings()
    return RedirectResponse(resolved_portal_url(settings), status_code=307)


@app.get("/downloads", response_class=HTMLResponse)
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


@app.get("/downloads/{product_key}", response_class=HTMLResponse)
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
