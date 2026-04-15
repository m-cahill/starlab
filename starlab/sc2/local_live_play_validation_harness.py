"""M44 orchestrator: match harness + M43 inference + replay binding + validation artifacts."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.hierarchy.hierarchical_training_models import (
    HIERARCHICAL_TRAINING_RUN_FILENAME,
    WEIGHTS_ARTIFACT_BASENAME,
    WEIGHTS_SUBDIR,
)
from starlab.hierarchy.m43_sklearn_runtime import (
    assert_workers_cover_delegates,
    load_hierarchical_sklearn_bundle,
    predict_delegate_and_coarse_label,
)
from starlab.runs.bind_replay import bind_replay_from_paths
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record
from starlab.sc2.artifacts import execution_proof_to_json, parse_execution_proof_mapping
from starlab.sc2.harness import run_match_execution
from starlab.sc2.local_live_play_validation_io import (
    minimal_report_from_run,
    seal_validation_run_body,
    write_validation_artifacts,
)
from starlab.sc2.local_live_play_validation_models import (
    LOCAL_LIVE_PLAY_VALIDATION_RUN_VERSION,
    NON_CLAIMS_V1,
    LivePlayValidationPaths,
    OptionalVideoRegistration,
    RuntimeMode,
)
from starlab.sc2.match_config import load_match_config, match_config_to_mapping
from starlab.sc2.semantic_live_action_adapter import (
    SEMANTIC_LIVE_ACTION_ADAPTER_POLICY_ID,
    map_semantic_to_live_action,
)


def _validate_runtime_mode_adapter(runtime_mode: RuntimeMode, adapter: str) -> None:
    if runtime_mode == "fixture_stub_ci" and adapter != "fake":
        msg = "runtime_mode fixture_stub_ci requires match config adapter=fake"
        raise ValueError(msg)
    if runtime_mode == "local_live_sc2" and adapter != "burnysc2":
        msg = "runtime_mode local_live_sc2 requires match config adapter=burnysc2"
        raise ValueError(msg)


def _derive_context_signature_for_step(step_index: int, obs: dict[str, int]) -> str:
    """Deterministic pseudo-signature for M44 live steps (feeds M43 DictVectorizer)."""

    gl = int(obs.get("game_loop", 0))
    minerals = int(obs.get("minerals", 0))
    vespene = int(obs.get("vespene", 0))
    return f"m44_step={step_index}|gameloop={gl}|minerals={minerals}|vespene={vespene}"


def deterministic_stub_replay_bytes(*, proof_artifact_hash: str, runtime_mode: str) -> bytes:
    """Deterministic bytes as ``.SC2Replay`` for CI/fixture paths (not a real replay)."""

    lines = [
        b"STARLAB M44 STUB REPLAY (NOT A REAL SC2 REPLAY FILE)",
        f"proof_artifact_hash={proof_artifact_hash}".encode("ascii"),
        f"runtime_mode={runtime_mode}".encode("ascii"),
    ]
    return b"\n".join(lines) + b"\n"


def resolve_paths(output_dir: Path) -> LivePlayValidationPaths:
    replay_dir = output_dir / "replay"
    return LivePlayValidationPaths(
        output_dir=output_dir,
        run_json=output_dir / "local_live_play_validation_run.json",
        report_json=output_dir / "local_live_play_validation_run_report.json",
        match_proof=output_dir / "match_execution_proof.json",
        match_config=output_dir / "match_config.json",
        run_identity=output_dir / "run_identity.json",
        lineage_seed=output_dir / "lineage_seed.json",
        replay_dir=replay_dir,
        validation_replay=replay_dir / "validation.SC2Replay",
        replay_binding=output_dir / "replay_binding.json",
    )


def _optional_video_metadata(path: Path) -> OptionalVideoRegistration:
    sha = sha256_hex_file(path)
    sz = path.stat().st_size
    suffix = path.suffix.lower().lstrip(".") or "unknown"
    return OptionalVideoRegistration(
        path=str(path.resolve()),
        sha256=sha,
        size_bytes=int(sz),
        duration_seconds=None,
        format=suffix,
        resolution=None,
        codec=None,
    )


@dataclass(frozen=True, slots=True)
class LivePlayValidationResult:
    output_dir: Path
    validation_run: dict[str, Any]


def run_local_live_play_validation(
    *,
    hierarchical_training_run_dir: Path,
    match_config_path: Path,
    output_dir: Path,
    runtime_mode: RuntimeMode,
    weights_path: Path | None = None,
    optional_video_path: Path | None = None,
    run_id: str | None = None,
    include_environment_fingerprint: bool = True,
    env_json_path: Path | None = None,
    enforce_weights_sidecar_sha256: bool = True,
) -> LivePlayValidationResult:
    """Execute bounded validation: M02 harness, M43 sklearn inference trace, M04 replay binding.

    When ``enforce_weights_sidecar_sha256`` is False, a ``weights_path`` whose SHA does not match
    ``hierarchical_training_run.json``/``weights_sidecar`` is allowed (e.g. M51 campaign refit
    bundle). A warning is recorded on the validation run.
    """

    hr_path = hierarchical_training_run_dir / HIERARCHICAL_TRAINING_RUN_FILENAME
    training_run = json.loads(hr_path.read_text(encoding="utf-8"))
    if not isinstance(training_run, dict):
        msg = "hierarchical training run root must be an object"
        raise ValueError(msg)
    tr_ver = training_run.get("training_run_version")
    if tr_ver != "starlab.hierarchical_training_run.v1":
        msg = f"unsupported hierarchical training_run_version: {tr_ver!r}"
        raise ValueError(msg)

    training_run_sha256 = training_run.get("training_run_sha256")
    if not isinstance(training_run_sha256, str):
        msg = "hierarchical_training_run.json missing training_run_sha256"
        raise ValueError(msg)
    stripped = {k: v for k, v in training_run.items() if k != "training_run_sha256"}
    if sha256_hex_of_canonical_json(stripped) != training_run_sha256:
        msg = "hierarchical_training_run.json training_run_sha256 does not match content"
        raise ValueError(msg)

    wpath = weights_path
    if wpath is None:
        wpath = hierarchical_training_run_dir / WEIGHTS_SUBDIR / WEIGHTS_ARTIFACT_BASENAME
    if not wpath.is_file():
        msg = f"M43 joblib weights not found at {wpath}"
        raise ValueError(msg)

    weight_warnings: list[str] = []
    sidecar = training_run.get("weights_sidecar")
    if isinstance(sidecar, dict):
        expected_sha = sidecar.get("artifact_sha256")
        if isinstance(expected_sha, str) and expected_sha:
            actual = sha256_hex_file(wpath)
            if actual != expected_sha:
                if enforce_weights_sidecar_sha256:
                    msg = (
                        "weights file sha256 does not match hierarchical_training_run "
                        "weights_sidecar"
                    )
                    raise ValueError(msg)
                weight_warnings.append(
                    "m51_weights_override: joblib sha256 does not match "
                    "hierarchical_training_run weights_sidecar (non-M43 candidate weights)"
                )

    bundle = load_hierarchical_sklearn_bundle(wpath)
    assert_workers_cover_delegates(bundle)

    cfg = load_match_config(match_config_path)
    _validate_runtime_mode_adapter(runtime_mode, cfg.adapter)

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = resolve_paths(output_dir)

    shutil.copy(match_config_path, paths.match_config)

    harness_result = run_match_execution(cfg, output_dir=output_dir)
    if not harness_result.ok or harness_result.proof is None:
        msg = harness_result.message or "match harness failed"
        raise RuntimeError(msg)

    proof_text = execution_proof_to_json(harness_result.proof, redact=False)
    paths.match_proof.write_text(proof_text, encoding="utf-8")

    proof_mapping = json.loads(proof_text)
    if not isinstance(proof_mapping, dict):
        msg = "internal: proof mapping must be dict"
        raise ValueError(msg)
    record = parse_execution_proof_mapping(proof_mapping)
    proof_hash = str(proof_mapping.get("artifact_hash", ""))
    if not proof_hash:
        msg = "internal: match proof missing artifact_hash"
        raise ValueError(msg)

    paths.replay_dir.mkdir(parents=True, exist_ok=True)
    replay_warnings: list[str] = []

    if runtime_mode == "fixture_stub_ci":
        stub_bytes = deterministic_stub_replay_bytes(
            proof_artifact_hash=proof_hash,
            runtime_mode=runtime_mode,
        )
        paths.validation_replay.write_bytes(stub_bytes)
    else:
        rp = record.replay
        copied = False
        if (
            rp is not None
            and rp.replay_saved
            and rp.replay_file_name
            and (output_dir / rp.replay_file_name).is_file()
        ):
            shutil.copy(output_dir / rp.replay_file_name, paths.validation_replay)
            copied = True
        elif rp is not None and rp.replay_file_name:
            alt = Path(rp.replay_file_name)
            if alt.is_file():
                shutil.copy(alt, paths.validation_replay)
                copied = True
        if not copied:
            replay_warnings.append(
                "local_live_sc2: real replay not copied; emitted deterministic stub replay instead",
            )
            stub_bytes = deterministic_stub_replay_bytes(
                proof_artifact_hash=proof_hash,
                runtime_mode=runtime_mode,
            )
            paths.validation_replay.write_bytes(stub_bytes)

    run_identity, lineage_seed = build_seed_from_paths(
        config_path=paths.match_config,
        env_path=env_json_path,
        include_fingerprint=include_environment_fingerprint,
        proof_path=paths.match_proof,
    )
    write_json_record(paths.run_identity, run_identity)
    write_json_record(paths.lineage_seed, lineage_seed)

    bind_replay_from_paths(
        lineage_seed_path=paths.lineage_seed,
        output_dir=output_dir,
        replay_path=paths.validation_replay,
        run_identity_path=paths.run_identity,
    )

    replay_binding = json.loads(paths.replay_binding.read_text(encoding="utf-8"))
    if not isinstance(replay_binding, dict):
        msg = "replay_binding.json must be an object"
        raise ValueError(msg)

    summaries = [dict(x) for x in proof_mapping.get("observation_summaries", [])]
    semantic_steps: list[dict[str, Any]] = []
    for i, obs in enumerate(summaries):
        sig = _derive_context_signature_for_step(i, obs)
        delegate_id, coarse = predict_delegate_and_coarse_label(bundle, sig)
        action = map_semantic_to_live_action(delegate_id=delegate_id, coarse_label=coarse)
        semantic_steps.append(
            {
                "step_index": i,
                "context_signature": sig,
                "predicted_delegate_id": delegate_id,
                "predicted_coarse_label": coarse,
                "live_action": action,
            },
        )

    vid_meta: dict[str, Any] | None = None
    if optional_video_path is not None:
        if not optional_video_path.is_file():
            msg = f"optional video path is not a file: {optional_video_path}"
            raise ValueError(msg)
        vm = _optional_video_metadata(optional_video_path)
        vid_meta = {
            "codec": vm.codec,
            "duration_seconds": vm.duration_seconds,
            "format": vm.format,
            "path": vm.path,
            "resolution": vm.resolution,
            "sha256": vm.sha256,
            "size_bytes": vm.size_bytes,
        }

    identity_payload = {
        "hierarchical_training_run_sha256": training_run_sha256,
        "match_config_canonical": match_config_to_mapping(cfg),
        "proof_artifact_hash": proof_hash,
        "runtime_mode": runtime_mode,
        "semantic_live_action_adapter_policy_id": SEMANTIC_LIVE_ACTION_ADAPTER_POLICY_ID,
    }
    derived_id = sha256_hex_of_canonical_json(identity_payload)
    final_run_id = run_id or derived_id

    env_fp = run_identity.get("environment_fingerprint")
    caveats = [
        "ci_validates_fixture_stub_path_only_when_runtime_mode_is_fixture_stub_ci",
        "m44_proves_bounded_plumbing_not_strong_gameplay",
        "replay_stub_in_fixture_mode_is_not_a_real_sc2_replay_semantics_wise",
    ]

    body_pre: dict[str, Any] = {
        "action_adapter_steps": semantic_steps,
        "caveats": caveats,
        "candidate": {
            "hierarchical_training_run_path": str(hr_path.resolve()),
            "hierarchical_training_run_sha256": training_run_sha256,
            "joblib_weights_path": str(wpath.resolve()),
            "joblib_weights_sha256": sha256_hex_file(wpath),
            "training_program_contract_sha256": training_run["training_program_contract_sha256"],
            "training_program_contract_version": training_run["training_program_contract_version"],
            "training_run_id": training_run["run_id"],
        },
        "interface_trace_schema_version": training_run["interface_trace_schema_version"],
        "delegate_policy_id": training_run["delegate_policy_id"],
        "match_execution": {
            "adapter": cfg.adapter,
            "final_status": proof_mapping.get("final_status"),
            "map_logical_key": proof_mapping.get("map_logical_key"),
            "proof_artifact_hash": proof_hash,
            "seed": cfg.seed,
            **(
                {"sc2_game_result": proof_mapping["sc2_game_result"]}
                if proof_mapping.get("sc2_game_result") is not None
                else {}
            ),
        },
        "non_claims": sorted(NON_CLAIMS_V1),
        "optional_media_registration": vid_meta,
        "replay": {
            "kind": "fixture_stub_replay_file"
            if runtime_mode == "fixture_stub_ci"
            else "local_replay_or_stub",
            "replay_content_sha256": replay_binding.get("replay_content_sha256"),
            "replay_file": "replay/validation.SC2Replay",
            "replay_binding_id": replay_binding.get("replay_binding_id"),
        },
        "replay_binding": replay_binding,
        "run_id": final_run_id,
        "runtime_environment": {
            "environment_fingerprint": env_fp,
            "lineage_seed_id": lineage_seed.get("lineage_seed_id"),
            "run_spec_id": run_identity.get("run_spec_id"),
        },
        "runtime_mode": runtime_mode,
        "semantic_live_action_adapter_policy_id": SEMANTIC_LIVE_ACTION_ADAPTER_POLICY_ID,
        "validation_run_version": LOCAL_LIVE_PLAY_VALIDATION_RUN_VERSION,
    }
    body_pre["warnings"] = list(replay_warnings) + weight_warnings

    run = seal_validation_run_body(body_pre)
    report = minimal_report_from_run(run)
    write_validation_artifacts(run_body=run, report_body=report, output_dir=output_dir)

    return LivePlayValidationResult(output_dir=output_dir, validation_run=run)
