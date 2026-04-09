"""Build observation reconciliation audit artifacts (M19)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.observation.observation_reconciliation_inputs import load_json_object
from starlab.observation.observation_reconciliation_rules import (
    SCALAR_SEMANTIC_WHEN_MATCH as _SEM,
)
from starlab.observation.observation_reconciliation_rules import (
    expected_observation_from_canonical,
    ordered_action_family_names,
    ordered_scalar_names,
    scalar_paths_for_perspective,
)
from starlab.observation.observation_surface_inputs import (
    canonical_state_sha256,
    provenance_report_matches_state,
)
from starlab.observation.observation_surface_schema import validate_observation_surface_frame
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

AUDIT_ARTIFACT_VERSION = "starlab.observation_reconciliation_audit.v1"
REPORT_ARTIFACT_VERSION = "starlab.observation_reconciliation_audit_report.v1"

AUDIT_FILENAME = "observation_reconciliation_audit.json"
REPORT_FILENAME = "observation_reconciliation_audit_report.json"

_DEFERRED_NON_CLAIMS: tuple[str, ...] = (
    (
        "Does not prove replay parsing, M14 bundle loading, or Blizzard parser-stack "
        "isolation beyond this audit boundary."
    ),
    "Does not prove action legality, benchmark integrity, or replay↔execution equivalence.",
    (
        "Does not certify fog-of-war truth or exact banked resources beyond prior bounded "
        "M11/M12/M16 claims."
    ),
    (
        "Spatial and action-mask rows classify prototype posture only — not map truth or "
        "legal actions."
    ),
)


def _json_equal(a: Any, b: Any) -> bool:
    return canonical_json_dumps(a).strip() == canonical_json_dumps(b).strip()


def _observation_scalar_map(obs: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    sf = obs.get("scalar_features") or {}
    entries = sf.get("ordered_entries") if isinstance(sf, dict) else None
    if not isinstance(entries, list):
        return out
    for e in entries:
        if isinstance(e, dict) and isinstance(e.get("name"), str):
            out[str(e["name"])] = e.get("value")
    return out


def _reconcile_scalars(
    *,
    perspective_player_index: int,
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str], int]:
    """Return rows, warning lines (semantic bounded rows), mismatch count."""

    obs_map = _observation_scalar_map(observed)
    exp_map = _observation_scalar_map(expected)
    paths = scalar_paths_for_perspective(perspective_player_index)
    rows: list[dict[str, Any]] = []
    warn_lines: list[str] = []
    mismatches = 0

    for name in ordered_scalar_names():
        exp_val = exp_map.get(name)
        obs_val = obs_map.get(name)
        paths_s = paths.get(name, name)
        match = _json_equal(obs_val, exp_val)

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


def _reconcile_entities(
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
        same = _json_equal(orow, e_row)
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


def _reconcile_spatial(
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    obs_sp = observed.get("spatial_plane_family")
    exp_sp = expected.get("spatial_plane_family")
    same = _json_equal(obs_sp, exp_sp)
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


def _reconcile_action_masks(
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
        same = isinstance(o_f, dict) and isinstance(e_f, dict) and _json_equal(o_f, e_f)
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


def build_reconciliation_artifacts(
    *,
    canonical_state: dict[str, Any],
    observation_surface: dict[str, Any],
    canonical_state_report: dict[str, Any] | None,
    observation_surface_report: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(audit_json, report_json)``.

    Raises ``ValueError`` on schema validation failure. Identity/provenance failures are recorded
    in the report (``audit_verdict`` ``fail``) rather than raised when inputs parse.
    """

    failures: list[str] = []

    obs_errs = validate_observation_surface_frame(observation_surface)
    if obs_errs:
        msg = "observation_surface failed schema validation: " + "; ".join(obs_errs)
        raise ValueError(msg)

    meta = observation_surface.get("metadata")
    if not isinstance(meta, dict):
        msg = "observation_surface.metadata missing or not an object"
        raise ValueError(msg)

    gameloop_o = meta.get("gameloop")
    perspective = meta.get("perspective_player_index")
    src_sha_obs = meta.get("source_canonical_state_sha256")

    if not isinstance(gameloop_o, int):
        msg = "observation metadata.gameloop must be an integer"
        raise ValueError(msg)
    if not isinstance(perspective, int):
        msg = "observation metadata.perspective_player_index must be an integer"
        raise ValueError(msg)
    if not isinstance(src_sha_obs, str) or len(src_sha_obs) != 64:
        msg = "observation metadata.source_canonical_state_sha256 must be a 64-char hex string"
        raise ValueError(msg)

    gameloop_c = canonical_state.get("gameloop")
    if not isinstance(gameloop_c, int):
        msg = "canonical_state.gameloop must be an integer"
        raise ValueError(msg)
    if gameloop_c != gameloop_o:
        failures.append(
            f"gameloop mismatch: canonical_state={gameloop_c} observation_metadata={gameloop_o}",
        )

    state_sha = canonical_state_sha256(canonical_state)
    if state_sha.lower() != src_sha_obs.lower():
        failures.append(
            "source_canonical_state_sha256 mismatch: recomputed from canonical_state.json vs "
            "observation metadata",
        )

    if canonical_state_report is not None:
        rep_err = provenance_report_matches_state(
            state=canonical_state,
            report=canonical_state_report,
        )
        if rep_err:
            failures.append(rep_err)

    if observation_surface_report is not None:
        osr = observation_surface_report
        obs_sha = sha256_hex_of_canonical_json(observation_surface)
        reported_obs = osr.get("observation_surface_sha256")
        if isinstance(reported_obs, str) and len(reported_obs) == 64:
            if reported_obs.lower() != obs_sha.lower():
                failures.append(
                    "observation_surface_report.json: observation_surface_sha256 does not match "
                    "loaded observation_surface.json",
                )
        reported_src = osr.get("source_canonical_state_sha256")
        if isinstance(reported_src, str) and len(reported_src) == 64:
            if reported_src.lower() != state_sha.lower():
                failures.append(
                    "observation_surface_report.json: source_canonical_state_sha256 does not "
                    "match recomputed canonical state hash",
                )
        gl_r = osr.get("gameloop")
        if isinstance(gl_r, int) and gl_r != gameloop_o:
            failures.append(
                "observation_surface_report gameloop mismatch: "
                f"report={gl_r} observation={gameloop_o}",
            )
        pp_r = osr.get("perspective_player_index")
        if isinstance(pp_r, int) and pp_r != perspective:
            failures.append(
                "observation_surface_report perspective_player_index mismatch vs "
                "observation metadata",
            )

    upstream_warnings: list[str] = []
    if canonical_state_report is not None:
        w = canonical_state_report.get("warnings")
        if isinstance(w, list):
            for x in w:
                if isinstance(x, str):
                    upstream_warnings.append(f"canonical_state_report:{x}")
    if observation_surface_report is not None:
        w = observation_surface_report.get("warnings")
        if isinstance(w, list):
            for x in w:
                if isinstance(x, str):
                    upstream_warnings.append(f"observation_surface_report:{x}")
    upstream_warnings = sorted(set(upstream_warnings))

    if failures:
        report: dict[str, Any] = {
            "report_version": REPORT_ARTIFACT_VERSION,
            "audit_verdict": "fail",
            "failures": sorted(failures),
            "warnings": [],
            "upstream_warnings": upstream_warnings,
            "summary": "Hard identity or provenance check failed before representation audit.",
        }
        audit: dict[str, Any] = {
            "audit_metadata": {
                "audit_artifact_version": AUDIT_ARTIFACT_VERSION,
                "contract": "starlab.observation_reconciliation_audit.v1",
            },
            "source_identity": {
                "gameloop_canonical": gameloop_c,
                "gameloop_observation": gameloop_o,
                "perspective_player_index": perspective,
                "source_canonical_state_sha256_computed": state_sha,
                "source_canonical_state_sha256_observation_metadata": src_sha_obs,
            },
            "scalar_audit_rows": [],
            "entity_audit_rows": [],
            "spatial_audit_rows": [],
            "action_mask_audit_rows": [],
            "status_counts": {},
            "deferred_non_claims": list(_DEFERRED_NON_CLAIMS),
        }
        return audit, report

    expected_frame, deriv_warnings = expected_observation_from_canonical(
        canonical_state,
        perspective_player_index=perspective,
        source_canonical_state_sha256=state_sha,
    )

    scalar_rows, scalar_warn, sc_mis = _reconcile_scalars(
        perspective_player_index=perspective,
        observed=observation_surface,
        expected=expected_frame,
    )
    ent_rows, ent_mis = _reconcile_entities(observation_surface, expected_frame)
    sp_rows, sp_mis = _reconcile_spatial(observation_surface, expected_frame)
    am_rows, am_mis = _reconcile_action_masks(observation_surface, expected_frame)

    total_mis = sc_mis + ent_mis + sp_mis + am_mis

    status_counts: dict[str, int] = {}
    for row in scalar_rows + ent_rows + sp_rows + am_rows:
        st = row.get("reconciliation_status")
        if isinstance(st, str):
            status_counts[st] = status_counts.get(st, 0) + 1

    warn_set = set(scalar_warn)
    for w in deriv_warnings:
        warn_set.add(f"derivation:{w}")
    warnings_sorted = sorted(warn_set)

    fail_rows: list[str] = []
    if total_mis > 0:
        for row in scalar_rows:
            if row.get("reconciliation_status") == "mismatch" and isinstance(
                row.get("observation_feature_name"),
                str,
            ):
                fail_rows.append(f"mismatch:scalar:{row['observation_feature_name']}")
        for row in ent_rows:
            if row.get("reconciliation_status") == "mismatch" and isinstance(
                row.get("stable_key"), str
            ):
                fail_rows.append(f"mismatch:entity:{row['stable_key']}")
        for row in sp_rows:
            if row.get("reconciliation_status") == "mismatch" and isinstance(
                row.get("plane_family_key"),
                str,
            ):
                fail_rows.append(f"mismatch:spatial:{row['plane_family_key']}")
        for row in am_rows:
            if row.get("reconciliation_status") == "mismatch" and isinstance(
                row.get("family_name"),
                str,
            ):
                fail_rows.append(f"mismatch:action_mask:{row['family_name']}")
        fail_rows.append(f"mismatch:total:{total_mis}")

    verdict = "pass"
    if fail_rows:
        verdict = "fail"
    elif warnings_sorted:
        verdict = "pass_with_warnings"

    summary = (
        "Representation audit: all audited mappings match M18 deterministic expectation from "
        "canonical_state."
        if verdict == "pass"
        else (
            (
                "Representation audit: bounded or unavailable-by-design semantics present "
                "(see warnings)."
            )
            if verdict == "pass_with_warnings"
            else "Representation audit failed: mismatches or provenance errors."
        )
    )

    audit = {
        "audit_metadata": {
            "audit_artifact_version": AUDIT_ARTIFACT_VERSION,
            "contract": "starlab.observation_reconciliation_audit.v1",
        },
        "source_identity": {
            "gameloop": gameloop_o,
            "perspective_player_index": perspective,
            "source_canonical_state_sha256": state_sha,
            "canonical_state_report_supplied": canonical_state_report is not None,
            "observation_surface_report_supplied": observation_surface_report is not None,
        },
        "scalar_audit_rows": scalar_rows,
        "entity_audit_rows": ent_rows,
        "spatial_audit_rows": sp_rows,
        "action_mask_audit_rows": am_rows,
        "status_counts": dict(sorted(status_counts.items())),
        "deferred_non_claims": list(_DEFERRED_NON_CLAIMS),
    }

    report = {
        "report_version": REPORT_ARTIFACT_VERSION,
        "audit_verdict": verdict,
        "failures": sorted(fail_rows),
        "warnings": warnings_sorted,
        "upstream_warnings": upstream_warnings,
        "summary": summary,
    }

    return audit, report


def emit_reconciliation_artifacts(
    *,
    canonical_state_path: Path,
    observation_surface_path: Path,
    output_dir: Path,
    canonical_state_report_path: Path | None = None,
    observation_surface_report_path: Path | None = None,
) -> tuple[Path, Path, str]:
    """Load inputs, run audit, write ``observation_reconciliation_audit.json`` + report.

    Returns ``(audit_path, report_path, audit_verdict)`` where ``audit_verdict`` is
    ``pass``, ``pass_with_warnings``, or ``fail``.
    """

    cs, err = load_json_object(canonical_state_path)
    if cs is None:
        msg = err or "failed to load canonical_state.json"
        raise ValueError(msg)
    obs, oerr = load_json_object(observation_surface_path)
    if obs is None:
        msg = oerr or "failed to load observation_surface.json"
        raise ValueError(msg)

    csr: dict[str, Any] | None = None
    if canonical_state_report_path is not None:
        csr, e2 = load_json_object(canonical_state_report_path)
        if csr is None:
            msg = e2 or "failed to load canonical_state_report.json"
            raise ValueError(msg)

    osr: dict[str, Any] | None = None
    if observation_surface_report_path is not None:
        osr, e3 = load_json_object(observation_surface_report_path)
        if osr is None:
            msg = e3 or "failed to load observation_surface_report.json"
            raise ValueError(msg)

    audit, report = build_reconciliation_artifacts(
        canonical_state=cs,
        observation_surface=obs,
        canonical_state_report=csr,
        observation_surface_report=osr,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    ap = output_dir / AUDIT_FILENAME
    rp = output_dir / REPORT_FILENAME
    ap.write_text(canonical_json_dumps(audit), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    verdict = report.get("audit_verdict")
    if not isinstance(verdict, str):
        msg = "internal error: audit report missing audit_verdict"
        raise ValueError(msg)
    return ap, rp, verdict
