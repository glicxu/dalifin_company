from __future__ import annotations

import argparse
import os

import uvicorn

from app.ini_runtime import apply_runtime_from_ini


def main() -> None:
    parser = argparse.ArgumentParser(description="Run dalifin_company from an ini config.")
    parser.add_argument("-c", "--config", required=True, help="Path to config ini file")
    args = parser.parse_args()

    apply_runtime_from_ini(args.config)
    from app.main import app

    uvicorn.run(
        app,
        host=os.environ.get("DALIFIN_HOST", "127.0.0.1"),
        port=int(os.environ.get("DALIFIN_PORT", "5003")),
    )


if __name__ == "__main__":
    main()
