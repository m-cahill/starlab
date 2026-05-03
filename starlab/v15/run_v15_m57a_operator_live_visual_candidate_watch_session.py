"""CLI: V15-M57A operator-local live visual watch session runner (dual-guard)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m51_live_candidate_watchability_harness_io import (
    M51LiveRunParams,
    run_m51_operator_local_watchability,
)
from starlab.v15.m52_candidate_live_adapter_spike_io import (
    M52aAdapterRunParams,
    run_m52a_operator_local_adapter_spike,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    FORBIDDEN_CLI_FLAGS as M52_FORBIDDEN,
)
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_io import (
    build_runner_blocked_watch_session,
    session_body_from_m51_delegate,
    session_body_from_m52a_delegate,
    validate_candidate_sha,
    write_watch_session_artifacts,
)
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
    FLAG_PREFER_ADAPTER,
    FLAG_SCAFFOLD_POLICY,
    FORBIDDEN_CLI_FLAGS,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_SESSION,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    m57_forbidden = set(FORBIDDEN_CLI_FLAGS)
    m52_forbidden = set(M52_FORBIDDEN)
    bad = sorted({x for x in m57_forbidden | m52_forbidden if x in argv_list})

    allow_local = GUARD_ALLOW_OPERATOR_LOCAL in argv_list
    authorize = GUARD_AUTHORIZE_SESSION in argv_list
    prefer_adapter = FLAG_PREFER_ADAPTER in argv_list
    allow_scaffold = FLAG_SCAFFOLD_POLICY in argv_list

    skip_for_parser = (
        m57_forbidden
        | m52_forbidden
        | {
            GUARD_ALLOW_OPERATOR_LOCAL,
            GUARD_AUTHORIZE_SESSION,
            FLAG_PREFER_ADAPTER,
            FLAG_SCAFFOLD_POLICY,
        }
    )
    clean = [a for a in argv_list if a not in skip_for_parser]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M57A: dual-guard operator live visual watch session. "
            "Prefer M52A delegate when --prefer-candidate-live-adapter; "
            "otherwise requires --allow-scaffold-watchability-policy for M51 scaffold. "
            "No benchmark execution."
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-candidate-sha256", type=str, required=True)
    parser.add_argument("--save-replay", action="store_true")
    parser.add_argument("--game-step", type=int, default=8)
    parser.add_argument("--max-game-steps", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--m51-watchability-json", type=Path, default=None)
    parser.add_argument("--expected-m51-watchability-sha256", type=str, default=None)
    parser.add_argument("--candidate-checkpoint", type=Path, required=True)
    parser.add_argument("--sc2-root", type=Path, default=None)
    parser.add_argument("--map-path", type=Path, default=None)
    parser.add_argument("--m50-readout-json", type=Path, default=None)
    parser.add_argument("--expected-m50-readout-sha256", type=str, default=None)
    parser.add_argument("--m42-package-json", type=Path, default=None)
    parser.add_argument("--m39-run-json", type=Path, default=None)
    parser.add_argument("--operator-note", type=Path, default=None)
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()

    if bad:
        sys.stderr.write(f"error: forbidden flags present: {', '.join(bad)}\n")
        return 2

    if not allow_local or not authorize:
        sys.stderr.write(
            f"error: requires {GUARD_ALLOW_OPERATOR_LOCAL} and {GUARD_AUTHORIZE_SESSION}\n",
        )
        return 2

    exp_ck = str(args.expected_candidate_sha256).strip().lower()
    if exp_ck != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        sys.stderr.write("error: runner binds canonical latest candidate SHA only.\n")
        return 2

    ck_err = validate_candidate_sha(args.candidate_checkpoint, expected=exp_ck)
    if ck_err:
        write_watch_session_artifacts(
            out,
            body_unsealed=build_runner_blocked_watch_session(
                reason=f"blocked: {ck_err}",
                classification=CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
            ),
        )
        return 3

    if prefer_adapter:
        if args.m51_watchability_json is None or args.sc2_root is None or args.map_path is None:
            write_watch_session_artifacts(
                out,
                body_unsealed=build_runner_blocked_watch_session(
                    reason="blocked: M52A delegate requires --m51-watchability-json, "
                    "--sc2-root, --map-path",
                    classification=CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
                ),
            )
            return 3
        m52_out = out / "m52a_delegate"
        params = M52aAdapterRunParams(
            m51_path=args.m51_watchability_json.resolve(),
            output_dir=m52_out,
            sc2_root=args.sc2_root.resolve(),
            map_path=args.map_path.resolve(),
            candidate_checkpoint_path=args.candidate_checkpoint.resolve(),
            expected_candidate_sha256=exp_ck,
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
        sealed_m52, _paths = run_m52a_operator_local_adapter_spike(
            params,
            allow_local=True,
            authorize_spike=True,
        )
        body = session_body_from_m52a_delegate(sealed_m52, m57_output_dir=out)
        write_watch_session_artifacts(out, body_unsealed=body)
        return 0

    if not allow_scaffold:
        write_watch_session_artifacts(
            out,
            body_unsealed=build_runner_blocked_watch_session(
                reason="blocked: missing --prefer-candidate-live-adapter path and "
                "scaffold not authorized (--allow-scaffold-watchability-policy)",
                classification=CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
            ),
        )
        return 3

    if args.m50_readout_json is None or args.sc2_root is None or args.map_path is None:
        write_watch_session_artifacts(
            out,
            body_unsealed=build_runner_blocked_watch_session(
                reason="blocked: M51 scaffold requires --m50-readout-json, --sc2-root, --map-path",
                classification=CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
            ),
        )
        return 3

    m51_out = out / "m51_delegate"
    params51 = M51LiveRunParams(
        m50_path=args.m50_readout_json.resolve(),
        output_dir=m51_out,
        sc2_root=args.sc2_root.resolve(),
        map_path=args.map_path.resolve(),
        game_step=int(args.game_step),
        max_game_steps=int(args.max_game_steps),
        save_replay=bool(args.save_replay),
        allow_scaffold=True,
        seed=int(args.seed),
        video_path=None,
        operator_note_path=args.operator_note.resolve() if args.operator_note else None,
        run_id=None,
        expected_m50_sha256=str(args.expected_m50_readout_sha256).strip().lower()
        if args.expected_m50_readout_sha256
        else None,
        checkpoint_path=args.candidate_checkpoint.resolve(),
        expected_candidate_sha256=exp_ck,
        m42_path=args.m42_package_json.resolve() if args.m42_package_json else None,
    )

    sealed_m51, _ = run_m51_operator_local_watchability(
        params51,
        allow_local=True,
        authorize_watchability=True,
    )
    body = session_body_from_m51_delegate(sealed_m51, m57_output_dir=out)
    write_watch_session_artifacts(out, body_unsealed=body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
