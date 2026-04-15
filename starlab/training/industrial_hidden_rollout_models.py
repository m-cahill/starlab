"""M50: industrial hidden rollout capability / visibility posture (honest downgrade reporting)."""

from __future__ import annotations

import sys
from typing import Final, TypedDict

EXECUTION_PREFLIGHT_RECEIPT_NOTE: Final[str] = (
    "Extended execution readiness checks (M50); see individual check_id entries."
)

INDUSTRIAL_HIDDEN_ROLLOUT_CONTRACT_VERSION: Final[str] = "starlab.industrial_hidden_rollout_mode.v1"
HIDDEN_ROLLOUT_CAMPAIGN_RUN_VERSION: Final[str] = "starlab.hidden_rollout_campaign_run.v2"
HIDDEN_ROLLOUT_CAMPAIGN_RUN_REPORT_VERSION: Final[str] = (
    "starlab.hidden_rollout_campaign_run_report.v1"
)
CAMPAIGN_EXECUTION_MANIFEST_VERSION: Final[str] = "starlab.campaign_execution_manifest.v1"
CAMPAIGN_HEARTBEAT_VERSION: Final[str] = "starlab.campaign_heartbeat.v1"
CAMPAIGN_RESUME_STATE_VERSION: Final[str] = "starlab.campaign_resume_state.v1"
CAMPAIGN_OUTPUT_LOCK_VERSION: Final[str] = "starlab.campaign_output_lock.v1"
CAMPAIGN_EXECUTION_LOCK_VERSION: Final[str] = "starlab.campaign_execution_lock.v1"


class IndustrialHiddenRolloutCapabilityV1(TypedDict, total=False):
    """Resolved capability record for campaign execution artifacts."""

    requested_visibility_mode: str
    resolved_visibility_mode: str
    hidden_rollout_supported: bool
    hidden_rollout_mechanism_id: str
    capability_warnings: list[str]
    platform: str


def _platform_tag() -> str:
    return sys.platform


def resolve_visibility_posture_v1(*, requested: str) -> IndustrialHiddenRolloutCapabilityV1:
    """Resolve requested visibility to an honest posture (no silent downgrade).

    Policy (M50): do not assume true headless on Windows; ``hidden`` requested often resolves to
    ``minimized`` with explicit warnings — never claim ``hidden`` unless mechanism proves it.
    """

    req = requested.strip().lower()
    valid: tuple[str, ...] = ("hidden", "minimized", "visible_fallback", "unsupported")
    if req not in valid:
        return {
            "capability_warnings": [
                f"invalid requested_visibility_mode {requested!r}; treating as unsupported"
            ],
            "hidden_rollout_mechanism_id": "invalid_request",
            "hidden_rollout_supported": False,
            "platform": _platform_tag(),
            "requested_visibility_mode": requested,
            "resolved_visibility_mode": "unsupported",
        }

    if req == "unsupported":
        return {
            "capability_warnings": [],
            "hidden_rollout_mechanism_id": "explicit_unsupported",
            "hidden_rollout_supported": False,
            "platform": _platform_tag(),
            "requested_visibility_mode": req,
            "resolved_visibility_mode": "unsupported",
        }

    if req == "visible_fallback":
        return {
            "capability_warnings": [],
            "hidden_rollout_mechanism_id": "visible_window_default",
            "hidden_rollout_supported": False,
            "platform": _platform_tag(),
            "requested_visibility_mode": req,
            "resolved_visibility_mode": "visible_fallback",
        }

    if req == "minimized":
        return {
            "capability_warnings": [],
            "hidden_rollout_mechanism_id": "best_effort_minimized_not_guaranteed",
            "hidden_rollout_supported": False,
            "platform": _platform_tag(),
            "requested_visibility_mode": req,
            "resolved_visibility_mode": "minimized",
        }

    # req == "hidden"
    warnings = [
        (
            "requested_visibility_mode=hidden: true headless / fully hidden SC2 is not promised on "
            "this platform in M50; resolved to minimized best-effort unless a stronger mechanism "
            "is proven and recorded out-of-band."
        ),
    ]
    return {
        "capability_warnings": warnings,
        "hidden_rollout_mechanism_id": "windows_style_best_effort_minimized_fallback",
        "hidden_rollout_supported": False,
        "platform": _platform_tag(),
        "requested_visibility_mode": req,
        "resolved_visibility_mode": "minimized",
    }
