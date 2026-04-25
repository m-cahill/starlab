"""Build, seal, and write V15-M02 long GPU environment lock JSON + report."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_models import (
    CHECK_FAIL,
    CHECK_FIXTURE,
    CHECK_NOT_EVALUATED,
    CHECK_PASS,
    CONTRACT_ID_LONG_GPU_ENV,
    EMITTER_MODULE,
    EVIDENCE_CI_FIXTURE,
    EVIDENCE_NOT_EVALUATED,
    EVIDENCE_OPERATOR_DECLARED,
    EVIDENCE_OPERATOR_PROBE,
    FILENAME_LONG_GPU_ENV,
    MILESTONE_ID_V15_M02,
    NON_CLAIMS_V15_M02,
    PATH_LOGICAL_REFERENCE,
    PATH_PUBLIC_SAFE,
    PATH_REDACTED,
    PROBE_OPTIONAL_ROOT_KEYS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL,
    REPORT_FILENAME_LONG_GPU_ENV,
    REPORT_VERSION_LONG_GPU_ENV,
    STATUS_BLOCKED,
    STATUS_FIXTURE_ONLY,
    STATUS_OPERATOR_LOCAL_INCOMPLETE,
    STATUS_OPERATOR_LOCAL_READY,
    STATUS_VOCABULARY,
)

_SEAL_KEY: Final[str] = "long_gpu_environment_lock_sha256"

# Absolute path patterns for redaction in emitted operator-local artifacts
_WIN_ABS: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z]:[\\/].*")
_UNC: Final[re.Pattern[str]] = re.compile(r"^\\\\")
_UNIX_ABS: Final[re.Pattern[str]] = re.compile(r"^/[^/].*")  # /foo but not // or relative


def _is_probable_absolute_path(s: str) -> bool:
    t = s.strip()
    if len(t) < 3:
        return False
    if _WIN_ABS.match(t):
        return True
    if _UNC.match(t):
        return True
    if _UNIX_ABS.match(t) and not t.startswith("//"):
        return True
    return False


# Windows drive + path to end of token (no embedded newlines) — in-string redaction
_SUB_WIN_PATH: Final[re.Pattern[str]] = re.compile(r"(?<![A-Za-z0-9])([A-Za-z]:[\\/][^\"'\s,}\]]+)")


def _redact_path_substrings(s: str) -> str:
    if _is_probable_absolute_path(s):
        return "<REDACTED_ABSOLUTE_PATH>"
    if not any(c in s for c in (":\\", ":/", "/")):
        return s
    t = _SUB_WIN_PATH.sub("<REDACTED_ABSOLUTE_PATH>", s)
    # POSIX-like absolute segments /home/foo, /var/...
    t = re.sub(
        r"(?<![A-Za-z0-9])(/[^/\s\"']+[/][^\s\"']+)",
        "<REDACTED_ABSOLUTE_PATH>",
        t,
    )
    return t


def redact_paths_in_value(obj: Any) -> Any:
    """Redact likely absolute paths in nested JSON (operator-local emission)."""

    if isinstance(obj, dict):
        return {k: redact_paths_in_value(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_paths_in_value(x) for x in obj]
    if isinstance(obj, str):
        return _redact_path_substrings(obj)
    return obj


def _empty_section(repo: str) -> dict[str, Any]:
    return {
        "repo_identity": {
            "git_sha": "0000000000000000000000000000000000000000",
            "branch": "fixture",
            "dirty_tree_policy": "not_applicable",
            "repository": repo,
        },
        "python_environment": {
            "python_version": "3.11.x",
            "implementation": "cpython",
            "platform": "fixture",
            "venv_policy": "not_applicable",
        },
        "dependency_environment": {
            "requirements_source": "pyproject.toml",
            "lockfile_paths": [],
            "dependency_fingerprint": "fixture:deterministic",
            "pip_audit_status": "not_evaluated",
            "sbom_status": "not_evaluated",
        },
        "cuda_environment": {
            "cuda_available": False,
            "cuda_version": "not_applicable",
            "driver_version": "not_applicable",
            "nvidia_smi_status": "not_applicable",
        },
        "pytorch_environment": {
            "torch_installed": True,
            "torch_version": "pinned_in_pyproject",
            "torch_cuda_version": "not_evaluated",
            "cuda_device_count": 0,
        },
        "gpu_environment": {
            "gpu_present": False,
            "gpu_name": "not_applicable",
            "gpu_memory_total_bytes": None,
            "gpu_compute_capability": "not_applicable",
            "gpu_driver": "not_applicable",
        },
        "sc2_environment": {
            "sc2_client_declared": False,
            "sc2_version": "not_applicable",
            "sc2_path_disclosure": PATH_REDACTED,
            "sc2_probe_status": "not_applicable",
        },
        "map_pool_environment": {
            "map_pool_id": "not_applicable",
            "required_maps": [],
            "maps_present": False,
            "map_probe_status": "not_applicable",
        },
        "disk_environment": {
            "output_root_policy": "operator_local",
            "free_bytes_required": None,
            "free_bytes_observed": None,
            "disk_probe_status": "not_applicable",
        },
    }


def _operator_probe_base(repo: str) -> dict[str, Any]:
    """Neutral starting point for operator_local without contradictory fail signals."""

    return {
        "repo_identity": {
            "git_sha": "",
            "branch": "",
            "dirty_tree_policy": "not_evaluated",
            "repository": repo,
        },
        "python_environment": {
            "python_version": "",
            "implementation": "",
            "platform": "",
            "venv_policy": "not_evaluated",
        },
        "dependency_environment": {
            "requirements_source": "pyproject.toml",
            "lockfile_paths": [],
            "dependency_fingerprint": "",
            "pip_audit_status": "not_evaluated",
            "sbom_status": "not_evaluated",
        },
        "cuda_environment": {
            "cuda_available": None,
            "cuda_version": "not_applicable",
            "driver_version": "not_applicable",
            "nvidia_smi_status": "not_applicable",
        },
        "pytorch_environment": {
            "torch_installed": None,
            "torch_version": "",
            "torch_cuda_version": "not_applicable",
            "cuda_device_count": None,
        },
        "gpu_environment": {
            "gpu_present": None,
            "gpu_name": "",
            "gpu_memory_total_bytes": None,
            "gpu_compute_capability": "not_applicable",
            "gpu_driver": "not_applicable",
        },
        "sc2_environment": {
            "sc2_client_declared": None,
            "sc2_version": "not_applicable",
            "sc2_path_disclosure": PATH_REDACTED,
            "sc2_probe_status": "not_applicable",
        },
        "map_pool_environment": {
            "map_pool_id": "",
            "required_maps": [],
            "maps_present": None,
            "map_probe_status": "not_applicable",
        },
        "disk_environment": {
            "output_root_policy": "",
            "free_bytes_required": None,
            "free_bytes_observed": None,
            "disk_probe_status": "not_applicable",
        },
    }


REQUIRED_CHECK_SPECS: Final[tuple[dict[str, str], ...]] = (
    {"check_id": "repo_identity", "description": "git SHA and branch declared"},
    {"check_id": "python_environment", "description": "python version and platform declared"},
    {"check_id": "dependency_environment", "description": "dependency fingerprint present"},
    {
        "check_id": "cuda_operator_declared",
        "description": "CUDA / driver fields declared (operator)",
    },
    {
        "check_id": "pytorch_operator_declared",
        "description": "PyTorch and CUDA build fields declared (operator)",
    },
    {
        "check_id": "gpu_operator_declared",
        "description": "GPU identity fields declared when gpu_present (operator)",
    },
    {"check_id": "sc2_operator_declared", "description": "SC2 client version declared (operator)"},
    {
        "check_id": "map_pool_declared",
        "description": "Map pool and required maps declared (operator)",
    },
    {"check_id": "disk_posture_declared", "description": "Disk/output posture declared (operator)"},
)


def _is_nonempty_str(x: Any) -> bool:
    return (
        isinstance(x, str)
        and bool(x.strip())
        and x.strip()
        not in (
            "not_applicable",
            "not_evaluated",
        )
    )


def _eval_probe_readiness(sections: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    """
    Return (environment_lock_status, operator_local_ready, check_results) — third is check_results.
    """
    r = sections["repo_identity"]
    p = sections["python_environment"]
    d = sections["dependency_environment"]
    c = sections["cuda_environment"]
    t = sections["pytorch_environment"]
    g = sections["gpu_environment"]
    s = sections["sc2_environment"]
    m = sections["map_pool_environment"]
    disk = sections["disk_environment"]

    results: list[dict[str, Any]] = []

    def add(cid: str, st: str, detail: str) -> None:
        results.append({"check_id": cid, "check_status": st, "detail": detail})

    block = False
    gsha = str(r.get("git_sha", "")).strip()
    if _is_nonempty_str(gsha) and len(gsha) >= 7 and _is_nonempty_str(r.get("branch")):
        add("repo_identity", CHECK_PASS, "git_sha and branch present")
    else:
        add("repo_identity", CHECK_NOT_EVALUATED, "git_sha and/or branch incomplete")

    if _is_nonempty_str(p.get("python_version")) and _is_nonempty_str(p.get("platform")):
        add("python_environment", CHECK_PASS, "python version and platform present")
    else:
        add("python_environment", CHECK_NOT_EVALUATED, "python version or platform missing")

    if _is_nonempty_str(d.get("dependency_fingerprint")) and str(
        d.get("dependency_fingerprint")
    ) not in ("fixture:deterministic",):
        add("dependency_environment", CHECK_PASS, "non-fixture dependency_fingerprint")
    else:
        add(
            "dependency_environment",
            CHECK_NOT_EVALUATED,
            "dependency_fingerprint missing or fixture",
        )

    if c.get("cuda_version") and str(c.get("cuda_version")) not in (
        "not_applicable",
        "not_evaluated",
    ):
        add("cuda_operator_declared", CHECK_PASS, "cuda_version set")
    else:
        add("cuda_operator_declared", CHECK_NOT_EVALUATED, "cuda_version not set")

    if t.get("torch_version") and str(t.get("torch_version")) not in (
        "not_applicable",
        "not_evaluated",
        "pinned_in_pyproject",
    ):
        add("pytorch_operator_declared", CHECK_PASS, "torch_version set (operator)")
    else:
        add("pytorch_operator_declared", CHECK_NOT_EVALUATED, "torch_version not operator-declared")

    if g.get("gpu_present") is True and _is_nonempty_str(g.get("gpu_name")):
        add("gpu_operator_declared", CHECK_PASS, "GPU present and named")
    elif g.get("gpu_present") is False:
        add("gpu_operator_declared", CHECK_FAIL, "gpu_present false — blocked for long GPU run")
        block = True
    else:
        add("gpu_operator_declared", CHECK_NOT_EVALUATED, "gpu_present or gpu_name incomplete")

    if s.get("sc2_client_declared") is True and _is_nonempty_str(s.get("sc2_version")):
        add("sc2_operator_declared", CHECK_PASS, "SC2 client declared with version")
    elif s.get("sc2_client_declared") is False:
        add("sc2_operator_declared", CHECK_FAIL, "sc2 not declared")
        block = True
    else:
        add("sc2_operator_declared", CHECK_NOT_EVALUATED, "sc2 version incomplete")

    if _is_nonempty_str(m.get("map_pool_id")) and m.get("required_maps"):
        add("map_pool_declared", CHECK_PASS, "map pool and maps listed")
    else:
        add("map_pool_declared", CHECK_NOT_EVALUATED, "map pool incomplete")

    if (
        _is_nonempty_str(disk.get("output_root_policy"))
        and disk.get("free_bytes_required") is not None
    ):
        add("disk_posture_declared", CHECK_PASS, "output policy and size requirement set")
    else:
        add("disk_posture_declared", CHECK_NOT_EVALUATED, "disk fields incomplete")

    if block:
        return STATUS_BLOCKED, "false", results
    not_ev = [x for x in results if x["check_status"] == CHECK_NOT_EVALUATED]
    fail = [x for x in results if x["check_status"] == CHECK_FAIL]
    if fail:
        return STATUS_BLOCKED, "false", results
    if not_ev:
        return STATUS_OPERATOR_LOCAL_INCOMPLETE, "false", results
    return STATUS_OPERATOR_LOCAL_READY, "true", results


def _default_path_policy() -> dict[str, str]:
    return {
        "public_surface_rule": "no_absolute_paths_in_public_docs",
        "sc2_paths": PATH_REDACTED,
        "map_paths": PATH_LOGICAL_REFERENCE,
        "default_posture": PATH_LOGICAL_REFERENCE,
    }


def _fixture_check_results() -> list[dict[str, Any]]:
    return [
        {
            "check_id": s["check_id"],
            "check_status": CHECK_FIXTURE,
            "detail": "fixture_ci profile does not evaluate operator environment",
        }
        for s in REQUIRED_CHECK_SPECS
    ]


def build_environment_lock_body(
    profile: str,
    probe: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Canonical contract body (before seal) for a profile / optional operator probe."""

    if profile not in (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_LOCAL):
        raise ValueError(f"unknown profile: {profile!r}")

    probe = probe or {}
    if profile == PROFILE_FIXTURE_CI:
        sections = _empty_section("starlab")
        fpolicy = {**_default_path_policy(), "emission": PATH_PUBLIC_SAFE}
        return {
            "contract_id": CONTRACT_ID_LONG_GPU_ENV,
            "milestone_id": MILESTONE_ID_V15_M02,
            "generated_by": EMITTER_MODULE,
            "profile": PROFILE_FIXTURE_CI,
            "environment_lock_status": STATUS_FIXTURE_ONLY,
            "long_gpu_run_authorized": False,
            "operator_local_ready": False,
            "evidence_scope": EVIDENCE_CI_FIXTURE,
            "repo_identity": sections["repo_identity"],
            "python_environment": sections["python_environment"],
            "dependency_environment": sections["dependency_environment"],
            "cuda_environment": sections["cuda_environment"],
            "pytorch_environment": sections["pytorch_environment"],
            "gpu_environment": sections["gpu_environment"],
            "sc2_environment": sections["sc2_environment"],
            "map_pool_environment": sections["map_pool_environment"],
            "disk_environment": sections["disk_environment"],
            "path_disclosure_policy": fpolicy,
            "required_checks": [dict(s) for s in REQUIRED_CHECK_SPECS],
            "check_results": _fixture_check_results(),
            "status_vocabulary": {k: list(v) for k, v in STATUS_VOCABULARY.items()},
            "non_claims": list(NON_CLAIMS_V15_M02),
            "carry_forward_items": _carry_forward(),
            "m02_note": (
                "V15-M02 does not grant long-GPU-run authorization; "
                "long_gpu_run_authorized remains false for this milestone. "
                "A fixture-only lock is not an operator-local RTX 5090 environment lock."
            ),
            "operator_notes": None,
        }

    # operator_local: start from operator-neutral base, merge probe
    sections = _operator_probe_base("starlab")
    ev_scope = EVIDENCE_NOT_EVALUATED
    if "evidence_scope" in probe and isinstance(probe["evidence_scope"], str):
        ev_scope = probe["evidence_scope"]
    if ev_scope not in (
        EVIDENCE_OPERATOR_PROBE,
        EVIDENCE_OPERATOR_DECLARED,
        EVIDENCE_NOT_EVALUATED,
    ):
        ev_scope = EVIDENCE_NOT_EVALUATED

    for key in PROBE_OPTIONAL_ROOT_KEYS:
        if (
            key not in probe
            or key == "path_disclosure_policy"
            or key == "operator_notes"
            or key == "evidence_scope"
        ):
            continue
        if not isinstance(probe[key], dict):
            raise ValueError(f"probe.{key} must be a JSON object")
        merged = {**deepcopy(sections[key]), **probe[key]}
        sections[key] = merged

    disclosure_policy: dict[str, Any] = (
        {**_default_path_policy(), **probe["path_disclosure_policy"]}
        if isinstance(probe.get("path_disclosure_policy"), dict)
        else _default_path_policy()
    )

    st, _, check_results = _eval_probe_readiness(sections)
    if not check_results:
        check_results = []

    onotes = probe.get("operator_notes")
    op_notes: str | None
    if onotes is None:
        op_notes = None
    elif isinstance(onotes, str):
        op_notes = onotes
    else:
        raise ValueError("operator_notes must be a string or null")

    return {
        "contract_id": CONTRACT_ID_LONG_GPU_ENV,
        "milestone_id": MILESTONE_ID_V15_M02,
        "generated_by": EMITTER_MODULE,
        "profile": PROFILE_OPERATOR_LOCAL,
        "environment_lock_status": st,
        "long_gpu_run_authorized": False,
        "operator_local_ready": (st == STATUS_OPERATOR_LOCAL_READY),
        "evidence_scope": ev_scope,
        "path_disclosure_policy": disclosure_policy,
        "repo_identity": sections["repo_identity"],
        "python_environment": sections["python_environment"],
        "dependency_environment": sections["dependency_environment"],
        "cuda_environment": sections["cuda_environment"],
        "pytorch_environment": sections["pytorch_environment"],
        "gpu_environment": sections["gpu_environment"],
        "sc2_environment": sections["sc2_environment"],
        "map_pool_environment": sections["map_pool_environment"],
        "disk_environment": sections["disk_environment"],
        "operator_notes": op_notes,
        "required_checks": [dict(s) for s in REQUIRED_CHECK_SPECS],
        "check_results": check_results,
        "status_vocabulary": {k: list(v) for k, v in STATUS_VOCABULARY.items()},
        "non_claims": list(NON_CLAIMS_V15_M02),
        "carry_forward_items": _carry_forward(),
        "m02_note": (
            "V15-M02 does not grant long-GPU-run authorization; "
            "long_gpu_run_authorized remains false. "
            "Use operator_local_ready for probe completeness, not program authorization."
        ),
    }


def _carry_forward() -> list[dict[str, str]]:
    return [
        {
            "item_id": "pip_cve_2026_3219",
            "summary": (
                "pip-audit may require --ignore-vuln CVE-2026-3219 for the pip toolchain until "
                "PyPI publishes an audit-clean release; "
                "V15-M02 re-check 2026-04-25: still present on pip 26.0.1."
            ),
        },
        {
            "item_id": "checkpoint_lineage_m03",
            "summary": "V15-M03 — checkpoint lineage / resume; not M02.",
        },
    ]


def _validate_body_invariants(body: dict[str, Any]) -> None:
    assert body["contract_id"] == CONTRACT_ID_LONG_GPU_ENV
    assert body["milestone_id"] == MILESTONE_ID_V15_M02
    for k, vals in STATUS_VOCABULARY.items():
        assert set(body["status_vocabulary"][k]) == set(vals)
    assert body["long_gpu_run_authorized"] is False


def seal_environment_lock_body(body_no_seal: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_no_seal)
    return {**body_no_seal, _SEAL_KEY: digest}


def build_environment_lock_report(
    contract: dict[str, Any], *, emission_context: dict[str, Any] | None = None
) -> dict[str, Any]:
    digest = contract[_SEAL_KEY]
    rep: dict[str, Any] = {
        "report_version": REPORT_VERSION_LONG_GPU_ENV,
        "milestone_id": MILESTONE_ID_V15_M02,
        "contract_id": CONTRACT_ID_LONG_GPU_ENV,
        "long_gpu_environment_lock_sha256": digest,
        "profile": contract["profile"],
        "validation": {
            "contract_id_recognized": contract["contract_id"] == CONTRACT_ID_LONG_GPU_ENV,
            "seal_key_present": _SEAL_KEY in contract,
            "non_claims_count": len(contract["non_claims"]),
            "m02_never_authorizes_long_run": contract["long_gpu_run_authorized"] is False,
        },
    }
    if emission_context is not None:
        rep["emission_context"] = emission_context
    return rep


def write_environment_lock_artifacts(
    *,
    output_dir: Path,
    contract: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_LONG_GPU_ENV
    r_path = output_dir / REPORT_FILENAME_LONG_GPU_ENV
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def parse_probe_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("probe JSON must be a single object")
    unknown = set(raw) - PROBE_OPTIONAL_ROOT_KEYS
    if unknown:
        raise ValueError(f"unknown top-level keys in probe JSON: {sorted(unknown)}")
    return raw


def emit_long_gpu_environment_lock(
    output_dir: Path,
    *,
    profile: str,
    probe_path: Path | None = None,
    emission_context: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    probe: dict[str, Any] | None = None
    if probe_path is not None:
        probe = parse_probe_json(probe_path)
    body = build_environment_lock_body(profile, probe=probe)
    if profile == PROFILE_OPERATOR_LOCAL and probe is not None:
        body = redact_paths_in_value(body)
    _validate_body_invariants(body)
    sealed = seal_environment_lock_body(body)
    ctx = emission_context
    if ctx is None and profile == PROFILE_FIXTURE_CI:
        ctx = {"emission_mode": "fixture", "emission_context_note": "deterministic; no host paths"}
    rep = build_environment_lock_report(sealed, emission_context=ctx)
    c_path, r_path = write_environment_lock_artifacts(
        output_dir=output_dir, contract=sealed, report=rep
    )
    return sealed, rep, c_path, r_path
