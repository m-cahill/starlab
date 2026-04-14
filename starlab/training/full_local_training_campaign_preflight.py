"""M49: deterministic preflight checks for a full local training campaign contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.env_probe import run_probe
from starlab.training.full_local_training_campaign_io import (
    load_benchmark_contract_m20,
    load_m26_dataset_file,
    m14_bundle_identity,
    verify_hierarchical_training_run_file,
)
from starlab.training.full_local_training_campaign_models import (
    CAMPAIGN_PREFLIGHT_RECEIPT_FILENAME,
    FULL_LOCAL_TRAINING_CAMPAIGN_PREFLIGHT_RECEIPT_VERSION,
    FULL_LOCAL_TRAINING_CAMPAIGN_VERSION,
)
from starlab.training.training_program_io import load_agent_training_program_contract_from_path


def _load_contract(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "campaign contract root must be a JSON object"
        raise ValueError(msg)
    return raw


def verify_campaign_contract_seal(contract: dict[str, Any]) -> None:
    """Ensure campaign_sha256 matches canonical body without that field."""

    stored = contract.get("campaign_sha256")
    if not isinstance(stored, str) or len(stored) != 64:
        msg = "campaign contract must include 64-char hex campaign_sha256"
        raise ValueError(msg)
    body_wo = {k: v for k, v in contract.items() if k != "campaign_sha256"}
    computed = sha256_hex_of_canonical_json(body_wo)
    if stored != computed:
        msg = "campaign_sha256 does not match contract body"
        raise ValueError(msg)


def _check_sc2_harness_importable() -> tuple[bool, str]:
    try:
        from sc2.bot_ai import BotAI  # noqa: F401
    except ImportError:
        return False, (
            "sc2 python package not importable; install optional extras "
            "(e.g. pip install -e '.[sc2-harness]') for local_live_sc2"
        )
    return True, "sc2 import ok"


def _check_sc2_install_probe() -> tuple[bool, str]:
    probe = run_probe()
    root = probe.paths.get("root")
    if not root:
        return (
            False,
            "SC2 install root not resolved by probe (see docs/runtime/sc2_runtime_surface.md)",
        )
    return True, f"SC2 probe root: {root}"


def run_campaign_preflight(*, contract_path: Path) -> tuple[bool, dict[str, Any]]:
    """Run all preflight checks; return (ok, receipt_dict)."""

    contract = _load_contract(contract_path)
    checks: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "detail": detail, "ok": ok})

    ver = contract.get("campaign_version")
    if ver != FULL_LOCAL_TRAINING_CAMPAIGN_VERSION:
        add(
            "campaign_version",
            False,
            f"expected {FULL_LOCAL_TRAINING_CAMPAIGN_VERSION!r}, got {ver!r}",
        )
        receipt = _receipt_body(contract, checks, ok=False)
        return False, receipt
    add("campaign_version", True, "version matches")

    try:
        verify_campaign_contract_seal(contract)
        add("campaign_seal", True, "campaign_sha256 matches body")
    except ValueError as e:
        add("campaign_seal", False, str(e))
        receipt = _receipt_body(contract, checks, ok=False)
        return False, receipt

    m43 = contract.get("m43_candidate")
    if not isinstance(m43, dict):
        add("m43_block", False, "missing m43_candidate")
        receipt = _receipt_body(contract, checks, ok=False)
        return False, receipt

    hr_path = Path(m43["hierarchical_training_run_path"])
    try:
        run = verify_hierarchical_training_run_file(hr_path)
        if run["training_run_sha256"] != m43["training_run_sha256"]:
            add("m43_training_run_identity", False, "file hash mismatch vs contract")
        else:
            add("m43_training_run_identity", True, "training_run_sha256 coherent")
    except (OSError, ValueError) as e:
        add("m43_training_run_identity", False, str(e))

    wpath = Path(m43["resolved_weights_path"])
    try:
        if not wpath.is_file():
            add("m43_weights", False, f"missing weights file: {wpath}")
        elif sha256_hex_file(wpath) != m43["weights_sha256"]:
            add("m43_weights", False, "weights_sha256 mismatch vs file")
        else:
            add("m43_weights", True, "weights present and hash matches")
    except OSError as e:
        add("m43_weights", False, str(e))

    m40 = contract.get("m40_training_program_contract")
    if isinstance(m40, dict):
        p = Path(m40["resolved_path"])
        try:
            loaded = load_agent_training_program_contract_from_path(p)
            if str(loaded["contract_sha256"]) != str(m40["contract_sha256"]):
                add("m40_contract", False, "contract_sha256 mismatch vs file")
            else:
                add("m40_contract", True, "M40 contract loads and digest matches")
        except (OSError, ValueError) as e:
            add("m40_contract", False, str(e))
    else:
        add("m40_contract", False, "missing m40_training_program_contract")

    m20 = contract.get("m20_benchmark_contract")
    if isinstance(m20, dict):
        p = Path(m20["resolved_path"])
        try:
            bench = load_benchmark_contract_m20(p)
            if sha256_hex_of_canonical_json(bench) != m20["benchmark_contract_sha256"]:
                add("m20_benchmark", False, "benchmark_contract_sha256 mismatch vs file")
            else:
                add("m20_benchmark", True, "M20 benchmark loads and hash matches")
        except (OSError, ValueError) as e:
            add("m20_benchmark", False, str(e))
    else:
        add("m20_benchmark", False, "missing m20_benchmark_contract")

    m45 = contract.get("m45_planned_bootstrap")
    if isinstance(m45, dict):
        mp = Path(m45["match_config_path"])
        try:
            if not mp.is_file():
                add("match_config", False, f"missing match config: {mp}")
            elif sha256_hex_file(mp) != m45["match_config_sha256"]:
                add("match_config", False, "match_config_sha256 mismatch vs file")
            else:
                add("match_config", True, "match config present and hash matches")
        except OSError as e:
            add("match_config", False, str(e))
        rt = str(m45.get("runtime_mode", ""))
        if rt == "local_live_sc2":
            ok_imp, det = _check_sc2_harness_importable()
            add("sc2_python_import", ok_imp, det)
            ok_pr, det2 = _check_sc2_install_probe()
            add("sc2_install_probe", ok_pr, det2)
    else:
        add("m45_bootstrap", False, "missing m45_planned_bootstrap")

    planned_refit = bool(m45.get("planned_weighted_refit")) if isinstance(m45, dict) else False
    m26 = contract.get("m26_replay_training_dataset")
    bundles = contract.get("m14_replay_bundle_directories")
    if planned_refit:
        if not isinstance(m26, dict) or not m26.get("resolved_path"):
            add(
                "m26_dataset_refit",
                False,
                "planned_weighted_refit requires m26_replay_training_dataset",
            )
        else:
            dp = Path(str(m26["resolved_path"]))
            try:
                ds = load_m26_dataset_file(dp)
                if str(ds["dataset_sha256"]) != str(m26["dataset_sha256"]):
                    add("m26_dataset_refit", False, "dataset_sha256 mismatch")
                else:
                    add("m26_dataset_refit", True, "M26 dataset loads and hash matches")
            except (OSError, ValueError) as e:
                add("m26_dataset_refit", False, str(e))
        if not isinstance(bundles, list) or not bundles:
            add(
                "m14_bundles_refit",
                False,
                "planned_weighted_refit requires m14 bundle directories",
            )
        else:
            b_ok = True
            details: list[str] = []
            for ent in bundles:
                if not isinstance(ent, dict):
                    b_ok = False
                    details.append("non-object bundle entry")
                    continue
                bd = Path(str(ent["resolved_path"]))
                try:
                    ident = m14_bundle_identity(bd)
                    if ident["bundle_id"] != str(ent.get("bundle_id")):
                        b_ok = False
                        details.append(f"bundle_id mismatch for {bd}")
                    else:
                        details.append(f"ok {ident['bundle_id']}")
                except (OSError, ValueError) as e:
                    b_ok = False
                    details.append(str(e))
            add("m14_bundles_refit", b_ok, "; ".join(details))
    else:
        add(
            "refit_prerequisites",
            True,
            "planned_weighted_refit false — M26/M14 refit paths not required",
        )

    ok = all(bool(c.get("ok")) for c in checks)
    receipt = _receipt_body(contract, checks, ok=ok)
    return ok, receipt


def _receipt_body(
    contract: dict[str, Any],
    checks: list[dict[str, Any]],
    *,
    ok: bool,
) -> dict[str, Any]:
    return {
        "campaign_contract_sha256": contract.get("campaign_sha256"),
        "checks": checks,
        "preflight_ok": ok,
        "receipt_version": FULL_LOCAL_TRAINING_CAMPAIGN_PREFLIGHT_RECEIPT_VERSION,
    }


def write_preflight_receipt(*, receipt: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / CAMPAIGN_PREFLIGHT_RECEIPT_FILENAME
    path.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    return path
