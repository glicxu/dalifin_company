from __future__ import annotations

from typing import Any

from app.privacy.classroom import POLICY as CLASSROOM_POLICY
from app.privacy.dali_interpreter import POLICY as DALI_INTERPRETER_POLICY
from app.privacy.dali_wilderness import POLICY as DALI_WILDERNESS_POLICY
from app.privacy.daligo import POLICY as DALIGO_POLICY
from app.privacy.dalitrail import POLICY as DALITRAIL_POLICY
from app.privacy.homepoint import POLICY as HOMEPOINT_POLICY
from app.privacy.scribe import POLICY as SCRIBE_POLICY


APP_PRIVACY_POLICIES: dict[str, dict[str, Any]] = {
    "classroom": CLASSROOM_POLICY,
    "dali-interpreter": DALI_INTERPRETER_POLICY,
    "scribe": SCRIBE_POLICY,
    "homepoint": HOMEPOINT_POLICY,
    "dalitrail": DALITRAIL_POLICY,
    "dali-wilderness": DALI_WILDERNESS_POLICY,
    "daligo": DALIGO_POLICY,
}


def get_app_privacy_policy(app_name: str) -> dict[str, Any] | None:
    return APP_PRIVACY_POLICIES.get(app_name.strip().lower())
