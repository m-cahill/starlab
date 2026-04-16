"""Build deterministic SC2 foundation v1 proof pack JSON + report (M61)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Final

from starlab.release_lock.release_lock_models import (
    CAMPAIGN_EVIDENCE_PROFILE_OPERATOR_LOCAL_V1,
    CAMPAIGN_LENGTH_OPERATOR_FULL_RUN,
    PROOF_PACK_CONTRACT_V1,
    PROOF_PACK_REPORT_CONTRACT_V1,
    RELEASE_SCOPE_SC2_FOUNDATION_V1,
    SC2_FOUNDATION_V1_DEFAULT_NON_CLAIMS,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

_INPUT_VERSION: Final[str] = "starlab.sc2_foundation_v1_proof_pack_input.v1"
_REQUIRED_INPUT_KEYS: Final[frozenset[str]] = frozenset(
    {
        "input_version",
        "release_scope_id",
        "proof_pack_profile_id",
        "foundation_track_refs",
        "campaign_evidence_paths",
        "campaign_threshold_declaration",
        "explicit_non_claims",
        "unresolved_gaps",
    }
)


def _resolve_path(raw: str, *, base_dir: Path) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    return (base_dir / p).resolve()


def _load_json(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object at {path}")
    return data


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _phase_receipt_by_name(
    receipts: object, name: str
) -> dict[str, Any] | None:
    if not isinstance(receipts, list):
        return None
    for rec in receipts:
        if isinstance(rec, dict) and rec.get("phase_name") == name:
            return rec
    return None


def _extract_m44_validation_fields(m44: dict[str, Any]) -> dict[str, Any]:
    me = m44.get("match_execution")
    fs: str | None = None
    sgr: str | None = None
    if isinstance(me, dict):
        fs = me.get("final_status") if isinstance(me.get("final_status"), str) else None
        sgr = me.get("sc2_game_result") if isinstance(me.get("sc2_game_result"), str) else None
    return {
        "final_status": fs,
        "sc2_game_result": sgr,
        "validation_run_version": m44.get("run_version"),
    }


def _normalize_foundation_refs(refs: object) -> list[dict[str, Any]]:
    if not isinstance(refs, list):
        raise ValueError("foundation_track_refs must be a list")
    out: list[dict[str, Any]] = []
    for r in refs:
        if not isinstance(r, dict):
            raise ValueError("each foundation_track_refs entry must be an object")
        tag = r.get("milestone_tag")
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("each foundation_track_refs entry requires milestone_tag (str)")
        entry: dict[str, Any] = {"milestone_tag": tag.strip()}
        for key in ("milestone_id", "merge_commit_sha", "pr_url", "notes"):
            v = r.get(key)
            if isinstance(v, str) and v.strip():
                entry[key] = v.strip()
        out.append(entry)
    out.sort(key=lambda x: x["milestone_tag"])
    return out


def _validate_threshold_declaration(decl: object) -> dict[str, Any]:
    if not isinstance(decl, dict):
        raise ValueError("campaign_threshold_declaration must be an object")
    need = (
        "campaign_length_class",
        "operator_defined_full_run_threshold",
        "threshold_satisfied",
        "operator_declared_at",
    )
    for k in need:
        if k not in decl:
            raise ValueError(f"campaign_threshold_declaration missing {k!r}")
    cl = decl["campaign_length_class"]
    if cl != CAMPAIGN_LENGTH_OPERATOR_FULL_RUN:
        raise ValueError(
            "M61 proof pack input requires campaign_length_class="
            f"{CAMPAIGN_LENGTH_OPERATOR_FULL_RUN!r} for release-lock alignment"
        )
    if decl.get("threshold_satisfied") is not True:
        raise ValueError(
            "M61 proof pack input requires campaign_threshold_declaration.threshold_satisfied"
            " == true"
        )
    return {k: decl[k] for k in need}


def validate_and_normalize_input(data: dict[str, Any]) -> dict[str, Any]:
    """Validate operator-authored proof-pack input; raises ValueError on contract violations."""

    missing = _REQUIRED_INPUT_KEYS.difference(data.keys())
    if missing:
        raise ValueError(f"proof pack input missing keys: {sorted(missing)}")
    if data.get("input_version") != _INPUT_VERSION:
        raise ValueError(f"input_version must be {_INPUT_VERSION!r}")
    if data.get("release_scope_id") != RELEASE_SCOPE_SC2_FOUNDATION_V1:
        raise ValueError(f"release_scope_id must be {RELEASE_SCOPE_SC2_FOUNDATION_V1!r}")
    if data.get("proof_pack_profile_id") != CAMPAIGN_EVIDENCE_PROFILE_OPERATOR_LOCAL_V1:
        raise ValueError(
            "proof_pack_profile_id must match the mandatory M61 operator-local campaign profile"
        )
    _validate_threshold_declaration(data["campaign_threshold_declaration"])
    if not isinstance(data.get("explicit_non_claims"), list):
        raise ValueError("explicit_non_claims must be a list of strings")
    for x in data["explicit_non_claims"]:
        if not isinstance(x, str):
            raise ValueError("explicit_non_claims must contain only strings")
    if not isinstance(data.get("unresolved_gaps"), list):
        raise ValueError("unresolved_gaps must be a list")
    return data


def build_sc2_foundation_v1_proof_pack(
    *,
    input_data: dict[str, Any],
    base_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load campaign artifacts from paths in input_data and emit proof pack + report."""

    normalized = validate_and_normalize_input(dict(input_data))
    paths_raw = normalized["campaign_evidence_paths"]
    if not isinstance(paths_raw, dict):
        raise ValueError("campaign_evidence_paths must be an object")

    required_path_keys = (
        "full_local_training_campaign_contract",
        "campaign_preflight_receipt",
        "hidden_rollout_campaign_run",
        "hidden_rollout_campaign_run_report",
        "bootstrap_run_report",
        "watchable_m44_local_live_play_validation_run",
        "replay_binding",
        "validation_replay_path",
    )
    for k in required_path_keys:
        if k not in paths_raw or not isinstance(paths_raw[k], str):
            raise ValueError(
                f"campaign_evidence_paths.{k} must be a non-empty string path relative to base"
                " or absolute"
            )

    resolved: dict[str, str] = {}
    for k, v in paths_raw.items():
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"campaign_evidence_paths.{k} must be a non-empty string")
        resolved[k] = str(_resolve_path(v.strip(), base_dir=base_dir))

    # Load and hash governed artifacts
    contract = _load_json(Path(resolved["full_local_training_campaign_contract"]))
    _ = _load_json(Path(resolved["campaign_preflight_receipt"]))
    campaign_run = _load_json(Path(resolved["hidden_rollout_campaign_run"]))
    campaign_run_rep = _load_json(Path(resolved["hidden_rollout_campaign_run_report"]))
    bootstrap_rep = _load_json(Path(resolved["bootstrap_run_report"]))
    m44 = _load_json(Path(resolved["watchable_m44_local_live_play_validation_run"]))
    replay_binding = _load_json(Path(resolved["replay_binding"]))

    replay_path = Path(resolved["validation_replay_path"])
    if not replay_path.is_file():
        raise ValueError(f"validation_replay_path must exist and be a file: {replay_path}")

    video_meta: dict[str, Any] | None = None
    video_path_key = paths_raw.get("video_metadata_path")
    if isinstance(video_path_key, str) and video_path_key.strip():
        vp = _resolve_path(video_path_key.strip(), base_dir=base_dir)
        if vp.is_file():
            video_meta = {"path": str(vp), "sha256": _file_sha256(vp)}
        else:
            raise ValueError(f"video_metadata_path not found: {vp}")

    watch_note: str | None = None
    wn_key = paths_raw.get("operator_watch_note_path")
    if isinstance(wn_key, str) and wn_key.strip():
        wnp = _resolve_path(wn_key.strip(), base_dir=base_dir)
        if wnp.is_file():
            watch_note = wnp.read_text(encoding="utf-8").strip()
        else:
            raise ValueError(f"operator_watch_note_path not found: {wnp}")

    receipts = campaign_run.get("phase_receipts")
    w44_rec = _phase_receipt_by_name(receipts, "watchable_m44_validation")
    post_boot = bool(campaign_run.get("post_bootstrap_protocol_phases_enabled"))
    exec_id = campaign_run.get("execution_id")
    camp_sha = campaign_run.get("campaign_sha256")
    rt_mode = m44.get("runtime_mode")

    campaign_run_derived: dict[str, Any] = {
        "campaign_id": contract.get("campaign_id"),
        "campaign_sha256": camp_sha,
        "execution_id": exec_id,
        "execution_status": campaign_run.get("execution_status"),
        "runtime_mode": rt_mode,
        "post_bootstrap_protocol_phases_enabled": post_boot,
        "completed_phase_names": sorted(
            {
                str(r.get("phase_name"))
                for r in (receipts if isinstance(receipts, list) else [])
                if isinstance(r, dict) and r.get("executed") is True
            }
        ),
        "watchable_m44_phase_executed": bool(w44_rec and w44_rec.get("executed") is True),
        "watchable_m44_phase_final_status": w44_rec.get("final_status")
        if isinstance(w44_rec, dict)
        else None,
    }
    edw = campaign_run.get("episode_distinctness_warnings")
    if isinstance(edw, list):
        campaign_run_derived["episode_distinctness_warnings"] = [str(x) for x in edw]
    else:
        campaign_run_derived["episode_distinctness_warnings"] = []
    wrn_list = campaign_run.get("warnings")
    if isinstance(wrn_list, list):
        campaign_run_derived["hidden_rollout_run_warnings"] = sorted(
            str(w) for w in wrn_list if isinstance(w, str)
        )
    else:
        campaign_run_derived["hidden_rollout_run_warnings"] = []

    watchable_summary = _extract_m44_validation_fields(m44)
    watchable_summary["replay_binding_sha256"] = replay_binding.get(
        "replay_content_sha256",
    ) or replay_binding.get("replay_sha256")

    artifact_integrity: dict[str, Any] = {
        "full_local_training_campaign_contract_sha256": _file_sha256(
            Path(resolved["full_local_training_campaign_contract"])
        ),
        "campaign_preflight_receipt_sha256": _file_sha256(
            Path(resolved["campaign_preflight_receipt"])
        ),
        "hidden_rollout_campaign_run_sha256": _file_sha256(
            Path(resolved["hidden_rollout_campaign_run"])
        ),
        "hidden_rollout_campaign_run_report_sha256": _file_sha256(
            Path(resolved["hidden_rollout_campaign_run_report"])
        ),
        "bootstrap_run_report_sha256": _file_sha256(Path(resolved["bootstrap_run_report"])),
        "watchable_m44_local_live_play_validation_run_sha256": _file_sha256(
            Path(resolved["watchable_m44_local_live_play_validation_run"])
        ),
        "replay_binding_sha256": _file_sha256(Path(resolved["replay_binding"])),
        "validation_replay_sha256": _file_sha256(replay_path),
    }

    explicit_nc = sorted({str(x) for x in normalized["explicit_non_claims"]})
    merged_non_claims = sorted(
        set(SC2_FOUNDATION_V1_DEFAULT_NON_CLAIMS).union(explicit_nc),
    )

    foundation_refs = _normalize_foundation_refs(normalized["foundation_track_refs"])

    proof_pack_body: dict[str, Any] = {
        "contract_id": PROOF_PACK_CONTRACT_V1,
        "release_scope_id": RELEASE_SCOPE_SC2_FOUNDATION_V1,
        "proof_pack_profile_id": CAMPAIGN_EVIDENCE_PROFILE_OPERATOR_LOCAL_V1,
        "foundation_track_refs": foundation_refs,
        "campaign_release_evidence": {
            "artifact_paths": {k: resolved[k] for k in sorted(resolved.keys())},
            "artifact_sha256": artifact_integrity,
            "campaign_run_derived": campaign_run_derived,
            "embedded_campaign_run_report_summary": campaign_run_rep.get("summary")
            if isinstance(campaign_run_rep.get("summary"), dict)
            else {"note": "missing_summary_in_report"},
            "bootstrap_run_report_campaign_id": bootstrap_rep.get("campaign_id"),
            "watchable_validation_summary": watchable_summary,
            "optional_video_metadata": video_meta,
            "optional_operator_watch_note_excerpt": (watch_note[:2000] if watch_note else None),
        },
        "watchable_validation_evidence": {
            "primary_proof_surface": "replay_backed_local_live_play_validation",
            "local_live_play_artifact": resolved["watchable_m44_local_live_play_validation_run"],
            "replay_binding": resolved["replay_binding"],
            "validation_replay": resolved["validation_replay_path"],
        },
        "campaign_threshold_declaration": dict(normalized["campaign_threshold_declaration"]),
        "unresolved_gaps": list(normalized["unresolved_gaps"]),
        "non_claims": merged_non_claims,
    }

    fixed_ts = normalized.get("emit_metadata")
    if isinstance(fixed_ts, dict) and isinstance(fixed_ts.get("fixed_timestamp_utc"), str):
        proof_pack_body["proof_pack_fixed_timestamp_utc"] = fixed_ts["fixed_timestamp_utc"]

    proof_pack_sha256 = sha256_hex_of_canonical_json(proof_pack_body)
    proof_pack_out = {**proof_pack_body, "proof_pack_sha256": proof_pack_sha256}

    report: dict[str, Any] = {
        "contract_id": PROOF_PACK_REPORT_CONTRACT_V1,
        "proof_pack_sha256": proof_pack_sha256,
        "referenced_inputs_ok": True,
        "summary": {
            "release_scope_id": RELEASE_SCOPE_SC2_FOUNDATION_V1,
            "campaign_execution_id": exec_id,
            "watchable_m44_executed": campaign_run_derived["watchable_m44_phase_executed"],
            "post_bootstrap_enabled": post_boot,
        },
    }

    return proof_pack_out, report


def write_sc2_foundation_v1_proof_pack_artifacts(
    *,
    input_path: Path,
    output_dir: Path,
    base_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Read JSON input from disk, write proof pack + report under output_dir."""

    raw = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("proof pack input must be a JSON object")
    root = base_dir if base_dir is not None else input_path.resolve().parent
    pack, rep = build_sc2_foundation_v1_proof_pack(input_data=raw, base_dir=root)
    output_dir.mkdir(parents=True, exist_ok=True)
    from starlab.release_lock.release_lock_models import (
        PROOF_PACK_FILENAME,
        PROOF_PACK_REPORT_FILENAME,
    )

    p1 = output_dir / PROOF_PACK_FILENAME
    p2 = output_dir / PROOF_PACK_REPORT_FILENAME
    p1.write_text(canonical_json_dumps(pack), encoding="utf-8")
    p2.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return p1, p2
