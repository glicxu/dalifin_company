from __future__ import annotations

from app.config import get_settings, refresh_settings


def test_refresh_settings_reloads_environment(monkeypatch) -> None:
    monkeypatch.setenv("DALIFIN_API_BASE_URL", "http://127.0.0.1:5005/account/api")
    monkeypatch.setenv("DALIFIN_SITE_NAME", "Dalifin")
    refresh_settings()

    settings = get_settings()

    assert settings.api_base_url == "http://127.0.0.1:5005/account/api"
    assert settings.site_name == "Dalifin"
