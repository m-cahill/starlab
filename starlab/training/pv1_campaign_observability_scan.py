"""Filesystem scan for M49/M50/M51 campaign trees (PV1-M01 observability)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from starlab.training.campaign_execution_io import (
    HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME,
    campaign_runs_dir,
)
from starlab.training.campaign_phase_receipt import PHASE_RECEIPT_FILENAME
from starlab.training.full_local_training_campaign_models import (
    CAMPAIGN_PREFLIGHT_RECEIPT_FILENAME,
    FULL_LOCAL_TRAINING_CAMPAIGN_FILENAME,
)

LOCAL_LIVE_PLAY_VALIDATION_RUN: Final[str] = "local_live_play_validation_run.json"
REPLAY_BINDING: Final[str] = "replay_binding.json"
CHECKPOINT_RECEIPT: Final[str] = "tranche_checkpoint_receipt.json"


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _sorted_rel(paths: list[Path], root: Path) -> list[str]:
    rels = [_safe_rel(p, root) for p in paths]
    return sorted(set(rels))


@dataclass
class CampaignObservabilityScan:
    """Immutable summary of discoverable artifacts under a campaign root."""

    campaign_root_resolved: str
    campaign_id: str | None
    campaign_contract_rel: str | None
    preflight_receipt_rel: str | None
    execution_ids: list[str] = field(default_factory=list)
    hidden_rollout_run_rels: list[str] = field(default_factory=list)
    phase_receipt_rels: list[str] = field(default_factory=list)
    replay_binding_rels: list[str] = field(default_factory=list)
    watchable_validation_rels: list[str] = field(default_factory=list)
    checkpoint_receipt_rels: list[str] = field(default_factory=list)


def load_campaign_id_from_contract_path(contract_path: Path) -> str | None:
    try:
        raw = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    cid = raw.get("campaign_id")
    return str(cid) if isinstance(cid, str) and cid else None


def scan_campaign_observability_tree(campaign_root: Path) -> CampaignObservabilityScan:
    """Walk ``campaign_root`` and collect relative paths (sorted, POSIX-style).

    Does not interpret replay or execution semantics — existence/layout only.
    """

    root = campaign_root.resolve()
    if not root.is_dir():
        raise ValueError(f"campaign root is not a directory: {root}")

    contract_path = root / FULL_LOCAL_TRAINING_CAMPAIGN_FILENAME
    contract_rel: str | None = None
    campaign_id: str | None = None
    if contract_path.is_file():
        contract_rel = _safe_rel(contract_path, root)
        campaign_id = load_campaign_id_from_contract_path(contract_path)

    if campaign_id is None:
        campaign_id = root.name

    preflight = root / CAMPAIGN_PREFLIGHT_RECEIPT_FILENAME
    preflight_rel: str | None = None
    if preflight.is_file():
        preflight_rel = _safe_rel(preflight, root)

    exec_ids: list[str] = []
    hidden_runs: list[Path] = []
    cr = campaign_runs_dir(root)
    if cr.is_dir():
        for child in sorted(cr.iterdir()):
            if not child.is_dir():
                continue
            exec_ids.append(child.name)
            hr = child / HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME
            if hr.is_file():
                hidden_runs.append(hr)

    phase_paths = [p for p in root.rglob(PHASE_RECEIPT_FILENAME) if p.is_file()]
    replay_paths = [p for p in root.rglob(REPLAY_BINDING) if p.is_file()]
    watch_paths = [p for p in root.rglob(LOCAL_LIVE_PLAY_VALIDATION_RUN) if p.is_file()]
    ckpt_paths = [p for p in root.rglob(CHECKPOINT_RECEIPT) if p.is_file()]

    return CampaignObservabilityScan(
        campaign_root_resolved=root.as_posix(),
        campaign_id=campaign_id,
        campaign_contract_rel=contract_rel,
        preflight_receipt_rel=preflight_rel,
        execution_ids=sorted(exec_ids),
        hidden_rollout_run_rels=_sorted_rel(hidden_runs, root),
        phase_receipt_rels=_sorted_rel(phase_paths, root),
        replay_binding_rels=_sorted_rel(replay_paths, root),
        watchable_validation_rels=_sorted_rel(watch_paths, root),
        checkpoint_receipt_rels=_sorted_rel(ckpt_paths, root),
    )


def scan_to_jsonable(scan: CampaignObservabilityScan) -> dict[str, Any]:
    return {
        "campaign_contract_path": scan.campaign_contract_rel,
        "campaign_id": scan.campaign_id,
        "campaign_root": scan.campaign_root_resolved,
        "checkpoint_receipt_refs": list(scan.checkpoint_receipt_rels),
        "execution_ids": list(scan.execution_ids),
        "hidden_rollout_run_refs": list(scan.hidden_rollout_run_rels),
        "phase_receipt_refs": list(scan.phase_receipt_rels),
        "preflight_receipt_path": scan.preflight_receipt_rel,
        "replay_binding_refs": list(scan.replay_binding_rels),
        "watchable_validation_refs": list(scan.watchable_validation_rels),
    }
