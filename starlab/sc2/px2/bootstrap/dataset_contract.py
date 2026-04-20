"""Governed PX2 replay-bootstrap dataset contract helpers (PX2-M02)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal

from starlab.sc2.px2.terran_action_schema import family_for_action

PX2_REPLAY_BOOTSTRAP_DATASET_CONTRACT: Final[str] = "starlab.px2.replay_bootstrap_dataset.v1"
PX2_REPLAY_BOOTSTRAP_REPORT_CONTRACT: Final[str] = "starlab.px2.replay_bootstrap_dataset_report.v1"

SplitName = Literal["train", "eval"]


def split_assignment_for_replay(
    *,
    source_replay_identity: str,
    split_salt: str = "px2_m02_replay_split_v1",
    train_threshold_hex: str = "8",
) -> SplitName:
    """Deterministic replay-level split: hash replay identity, compare first hex nibble.

    Default threshold assigns ~50/50 over uniform hashes; adjust ``train_threshold_hex`` for ratio.
    """

    h = hashlib.sha256(f"{split_salt}:{source_replay_identity}".encode()).hexdigest()
    return "train" if h[0] < train_threshold_hex else "eval"


def _canonical_json_dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class DatasetExampleRecord:
    """One supervised example (feature tensor stored by reference in CI fixtures)."""

    example_id: str
    source_replay_identity: str
    gameloop: int
    label_action_id: str
    label_arguments: dict[str, Any]
    game_state_snapshot: dict[str, Any]
    feature_vector: list[float]
    split: SplitName
    observation_surface: dict[str, Any] | None = None


def build_dataset_artifacts(
    *,
    examples: list[DatasetExampleRecord],
    upstream_bundle_ids: list[str],
    split_salt: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(dataset_json, report_json)``.

    Large tensor blobs stay out of the dataset JSON; M02 fixtures inline small feature vectors.
    """

    kept = len(examples)
    by_family: dict[str, int] = {}
    by_action: dict[str, int] = {}
    for ex in examples:
        by_action[ex.label_action_id] = by_action.get(ex.label_action_id, 0) + 1
        fam = family_for_action(ex.label_action_id).value
        by_family[fam] = by_family.get(fam, 0) + 1

    dataset: dict[str, Any] = {
        "contract_id": PX2_REPLAY_BOOTSTRAP_DATASET_CONTRACT,
        "surface_version": "starlab.px2.terran_core.v1",
        "terr_only": True,
        "split_policy": {
            "kind": "deterministic_replay_level_sha256",
            "split_salt": split_salt,
            "train_threshold_hex": "8",
            "notes": (
                "Train vs eval is assigned per source_replay_identity using "
                "sha256(split_salt:identity).hexdigest()[0] < train_threshold_hex."
            ),
        },
        "upstream": {
            "bundle_ids": upstream_bundle_ids,
            "governed_surfaces": [
                "starlab.replay_bundle_manifest.v1",
                "starlab.replay_build_order_economy.v1",
                "starlab.canonical_state_frame.v1",
                "starlab.observation_frame.v1",
            ],
        },
        "examples": [
            {
                "example_id": ex.example_id,
                "source_replay_identity": ex.source_replay_identity,
                "gameloop": ex.gameloop,
                "split": ex.split,
                "label": {"action_id": ex.label_action_id, "arguments": ex.label_arguments},
                "game_state_snapshot": ex.game_state_snapshot,
                "feature_vector": ex.feature_vector,
                **(
                    {"observation_surface": ex.observation_surface}
                    if ex.observation_surface is not None
                    else {}
                ),
            }
            for ex in examples
        ],
        "non_claims": [
            "Does not prove autonomous strength or ladder performance.",
            "Does not run self-play or industrial Blackwell campaigns (PX2-M03).",
            (
                "Replay-bootstrap supervision only — bounded offline metrics on "
                "held-out replay identities."
            ),
        ],
    }

    report: dict[str, Any] = {
        "contract_id": PX2_REPLAY_BOOTSTRAP_REPORT_CONTRACT,
        "dataset_sha256": __import__("hashlib")
        .sha256(
            _canonical_json_dumps(dataset).encode(),
        )
        .hexdigest(),
        "counts": {
            "examples_kept": kept,
            "examples_skipped": 0,
            "by_action_id": dict(sorted(by_action.items())),
            "by_action_family": by_family,
        },
        "skip_reasons": {},
        "split_counts": {
            "train": sum(1 for e in examples if e.split == "train"),
            "eval": sum(1 for e in examples if e.split == "eval"),
        },
    }
    return dataset, report


def write_dataset_outputs(
    output_dir: Path,
    *,
    dataset: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    dp = output_dir / "px2_replay_bootstrap_dataset.json"
    rp = output_dir / "px2_replay_bootstrap_dataset_report.json"
    dp.write_text(json.dumps(dataset, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return dp, rp


def load_examples_from_dataset_file(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return list(raw["examples"])
