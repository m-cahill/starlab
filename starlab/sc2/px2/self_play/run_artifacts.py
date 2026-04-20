"""Campaign run manifest and on-disk layout helpers (PX2-M03 slice 2)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps

RUN_MANIFEST_VERSION: Final[str] = "starlab.px2.self_play_run_manifest.v1"


def default_run_subdirs() -> dict[str, str]:
    """Relative directory names under a campaign run root."""

    return {
        "checkpoints": "checkpoint_receipts",
        "evaluations": "evaluation_receipts",
    }


def default_operator_local_slice4_subdirs() -> dict[str, str]:
    """Slice-4 operator-local layout: slice-2 dirs plus promotion/rollback receipt folders."""

    base = default_run_subdirs()
    return {
        **base,
        "promotions": "promotion_receipts",
        "rollbacks": "rollback_receipts",
    }


def ensure_operator_local_slice4_layout(run_root: Path) -> dict[str, Path]:
    """Create expected subdirectories under ``run_root``; return absolute paths by logical key."""

    out: dict[str, Path] = {}
    for key, rel in default_operator_local_slice4_subdirs().items():
        p = (run_root / rel).resolve()
        p.mkdir(parents=True, exist_ok=True)
        out[key] = p
    return out


def build_run_manifest(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    execution_kind: str,
    fixture_episode_count: int,
    checkpoint_episode_cadence: int,
    eval_episode_cadence: int,
    corpus_note: str,
    torch_seed: int,
) -> dict[str, Any]:
    """Deterministic run manifest (not sealed — companion to sealed campaign run)."""

    return {
        "run_manifest_version": RUN_MANIFEST_VERSION,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "execution_kind": execution_kind,
        "fixture_episode_count": fixture_episode_count,
        "effective_checkpoint_cadence_episodes": checkpoint_episode_cadence,
        "effective_eval_cadence_episodes": eval_episode_cadence,
        "cadence_note": (
            "Effective cadences are slice-2 skeleton overrides so receipts appear in bounded CI; "
            "industrial runs follow campaign contract cadence fields."
        ),
        "corpus_note": corpus_note,
        "torch_seed": torch_seed,
        "non_claims": [
            "Slice-2 skeleton manifest — not industrial campaign evidence.",
        ],
    }


def build_slice4_continuity_manifest(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    execution_kind: str,
    continuity_step_count: int,
    preflight_sha256: str,
    corpus_note: str,
    torch_seed: int,
    operator_local_layout: dict[str, str],
) -> dict[str, Any]:
    """Companion manifest for slice-4 continuity runs (not sealed)."""

    return {
        "run_manifest_version": RUN_MANIFEST_VERSION,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "execution_kind": execution_kind,
        "continuity_step_count": continuity_step_count,
        "preflight_sha256": preflight_sha256,
        "corpus_note": corpus_note,
        "torch_seed": torch_seed,
        "operator_local_layout": operator_local_layout,
        "non_claims": (
            [
                "Slice-5 continuity manifest — bounded campaign-root run; not industrial campaign.",
            ]
            if "slice5" in execution_kind
            else [
                (
                    "Slice-4 continuity manifest — bounded multi-step linkage; "
                    "not industrial campaign."
                ),
            ]
        ),
    }


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(obj), encoding="utf-8")
