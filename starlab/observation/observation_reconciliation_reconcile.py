"""Row-level reconciliation helpers for observation vs canonical expectation (M19 / M35)."""

from __future__ import annotations

from typing import Any

from starlab.observation.observation_reconciliation_rules import (
    SCALAR_SEMANTIC_WHEN_MATCH as _SEM,
)
from starlab.observation.observation_reconciliation_rules import (
    ordered_action_family_names,
    ordered_scalar_names,
    scalar_paths_for_perspective,
)
from starlab.runs.json_util import canonical_json_dumps


def json_equal(a: Any, b: Any) -> bool:
    return canonical_json_dumps(a).strip() == canonical_json_dumps(b).strip()


def observation_scalar_map(obs: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    sf = obs.get("scalar_features") or {}
    entries = sf.get("ordered_entries") if isinstance(sf, dict) else None
    if not isinstance(entries, list):
        return out
    for e in entries:
        if isinstance(e, dict) and isinstance(e.get("name"), str):
            out[str(e["name"])] = e.get("value")
    return out


def reconcile_scalars(
    *,
    perspective_player_index: int,
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str], int]:
    """Return rows, warning lines (semantic bounded rows), mismatch count."""

    obs_map = observation_scalar_map(observed)
    exp_map = observation_scalar_map(expected)
    paths = scalar_paths_for_perspective(perspective_player_index)
    rows: list[dict[str, Any]] = []
    warn_lines: list[str] = []
    mismatches = 0

    for name in ordered_scalar_names():
        exp_val = exp_map.get(name)
        obs_val = obs_map.get(name)
        paths_s = paths.get(name, name)
        match = json_equal(obs_val, exp_val)

        if not match:
            rows.append(
                {
                    "observation_feature_name": name,
                    "canonical_source_paths": [paths_s],
                    "reconciliation_status": "mismatch",
                    "rationale": (
                        "Observation scalar value differs from M18 deterministic expectation "
                        "from canonical_state.json."
                    ),
                    "expected_value": exp_val,
                    "observed_value": obs_val,
                },
            )
            mismatches += 1
            continue

        sem = _SEM[name]
        if name == "visibility.proxy_level" and obs_val is None:
            sem_use: str = "unavailable_by_design"
            rationale = (
                "No visibility_proxy_level in canonical perspective player; observation null — "
                "proxy visibility not materialized (not fog-of-war truth)."
            )
        elif name == "visibility.proxy_level":
            sem_use = "bounded_lossy"
            rationale = (
                "Proxy visibility level from M16 visibility_context — bounded signal, not "
                "certified fog-of-war truth."
            )
        elif sem == "bounded_lossy":
            sem_use = "bounded_lossy"
            rationale = (
                "Replay-derived bounded summary or category signal — not exact banked resources "
                "or full semantic truth."
            )
        elif sem == "derived":
            sem_use = "derived"
            rationale = (
                "Deterministic aggregate: list length / count from canonical global_context."
            )
        else:
            sem_use = "exact"
            rationale = "Direct carry-through from canonical perspective player fields."

        rows.append(
            {
                "observation_feature_name": name,
                "canonical_source_paths": [paths_s],
                "reconciliation_status": sem_use,
                "rationale": rationale,
            },
        )
        if sem_use in ("bounded_lossy", "unavailable_by_design"):
            warn_lines.append(f"scalar:{name}:{sem_use}")

    return rows, sorted(warn_lines), mismatches


def reconcile_entities(
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    """Entity rows mirror observation order; compare to expected."""

    obs_rows = (observed.get("entity_rows") or {}).get("rows")
    exp_rows = (expected.get("entity_rows") or {}).get("rows")
    if not isinstance(obs_rows, list):
        obs_rows = []
    if not isinstance(exp_rows, list):
        exp_rows = []

    out: list[dict[str, Any]] = []
    mismatches = 0
    for i, orow in enumerate(obs_rows):
        e_row = exp_rows[i] if i < len(exp_rows) else None
        key = f"row_index={i}"
        if not isinstance(orow, dict):
            mismatches += 1
            out.append(
                {
                    "stable_key": key,
                    "reconciliation_status": "mismatch",
                    "rationale": "Entity row is not an object.",
                },
            )
            continue
        if e_row is None or not isinstance(e_row, dict):
            mismatches += 1
            out.append(
                {
                    "stable_key": key,
                    "observation_row": orow,
                    "reconciliation_status": "mismatch",
                    "rationale": (
                        "Unexpected extra entity row vs M18 expectation from canonical_state."
                    ),
                },
            )
            continue
        same = json_equal(orow, e_row)
        ov = orow.get("owner_view")
        rationale = (
            "Aggregated army category counts from canonical_state army_summary — "
            "faithful to M18 rules."
        )
        if same:
            status = "exact"
            if ov == "enemy":
                rationale = (
                    "Enemy aggregated categories emitted only for positive counts — omission when "
                    "zero is faithful to upstream."
                )
        else:
            status = "mismatch"
            mismatches += 1
            rationale = (
                "Entity row differs from M18 deterministic expectation from canonical_state."
            )
        row: dict[str, Any] = {
            "stable_key": key,
            "reconciliation_status": status,
            "rationale": rationale,
            "owner_view": ov,
            "category": orow.get("category"),
        }
        if status == "mismatch":
            row["expected_row"] = e_row
            row["observed_row"] = orow
        out.append(row)

    if len(exp_rows) > len(obs_rows):
        for j in range(len(obs_rows), len(exp_rows)):
            mismatches += 1
            out.append(
                {
                    "stable_key": f"row_index={j}",
                    "reconciliation_status": "mismatch",
                    "rationale": "Missing entity row vs M18 expectation from canonical_state.",
                    "expected_row": exp_rows[j],
                },
            )

    return out, mismatches


def reconcile_spatial(
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    obs_sp = observed.get("spatial_plane_family")
    exp_sp = expected.get("spatial_plane_family")
    same = json_equal(obs_sp, exp_sp)
    plane_id = None
    if isinstance(obs_sp, dict):
        planes = obs_sp.get("planes")
        if isinstance(planes, list) and planes and isinstance(planes[0], dict):
            plane_id = planes[0].get("plane_id")

    row = {
        "plane_family_key": str(plane_id or "spatial_plane_family"),
        "reconciliation_status": "bounded_lossy" if same else "mismatch",
        "rationale": (
            "M18 spatial planes are prototype structural metadata only — not map-grounded terrain "
            "or control truth."
            if same
            else (
                "Spatial plane family differs from M18 deterministic placeholder from "
                "canonical_state."
            )
        ),
    }
    return [row], 0 if same else 1


def reconcile_action_masks(
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    obs_fams = ((observed.get("action_mask_families") or {}).get("families")) or []
    exp_fams = ((expected.get("action_mask_families") or {}).get("families")) or []
    if not isinstance(obs_fams, list):
        obs_fams = []
    if not isinstance(exp_fams, list):
        exp_fams = []

    out: list[dict[str, Any]] = []
    mismatches = 0
    for i, name in enumerate(ordered_action_family_names()):
        o_f = obs_fams[i] if i < len(obs_fams) else None
        e_f = exp_fams[i] if i < len(exp_fams) else None
        same = isinstance(o_f, dict) and isinstance(e_f, dict) and json_equal(o_f, e_f)
        if same:
            status = "derived"
            rationale = (
                "Coarse prototype family mask from bounded M16 summaries — not legality or full "
                "action coverage."
            )
        else:
            status = "mismatch"
            mismatches += 1
            rationale = (
                "Action mask family differs from M18 heuristic expectation from canonical_state."
            )
        row: dict[str, Any] = {
            "family_name": name,
            "family_order_index": i,
            "reconciliation_status": status,
            "rationale": rationale,
        }
        if not same:
            row["expected_family"] = e_f
            row["observed_family"] = o_f
        out.append(row)
    return out, mismatches
