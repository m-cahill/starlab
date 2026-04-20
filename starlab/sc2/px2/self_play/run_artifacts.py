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


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(obj), encoding="utf-8")
