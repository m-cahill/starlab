"""CLI: V15-M56A operator-local watchability runner (stub / scaffold receipt only)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m51_live_candidate_watchability_harness_models import (
    real_candidate_live_policy_adapter_available,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    build_runner_refused_missing_adapter,
    build_runner_stub_scaffold_confirmation,
    sha256_file_hex,
    write_confirmation_artifacts,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    FLAG_SCAFFOLD_POLICY,
    FORBIDDEN_CLI_FLAGS,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_VISUAL,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    allow_local = GUARD_ALLOW_OPERATOR_LOCAL in argv_list
    authorize = GUARD_AUTHORIZE_VISUAL in argv_list
    allow_scaffold = FLAG_SCAFFOLD_POLICY in argv_list
    skip = set(FORBIDDEN_CLI_FLAGS) | {
        GUARD_ALLOW_OPERATOR_LOCAL,
        GUARD_AUTHORIZE_VISUAL,
        FLAG_SCAFFOLD_POLICY,
    }
    clean = [a for a in argv_list if a not in skip]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M56A: operator-local visual watchability runner. Without a real candidate-live "
            "adapter this entrypoint emits a refusal or a stub scaffold receipt only — it does "
            "not invoke live SC2 here. Use "
            "starlab.v15.run_v15_m51_live_candidate_watchability_harness "
            "for bounded live SC2 under M51 guards."
        ),
    )
    parser.add_argument("--m55-preflight-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--expected-m54-package-sha256",
        type=str,
        default=CANONICAL_M54_PACKAGE_SHA256,
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        sys.stderr.write(f"error: forbidden flags present: {', '.join(bad)}\n")
        return 2

    if not allow_local or not authorize:
        sys.stderr.write(
            f"error: requires {GUARD_ALLOW_OPERATOR_LOCAL} and {GUARD_AUTHORIZE_VISUAL}\n",
        )
        return 2

    exp54 = str(args.expected_m54_package_sha256).strip().lower()
    exp_ck = str(args.expected_candidate_sha256).strip().lower()
    if exp54 != CANONICAL_M54_PACKAGE_SHA256 or exp_ck != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        sys.stderr.write(
            "error: runner binds canonical M54 package and latest candidate SHA only.\n"
        )
        return 2

    m55_path = args.m55_preflight_json.resolve()
    m55_digest: str | None = None
    if m55_path.is_file():
        m55_digest = sha256_file_hex(m55_path)

    if real_candidate_live_policy_adapter_available():
        sys.stderr.write(
            "error: real_candidate_live_policy_adapter_available unexpectedly true; "
            "extend this runner to delegate safely before executing.\n",
        )
        return 2

    if not allow_scaffold:
        write_confirmation_artifacts(
            out,
            body_unsealed=build_runner_refused_missing_adapter(
                m55_preflight_sha256=m55_digest,
            ),
        )
        return 3

    write_confirmation_artifacts(
        out,
        body_unsealed=build_runner_stub_scaffold_confirmation(
            m55_preflight_sha256=m55_digest,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
