from __future__ import annotations

from typing import Any

from app.privacy.dali_interpreter import POLICY as DALI_INTERPRETER_POLICY
from app.privacy.dali_wilderness import POLICY as DALI_WILDERNESS_POLICY
from app.privacy.dalitrail import POLICY as DALITRAIL_POLICY
from app.privacy.homepoint import POLICY as HOMEPOINT_POLICY


APP_PRIVACY_POLICIES: dict[str, dict[str, Any]] = {
    "dali-interpreter": DALI_INTERPRETER_POLICY,
    "homepoint": HOMEPOINT_POLICY,
    "dalitrail": DALITRAIL_POLICY,
    "dali-wilderness": DALI_WILDERNESS_POLICY,
}


def get_app_privacy_policy(app_name: str) -> dict[str, Any] | None:
    return APP_PRIVACY_POLICIES.get(app_name.strip().lower())
