"""CLI: emit V15-M61 showcase video capture manifest (hash-only binding)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m61_release_lock_proof_pack_io import (
    build_fixture_capture_manifest_body,
    declared_metadata_forbidden,
    sha256_file,
    validate_hex64,
)
from starlab.v15.m61_release_lock_proof_pack_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CAPTURE_STATUS_OPERATOR_CAPTURED,
    CONTRACT_ID_CAPTURE_MANIFEST,
    FILENAME_CAPTURE_MANIFEST_JSON,
    FIXTURE_PLACEHOLDER_SHA256,
    MILESTONE,
    SESSION_SOURCES_ALLOWED,
)


def _build_operator_manifest(
    *,
    candidate_sha: str,
    video_sha: str,
    replay_sha: str,
    capture_method: str,
    playback_speed: str,
    session_source: str,
    map_name: str,
    opponent: str,
    rel_video: str,
    rel_replay: str,
    duration_seconds: str,
    video_format: str,
) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID_CAPTURE_MANIFEST,
        "milestone": MILESTONE,
        "candidate_checkpoint_sha256": candidate_sha.lower().strip(),
        "capture_status": CAPTURE_STATUS_OPERATOR_CAPTURED,
        "capture_method": capture_method,
        "video_file": {
            "storage_posture": "operator_local_not_committed",
            "relative_or_redacted_path": rel_video,
            "sha256": video_sha,
            "duration_seconds": duration_seconds,
            "format": video_format,
        },
        "replay_file": {
            "storage_posture": "operator_local_not_committed",
            "relative_or_redacted_path": rel_replay,
            "sha256": replay_sha,
        },
        "sc2_context": {
            "map": map_name,
            "opponent_or_baseline": opponent,
            "session_source": session_source,
            "playback_speed": playback_speed,
            "slow_watchability_mode": True,
        },
        "non_claims": [
            "not_benchmark_execution",
            "not_benchmark_pass_fail",
            "not_strength_evaluation",
            "not_checkpoint_promotion",
            "not_ladder_claim",
            "not_human_panel_claim",
            "not_v2_authorization",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M61: build showcase_video_capture_manifest.json with file hashes. "
            "Does not commit raw media."
        ),
    )
    parser.add_argument(
        "--candidate-checkpoint-sha256",
        default=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    parser.add_argument("--video-file", type=Path, default=None)
    parser.add_argument("--replay-file", type=Path, default=None)
    parser.add_argument(
        "--capture-method",
        default="replay_playback_screen_recording",
    )
    parser.add_argument("--playback-speed", default="")
    parser.add_argument("--session-source", default="")
    parser.add_argument("--map", default="Waterfall")
    parser.add_argument("--opponent-or-baseline", default="declared_operator")
    parser.add_argument(
        "--relative-video-path",
        default="showcase_video/showcase.mp4",
        help="Redacted or repo-relative path string stored in manifest (not absolute).",
    )
    parser.add_argument(
        "--relative-replay-path",
        default="showcase_video/showcase.SC2Replay",
    )
    parser.add_argument("--duration-seconds", default="180")
    parser.add_argument("--video-format", default="mp4")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--fixture-only",
        action="store_true",
        help="Emit fixture_schema_only_no_video manifest (ignores file args).",
    )
    args = parser.parse_args(list(argv if argv is not None else sys.argv[1:]))

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    dest = out / FILENAME_CAPTURE_MANIFEST_JSON

    if args.fixture_only:
        body = build_fixture_capture_manifest_body()
        dest.write_text(canonical_json_dumps(body), encoding="utf-8")
        return 0

    vf = args.video_file
    rf = args.replay_file
    if (vf is None) ^ (rf is None):
        sys.stderr.write("error: pass both --video-file and --replay-file, or use --fixture-only\n")
        return 2

    if vf is None and rf is None:
        body = build_fixture_capture_manifest_body()
        dest.write_text(canonical_json_dumps(body), encoding="utf-8")
        return 0

    cand = str(args.candidate_checkpoint_sha256).lower().strip()
    if cand != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        sys.stderr.write("error: candidate_checkpoint_sha256 must match the v1.5 program anchor\n")
        return 2

    if not args.session_source:
        sys.stderr.write("error: --session-source is required for operator capture\n")
        return 2
    if str(args.session_source) not in SESSION_SOURCES_ALLOWED:
        sys.stderr.write("error: --session-source not in allowed operator vocabulary\n")
        return 2
    if not args.playback_speed:
        sys.stderr.write("error: --playback-speed is required for operator capture\n")
        return 2

    assert vf is not None and rf is not None
    try:
        v_sha = sha256_file(vf.resolve())
        r_sha = sha256_file(rf.resolve())
    except OSError as exc:
        sys.stderr.write(f"error: could not hash media: {exc}\n")
        return 2

    for label, h in (("video", v_sha), ("replay", r_sha)):
        ok, hex_err = validate_hex64(f"{label} hash", h)
        if not ok:
            sys.stderr.write(f"error: {hex_err}\n")
            return 2
        if h == FIXTURE_PLACEHOLDER_SHA256:
            sys.stderr.write("error: computed hash must not equal fixture placeholder\n")
            return 2

    body = _build_operator_manifest(
        candidate_sha=str(args.candidate_checkpoint_sha256),
        video_sha=v_sha,
        replay_sha=r_sha,
        capture_method=str(args.capture_method),
        playback_speed=str(args.playback_speed),
        session_source=str(args.session_source),
        map_name=str(args.map),
        opponent=str(args.opponent_or_baseline),
        rel_video=str(args.relative_video_path),
        rel_replay=str(args.relative_replay_path),
        duration_seconds=str(args.duration_seconds),
        video_format=str(args.video_format),
    )
    err = declared_metadata_forbidden(body)
    if err:
        sys.stderr.write(f"error: {err}\n")
        return 2

    dest.write_text(canonical_json_dumps(body), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
