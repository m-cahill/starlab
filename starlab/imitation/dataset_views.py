"""Build replay training dataset + report from governed M14 bundle directories (M26)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from starlab._io import JSON_ROOT_MUST_BE_OBJECT, parse_json_object_text
from starlab.imitation.dataset_models import (
    APPROVED_TARGET_SEMANTIC_KINDS,
    LABEL_POLICY_ID,
    NON_CLAIMS_V1,
    REPLAY_TRAINING_DATASET_REPORT_VERSION,
    REPLAY_TRAINING_DATASET_VERSION,
    SELECTION_POLICY_ID,
    SPLIT_POLICY_ID,
    UNSAFE_INTAKE_STATUSES,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def load_json_object(path: Path) -> dict[str, Any]:
    """Load JSON object from ``path``; propagate :exc:`json.JSONDecodeError` on decode failure."""

    raw = path.read_text(encoding="utf-8")
    obj, err = parse_json_object_text(raw)
    if err is None:
        assert obj is not None
        return obj
    if err == JSON_ROOT_MUST_BE_OBJECT:
        msg = f"{path}: JSON root must be an object"
        raise ValueError(msg)
    try:
        json.loads(raw)
    except json.JSONDecodeError:
        raise
    raise RuntimeError("unreachable")


def split_mod100_from_example_id(example_id: str) -> str:
    """Deterministic train/validation/test split (80/10/10) over SHA-256(example_id)."""

    digest = hashlib.sha256(example_id.encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:8], byteorder="big", signed=False) % 100
    if bucket < 80:
        return "train"
    if bucket < 90:
        return "validation"
    return "test"


def map_timeline_to_coarse_label(
    *,
    semantic_kind: str,
    source_stream: str,
) -> str:
    """Map governed timeline semantics to a coarse, non-claiming action label."""

    sk = semantic_kind
    if sk == "upgrade_completed":
        return "research_upgrade"
    if sk == "unit_born":
        return "production_unit"
    if sk == "unit_init":
        return "production_structure"
    if sk == "unit_type_changed":
        return "economy_expand"
    if sk == "command_issued":
        if source_stream == "game":
            return "army_move"
        return "other"
    if sk == "ping_event":
        return "scout"
    if sk == "message_event":
        return "other"
    if sk in ("unit_died", "unit_owner_changed"):
        return "other"
    return "other"


def _perspective_player_index(entry: dict[str, Any]) -> int | None:
    pi = entry.get("player_index")
    if isinstance(pi, int) and not isinstance(pi, bool):
        return pi
    payload = entry.get("payload")
    if isinstance(payload, dict):
        cid = payload.get("m_controlPlayerId")
        if isinstance(cid, int) and not isinstance(cid, bool) and cid >= 1:
            return cid - 1
        if isinstance(cid, int) and not isinstance(cid, bool) and cid == 0:
            return 0
    return None


def _validate_m14_bundle_directory(
    bundle_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    mp = bundle_dir / "replay_bundle_manifest.json"
    lp = bundle_dir / "replay_bundle_lineage.json"
    cp = bundle_dir / "replay_bundle_contents.json"
    for p, label in ((mp, "manifest"), (lp, "lineage"), (cp, "contents")):
        if not p.is_file():
            msg = f"{bundle_dir}: missing {label} ({p.name})"
            raise ValueError(msg)

    manifest = load_json_object(mp)
    lineage = load_json_object(lp)
    contents = load_json_object(cp)

    if manifest.get("contract") != "starlab.replay_bundle_contract.v1":
        msg = f"{mp}: unsupported bundle contract {manifest.get('contract')!r}"
        raise ValueError(msg)
    if manifest.get("profile") != "starlab.replay_bundle.m14.v1":
        msg = f"{mp}: unsupported bundle profile {manifest.get('profile')!r}"
        raise ValueError(msg)
    if manifest.get("schema_version") != "starlab.replay_bundle_manifest.v1":
        msg = f"{mp}: unsupported manifest schema {manifest.get('schema_version')!r}"
        raise ValueError(msg)

    if lineage.get("contract") != "starlab.replay_bundle_contract.v1":
        msg = f"{lp}: lineage contract mismatch"
        raise ValueError(msg)
    if lineage.get("schema_version") != "starlab.replay_bundle_lineage.v1":
        msg = f"{lp}: unsupported lineage schema"
        raise ValueError(msg)

    bid_m = manifest.get("bundle_id")
    bid_l = lineage.get("bundle_id")
    if not isinstance(bid_m, str) or not isinstance(bid_l, str) or bid_m != bid_l:
        msg = f"{bundle_dir}: manifest.bundle_id and lineage.bundle_id mismatch"
        raise ValueError(msg)

    lr = manifest.get("lineage_root")
    roots = lineage.get("root_hashes")
    if not isinstance(lr, str) or not isinstance(roots, list):
        msg = f"{bundle_dir}: invalid lineage_root or root_hashes"
        raise ValueError(msg)
    if lr not in roots:
        msg = f"{bundle_dir}: manifest.lineage_root not in lineage.root_hashes"
        raise ValueError(msg)

    ah = manifest.get("artifact_hashes")
    if not isinstance(ah, dict):
        msg = f"{mp}: artifact_hashes must be an object"
        raise ValueError(msg)

    for fn in sorted(ah.keys()):
        p = bundle_dir / fn
        if not p.is_file():
            msg = f"{bundle_dir}: artifact_hashes references missing file {fn!r}"
            raise ValueError(msg)
        obj = load_json_object(p)
        computed = sha256_hex_of_canonical_json(obj)
        expected = ah[fn]
        if not isinstance(expected, str) or computed != expected:
            msg = f"{bundle_dir}: hash mismatch for {fn!r} (manifest vs disk canonical JSON)"
            raise ValueError(msg)

    return manifest, lineage, contents


def _check_optional_intake(bundle_dir: Path) -> None:
    p = bundle_dir / "replay_intake_receipt.json"
    if not p.is_file():
        return
    receipt = load_json_object(p)
    status = receipt.get("intake_status")
    if isinstance(status, str) and status in UNSAFE_INTAKE_STATUSES:
        msg = f"{p}: intake_status {status!r} is not allowed for dataset inclusion"
        raise ValueError(msg)


def build_replay_training_dataset_artifacts(
    *,
    bundle_dirs: list[Path],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load one or more M14 bundle directories; emit dataset + report dicts."""

    if not bundle_dirs:
        msg = "at least one --bundle directory is required"
        raise ValueError(msg)

    sorted_dirs = sorted(bundle_dirs, key=lambda p: str(p.resolve()))
    warnings: list[str] = []
    bundle_ids_seen: set[str] = set()
    lineage_roots: list[str] = []
    examples: list[dict[str, Any]] = []

    for bundle_dir in sorted_dirs:
        manifest, _lineage, _contents = _validate_m14_bundle_directory(bundle_dir)
        _check_optional_intake(bundle_dir)

        intake_path = bundle_dir / "replay_intake_receipt.json"
        if not intake_path.is_file():
            warnings.append("intake_provenance_absent")

        bundle_id = str(manifest["bundle_id"])
        if bundle_id in bundle_ids_seen:
            msg = f"duplicate bundle_id across inputs: {bundle_id}"
            raise ValueError(msg)
        bundle_ids_seen.add(bundle_id)

        lr = str(manifest["lineage_root"])
        lineage_roots.append(lr)

        timeline = load_json_object(bundle_dir / "replay_timeline.json")
        entries = timeline.get("entries")
        if not isinstance(entries, list):
            msg = f"{bundle_dir / 'replay_timeline.json'}: entries must be a list"
            raise ValueError(msg)

        for entry in entries:
            if not isinstance(entry, dict):
                continue
            sk = entry.get("semantic_kind")
            ss = entry.get("source_stream")
            if not isinstance(sk, str) or not isinstance(ss, str):
                continue
            g = entry.get("gameloop")
            ti = entry.get("timeline_index")
            if not isinstance(g, int) or not isinstance(ti, int):
                continue
            ppi = _perspective_player_index(entry)
            if ppi is None:
                continue

            coarse = map_timeline_to_coarse_label(semantic_kind=sk, source_stream=ss)
            if coarse not in APPROVED_TARGET_SEMANTIC_KINDS:
                coarse = "other"

            example_id = f"starlab.m26.example.v1:{lr}:{bundle_id}:{ppi}:{g}:{ti}:{coarse}"
            split = split_mod100_from_example_id(example_id)

            source_timeline_ref: dict[str, Any] = {
                "gameloop": g,
                "semantic_kind_upstream": sk,
                "timeline_index": ti,
                "timeline_schema_version": str(timeline.get("schema_version", "")),
            }
            observation_request: dict[str, Any] = {
                "bundle_id": bundle_id,
                "gameloop": g,
                "lineage_root": lr,
                "perspective_player_index": ppi,
            }
            evidence_refs = [
                f"artifact:{bundle_id}:replay_timeline.json",
                f"bundle_manifest:{bundle_id}",
            ]

            examples.append(
                {
                    "bundle_id": bundle_id,
                    "evidence_refs": evidence_refs,
                    "example_id": example_id,
                    "gameloop": g,
                    "lineage_root": lr,
                    "observation_request": observation_request,
                    "perspective_player_index": ppi,
                    "source_timeline_ref": source_timeline_ref,
                    "split": split,
                    "target_semantic_kind": coarse,
                }
            )

    example_ids = [ex["example_id"] for ex in examples]
    if len(example_ids) != len(set(example_ids)):
        msg = "duplicate example_id in dataset (identity collision)"
        raise ValueError(msg)

    examples.sort(
        key=lambda e: (
            e["lineage_root"],
            e["bundle_id"],
            e["perspective_player_index"],
            e["gameloop"],
            e["source_timeline_ref"]["timeline_index"],
            e["target_semantic_kind"],
            e["example_id"],
        )
    )

    warnings_sorted = sorted(set(warnings))
    non_claims = sorted(NON_CLAIMS_V1)

    source_lineage_roots = sorted(set(lineage_roots))

    body_pre_hash: dict[str, Any] = {
        "dataset_version": REPLAY_TRAINING_DATASET_VERSION,
        "examples": examples,
        "label_policy_id": LABEL_POLICY_ID,
        "non_claims": non_claims,
        "selection_policy_id": SELECTION_POLICY_ID,
        "source_lineage_roots": source_lineage_roots,
        "split_policy_id": SPLIT_POLICY_ID,
        "warnings": warnings_sorted,
    }
    dataset_sha256 = sha256_hex_of_canonical_json(body_pre_hash)

    dataset: dict[str, Any] = {
        **body_pre_hash,
        "dataset_sha256": dataset_sha256,
    }

    split_counts: dict[str, int] = {}
    for ex in examples:
        sp = ex["split"]
        split_counts[sp] = split_counts.get(sp, 0) + 1
    split_counts_out = {k: split_counts[k] for k in sorted(split_counts.keys())}

    kind_counts: dict[str, int] = {}
    for ex in examples:
        tk = ex["target_semantic_kind"]
        kind_counts[tk] = kind_counts.get(tk, 0) + 1
    kind_counts_out = {k: kind_counts[k] for k in sorted(kind_counts.keys())}

    report: dict[str, Any] = {
        "dataset_sha256": dataset_sha256,
        "example_count": len(examples),
        "non_claims": list(non_claims),
        "report_version": REPLAY_TRAINING_DATASET_REPORT_VERSION,
        "source_bundle_count": len(bundle_ids_seen),
        "split_counts": split_counts_out,
        "target_semantic_kind_counts": kind_counts_out,
        "warnings": list(warnings_sorted),
    }

    return dataset, report
