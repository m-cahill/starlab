"""CLI: governed V15-M51 operator-local watchability (dual-guard; optional Burny scaffold)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m51_live_candidate_watchability_harness_io import (
    M51LiveRunParams,
    emit_m51_forbidden_flag_refusal,
    run_m51_operator_local_watchability,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
    FLAG_SCAFFOLD_POLICY,
    FORBIDDEN_CLI_FLAGS,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_WATCHABILITY,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    allow_local = GUARD_ALLOW_OPERATOR_LOCAL in argv_list
    authorize = GUARD_AUTHORIZE_WATCHABILITY in argv_list
    skip = set(FORBIDDEN_CLI_FLAGS) | {GUARD_ALLOW_OPERATOR_LOCAL, GUARD_AUTHORIZE_WATCHABILITY}
    clean = [a for a in argv_list if a not in skip]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M51: optional operator-local live watchability. Requires dual guards. "
            "Does not authorize benchmark pass/fail, strength, promotion, 12-hour execution, v2, "
            "T2–T5, XAI, human-panel, or showcase. Scaffold is PX1/M27 watchability only."
        ),
    )
    parser.add_argument("--m50-readout-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sc2-root", type=Path, required=True)
    parser.add_argument("--map-path", type=Path, required=True)
    parser.add_argument("--game-step", type=int, default=8)
    parser.add_argument("--max-game-steps", type=int, default=4096)
    parser.add_argument("--save-replay", action="store_true")
    parser.add_argument("--video-path", type=Path, default=None)
    parser.add_argument("--operator-note", type=Path, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--expected-m50-readout-sha256", type=str, default=None)
    parser.add_argument("--candidate-checkpoint-path", type=Path, default=None)
    parser.add_argument("--expected-candidate-checkpoint-sha256", type=str, default=None)
    parser.add_argument("--m42-package-json", type=Path, default=None)
    parser.add_argument(FLAG_SCAFFOLD_POLICY, action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()

    if bad:
        emit_m51_forbidden_flag_refusal(
            out,
            emit_profile_short="operator_local_watchability_run",
            triggered_flags=bad,
        )
        return 0

    params = M51LiveRunParams(
        m50_path=args.m50_readout_json.resolve(),
        output_dir=out,
        sc2_root=args.sc2_root.resolve(),
        map_path=args.map_path.resolve(),
        game_step=int(args.game_step),
        max_game_steps=int(args.max_game_steps),
        save_replay=bool(args.save_replay),
        allow_scaffold=bool(args.allow_scaffold_watchability_policy),
        seed=int(args.seed),
        video_path=args.video_path.resolve() if args.video_path is not None else None,
        operator_note_path=args.operator_note.resolve() if args.operator_note is not None else None,
        run_id=args.run_id,
        expected_m50_sha256=str(args.expected_m50_readout_sha256).strip().lower()
        if args.expected_m50_readout_sha256
        else None,
        checkpoint_path=args.candidate_checkpoint_path.resolve()
        if args.candidate_checkpoint_path is not None
        else None,
        expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
        m42_path=args.m42_package_json.resolve() if args.m42_package_json is not None else None,
    )

    run_m51_operator_local_watchability(
        params,
        allow_local=allow_local,
        authorize_watchability=authorize,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
