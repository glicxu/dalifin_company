from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

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


def test_sso_route_renders_homepage() -> None:
    response = client.get("/sso")
    assert response.status_code == 200
    assert "Create Agents. Orchestrate Intelligence." in response.text


def test_about_page_renders_public_company_copy() -> None:
    response = client.get("/about")
    assert response.status_code == 200
    assert "We build agentic systems for complex decision environments." in response.text


def test_contact_page_renders_contact_details() -> None:
    response = client.get("/contact")
    assert response.status_code == 200
    assert "gli@dalifin.com" in response.text


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
