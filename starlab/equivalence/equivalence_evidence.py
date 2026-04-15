"""Deterministic replay↔execution equivalence evidence payloads (M53 — evidence only)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.equivalence.equivalence_charter import (
    build_replay_execution_equivalence_charter_artifact,
)
from starlab.equivalence.equivalence_models import (
    CHARTER_CONTRACT_ID,
    EVIDENCE_RUNTIME_CONTRACT_REL_PATH,
    PROFILE_IDENTITY_BINDING_V1,
    REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_REPORT_SCHEMA_VERSION,
    REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION,
)
from starlab.equivalence.equivalence_profiles import resolve_profile
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.runs.replay_binding import (
    compute_replay_binding_id,
    load_lineage_seed,
    load_replay_binding,
    load_run_identity,
)

_ARTIFACT_RUN_IDENTITY = "run_identity.json"
_ARTIFACT_LINEAGE_SEED = "lineage_seed.json"
_ARTIFACT_REPLAY_BINDING = "replay_binding.json"


def _posix_display(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.as_posix()


def _safe_load_run_identity(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        return load_run_identity(path), None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def _safe_load_lineage_seed(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        return load_lineage_seed(path), None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def _safe_load_replay_binding(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        return load_replay_binding(path), None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def _pair_string_entry(
    *,
    subject: str,
    left_val: str | None,
    right_val: str | None,
    left_artifact: str,
    right_artifact: str,
    left_path: Path | None,
    right_path: Path | None,
    field: str,
    missing_kind: str | None,
) -> dict[str, Any]:
    refs_l: list[dict[str, Any]] = []
    refs_r: list[dict[str, Any]] = []
    if left_path is not None and left_val is not None:
        refs_l.append(
            {
                "artifact": left_artifact,
                "path": _posix_display(left_path),
                "field": field,
                "value": left_val,
            }
        )
    if right_path is not None and right_val is not None:
        refs_r.append(
            {
                "artifact": right_artifact,
                "path": _posix_display(right_path),
                "field": field,
                "value": right_val,
            }
        )
    execution_refs = refs_l
    replay_refs = refs_r
    if missing_kind:
        return {
            "subject": subject,
            "comparison_mode": "exact_string_equality",
            "replay_artifact_refs": replay_refs,
            "execution_artifact_refs": execution_refs,
            "availability_class": "mismatch",
            "mismatch_kind": missing_kind,
            "notes": "Required artifact or field missing for governed join.",
        }
    agree = left_val == right_val
    if agree:
        return {
            "subject": subject,
            "comparison_mode": "exact_string_equality",
            "replay_artifact_refs": replay_refs,
            "execution_artifact_refs": execution_refs,
            "availability_class": "available",
            "mismatch_kind": None,
            "notes": "lineage_seed and replay_binding agree on lineage_seed_id.",
        }
    return {
        "subject": subject,
        "comparison_mode": "exact_string_equality",
        "replay_artifact_refs": replay_refs,
        "execution_artifact_refs": execution_refs,
        "availability_class": "mismatch",
        "mismatch_kind": "identity_mismatch",
        "notes": "lineage_seed_id differs between lineage_seed and replay_binding.",
    }


def _triple_string_entry(
    *,
    subject: str,
    ri_val: str | None,
    ls_val: str | None,
    rb_val: str | None,
    field: str,
    ri_path: Path | None,
    ls_path: Path | None,
    rb_path: Path | None,
    missing_kind: str | None,
) -> dict[str, Any]:
    refs_r: list[dict[str, Any]] = []
    refs_e: list[dict[str, Any]] = []
    if rb_path is not None and rb_val is not None:
        refs_r.append(
            {
                "artifact": _ARTIFACT_REPLAY_BINDING,
                "path": _posix_display(rb_path),
                "field": field,
                "value": rb_val,
            }
        )
    if ri_path is not None and ri_val is not None:
        refs_e.append(
            {
                "artifact": _ARTIFACT_RUN_IDENTITY,
                "path": _posix_display(ri_path),
                "field": field,
                "value": ri_val,
            }
        )
    if ls_path is not None and ls_val is not None:
        refs_e.append(
            {
                "artifact": _ARTIFACT_LINEAGE_SEED,
                "path": _posix_display(ls_path),
                "field": field,
                "value": ls_val,
            }
        )

    if missing_kind:
        return {
            "subject": subject,
            "comparison_mode": "exact_string_equality",
            "replay_artifact_refs": refs_r,
            "execution_artifact_refs": refs_e,
            "availability_class": "mismatch",
            "mismatch_kind": missing_kind,
            "notes": "Required artifact or field missing for governed join.",
        }

    agree = ri_val == ls_val == rb_val
    if agree:
        return {
            "subject": subject,
            "comparison_mode": "exact_string_equality",
            "replay_artifact_refs": refs_r,
            "execution_artifact_refs": refs_e,
            "availability_class": "available",
            "mismatch_kind": None,
            "notes": "All three artifacts agree on this join key.",
        }
    return {
        "subject": subject,
        "comparison_mode": "exact_string_equality",
        "replay_artifact_refs": refs_r,
        "execution_artifact_refs": refs_e,
        "availability_class": "mismatch",
        "mismatch_kind": "identity_mismatch",
        "notes": "Governed join key differs across M03/M04 artifacts.",
    }


def _binding_id_entry(
    *,
    rb: dict[str, Any] | None,
    rb_path: Path | None,
) -> dict[str, Any]:
    if rb is None or rb_path is None:
        return {
            "subject": "replay_binding.replay_binding_id",
            "comparison_mode": "recompute_starlab_replay_binding_id",
            "replay_artifact_refs": [],
            "execution_artifact_refs": [],
            "availability_class": "mismatch",
            "mismatch_kind": "missing_counterpart",
            "notes": "replay_binding.json not available for binding id check.",
        }
    expected = compute_replay_binding_id(
        execution_id=rb["execution_id"],
        lineage_seed_id=rb["lineage_seed_id"],
        proof_artifact_hash=rb["proof_artifact_hash"],
        replay_content_sha256=rb["replay_content_sha256"],
        run_spec_id=rb["run_spec_id"],
    )
    ok = expected == rb["replay_binding_id"]
    return {
        "subject": "replay_binding.replay_binding_id",
        "comparison_mode": "recompute_starlab_replay_binding_id",
        "replay_artifact_refs": [
            {
                "artifact": _ARTIFACT_REPLAY_BINDING,
                "path": _posix_display(rb_path),
                "field": "replay_binding_id",
                "value": rb["replay_binding_id"],
            }
        ],
        "execution_artifact_refs": [
            {
                "artifact": _ARTIFACT_REPLAY_BINDING,
                "path": _posix_display(rb_path),
                "field": "recomputed_replay_binding_id",
                "value": expected,
            }
        ],
        "availability_class": "available" if ok else "mismatch",
        "mismatch_kind": None if ok else "identity_mismatch",
        "notes": "Binding id must equal deterministic hash of M03 fields + replay_content_sha256.",
    }


def _parent_refs_entry(
    *,
    ls: dict[str, Any] | None,
    rb: dict[str, Any] | None,
    ls_path: Path | None,
    rb_path: Path | None,
) -> dict[str, Any]:
    if ls is None or rb is None or ls_path is None or rb_path is None:
        return {
            "subject": "parent_references.sequence_equality",
            "comparison_mode": "canonical_json_array_equality",
            "replay_artifact_refs": [
                {
                    "artifact": _ARTIFACT_REPLAY_BINDING,
                    "path": _posix_display(rb_path),
                    "field": "parent_references",
                    "value": rb.get("parent_references") if rb else None,
                }
            ],
            "execution_artifact_refs": [
                {
                    "artifact": _ARTIFACT_LINEAGE_SEED,
                    "path": _posix_display(ls_path),
                    "field": "parent_references",
                    "value": ls.get("parent_references") if ls else None,
                }
            ],
            "availability_class": "mismatch",
            "mismatch_kind": "missing_counterpart",
            "notes": (
                "Both lineage_seed and replay_binding are required for parent_references check."
            ),
        }
    a_ls = ls.get("parent_references")
    a_rb = rb.get("parent_references")
    ok = a_ls == a_rb
    kind: str | None = None
    if not ok:
        if not isinstance(a_ls, list) or not isinstance(a_rb, list):
            kind = "identity_mismatch"
        elif len(a_ls) != len(a_rb):
            kind = "count_mismatch"
        else:
            kind = "ordering_mismatch"
    return {
        "subject": "parent_references.sequence_equality",
        "comparison_mode": "canonical_json_array_equality",
        "replay_artifact_refs": [
            {
                "artifact": _ARTIFACT_REPLAY_BINDING,
                "path": _posix_display(rb_path),
                "field": "parent_references",
                "value": a_rb,
            }
        ],
        "execution_artifact_refs": [
            {
                "artifact": _ARTIFACT_LINEAGE_SEED,
                "path": _posix_display(ls_path),
                "field": "parent_references",
                "value": a_ls,
            }
        ],
        "availability_class": "available" if ok else "mismatch",
        "mismatch_kind": kind,
        "notes": "Empty parent lists must match; ordering is significant for this entry.",
    }


def _replay_hash_entry(*, rb: dict[str, Any] | None, rb_path: Path | None) -> dict[str, Any]:
    if rb is None or rb_path is None:
        return {
            "subject": "replay.replay_content_sha256",
            "comparison_mode": "replay_side_only_opaque_hash",
            "replay_artifact_refs": [],
            "execution_artifact_refs": [],
            "availability_class": "mismatch",
            "mismatch_kind": "missing_counterpart",
            "notes": "replay_binding.json missing; cannot record opaque replay hash.",
        }
    return {
        "subject": "replay.replay_content_sha256",
        "comparison_mode": "replay_side_only_opaque_hash",
        "replay_artifact_refs": [
            {
                "artifact": _ARTIFACT_REPLAY_BINDING,
                "path": _posix_display(rb_path),
                "field": "replay_content_sha256",
                "value": rb["replay_content_sha256"],
            }
        ],
        "execution_artifact_refs": [],
        "availability_class": "unavailable_by_design",
        "mismatch_kind": None,
        "notes": (
            "M03 run_identity / lineage_seed do not record replay bytes; replay_content_sha256 "
            "is replay-side authoritative per M04 (opaque bytes; not a semantic parse claim)."
        ),
    }


def _schema_entry(
    *,
    artifact: str,
    path: Path | None,
    expected: str,
    actual: str | None,
) -> dict[str, Any]:
    if path is None or actual is None:
        return {
            "subject": f"schema.{artifact}",
            "comparison_mode": "schema_version_token_equality",
            "replay_artifact_refs": [],
            "execution_artifact_refs": [],
            "availability_class": "mismatch",
            "mismatch_kind": "missing_counterpart",
            "notes": f"Expected schema_version {expected!r}; artifact missing.",
        }
    ok = actual == expected
    side = (
        "replay_artifact_refs"
        if artifact == _ARTIFACT_REPLAY_BINDING
        else "execution_artifact_refs"
    )
    ref = {
        "artifact": artifact,
        "path": _posix_display(path),
        "field": "schema_version",
        "value": actual,
    }
    row: dict[str, Any] = {
        "subject": f"schema.{artifact}",
        "comparison_mode": "schema_version_token_equality",
        "replay_artifact_refs": [ref] if side == "replay_artifact_refs" else [],
        "execution_artifact_refs": [ref] if side == "execution_artifact_refs" else [],
        "availability_class": "available" if ok else "mismatch",
        "mismatch_kind": None if ok else "identity_mismatch",
        "notes": "Profile requires a specific governed schema_version token.",
    }
    return row


def _config_hash_entry(
    *,
    ri: dict[str, Any] | None,
    ls: dict[str, Any] | None,
    ri_path: Path | None,
    ls_path: Path | None,
) -> dict[str, Any]:
    if ri is None or ls is None or ri_path is None or ls_path is None:
        return {
            "subject": "join.config_hash",
            "comparison_mode": "exact_string_equality",
            "replay_artifact_refs": [],
            "execution_artifact_refs": [],
            "availability_class": "mismatch",
            "mismatch_kind": "missing_counterpart",
            "notes": "run_identity and lineage_seed required for config_hash agreement check.",
        }
    a = ri.get("config_hash")
    b = ls.get("config_hash")
    ok = isinstance(a, str) and isinstance(b, str) and a == b
    return {
        "subject": "join.config_hash",
        "comparison_mode": "exact_string_equality",
        "replay_artifact_refs": [],
        "execution_artifact_refs": [
            {
                "artifact": _ARTIFACT_RUN_IDENTITY,
                "path": _posix_display(ri_path),
                "field": "config_hash",
                "value": a,
            },
            {
                "artifact": _ARTIFACT_LINEAGE_SEED,
                "path": _posix_display(ls_path),
                "field": "config_hash",
                "value": b,
            },
        ],
        "availability_class": "available" if ok else "mismatch",
        "mismatch_kind": None if ok else "identity_mismatch",
        "notes": "config_hash must agree between run_identity and lineage_seed for a single run.",
    }


def _sort_evidence_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(entries, key=lambda e: e["subject"])


def _summarize_mismatches(entries: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in entries:
        mk = e.get("mismatch_kind")
        if mk:
            out[mk] = out.get(mk, 0) + 1
    return dict(sorted(out.items()))


def _summarize_availability(entries: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in entries:
        ac = str(e.get("availability_class", "unknown"))
        out[ac] = out.get(ac, 0) + 1
    return dict(sorted(out.items()))


def build_identity_binding_evidence(
    *,
    run_identity_path: Path | None,
    lineage_seed_path: Path | None,
    replay_binding_path: Path | None,
) -> dict[str, Any]:
    """Emit evidence object for ``starlab.m53.profile.identity_binding_v1``."""

    spec = resolve_profile(PROFILE_IDENTITY_BINDING_V1)
    ri, _err_ri = _safe_load_run_identity(run_identity_path)
    ls, _err_ls = _safe_load_lineage_seed(lineage_seed_path)
    rb, _err_rb = _safe_load_replay_binding(replay_binding_path)

    entries: list[dict[str, Any]] = []

    entries.append(
        _schema_entry(
            artifact=_ARTIFACT_RUN_IDENTITY,
            path=run_identity_path,
            expected="starlab.run_identity.v1",
            actual=ri.get("schema_version") if ri else None,
        )
    )
    entries.append(
        _schema_entry(
            artifact=_ARTIFACT_LINEAGE_SEED,
            path=lineage_seed_path,
            expected="starlab.lineage_seed.v1",
            actual=ls.get("schema_version") if ls else None,
        )
    )
    entries.append(
        _schema_entry(
            artifact=_ARTIFACT_REPLAY_BINDING,
            path=replay_binding_path,
            expected="starlab.replay_binding.v1",
            actual=rb.get("schema_version") if rb else None,
        )
    )

    missing_join: str | None = None
    if ri is None or ls is None or rb is None:
        missing_join = "missing_counterpart"

    entries.append(
        _triple_string_entry(
            subject="join.run_spec_id",
            field="run_spec_id",
            ri_val=ri.get("run_spec_id") if ri else None,
            ls_val=ls.get("run_spec_id") if ls else None,
            rb_val=rb.get("run_spec_id") if rb else None,
            ri_path=run_identity_path,
            ls_path=lineage_seed_path,
            rb_path=replay_binding_path,
            missing_kind=missing_join,
        )
    )
    entries.append(
        _triple_string_entry(
            subject="join.execution_id",
            field="execution_id",
            ri_val=ri.get("execution_id") if ri else None,
            ls_val=ls.get("execution_id") if ls else None,
            rb_val=rb.get("execution_id") if rb else None,
            ri_path=run_identity_path,
            ls_path=lineage_seed_path,
            rb_path=replay_binding_path,
            missing_kind=missing_join,
        )
    )
    entries.append(
        _triple_string_entry(
            subject="join.proof_artifact_hash",
            field="proof_artifact_hash",
            ri_val=ri.get("proof_artifact_hash") if ri else None,
            ls_val=ls.get("proof_artifact_hash") if ls else None,
            rb_val=rb.get("proof_artifact_hash") if rb else None,
            ri_path=run_identity_path,
            ls_path=lineage_seed_path,
            rb_path=replay_binding_path,
            missing_kind=missing_join,
        )
    )
    entries.append(
        _pair_string_entry(
            subject="join.lineage_seed_id",
            field="lineage_seed_id",
            left_val=ls.get("lineage_seed_id") if ls else None,
            right_val=rb.get("lineage_seed_id") if rb else None,
            left_artifact=_ARTIFACT_LINEAGE_SEED,
            right_artifact=_ARTIFACT_REPLAY_BINDING,
            left_path=lineage_seed_path,
            right_path=replay_binding_path,
            missing_kind=missing_join,
        )
    )

    entries.append(
        _config_hash_entry(ri=ri, ls=ls, ri_path=run_identity_path, ls_path=lineage_seed_path)
    )
    entries.append(_binding_id_entry(rb=rb, rb_path=replay_binding_path))
    entries.append(
        _parent_refs_entry(ls=ls, rb=rb, ls_path=lineage_seed_path, rb_path=replay_binding_path)
    )
    entries.append(_replay_hash_entry(rb=rb, rb_path=replay_binding_path))
    entries.append(
        {
            "subject": "profile.excluded_gameplay_and_replay_parser_semantics",
            "comparison_mode": "not_compared",
            "replay_artifact_refs": [],
            "execution_artifact_refs": [],
            "availability_class": "out_of_scope",
            "mismatch_kind": None,
            "notes": (
                "Replay parse planes, timelines, BOE, combat, and canonical state are outside "
                "identity_binding_v1 (see M52 charter non-claims)."
            ),
        }
    )

    entries_sorted = _sort_evidence_entries(entries)

    charter_obj = build_replay_execution_equivalence_charter_artifact()
    charter_sha = sha256_hex_of_canonical_json(charter_obj)

    return {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION,
        "milestone": "M53",
        "charter_contract_id": CHARTER_CONTRACT_ID,
        "charter_artifact_sha256": charter_sha,
        "profile_id": spec.profile_id,
        "profile_version": spec.profile_version,
        "runtime_contract": EVIDENCE_RUNTIME_CONTRACT_REL_PATH,
        "bounded_claim": spec.bounded_claim,
        "pairing_inputs": {
            "mode": "explicit_artifact_paths",
            "run_identity_path": _posix_display(run_identity_path),
            "lineage_seed_path": _posix_display(lineage_seed_path),
            "replay_binding_path": _posix_display(replay_binding_path),
        },
        "replay_artifact_refs": [
            {
                "role": "m04_replay_binding",
                "path": _posix_display(replay_binding_path),
                "replay_binding_id": rb.get("replay_binding_id") if rb else None,
            }
        ],
        "execution_artifact_refs": [
            {
                "role": "m03_run_identity",
                "path": _posix_display(run_identity_path),
                "execution_id": ri.get("execution_id") if ri else None,
            },
            {
                "role": "m03_lineage_seed",
                "path": _posix_display(lineage_seed_path),
                "lineage_seed_id": ls.get("lineage_seed_id") if ls else None,
            },
        ],
        "join_key_projection": {
            "primary_join_keys": [
                "execution_id",
                "lineage_seed_id",
                "proof_artifact_hash",
                "run_spec_id",
            ],
            "sort_order": "lexicographic_utf8_by_evidence_subject",
        },
        "evidence_entries": entries_sorted,
        "availability_summary": _summarize_availability(entries_sorted),
        "mismatch_summary": _summarize_mismatches(entries_sorted),
        "non_claims": [
            spec.non_claims,
            "Does not assert replay↔execution equivalence beyond this bounded profile.",
            "Does not implement M54 audit gates or merge-bar semantics.",
            "Does not assert benchmark integrity, live SC2 in CI, or ladder/public performance.",
        ],
    }


def build_replay_execution_equivalence_evidence_report(
    *, evidence_obj: dict[str, Any]
) -> dict[str, Any]:
    ev_sha = sha256_hex_of_canonical_json(evidence_obj)
    spec = resolve_profile(str(evidence_obj["profile_id"]))
    return {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_REPORT_SCHEMA_VERSION,
        "milestone": "M53",
        "evidence_canonical_sha256": ev_sha,
        "evidence_artifact": "replay_execution_equivalence_evidence.json",
        "report_artifact": "replay_execution_equivalence_evidence_report.json",
        "emitter_module": "starlab.equivalence.emit_replay_execution_equivalence_evidence",
        "profile_id": evidence_obj["profile_id"],
        "profile_version": evidence_obj["profile_version"],
        "charter_contract_id": evidence_obj["charter_contract_id"],
        "bounded_claim": spec.bounded_claim,
        "availability_summary": evidence_obj["availability_summary"],
        "mismatch_summary": evidence_obj["mismatch_summary"],
        "non_claims": evidence_obj["non_claims"],
        "status": "evidence_only",
        "notes": (
            "Human-oriented deterministic report mirror of the evidence JSON. "
            "Not an audit pass/fail gate (M54)."
        ),
    }


def replay_execution_equivalence_evidence_bundle_for_profile(
    *,
    profile_id: str,
    run_identity_path: Path | None,
    lineage_seed_path: Path | None,
    replay_binding_path: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if profile_id != PROFILE_IDENTITY_BINDING_V1:
        msg = f"profile not implemented: {profile_id!r}"
        raise ValueError(msg)
    evidence = build_identity_binding_evidence(
        run_identity_path=run_identity_path,
        lineage_seed_path=lineage_seed_path,
        replay_binding_path=replay_binding_path,
    )
    report = build_replay_execution_equivalence_evidence_report(evidence_obj=evidence)
    return evidence, report
