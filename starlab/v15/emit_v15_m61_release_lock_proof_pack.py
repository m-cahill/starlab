"""CLI: V15-M61 release-lock / showcase video proof-pack emitter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.m61_release_lock_proof_pack_io import (
    _m60_upstream_summary,
    build_fixture_capture_manifest_body,
    build_fixture_proof_pack_body,
    build_proof_pack_body,
    load_m60_path,
    validate_capture_manifest,
    write_m61_artifacts,
)
from starlab.v15.m61_release_lock_proof_pack_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    PROFILE_OPERATOR_RELEASE_LOCK,
    RELEASE_LOCK_STATUS_LOCKED,
    RELEASE_LOCK_STATUS_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M61: emit release-lock proof pack and showcase capture manifest artifacts. "
            "Does not execute benchmarks, evaluate strength, promote checkpoints, or run training."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(
            PROFILE_FIXTURE_CI,
            PROFILE_OPERATOR_PREFLIGHT,
            PROFILE_OPERATOR_DECLARED,
            PROFILE_OPERATOR_RELEASE_LOCK,
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--m60-lock-decision-json",
        type=Path,
        default=None,
        help="Required for operator profiles; validated M60 decision JSON.",
    )
    parser.add_argument(
        "--showcase-video-capture-manifest-json",
        type=Path,
        default=None,
        help="Required for operator profiles; capture manifest JSON.",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help=f"Required with --authorize-v15-release-lock for {PROFILE_OPERATOR_RELEASE_LOCK}.",
    )
    parser.add_argument(
        "--authorize-v15-release-lock",
        action="store_true",
        help=f"Required with --allow-operator-local-execution for {PROFILE_OPERATOR_RELEASE_LOCK}.",
    )
    args = parser.parse_args(list(argv if argv is not None else sys.argv[1:]))

    out = args.output_dir.resolve()

    if args.profile == PROFILE_FIXTURE_CI:
        body = build_fixture_proof_pack_body()
        cap = build_fixture_capture_manifest_body()
        write_m61_artifacts(
            out,
            body=body,
            capture_manifest=cap,
            emitter_profile=PROFILE_FIXTURE_CI,
        )
        return 0

    if args.m60_lock_decision_json is None:
        sys.stderr.write("error: --m60-lock-decision-json is required for operator profiles\n")
        return 2
    if args.showcase_video_capture_manifest_json is None:
        sys.stderr.write(
            "error: --showcase-video-capture-manifest-json is required for operator profiles\n",
        )
        return 2

    ok60, err60, m60 = load_m60_path(args.m60_lock_decision_json.resolve())
    if not ok60 or m60 is None:
        sys.stderr.write(f"error: invalid M60 decision: {err60}\n")
        return 2

    try:
        mraw = json.loads(
            args.showcase_video_capture_manifest_json.resolve().read_text(encoding="utf-8"),
        )
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"error: could not load capture manifest: {exc}\n")
        return 2
    if not isinstance(mraw, dict):
        sys.stderr.write("error: capture manifest root must be an object\n")
        return 2

    req_cap = args.profile != PROFILE_OPERATOR_PREFLIGHT
    vok, verr = validate_capture_manifest(mraw, require_operator_capture=req_cap)
    if not vok:
        sys.stderr.write(f"error: capture manifest invalid: {verr}\n")
        return 2

    if args.profile == PROFILE_OPERATOR_RELEASE_LOCK:
        if not (args.allow_operator_local_execution and args.authorize_v15_release_lock):
            sys.stderr.write(
                "error: operator_release_lock requires "
                "--allow-operator-local-execution and --authorize-v15-release-lock\n",
            )
            return 2

    m60_digest = sha256_hex_of_canonical_json(m60)
    manifest_digest = sha256_hex_of_canonical_json(mraw)

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        release_lock_executed = False
        lock_status = RELEASE_LOCK_STATUS_PREFLIGHT
    else:
        release_lock_executed = True
        lock_status = RELEASE_LOCK_STATUS_LOCKED

    body = build_proof_pack_body(
        upstream_m60=_m60_upstream_summary(m60),
        capture_manifest=mraw,
        release_lock_executed=release_lock_executed,
        release_lock_status=lock_status,
    )

    write_m61_artifacts(
        out,
        body=body,
        capture_manifest=mraw,
        emitter_profile=args.profile,
        m60_digest=m60_digest,
        manifest_digest=manifest_digest,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
