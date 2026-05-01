"""CLI: V15-M52A dual-guarded candidate live adapter spike (watchability only)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m52_candidate_live_adapter_spike_io import (
    M52aAdapterRunParams,
    emit_m52a_forbidden_flag_refusal,
    run_m52a_operator_local_adapter_spike,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    FORBIDDEN_CLI_FLAGS,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_ADAPTER_SPIKE,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    allow_local = GUARD_ALLOW_OPERATOR_LOCAL in argv_list
    authorize = GUARD_AUTHORIZE_ADAPTER_SPIKE in argv_list
    skip = set(FORBIDDEN_CLI_FLAGS) | {GUARD_ALLOW_OPERATOR_LOCAL, GUARD_AUTHORIZE_ADAPTER_SPIKE}
    clean = [a for a in argv_list if a not in skip]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M52A: optional operator-local candidate adapter spike. Requires dual guards. "
            "May invoke torch.load only with matching checkpoint SHA. Watchability only — not "
            "benchmark, strength, promotion, or 12-hour execution."
        ),
    )
    parser.add_argument("--m51-watchability-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--candidate-checkpoint-path", type=Path, required=True)
    parser.add_argument("--expected-candidate-checkpoint-sha256", type=str, required=True)
    parser.add_argument("--sc2-root", type=Path, required=True)
    parser.add_argument("--map-path", type=Path, required=True)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--game-step", type=int, default=8)
    parser.add_argument("--max-game-steps", type=int, default=2048)
    parser.add_argument("--save-replay", action="store_true")
    parser.add_argument("--operator-note", type=Path, default=None)
    parser.add_argument("--expected-m51-watchability-sha256", type=str, default=None)
    parser.add_argument("--m39-run-json", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()
    if bad:
        emit_m52a_forbidden_flag_refusal(
            out,
            emit_profile_short="operator_local_adapter_spike",
            triggered_flags=bad,
        )
        return 0

    params = M52aAdapterRunParams(
        m51_path=args.m51_watchability_json.resolve(),
        output_dir=out,
        sc2_root=args.sc2_root.resolve(),
        map_path=args.map_path.resolve(),
        candidate_checkpoint_path=args.candidate_checkpoint_path.resolve(),
        expected_candidate_sha256=str(args.expected_candidate_checkpoint_sha256),
        game_step=int(args.game_step),
        max_game_steps=int(args.max_game_steps),
        save_replay=bool(args.save_replay),
        device=str(args.device),
        seed=int(args.seed),
        expected_m51_sha256=str(args.expected_m51_watchability_sha256).strip().lower()
        if args.expected_m51_watchability_sha256
        else None,
        operator_note_path=args.operator_note.resolve() if args.operator_note else None,
        m39_run_json_path=args.m39_run_json.resolve() if args.m39_run_json else None,
    )

    run_m52a_operator_local_adapter_spike(
        params,
        allow_local=allow_local,
        authorize_spike=authorize,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
