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
