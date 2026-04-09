from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.config import get_settings


class DownloadApiError(Exception):
    """Base error for website-facing download API failures."""


class DownloadApiNotFound(DownloadApiError):
    """Raised when the API returns 404 for a requested resource."""


@dataclass
class DownloadApiClient:
    base_url: str = ""
    timeout_seconds: float = 0.0

    def __post_init__(self) -> None:
        settings = get_settings()
        if not self.base_url:
            self.base_url = settings.api_base_url
        if not self.timeout_seconds:
            self.timeout_seconds = settings.request_timeout_seconds

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.get(url, params=params)
        except httpx.HTTPError as exc:
            raise DownloadApiError(f"Request failed for {url}") from exc
        if response.status_code == 404:
            raise DownloadApiNotFound(f"Resource not found for {url}")
        if response.status_code >= 400:
            raise DownloadApiError(f"Unexpected status {response.status_code} for {url}")
        return response.json()

    def list_products(self, platform: str = "android") -> list[dict[str, Any]]:
        payload = self._get_json("/downloads", params={"platform": platform})
        return list(payload.get("products") or [])

    def get_product_releases(
        self,
        product_key: str,
        platform: str = "android",
        channel: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"platform": platform}
        if channel:
            params["channel"] = channel
        return self._get_json(f"/downloads/{product_key}", params=params)

    def get_latest_release(
        self,
        product_key: str,
        platform: str = "android",
        channel: str = "stable",
    ) -> dict[str, Any]:
        return self._get_json(
            f"/downloads/{product_key}/latest",
            params={"platform": platform, "channel": channel},
        )
