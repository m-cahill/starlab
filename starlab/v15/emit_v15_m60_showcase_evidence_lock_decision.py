"""CLI: V15-M60 showcase-evidence lock vs continue/remediate decision emitter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.m60_showcase_evidence_lock_decision_io import (
    build_fixture_decision_body,
    load_and_validate_m59_path,
    validate_operator_declared_ack,
    write_decision_artifacts,
)
from starlab.v15.m60_showcase_evidence_lock_decision_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M60: emit showcase-evidence lock vs continue/remediate decision artifacts. "
            "Does not execute benchmarks, evaluate strength, promote checkpoints, or release."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(
            PROFILE_FIXTURE_CI,
            PROFILE_OPERATOR_PREFLIGHT,
            PROFILE_OPERATOR_DECLARED,
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m59-readout-json", type=Path, default=None)
    parser.add_argument(
        "--operator-declaration-json",
        type=Path,
        default=None,
        help="Required for operator_declared profile; acknowledgement JSON only.",
    )
    args = parser.parse_args(list(argv if argv is not None else sys.argv[1:]))

    out = args.output_dir.resolve()

    if args.profile == PROFILE_FIXTURE_CI:
        body = build_fixture_decision_body()
        write_decision_artifacts(out, body=body)
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        if args.m59_readout_json is None:
            sys.stderr.write("error: --m59-readout-json is required for operator_preflight\n")
            return 2
        ok, err = load_and_validate_m59_path(args.m59_readout_json.resolve())
        if not ok:
            sys.stderr.write(f"error: {err}\n")
            return 2
        blob = json.loads(args.m59_readout_json.resolve().read_text(encoding="utf-8"))
        m59_digest = sha256_hex_of_canonical_json(blob)
        body = build_fixture_decision_body()
        write_decision_artifacts(out, body=body, m59_digest=m59_digest)
        return 0

    assert args.profile == PROFILE_OPERATOR_DECLARED
    if args.operator_declaration_json is None:
        sys.stderr.write("error: --operator-declaration-json is required for operator_declared\n")
        return 2
    try:
        decl = json.loads(args.operator_declaration_json.resolve().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"error: could not load declaration JSON: {exc}\n")
        return 2
    if not isinstance(decl, dict):
        sys.stderr.write("error: declaration JSON root must be an object\n")
        return 2
    vd_ok, vd_err = validate_operator_declared_ack(decl)
    if not vd_ok:
        sys.stderr.write(f"error: {vd_err}\n")
        return 2
    body = build_fixture_decision_body()
    write_decision_artifacts(out, body=body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
