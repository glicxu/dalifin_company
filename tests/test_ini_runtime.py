from __future__ import annotations

from pathlib import Path

from app.ini_runtime import apply_runtime_from_ini


def test_apply_runtime_from_ini_uses_dali_user_slot_and_app_server_section(tmp_path: Path) -> None:
    common = tmp_path / "app_common.ini"
    common.write_text(
        "\n".join(
            [
                "[dali_user]",
                "server = 0.0.0.0",
                "port = 5003",
                "",
                "[app_server]",
                "host = 127.0.0.1",
                "port = 5005",
                "",
                "[dali_payment_service]",
                "server = 0.0.0.0",
                "port = 5006",
            ]
        ),
        encoding="utf-8",
    )
    root = tmp_path / "app_ops.ini"
    root.write_text(
        "\n".join(
            [
                "[config file]",
                f"app_common = {common}",
            ]
        ),
        encoding="utf-8",
    )

    env = apply_runtime_from_ini(str(root))

    assert env["DALIFIN_HOST"] == "0.0.0.0"
    assert env["DALIFIN_PORT"] == "5003"
    assert env["DALIFIN_API_BASE_URL"] == "http://127.0.0.1:5005/account/api"
    assert env["DALIFIN_PAYMENT_API_BASE_URL"] == "http://127.0.0.1:5006"


def test_apply_runtime_from_ini_prefers_dalifin_company_section(tmp_path: Path) -> None:
    common = tmp_path / "app_common.ini"
    common.write_text(
        "\n".join(
            [
                "[dalifin_company]",
                "host = 0.0.0.0",
                "port = 5104",
                "site_name = Dalifin",
                "portal_url = https://server.dalifin.com/sso",
                "payment_api_base_url = http://127.0.0.1:5106",
                "contact_email = gli@dalifin.com",
                "contact_name = Gang Li",
                "",
                "[app_server]",
                "host = 127.0.0.1",
                "port = 5005",
            ]
        ),
        encoding="utf-8",
    )
    root = tmp_path / "app_dalifin_company.ini"
    root.write_text(
        "\n".join(
            [
                "[config file]",
                f"common_config = {common}",
            ]
        ),
        encoding="utf-8",
    )

    env = apply_runtime_from_ini(str(root))

    assert env["DALIFIN_HOST"] == "0.0.0.0"
    assert env["DALIFIN_PORT"] == "5104"
    assert env["DALIFIN_API_BASE_URL"] == "http://127.0.0.1:5005/account/api"
    assert env["DALIFIN_PAYMENT_API_BASE_URL"] == "http://127.0.0.1:5106"
    assert env["DALIFIN_SITE_NAME"] == "Dalifin"
