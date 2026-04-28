from __future__ import annotations

import configparser
import os
from pathlib import Path

from app.config import refresh_settings


def _read_ini(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    with path.open("r", encoding="utf-8") as handle:
        parser.read_file(handle)
    return parser


def _iter_include_paths(parser: configparser.ConfigParser, base_dir: Path) -> list[Path]:
    includes: list[Path] = []
    if not parser.has_section("config file"):
        return includes
    for _, value in parser.items("config file"):
        raw = str(value or "").strip()
        if not raw:
            continue
        include_path = Path(raw)
        if not include_path.is_absolute():
            include_path = (base_dir / include_path).resolve()
        includes.append(include_path)
    return includes


def _merged_parser(config_path: Path) -> configparser.ConfigParser:
    root = _read_ini(config_path)
    merged = configparser.ConfigParser()
    for include_path in _iter_include_paths(root, config_path.parent):
        if include_path.exists():
            merged.read(include_path, encoding="utf-8")
    merged.read(config_path, encoding="utf-8")
    return merged


def apply_runtime_from_ini(config_path: str) -> dict[str, str]:
    path = Path(config_path).resolve()
    parser = _merged_parser(path)

    service_section = "dalifin_company" if parser.has_section("dalifin_company") else "dali_user"
    host = parser.get(service_section, "host", fallback=parser.get(service_section, "server", fallback="127.0.0.1"))
    port = parser.get(service_section, "port", fallback="5003")

    api_host = parser.get("app_server", "host", fallback=parser.get("app_server", "server", fallback="127.0.0.1"))
    if api_host == "0.0.0.0":
        api_host = "127.0.0.1"
    api_port = parser.get("app_server", "port", fallback="5005")

    env_updates = {
        "DALIFIN_HOST": host,
        "DALIFIN_PORT": port,
        "DALIFIN_API_BASE_URL": f"http://{api_host}:{api_port}/account/api",
    }

    if parser.has_section("dali_payment_service"):
        payment_host = parser.get(
            "dali_payment_service",
            "host",
            fallback=parser.get("dali_payment_service", "server", fallback="127.0.0.1"),
        )
        if payment_host == "0.0.0.0":
            payment_host = "127.0.0.1"
        payment_port = parser.get("dali_payment_service", "port", fallback="5006")
        env_updates["DALIFIN_PAYMENT_API_BASE_URL"] = f"http://{payment_host}:{payment_port}"

    if parser.has_section("dalifin_company"):
        optional_map = {
            "site_name": "DALIFIN_SITE_NAME",
            "portal_url": "DALIFIN_PORTAL_URL",
            "contact_email": "DALIFIN_CONTACT_EMAIL",
            "contact_name": "DALIFIN_CONTACT_NAME",
            "build_id": "DALIFIN_BUILD_ID",
            "payment_api_base_url": "DALIFIN_PAYMENT_API_BASE_URL",
        }
        for ini_key, env_key in optional_map.items():
            if parser.has_option("dalifin_company", ini_key):
                env_updates[env_key] = parser.get("dalifin_company", ini_key)

    os.environ.update(env_updates)
    refresh_settings()
    return env_updates
