"""M49: build, seal, and write full local training / bootstrap campaign contract artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.benchmarks.benchmark_contract_schema import validate_benchmark_contract
from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.hierarchy.hierarchical_training_models import (
    HIERARCHICAL_TRAINING_RUN_FILENAME,
    WEIGHTS_ARTIFACT_BASENAME,
    WEIGHTS_SUBDIR,
)
from starlab.imitation.dataset_models import REPLAY_TRAINING_DATASET_VERSION
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.local_live_play_validation_models import RuntimeMode
from starlab.sc2.match_config import match_config_from_mapping
from starlab.training.full_local_training_campaign_models import (
    AUTHORIZATION_POSTURE_PLANNED_CHARTER_ONLY,
    FULL_LOCAL_TRAINING_CAMPAIGN_FILENAME,
    FULL_LOCAL_TRAINING_CAMPAIGN_REPORT_FILENAME,
    FULL_LOCAL_TRAINING_CAMPAIGN_REPORT_VERSION,
    FULL_LOCAL_TRAINING_CAMPAIGN_VERSION,
    NON_CLAIMS_V1,
    default_campaign_protocol_v1,
    evidence_interpretation_block_v1,
)
from starlab.training.training_program_io import (
    load_agent_training_program_contract_from_path,
    write_agent_training_program_contract,
)


def _load_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"{path}: JSON root must be an object"
        raise ValueError(msg)
    return raw


def verify_hierarchical_training_run_file(path: Path) -> dict[str, Any]:
    """Load M43 hierarchical_training_run.json and verify training_run_sha256."""

    run = _load_json_object(path)
    tr_ver = run.get("training_run_version")
    if tr_ver != "starlab.hierarchical_training_run.v1":
        msg = f"unsupported hierarchical training_run_version: {tr_ver!r}"
        raise ValueError(msg)
    training_run_sha256 = run.get("training_run_sha256")
    if not isinstance(training_run_sha256, str):
        msg = "hierarchical_training_run.json missing training_run_sha256"
        raise ValueError(msg)
    stripped = {k: v for k, v in run.items() if k != "training_run_sha256"}
    if sha256_hex_of_canonical_json(stripped) != training_run_sha256:
        msg = "hierarchical_training_run.json training_run_sha256 does not match content"
        raise ValueError(msg)
    return run


def load_benchmark_contract_m20(path: Path) -> dict[str, Any]:
    """Load M20 benchmark contract JSON; validate schema."""

    c = _load_json_object(path)
    errs = validate_benchmark_contract(c)
    if errs:
        msg = f"{path}: benchmark contract invalid: {errs}"
        raise ValueError(msg)
    return c


def load_m26_dataset_file(path: Path) -> dict[str, Any]:
    """Load replay_training_dataset.json and verify dataset_sha256."""

    ds = _load_json_object(path)
    ver = ds.get("dataset_version")
    if ver != REPLAY_TRAINING_DATASET_VERSION:
        msg = f"{path}: unexpected dataset_version {ver!r}"
        raise ValueError(msg)
    stored = ds.get("dataset_sha256")
    if not isinstance(stored, str) or len(stored) != 64:
        msg = f"{path}: dataset_sha256 missing or not 64-char hex"
        raise ValueError(msg)
    stripped = {k: v for k, v in ds.items() if k != "dataset_sha256"}
    if sha256_hex_of_canonical_json(stripped) != stored:
        msg = f"{path}: dataset_sha256 does not match body"
        raise ValueError(msg)
    return ds


def m14_bundle_identity(bundle_dir: Path) -> dict[str, str]:
    """Read bundle_id and lineage_root from replay_bundle_manifest.json."""

    manifest_path = bundle_dir / "replay_bundle_manifest.json"
    if not manifest_path.is_file():
        msg = f"missing replay_bundle_manifest.json under {bundle_dir}"
        raise ValueError(msg)
    m = _load_json_object(manifest_path)
    bid = m.get("bundle_id")
    lr = m.get("lineage_root")
    if not isinstance(bid, str) or not isinstance(lr, str):
        msg = f"{manifest_path}: bundle_id and lineage_root must be strings"
        raise ValueError(msg)
    return {"bundle_id": bid, "lineage_root": lr}


def seal_campaign_contract_body(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    """Attach campaign_sha256 over the object without that field."""

    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "campaign_sha256": digest}


def build_full_local_training_campaign_contract(
    *,
    campaign_id: str,
    hierarchical_training_run_dir: Path,
    benchmark_contract_path: Path,
    match_config_path: Path,
    runtime_mode: RuntimeMode,
    output_dir: Path,
    training_program_contract_path: Path | None,
    weights_path: Path | None = None,
    dataset_path: Path | None = None,
    bundle_dirs: list[Path] | None = None,
    planned_weighted_refit: bool = False,
    campaign_protocol: dict[str, object] | None = None,
) -> dict[str, Any]:
    """Assemble governed campaign contract dict (sealed via ``seal_campaign_contract_body``)."""

    if planned_weighted_refit:
        if dataset_path is None:
            msg = "planned_weighted_refit requires --dataset"
            raise ValueError(msg)
        if not bundle_dirs:
            msg = "planned_weighted_refit requires at least one --bundle-dir"
            raise ValueError(msg)

    hr_path = hierarchical_training_run_dir / HIERARCHICAL_TRAINING_RUN_FILENAME
    training_run = verify_hierarchical_training_run_file(hr_path)

    wpath = weights_path
    if wpath is None:
        wpath = hierarchical_training_run_dir / WEIGHTS_SUBDIR / WEIGHTS_ARTIFACT_BASENAME
    if not wpath.is_file():
        msg = f"M43 weights not found at {wpath}"
        raise ValueError(msg)
    weights_sha256 = sha256_hex_file(wpath)

    if training_program_contract_path is not None:
        m40 = load_agent_training_program_contract_from_path(training_program_contract_path)
        m40_path_resolved = str(training_program_contract_path.resolve())
    else:
        ref_dir = output_dir / "referenced_artifacts" / "m40_training_program"
        c_path, _r = write_agent_training_program_contract(ref_dir)
        m40 = load_agent_training_program_contract_from_path(c_path)
        m40_path_resolved = str(c_path.resolve())

    m40_sha = str(m40["contract_sha256"])
    m40_ver = str(m40["program_version"])
    if m40_sha != str(training_run["training_program_contract_sha256"]):
        msg = (
            "M40 contract_sha256 does not match hierarchical_training_run."
            "training_program_contract_sha256"
        )
        raise ValueError(msg)
    if m40_ver != str(training_run["training_program_contract_version"]):
        msg = (
            "M40 program_version does not match hierarchical_training_run."
            "training_program_contract_version"
        )
        raise ValueError(msg)

    bench = load_benchmark_contract_m20(benchmark_contract_path)
    bench_sha = sha256_hex_of_canonical_json(bench)
    bench_id = str(bench["benchmark_id"])
    bench_version = str(bench["benchmark_version"])

    match_raw = _load_json_object(match_config_path)
    match_config_sha256 = sha256_hex_file(match_config_path)
    _validate_runtime_mode_adapter(runtime_mode, match_raw)

    m26_block: dict[str, Any] | None = None
    bundle_entries: list[dict[str, Any]] = []
    if dataset_path is not None:
        ds = load_m26_dataset_file(dataset_path)
        ds_sha = str(ds["dataset_sha256"])
        src = training_run.get("source_dataset")
        if not isinstance(src, dict):
            msg = "hierarchical_training_run missing source_dataset"
            raise ValueError(msg)
        if ds_sha != str(src.get("dataset_sha256")):
            msg = "M26 dataset_sha256 does not match hierarchical_training_run.source_dataset"
            raise ValueError(msg)
        m26_block = {
            "dataset_version": str(ds["dataset_version"]),
            "dataset_sha256": ds_sha,
            "resolved_path": str(dataset_path.resolve()),
        }

    if bundle_dirs:
        seen_ids: set[str] = set()
        for bd in sorted(bundle_dirs, key=lambda p: str(p.resolve())):
            if not bd.is_dir():
                msg = f"M14 bundle directory not found: {bd}"
                raise ValueError(msg)
            ident = m14_bundle_identity(bd)
            if ident["bundle_id"] in seen_ids:
                msg = f"duplicate bundle_id in --bundle-dir: {ident['bundle_id']}"
                raise ValueError(msg)
            seen_ids.add(ident["bundle_id"])
            bundle_entries.append(
                {
                    "bundle_id": ident["bundle_id"],
                    "lineage_root": ident["lineage_root"],
                    "resolved_path": str(bd.resolve()),
                }
            )

    protocol = (
        campaign_protocol if campaign_protocol is not None else default_campaign_protocol_v1()
    )

    body: dict[str, Any] = {
        "authorization_posture": dict(AUTHORIZATION_POSTURE_PLANNED_CHARTER_ONLY),
        "campaign_id": campaign_id,
        "campaign_protocol": protocol,
        "campaign_version": FULL_LOCAL_TRAINING_CAMPAIGN_VERSION,
        "evidence_interpretation": evidence_interpretation_block_v1(),
        "m20_benchmark_contract": {
            "benchmark_contract_sha256": bench_sha,
            "benchmark_id": bench_id,
            "benchmark_version": bench_version,
            "resolved_path": str(benchmark_contract_path.resolve()),
        },
        "m26_replay_training_dataset": m26_block,
        "m40_training_program_contract": {
            "contract_sha256": m40_sha,
            "program_version": m40_ver,
            "resolved_path": m40_path_resolved,
        },
        "m43_candidate": {
            "hierarchical_training_run_dir": str(hierarchical_training_run_dir.resolve()),
            "hierarchical_training_run_path": str(hr_path.resolve()),
            "resolved_weights_path": str(wpath.resolve()),
            "run_id": str(training_run["run_id"]),
            "training_run_sha256": str(training_run["training_run_sha256"]),
            "weights_sha256": weights_sha256,
        },
        "m45_planned_bootstrap": {
            "match_config_path": str(match_config_path.resolve()),
            "match_config_sha256": match_config_sha256,
            "planned_weighted_refit": planned_weighted_refit,
            "runtime_mode": runtime_mode,
        },
        "m14_replay_bundle_directories": bundle_entries,
        "non_claims": sorted(NON_CLAIMS_V1),
    }
    return body


def _validate_runtime_mode_adapter(runtime_mode: RuntimeMode, match_raw: dict[str, Any]) -> None:
    cfg = match_config_from_mapping(match_raw)
    adapter = str(cfg.adapter)
    if runtime_mode == "fixture_stub_ci" and adapter != "fake":
        msg = "runtime_mode fixture_stub_ci requires match config adapter=fake"
        raise ValueError(msg)
    if runtime_mode == "local_live_sc2" and adapter != "burnysc2":
        msg = "runtime_mode local_live_sc2 requires match config adapter=burnysc2"
        raise ValueError(msg)


def build_full_local_training_campaign_report(contract: dict[str, Any]) -> dict[str, Any]:
    """Compact report linked to campaign_sha256."""

    return {
        "campaign_id": contract["campaign_id"],
        "campaign_sha256": contract["campaign_sha256"],
        "m43_run_id": contract["m43_candidate"]["run_id"],
        "non_claims": contract["non_claims"],
        "report_version": FULL_LOCAL_TRAINING_CAMPAIGN_REPORT_VERSION,
        "summary": {
            "benchmark_id": contract["m20_benchmark_contract"]["benchmark_id"],
            "planned_weighted_refit": contract["m45_planned_bootstrap"]["planned_weighted_refit"],
            "posture": contract["authorization_posture"]["status"],
            "runtime_mode": contract["m45_planned_bootstrap"]["runtime_mode"],
        },
    }


def write_full_local_training_campaign_artifacts(
    *,
    contract: dict[str, Any],
    report: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FULL_LOCAL_TRAINING_CAMPAIGN_FILENAME
    r_path = output_dir / FULL_LOCAL_TRAINING_CAMPAIGN_REPORT_FILENAME
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_full_local_training_campaign(
    *,
    campaign_id: str,
    hierarchical_training_run_dir: Path,
    benchmark_contract_path: Path,
    match_config_path: Path,
    runtime_mode: RuntimeMode,
    output_dir: Path,
    training_program_contract_path: Path | None = None,
    weights_path: Path | None = None,
    dataset_path: Path | None = None,
    bundle_dirs: list[Path] | None = None,
    planned_weighted_refit: bool = False,
    campaign_protocol: dict[str, object] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    """Build, seal, and write campaign contract + report."""

    body = build_full_local_training_campaign_contract(
        benchmark_contract_path=benchmark_contract_path,
        bundle_dirs=bundle_dirs,
        campaign_id=campaign_id,
        campaign_protocol=campaign_protocol,
        dataset_path=dataset_path,
        hierarchical_training_run_dir=hierarchical_training_run_dir,
        match_config_path=match_config_path,
        output_dir=output_dir,
        planned_weighted_refit=planned_weighted_refit,
        runtime_mode=runtime_mode,
        training_program_contract_path=training_program_contract_path,
        weights_path=weights_path,
    )
    sealed = seal_campaign_contract_body(body)
    report = build_full_local_training_campaign_report(sealed)
    c_path, r_path = write_full_local_training_campaign_artifacts(
        contract=sealed,
        output_dir=output_dir,
        report=report,
    )
    return sealed, report, c_path, r_path
