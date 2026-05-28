from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import refresh_settings
from app.main import app


client = TestClient(app)


def test_download_artifact_serves_file(tmp_path, monkeypatch) -> None:
    artifact_root = tmp_path / "mobile-downloads"
    artifact_path = (
        artifact_root
        / "interprete"
        / "android"
        / "stable"
        / "interprete-android-stable-1.0.0+1.apk"
    )
    artifact_path.parent.mkdir(parents=True)
    artifact_path.write_bytes(b"apk bytes")

    monkeypatch.setenv("DALIFIN_DOWNLOAD_ARTIFACT_ROOT", str(artifact_root))
    refresh_settings()
    try:
        response = client.get(
            "/downloads/interprete/android/stable/interprete-android-stable-1.0.0+1.apk"
        )
    finally:
        monkeypatch.delenv("DALIFIN_DOWNLOAD_ARTIFACT_ROOT", raising=False)
        refresh_settings()

    assert response.status_code == 200
    assert response.content == b"apk bytes"
    assert response.headers["content-type"] == "application/vnd.android.package-archive"


def test_download_artifact_rejects_missing_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DALIFIN_DOWNLOAD_ARTIFACT_ROOT", str(tmp_path))
    refresh_settings()
    try:
        response = client.get("/downloads/interprete/android/stable/missing.apk")
    finally:
        monkeypatch.delenv("DALIFIN_DOWNLOAD_ARTIFACT_ROOT", raising=False)
        refresh_settings()

    assert response.status_code == 404
