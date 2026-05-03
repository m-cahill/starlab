"""CLI: V15-M59 adapter smoke readout & benchmark overclaim refusal emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m59_adapter_smoke_readout_io import (
    build_fixture_readout_body,
    build_readout_body,
    validate_operator_evidence_inputs,
    write_readout_artifacts,
)
from starlab.v15.m59_adapter_smoke_readout_models import (
    EVIDENCE_SOURCE_OPERATOR_LOCAL,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_EVIDENCE,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M59: emit adapter smoke readout and benchmark overclaim refusal artifacts. "
            "Does not run SC2, benchmarks, or evaluation."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_EVIDENCE),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m58-status", type=str, default=None)
    parser.add_argument("--m58-acceptance-reason", type=str, default=None)
    parser.add_argument("--main-sha", type=str, default=None)
    parser.add_argument("--m58-artifact-sha256", type=str, default=None)
    args = parser.parse_args(list(argv if argv is not None else sys.argv[1:]))

    out = args.output_dir.resolve()

    if args.profile == PROFILE_FIXTURE_CI:
        write_readout_artifacts(out, body=build_fixture_readout_body())
        return 0

    ok, err = validate_operator_evidence_inputs(
        m58_status=args.m58_status,
        m58_acceptance_reason=args.m58_acceptance_reason,
        main_sha=args.main_sha,
        m58_artifact_sha256=args.m58_artifact_sha256,
    )
    if not ok:
        sys.stderr.write(f"error: {err}\n")
        return 2

    body = build_readout_body(
        m58_status=str(args.m58_status).strip().lower(),
        m58_acceptance_reason=str(args.m58_acceptance_reason).strip(),
        main_sha=str(args.main_sha).strip().lower(),
        m58_artifact_sha256=str(args.m58_artifact_sha256).strip().lower(),
        evidence_source=EVIDENCE_SOURCE_OPERATOR_LOCAL,
    )
    write_readout_artifacts(out, body=body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
