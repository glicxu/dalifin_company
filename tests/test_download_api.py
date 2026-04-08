from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.download_api import DownloadApiClient, DownloadApiError, DownloadApiNotFound


def test_list_products_uses_expected_endpoint() -> None:
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"products": []}
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_client
    mock_context.__exit__.return_value = False
    with patch("app.download_api.httpx.Client", return_value=mock_context) as client_ctor:
        client = DownloadApiClient(base_url="https://example.com/account/api")
        products = client.list_products()
    assert products == []
    client_ctor.assert_called_once()
    mock_client.get.assert_called_once_with(
        "https://example.com/account/api/downloads",
        params={"platform": "android"},
    )


def test_get_latest_release_raises_not_found() -> None:
    mock_response = MagicMock(status_code=404)
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_client
    mock_context.__exit__.return_value = False
    with patch("app.download_api.httpx.Client", return_value=mock_context):
        client = DownloadApiClient(base_url="https://example.com/account/api")
        with pytest.raises(DownloadApiNotFound):
            client.get_latest_release("mobile_bible")


def test_get_json_raises_api_error_on_server_failure() -> None:
    mock_response = MagicMock(status_code=500)
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_client
    mock_context.__exit__.return_value = False
    with patch("app.download_api.httpx.Client", return_value=mock_context):
        client = DownloadApiClient(base_url="https://example.com/account/api")
        with pytest.raises(DownloadApiError):
            client.get_product_releases("mobile_bible")
