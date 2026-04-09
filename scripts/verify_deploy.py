from __future__ import annotations

import argparse
import sys

import httpx


def _check(client: httpx.Client, url: str) -> tuple[int, str]:
    response = client.get(url)
    return response.status_code, response.text[:300]


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-check dalifin_company deployment.")
    parser.add_argument("--base-url", required=True, help="Website base URL, e.g. http://127.0.0.1:5104")
    parser.add_argument(
        "--api-url",
        required=True,
        help="app_server API base URL, e.g. http://127.0.0.1:5005/account/api",
    )
    args = parser.parse_args()

    website_checks = [
        "/healthz",
        "/version",
        "/",
        "/about",
        "/contact",
        "/downloads",
        "/downloads/mobile_bible",
    ]
    api_checks = [
        "/downloads",
        "/downloads/mobile_bible/latest?platform=android&channel=stable",
    ]

    failures: list[str] = []
    with httpx.Client(timeout=10, follow_redirects=True) as client:
        for path in website_checks:
            status, body = _check(client, f"{args.base_url.rstrip('/')}{path}")
            if status != 200:
                failures.append(f"website {path} -> {status} body={body!r}")
        for path in api_checks:
            status, body = _check(client, f"{args.api_url.rstrip('/')}{path}")
            if status != 200:
                failures.append(f"api {path} -> {status} body={body!r}")

    if failures:
        for item in failures:
            print(item)
        return 1

    print("dalifin_company smoke checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
