"""M50: extended execution readiness preflight (maps, locks, posture hooks)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from starlab.sc2.env_probe import run_probe
from starlab.training.campaign_execution_lock import (
    CAMPAIGN_OUTPUT_LOCK_BASENAME,
    lock_is_stale,
    read_lock_file,
)
from starlab.training.full_local_training_campaign_preflight import (
    run_campaign_preflight,
    verify_campaign_contract_seal,
)
from starlab.training.industrial_hidden_rollout_models import (
    EXECUTION_PREFLIGHT_RECEIPT_NOTE,
    resolve_visibility_posture_v1,
)


def _load_contract(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "campaign contract root must be a JSON object"
        raise ValueError(msg)
    return raw


def _match_map_preflight(match_raw: dict[str, Any], *, maps_dir: str | None) -> tuple[bool, str]:
    m = match_raw.get("map") or {}
    if not isinstance(m, dict):
        return False, "match config map block missing or not an object"
    path = m.get("path")
    discover = bool(m.get("discover_under_maps_dir", False))
    bn = m.get("battle_net_map_name")
    n_modes = sum(
        1
        for x in (
            path is not None,
            discover,
            bn is not None and str(bn).strip() != "",
        )
        if x
    )
    if n_modes != 1:
        return (
            False,
            (
                "map selection must set exactly one of: path, "
                "discover_under_maps_dir, battle_net_map_name"
            ),
        )
    if discover:
        if not maps_dir:
            return False, "discover_under_maps_dir requires resolved SC2 Maps directory (see probe)"
        md = Path(maps_dir)
        if not md.is_dir():
            return False, f"Maps directory not found: {maps_dir}"
        return True, f"discover_under_maps_dir ok under {maps_dir}"
    if path is not None:
        p = Path(str(path))
        if p.is_file():
            return True, f"map path exists: {p}"
        if maps_dir:
            candidate = Path(maps_dir) / path
            if candidate.is_file():
                return True, f"map resolved under Maps dir: {candidate}"
        return (
            False,
            f"map path not found: {path} (and not under Maps dir {maps_dir!r})",
        )
    return True, f"battle_net_map_name={bn!r} (existence not verified offline)"


def _python_executable_check() -> tuple[bool, str]:
    return True, f"python executable: {sys.executable}"


def _sc2_import_check() -> tuple[bool, str]:
    if importlib.util.find_spec("sc2") is None:
        return False, "sc2 package not importable (optional extra sc2-harness)"
    return True, "sc2 importable"


def run_campaign_execution_preflight(
    *,
    contract_path: Path,
    campaign_root: Path,
    requested_visibility_mode: str = "hidden",
) -> tuple[bool, dict[str, Any]]:
    """M49 preflight plus M50 execution readiness checks."""

    ok, receipt = run_campaign_preflight(contract_path=contract_path)
    contract = _load_contract(contract_path)
    checks: list[dict[str, Any]] = list(receipt["checks"])

    def add(check_id: str, check_ok: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "detail": detail, "ok": check_ok})

    cap = resolve_visibility_posture_v1(requested=requested_visibility_mode)
    add(
        "m50_visibility_posture_resolution",
        True,
        f"requested={cap['requested_visibility_mode']} resolved={cap['resolved_visibility_mode']} "
        f"hidden_supported={cap['hidden_rollout_supported']}",
    )

    py_ok, py_det = _python_executable_check()
    add("m50_python_executable", py_ok, py_det)

    m45 = contract.get("m45_planned_bootstrap")
    rt = str(m45.get("runtime_mode", "")) if isinstance(m45, dict) else ""
    if rt == "local_live_sc2":
        sc_ok, sc_det = _sc2_import_check()
        add("m50_sc2_python_import", sc_ok, sc_det)
        probe = run_probe()
        root = probe.paths.get("root")
        maps = probe.paths.get("maps_dir")
        pres = probe.present
        add(
            "m50_sc2_root_present",
            bool(root and pres.get("root")),
            f"SC2 root={root!r} present={pres.get('root')}",
        )
        add(
            "m50_maps_dir_present",
            bool(maps and pres.get("maps_dir")),
            f"Maps dir={maps!r} present={pres.get('maps_dir')}",
        )
        try:
            mp = Path(m45["match_config_path"]) if isinstance(m45, dict) else None
            if mp is not None and mp.is_file():
                match_raw = json.loads(mp.read_text(encoding="utf-8"))
                if isinstance(match_raw, dict):
                    m_ok, m_det = _match_map_preflight(match_raw, maps_dir=maps)
                    add("m50_match_map_discoverability", m_ok, m_det)
                else:
                    add("m50_match_map_discoverability", False, "match config not an object")
            else:
                add("m50_match_map_discoverability", False, "match_config_path missing")
        except (OSError, json.JSONDecodeError) as e:
            add("m50_match_map_discoverability", False, str(e))

    out_lock = campaign_root / CAMPAIGN_OUTPUT_LOCK_BASENAME
    if out_lock.is_file():
        info = read_lock_file(out_lock)
        if info is not None:
            if lock_is_stale(info):
                add(
                    "m50_campaign_output_lock",
                    True,
                    f"stale lock file present (pid={info.pid} not running) — remove before execute",
                )
            else:
                add(
                    "m50_campaign_output_lock",
                    False,
                    f"active lock pid={info.pid} host={info.hostname}",
                )
        else:
            add("m50_campaign_output_lock", False, "unparseable campaign output lock file")
    else:
        add("m50_campaign_output_lock", True, "no campaign output lock file")

    cruns = campaign_root / "campaign_runs"
    if cruns.is_dir():
        subdirs = [p for p in cruns.iterdir() if p.is_dir()]
        add(
            "m50_campaign_runs_dir_exists",
            True,
            f"campaign_runs/ present with {len(subdirs)} entries (informational)",
        )
    else:
        add("m50_campaign_runs_dir_exists", True, "campaign_runs/ not yet created (ok)")

    try:
        verify_campaign_contract_seal(contract)
        add("m50_contract_seal_repeat", True, "seal verified for execution preflight")
    except ValueError as e:
        add("m50_contract_seal_repeat", False, str(e))

    receipt["checks"] = checks
    receipt["execution_readiness_note"] = EXECUTION_PREFLIGHT_RECEIPT_NOTE
    receipt["preflight_ok"] = ok and all(bool(c.get("ok")) for c in checks)
    return bool(receipt["preflight_ok"]), receipt
