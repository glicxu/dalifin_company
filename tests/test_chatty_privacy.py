from fastapi.testclient import TestClient

from app.main import app


def test_chatty_policy_is_public_and_has_current_data_and_deletion_disclosures():
    with TestClient(app) as client:
        response = client.get("/privacy/chatty")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
        body = response.text
        for disclosure in (
            "Dali Chatty Privacy Policy",
            "November 10, 2026",
            "adults aged 18 and older",
            "Gmail",
            "OAuth",
            "OpenAI",
            "Google Gemini",
            "scheduled",
            "private app storage",
            "Dalifin servers",
            "separate, explicit account-specific opt-in",
            "closing the app is not cancellation",
            "does not immediately erase every provider record",
            "gli@dalifin.com",
        ):
            assert disclosure in body
        assert "not directed to children under 13" not in body
        assert 'href="https://chatty.dalifin.com/account-deletion"' in body
        assert 'href="https://chatty.dalifin.com/terms"' in body
        assert client.head("/privacy/chatty").status_code == 200


def test_privacy_index_discovers_chatty_and_preserves_existing_policies():
    with TestClient(app) as client:
        response = client.get("/privacy")
        assert 'href="/privacy/chatty"' in response.text
        for slug in (
            "classroom", "dali-audio", "dali-cam", "dalijob", "dalibible",
            "dali-interpreter", "scribe", "homepoint", "daligo", "dalitrail",
            "dali-wilderness",
        ):
            assert f'href="/privacy/{slug}"' in response.text
            assert client.get(f"/privacy/{slug}").status_code == 200
