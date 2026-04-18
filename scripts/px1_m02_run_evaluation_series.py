"""PX1-M02: bounded live evaluation series driver (operator-local).

Runs frozen minimum matches per opponent profile, aggregates honest metrics,
writes evaluation_input JSON, emits px1_play_quality evidence artifacts, and
drafts operator markdown under the series root.

Does not modify protocol_input.json or frozen protocol semantics.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

STUB_WARNING = (
    "local_live_sc2: real replay not copied; emitted deterministic stub replay instead"
)

SCRIPTED = "px1_m02_opponent_scripted_style_v1"
HEURISTIC = "px1_m02_opponent_heuristic_style_v1"

MATCH_SCRIPTED = REPO_ROOT / "tests/fixtures/px1_m02/match_opponent_profile_scripted_style.json"
MATCH_HEURISTIC = REPO_ROOT / "tests/fixtures/px1_m02/match_opponent_profile_heuristic_style.json"
PROTOCOL_INPUT = REPO_ROOT / "tests/fixtures/px1_m02/protocol_input.json"

CANDIDATE_ID = "px1_m01_weighted_refit_rl_bootstrap_v1"


def _run_one(
    *,
    m43_run: Path,
    weights: Path,
    match_config: Path,
    out_dir: Path,
    optional_video: Path | None,
) -> int:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/px1_m02_local_validation_run.py"),
        "--hierarchical-training-run-dir",
        str(m43_run),
        "--weights",
        str(weights),
        "--match-config",
        str(match_config),
        "--output-dir",
        str(out_dir),
        "--runtime-mode",
        "local_live_sc2",
    ]
    if optional_video is not None:
        cmd.extend(["--optional-video", str(optional_video)])
    print("RUN:", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=str(REPO_ROOT))


def _parse_run(out_dir: Path) -> dict[str, Any]:
    run_json = out_dir / "local_live_play_validation_run.json"
    data = json.loads(run_json.read_text(encoding="utf-8"))
    me = data.get("match_execution") or {}
    result = str(me.get("sc2_game_result", ""))
    win = result.lower() == "victory"
    warnings = list(data.get("warnings") or [])
    stub = any(STUB_WARNING in str(w) for w in warnings)
    media = data.get("optional_media_registration")
    watchable = win and media is not None
    replay_backed = win and not stub
    return {
        "replay_backed_win": replay_backed,
        "result": result,
        "sc2_game_result": result,
        "stub_replay": stub,
        "watchable_win": watchable,
        "win": win,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--series-root",
        type=Path,
        default=REPO_ROOT
        / "out/training_campaigns/px1_m01_full_run_2026_04_17_a/px1_m02_eval_series",
        help="Root directory for protocol, runs, evidence, and operator notes",
    )
    ap.add_argument(
        "--matches-per-profile",
        type=int,
        default=5,
        help="Matches per opponent profile (frozen minimum is 5)",
    )
    ap.add_argument(
        "--optional-video",
        type=Path,
        default=None,
        help="If set, passed to the first winning run only (watchable evidence)",
    )
    args = ap.parse_args()

    series_root: Path = args.series_root
    protocol_dir = series_root / "protocol"
    runs_dir = series_root / "runs"
    evidence_dir = series_root / "evidence"

    _camp = "out/training_campaigns/px1_m01_full_run_2026_04_17_a"
    m43_run = REPO_ROOT / _camp / "referenced_artifacts/m43_materialization/m43_run"
    weights = (
        REPO_ROOT
        / _camp
        / "campaign_runs/px1_m01_exec_001/phases/optional_weighted_refit/updated_policy"
        / "rl_bootstrap_candidate_bundle.joblib"
    )

    if not m43_run.is_dir():
        sys.stderr.write(f"missing M43 run dir: {m43_run}\n")
        return 1
    if not weights.is_file():
        sys.stderr.write(f"missing refit weights: {weights}\n")
        return 1

    protocol_dir.mkdir(parents=True, exist_ok=True)
    runs_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: protocol artifacts
    cmd_proto = [
        sys.executable,
        "-m",
        "starlab.sc2.emit_px1_play_quality_protocol",
        "--input",
        str(PROTOCOL_INPUT),
        "--output-dir",
        str(protocol_dir),
    ]
    print("PROTO:", " ".join(cmd_proto), flush=True)
    if subprocess.call(cmd_proto, cwd=str(REPO_ROOT)) != 0:
        return 1

    n = int(args.matches_per_profile)
    per_prof: dict[str, list[dict[str, Any]]] = {SCRIPTED: [], HEURISTIC: []}

    video_used = False
    for i in range(n):
        od = runs_dir / f"scripted_{i:02d}"
        vid = None
        if args.optional_video and args.optional_video.is_file() and not video_used:
            # reserve optional video for first win if we can
            vid = args.optional_video
        rc = _run_one(
            match_config=MATCH_SCRIPTED,
            m43_run=m43_run,
            optional_video=vid,
            out_dir=od,
            weights=weights,
        )
        if rc != 0:
            sys.stderr.write(f"run failed scripted_{i:02d}\n")
            return rc
        pr = _parse_run(od)
        pr["run_dir"] = str(od)
        per_prof[SCRIPTED].append(pr)
        if vid and pr["win"]:
            video_used = True

    for i in range(n):
        od = runs_dir / f"heuristic_{i:02d}"
        vid = None
        if args.optional_video and args.optional_video.is_file() and not video_used:
            vid = args.optional_video
        rc = _run_one(
            match_config=MATCH_HEURISTIC,
            m43_run=m43_run,
            optional_video=vid,
            out_dir=od,
            weights=weights,
        )
        if rc != 0:
            sys.stderr.write(f"run failed heuristic_{i:02d}\n")
            return rc
        pr = _parse_run(od)
        pr["run_dir"] = str(od)
        per_prof[HEURISTIC].append(pr)
        if vid and pr["win"]:
            video_used = True

    # Aggregate
    def agg_profile(pid: str) -> dict[str, int]:
        rows = per_prof[pid]
        wins = sum(1 for r in rows if r["win"])
        rb = sum(1 for r in rows if r["replay_backed_win"])
        ww = sum(1 for r in rows if r["watchable_win"])
        return {
            "continuity_invalidations": 0,
            "matches_played": len(rows),
            "replay_backed_wins": rb,
            "watchable_wins": ww,
            "wins": wins,
        }

    a_scripted = agg_profile(SCRIPTED)
    a_heuristic = agg_profile(HEURISTIC)

    total_matches = a_scripted["matches_played"] + a_heuristic["matches_played"]
    total_wins = a_scripted["wins"] + a_heuristic["wins"]
    total_rb = a_scripted["replay_backed_wins"] + a_heuristic["replay_backed_wins"]
    total_ww = a_scripted["watchable_wins"] + a_heuristic["watchable_wins"]
    rate = (total_wins / total_matches) if total_matches else 0.0

    eval_body: dict[str, Any] = {
        "candidates_evaluated": [
            {
                "aggregate": {
                    "evidence_completeness": "complete",
                    "overall_win_rate": rate,
                    "overall_wins": total_wins,
                    "replay_backed_wins": total_rb,
                    "total_live_matches": total_matches,
                    "watchable_wins": total_ww,
                },
                "candidate_id": CANDIDATE_ID,
                "per_opponent_profile": {
                    HEURISTIC: a_heuristic,
                    SCRIPTED: a_scripted,
                },
            },
        ],
        "evaluation_series_id": "px1_m02_eval_series_local_2026_04_18",
        "required_runtime_mode_asserted": "local_live_sc2",
        "selection": {
            "rationale": "placeholder; replaced after threshold check",
            "status": "not_selected_within_scope",
        },
    }

    # Threshold check (mirror starlab.sc2.px1_play_quality_evidence logic)
    fp = json.loads((protocol_dir / "px1_play_quality_protocol.json").read_text(encoding="utf-8"))[
        "frozen_parameters"
    ]
    reasons: list[str] = []

    def chk(name: str, ok: bool, msg: str) -> None:
        if not ok:
            reasons.append(msg)

    chk(
        "matches_scripted",
        a_scripted["matches_played"] >= fp["minimum_matches_per_candidate_per_opponent_profile"],
        "scripted matches_played below minimum",
    )
    chk(
        "matches_heuristic",
        a_heuristic["matches_played"]
        >= fp["minimum_matches_per_candidate_per_opponent_profile"],
        "heuristic matches_played below minimum",
    )
    chk(
        "total",
        total_matches >= fp["minimum_total_live_matches_for_selected_candidate"],
        "total_live_matches below minimum",
    )
    chk(
        "wins",
        total_wins >= fp["minimum_selected_candidate_win_count"],
        "overall_wins below minimum",
    )
    chk(
        "rate",
        rate + 1e-9 >= float(fp["minimum_selected_candidate_overall_win_rate"]),
        "overall_win_rate below minimum",
    )
    chk(
        "rb",
        total_rb >= fp["minimum_replay_backed_wins_for_selected_candidate"],
        "replay_backed_wins below minimum",
    )
    chk(
        "ww",
        total_ww >= fp["minimum_watchable_wins_for_selected_candidate"],
        "watchable_wins below minimum",
    )

    thresholds_ok = not reasons
    if thresholds_ok:
        eval_body["selection"] = {
            "rationale": (
                "Aggregated local_live_sc2 series under frozen protocol; metrics satisfy "
                "frozen_parameters for px1_m01_weighted_refit_rl_bootstrap_v1."
            ),
            "selected_candidate_id": CANDIDATE_ID,
            "status": "candidate-selected",
        }
    else:
        eval_body["selection"] = {
            "rationale": "; ".join(reasons),
            "status": "not_selected_within_scope",
        }

    eval_path = evidence_dir / "px1_m02_evaluation_input.json"
    eval_path.write_text(json.dumps(eval_body, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    cmd_ev = [
        sys.executable,
        "-m",
        "starlab.sc2.emit_px1_play_quality_evidence",
        "--protocol",
        str(protocol_dir / "px1_play_quality_protocol.json"),
        "--evaluation-input",
        str(eval_path),
        "--output-dir",
        str(evidence_dir),
    ]
    print("EVIDENCE:", " ".join(cmd_ev), flush=True)
    if subprocess.call(cmd_ev, cwd=str(REPO_ROOT)) != 0:
        return 1

    # Operator notes (minimal; operator may expand)
    summary_path = series_root / "px1_play_quality_operator_note.md"
    stub_any = any(
        r.get("stub_replay")
        for plist in per_prof.values()
        for r in plist
    )
    summary_path.write_text(
        "\n".join(
            [
                "# PX1-M02 — operator note (auto-generated series summary)",
                "",
                f"- **Series root:** `{series_root}`",
                f"- **Protocol input:** `{PROTOCOL_INPUT}`",
                f"- **M43 run:** `{m43_run}`",
                f"- **Refit weights:** `{weights}`",
                f"- **Matches per profile:** {n} (scripted + heuristic)",
                f"- **Any stub replay warnings:** {stub_any}",
                f"- **Thresholds satisfied:** {thresholds_ok}",
                f"- **Selection (evidence JSON):** `{eval_body['selection']['status']}`",
                "",
                "Per-run JSON under `runs/`; protocol under `protocol/`; "
                "evidence under `evidence/`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    decl = series_root / "demo_candidate_selection_declaration.md"
    if thresholds_ok and eval_body["selection"]["status"] == "candidate-selected":
        decl_body = "candidate-selected"
    else:
        decl_body = "no-candidate-selected"
    decl.write_text(
        decl_body + "\n",
        encoding="utf-8",
    )

    print("DONE series_root=", series_root)
    print("evaluation_input=", eval_path)
    print("declaration_line=", decl_body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
