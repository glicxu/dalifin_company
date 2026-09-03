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
    assert 'href="/support"' in response.text
    assert 'href="/payments"' in response.text
    assert 'href="/privacy"' in response.text


def test_public_pages_accept_head_requests() -> None:
    for path in ("/", "/about", "/contact", "/support", "/payments", "/downloads"):
        response = client.head(path)
        assert response.status_code == 200


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


def test_support_page_renders_app_support_content() -> None:
    response = client.get("/support")
    assert response.status_code == 200
    assert "Get help with Dalifin apps and services." in response.text
    assert "gli@dalifin.com" in response.text
    assert "Dali Interpreter Listener, Host, and Personal" in response.text
    assert "/privacy" in response.text
    assert "/payments" in response.text
    assert "id=\"support-payment-form\"" not in response.text
    assert "support_checkout.js" not in response.text


def test_payments_page_renders_payment_form() -> None:
    response = client.get("/payments")
    assert response.status_code == 200
    assert "Support Dalifin by credit card." in response.text
    assert "/support" in response.text
    assert "id=\"support-payment-form\"" in response.text
    assert "support_checkout.js" in response.text


def test_privacy_page_renders_general_company_policy_and_app_directory() -> None:
    response = client.get("/privacy")
    assert response.status_code == 200
    assert "Dalifin Privacy Policy." in response.text
    assert "Dalifin LLC" in response.text
    assert "gli@dalifin.com" in response.text
    assert "This general policy" in response.text
    assert "Stripe" in response.text
    assert 'href="/privacy/classroom"' in response.text
    assert 'href="/privacy/dali-interpreter"' in response.text
    assert 'href="/privacy/scribe"' in response.text
    assert 'href="/privacy/homepoint"' in response.text
    assert 'href="/privacy/daligo"' in response.text
    assert 'href="/privacy/dalitrail"' in response.text
    assert 'href="/privacy/dali-wilderness"' in response.text


def test_privacy_pages_accept_head_requests_for_store_validators() -> None:
    for path in (
        "/privacy",
        "/privacy/classroom",
        "/privacy/scribe",
        "/privacy/homepoint",
        "/privacy/daligo",
        "/support/daligo",
        "/account-deletion/classroom",
        "/account-deletion/daligo",
    ):
        response = client.head(path)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")


def test_daligo_account_deletion_page_provides_external_request_path() -> None:
    response = client.get("/account-deletion/daligo")
    assert response.status_code == 200
    assert "Request deletion of your Daligo account and data" in response.text
    assert "Dalifin LLC" in response.text
    assert "Daligo account deletion request" in response.text
    assert "mailto:gli@dalifin.com" in response.text
    assert "within 30 days" in response.text
    assert "does not cancel a subscription" in response.text


def test_classroom_account_deletion_page_provides_external_request_path() -> None:
    response = client.get("/account-deletion/classroom")
    assert response.status_code == 200
    assert "Request deletion of your Dali Classroom account and associated data" in response.text
    assert "Dalifin LLC" in response.text
    assert "Dali Classroom account and data deletion request" in response.text
    assert "mailto:gli@dalifin.com" in response.text
    assert "Delete Classroom data only" in response.text
    assert "Delete the shared Dali account" in response.text
    assert "within 30 days" in response.text
    assert "does not cancel a subscription" in response.text


def test_dali_interpreter_privacy_page_contains_interpreter_disclosures() -> None:
    response = client.get("/privacy/dali-interpreter")
    assert response.status_code == 200
    assert "Dali Interpreter Privacy Policy" in response.text
    assert "Live audio" in response.text
    assert "transcripts" in response.text
    assert "third-party hosting" in response.text
    assert "Dalifin LLC" in response.text


def test_classroom_privacy_page_discloses_private_text_and_transient_audio() -> None:
    response = client.get("/privacy/classroom")
    assert response.status_code == 200
    assert "Dali Classroom Privacy Policy" in response.text
    assert "does not save source audio" in response.text
    assert "Google Gemini" in response.text
    assert "OpenAI" in response.text
    assert "private, student-owned Classroom content" in response.text
    assert "delete Classroom content" in response.text
    assert "shared Dali identity" in response.text
    assert "does not require location" in response.text
    assert "Dalifin LLC" in response.text
    assert 'href="/account-deletion/classroom"' in response.text


def test_scribe_privacy_page_discloses_transient_audio_and_local_content() -> None:
    response = client.get("/privacy/scribe")
    assert response.status_code == 200
    assert "Dali Scribe Privacy Policy" in response.text
    assert "does not save source audio" in response.text
    assert "stored primarily in the app&#39;s private storage" in response.text
    assert "authorized AI provider" in response.text
    assert "transaction-verification data" in response.text
    assert "recording, consent, privacy, confidentiality" in response.text
    assert "Dalifin LLC" in response.text


def test_homepoint_privacy_page_discloses_background_location() -> None:
    response = client.get("/privacy/homepoint")
    assert response.status_code == 200
    assert "HomePoint Privacy Policy" in response.text
    assert "precise location" in response.text
    assert "in the background" in response.text
    assert "does not transmit location" in response.text
    assert "Physical activity" in response.text
    assert "does not retain session or daily step totals" in response.text
    assert "continues using GPS and compass" in response.text
    assert "Dalifin LLC" in response.text


def test_dalitrail_privacy_page_discloses_online_and_local_processing() -> None:
    response = client.get("/privacy/dalitrail")
    assert response.status_code == 200
    assert "DaliTrail Privacy Policy" in response.text
    assert "background location" in response.text
    assert "Open-Meteo" in response.text
    assert "Nominatim" in response.text
    assert "live sharing" in response.text


def test_daligo_privacy_page_discloses_group_and_nearby_sharing() -> None:
    response = client.get("/privacy/daligo")
    assert response.status_code == 200
    assert "Daligo Privacy Policy" in response.text
    assert "background location" in response.text
    assert "members of that trip" in response.text
    assert "Bluetooth" in response.text
    assert "local Wi-Fi" in response.text
    assert "public recap" in response.text


def test_dali_wilderness_privacy_page_discloses_optional_location_services() -> None:
    response = client.get("/privacy/dali-wilderness")
    assert response.status_code == 200
    assert "Dali Wilderness Privacy Policy" in response.text
    assert "background location" in response.text
    assert "Open-Meteo" in response.text
    assert "Look Up Address" in response.text
    assert "Physical activity" in response.text
    assert "session step count" in response.text
    assert "continues recording and navigating with GPS and compass" in response.text
    assert "backup or export only when the user initiates" in response.text
    assert "Delete All Local Data" in response.text


def test_unknown_app_privacy_page_returns_not_found() -> None:
    response = client.get("/privacy/not-an-app")
    assert response.status_code == 404


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
    assert "DaliBible for Android" in response.text
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
    assert "iPhone TestFlight" in response.text
    assert "https://testflight.apple.com/join/3K8BrU1t" in response.text


def test_downloads_page_handles_api_failure_gracefully() -> None:
    with patch("app.main.get_download_api_client") as get_client:
        get_client.return_value.list_products.side_effect = DownloadApiError("unexpected")
        response = client.get("/downloads")
    assert response.status_code == 200
    assert "Download data is temporarily unavailable." in response.text
