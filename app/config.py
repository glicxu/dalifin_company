from __future__ import annotations

import os
from functools import lru_cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    site_name: str = os.getenv("DALIFIN_SITE_NAME", "Dalifin")
    api_base_url: str = os.getenv("DALIFIN_API_BASE_URL", "http://127.0.0.1:8000/account/api").rstrip("/")
    request_timeout_seconds: float = float(os.getenv("DALIFIN_API_TIMEOUT_SECONDS", "5"))
    portal_url: str = os.getenv("DALIFIN_PORTAL_URL", "https://server.dalifin.com/account")
    contact_email: str = os.getenv("DALIFIN_CONTACT_EMAIL", "gli@dalifin.com")
    contact_name: str = os.getenv("DALIFIN_CONTACT_NAME", "Gang Li")
    build_id: str = os.getenv("DALIFIN_BUILD_ID", "dev")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def refresh_settings() -> Settings:
    get_settings.cache_clear()
    return get_settings()
