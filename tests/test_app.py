from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

from app.download_api import DownloadApiError
from app.main import app


client = TestClient(app)


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version_returns_build_info_shape() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "dalifin_company"
    assert "buildId" in body


def test_homepage_renders_core_message() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Create Agents. Orchestrate Intelligence." in response.text
    assert "What Is Agentic Development?" in response.text


def test_sso_route_redirects_to_portal() -> None:
    response = client.get("/sso", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://server.dalifin.com/account"


def test_about_page_renders_public_company_copy() -> None:
    response = client.get("/about")
    assert response.status_code == 200
    assert "We build agentic systems for complex decision environments." in response.text


def test_contact_page_renders_contact_details() -> None:
    response = client.get("/contact")
    assert response.status_code == 200
    assert "gli@dalifin.com" in response.text


def test_support_page_renders_payment_form() -> None:
    response = client.get("/support")
    assert response.status_code == 200
    assert "Support Dalifin by credit card." in response.text
    assert "id=\"support-payment-form\"" in response.text
    assert "support_checkout.js" in response.text


def test_support_payment_config_proxies_to_payment_service() -> None:
    forwarded = AsyncMock(return_value=JSONResponse({"publishableKey": "pk_test_123"}))
    with patch("app.main._forward_payment_request", forwarded):
        response = client.get("/support/api/config")
    assert response.status_code == 200
    assert response.json()["publishableKey"] == "pk_test_123"
    forwarded.assert_awaited_once_with("/config")


def test_support_create_payment_intent_validates_amount() -> None:
    response = client.post("/support/api/create-payment-intent", json={"amount": 99})
    assert response.status_code == 400
    assert response.json()["error"] == "Minimum payment is $1."


def test_support_create_payment_intent_adds_site_metadata() -> None:
    forwarded = AsyncMock(return_value=JSONResponse({"clientSecret": "pi_secret"}))
    with patch("app.main._forward_payment_request", forwarded):
        response = client.post(
            "/support/api/create-payment-intent",
            json={"amount": 2500, "currency": "USD", "metadata": {"campaign": "home"}},
        )
    assert response.status_code == 200
    forwarded.assert_awaited_once()
    path, payload = forwarded.await_args.args
    assert path == "/create-payment-intent"
    assert payload["amount"] == 2500
    assert payload["currency"] == "usd"
    assert payload["metadata"]["campaign"] == "home"
    assert payload["metadata"]["site"] == "dalifin.com"
    assert payload["metadata"]["source"] == "dalifin_company_support"


def test_app_route_redirects_to_portal() -> None:
    response = client.get("/app", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://server.dalifin.com/account"


def test_downloads_page_lists_products_from_api() -> None:
    with patch("app.main.get_download_api_client") as get_client:
        get_client.return_value.list_products.return_value = [
            {
                "productKey": "mobile_bible",
                "displayName": "Mobile Bible for Android",
                "publicDownloads": True,
                "requireSignIn": False,
            }
        ]
        response = client.get("/downloads")
    assert response.status_code == 200
    assert "Mobile Bible for Android" in response.text
    assert "/downloads/mobile_bible" in response.text


def test_product_page_shows_latest_release_and_list() -> None:
    with patch("app.main.get_download_api_client") as get_client:
        api_client = get_client.return_value
        api_client.get_latest_release.return_value = {
            "latest": {
                "displayName": "Mobile Bible for Android",
                "versionLabel": "1.0.4",
                "fileName": "mobile_bible.apk",
                "minOsVersion": "Android 8.0+",
                "artifactUrl": "https://downloads.example/mobile_bible.apk",
                "artifactType": "apk",
                "packageName": "com.dalifin.mobile_bible",
                "publishedAt": "2026-04-07T18:00:00Z",
                "releaseNotes": "Bug fixes.",
            }
        }
        api_client.get_product_releases.return_value = {
            "releases": [
                {
                    "versionLabel": "1.0.4",
                    "artifactUrl": "https://downloads.example/mobile_bible.apk",
                    "publishedAt": "2026-04-07T18:00:00Z",
                }
            ]
        }
        response = client.get("/downloads/mobile_bible")
    assert response.status_code == 200
    assert "Version 1.0.4" in response.text
    assert "Bug fixes." in response.text
    assert "https://downloads.example/mobile_bible.apk" in response.text


def test_downloads_page_handles_api_failure_gracefully() -> None:
    with patch("app.main.get_download_api_client") as get_client:
        get_client.return_value.list_products.side_effect = DownloadApiError("unexpected")
        response = client.get("/downloads")
    assert response.status_code == 200
    assert "Download data is temporarily unavailable." in response.text
