"""Private helpers for replay slice identity and overlap logic (M13 / M35)."""

from __future__ import annotations

from typing import Any, Literal

from starlab.replays.combat_scouting_visibility_models import (
    COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION,
)
from starlab.replays.replay_slice_models import SLICE_KIND_COMBAT, SLICE_KIND_SCOUTING

RunStatus = Literal["completed", "extraction_failed", "lineage_failed", "source_contract_failed"]


def max_gameloop_from_timeline(timeline: dict[str, Any]) -> int:
    entries = timeline.get("entries")
    if not isinstance(entries, list) or not entries:
        return 0
    m = 0
    for e in entries:
        if not isinstance(e, dict):
            continue
        g = e.get("gameloop")
        if isinstance(g, int) and not isinstance(g, bool):
            m = max(m, g)
    return m


def validate_csv_contract(csv: dict[str, Any]) -> tuple[bool, str | None]:
    sv = csv.get("schema_version")
    if sv != COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION:
        return False, "unsupported or missing combat_scouting_visibility schema_version"
    cw = csv.get("combat_windows")
    so = csv.get("scouting_observations")
    vw = csv.get("visibility_windows")
    if not isinstance(cw, list) or not isinstance(so, list) or not isinstance(vw, list):
        return False, "combat_windows, scouting_observations, visibility_windows must be lists"
    return True, None


def hex_eq(a: str, b: str) -> bool:
    return a.lower() == b.lower()


def optional_report_hash_required(
    *,
    artifact_field: Any,
    report_path_provided: bool,
    label: str,
) -> tuple[bool, str | None]:
    if artifact_field is None:
        return True, None
    if not isinstance(artifact_field, str) or not artifact_field:
        return True, None
    if not report_path_provided:
        return False, f"{label} required when upstream embeds non-null report hash"
    return True, None


def slice_identity_payload_for_hash(
    *,
    slice_kind: str,
    start_gameloop: int,
    end_gameloop: int,
    anchor_gameloop: int,
    anchor_ref: dict[str, Any],
    subject_player_index: int | None,
    opponent_player_index: int | None,
    evidence_model: str | None,
) -> dict[str, Any]:
    """Stable semantic fields for slice_id only (excludes overlaps and overlap-derived tags)."""

    body: dict[str, Any] = {
        "anchor_gameloop": anchor_gameloop,
        "anchor_ref": anchor_ref,
        "end_gameloop": end_gameloop,
        "slice_kind": slice_kind,
        "start_gameloop": start_gameloop,
    }
    if evidence_model is not None:
        body["evidence_model"] = evidence_model
    if opponent_player_index is not None:
        body["opponent_player_index"] = opponent_player_index
    if subject_player_index is not None:
        body["subject_player_index"] = subject_player_index
    return body


def combat_window_id(window_index: int) -> str:
    return f"combat_window:{window_index}"


def scouting_observation_id(observation_index: int) -> str:
    return f"scouting_observation:{observation_index}"


def primary_anchor_id(
    *,
    slice_kind: str,
    window_index: int | None,
    observation_index: int | None,
) -> str:
    if slice_kind == SLICE_KIND_COMBAT and window_index is not None:
        return f"cw-{window_index}"
    if slice_kind == SLICE_KIND_SCOUTING and observation_index is not None:
        return f"so-{observation_index}"
    return "unknown"


def overlap_build_steps(
    *,
    steps: list[dict[str, Any]],
    start_gameloop: int,
    end_gameloop: int,
) -> list[str]:
    ids: list[str] = []
    for s in steps:
        if not isinstance(s, dict):
            continue
        si = s.get("step_index")
        gl = s.get("gameloop")
        if not isinstance(si, int) or isinstance(si, bool):
            continue
        if not isinstance(gl, int) or isinstance(gl, bool):
            continue
        if start_gameloop <= gl <= end_gameloop:
            ids.append(str(si))
    return sorted(set(ids))


def overlap_visibility_windows(
    *,
    visibility_windows: list[dict[str, Any]],
    start_gameloop: int,
    end_gameloop: int,
) -> tuple[list[str], bool, bool]:
    """Return (sorted window_index ids, has_proxy, has_explicit)."""

    ids: list[str] = []
    proxy = False
    explicit = False
    for w in visibility_windows:
        if not isinstance(w, dict):
            continue
        wi = w.get("window_index")
        sg = w.get("start_gameloop")
        eg = w.get("end_gameloop")
        if not isinstance(wi, int) or isinstance(wi, bool):
            continue
        if not isinstance(sg, int) or isinstance(sg, bool):
            continue
        if not isinstance(eg, int) or isinstance(eg, bool):
            continue
        if eg < start_gameloop or sg > end_gameloop:
            continue
        ids.append(str(wi))
        vm = w.get("visibility_model")
        if vm == "observation_proxy":
            proxy = True
        elif vm == "explicit_visibility":
            explicit = True
    ids_sorted = sorted(set(ids))
    return ids_sorted, proxy, explicit


def metadata_max_loops_optional(metadata: dict[str, Any] | None) -> int | None:
    if metadata is None:
        return None
    inner = metadata.get("metadata")
    if not isinstance(inner, dict):
        return None
    game = inner.get("game")
    if not isinstance(game, dict):
        return None
    gl = game.get("game_length_loops")
    if isinstance(gl, int) and not isinstance(gl, bool):
        return gl
    return None
