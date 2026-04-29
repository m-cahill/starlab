"""V15-M33: validate M32 chain, SHA checkpoint blobs, optional CUDA inference probe."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m32_candidate_checkpoint_evaluation_execution_models import (
    CONTRACT_ID_M32_EVAL_EXEC,
    PROFILE_M32_BOUNDED,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M33_PROBE,
    EMITTER_MODULE_M33,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M32_EXECUTION_STATUSES_OK,
    MILESTONE_LABEL_M33,
    NON_CLAIMS_M33,
    PROFILE_M33_PROBE,
    RECOMMENDED_NEXT_LOADER_REMEDIATION,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_PROBE_COMPLETED,
    STATUS_REFUSED_BLOCKERS,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _blocked_sorted(reasons: list[str]) -> list[str]:
    return sorted(dict.fromkeys(reasons))


def _canonical_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(GATE_ARTIFACT_DIGEST_FIELD)
    wo = {k: v for k, v in raw.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in or "").lower() == computed.lower()


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def load_m32_evaluation_execution_json(path: Path) -> dict[str, Any]:
    return _parse_json_object(path)


def validate_m32_for_m33(
    m32: dict[str, Any],
    *,
    expected_candidate_sha256: str,
) -> list[str]:
    blocked: list[str] = []
    exp = str(expected_candidate_sha256 or "").lower()
    if not _is_hex64(exp):
        blocked.append("blocked_candidate_checkpoint_sha_missing")

    if not _canonical_seal_ok(m32):
        blocked.append("blocked_invalid_m32_contract")

    if str(m32.get("contract_id", "")) != CONTRACT_ID_M32_EVAL_EXEC:
        blocked.append("blocked_invalid_m32_contract")

    if str(m32.get("profile", "")) != PROFILE_M32_BOUNDED:
        blocked.append("blocked_invalid_m32_contract")

    st = str(m32.get("execution_status") or "")
    if st not in M32_EXECUTION_STATUSES_OK:
        blocked.append("blocked_m32_claim_flags_inconsistent")

    must_be_false = (
        "benchmark_passed",
        "strength_evaluated",
        "checkpoint_promoted",
        "scorecard_execution_performed",
    )
    for k in must_be_false:
        if m32.get(k) is not False:
            blocked.append("blocked_m32_claim_flags_inconsistent")

    cand_o = m32.get("candidate_checkpoint")
    cand: dict[str, Any] = cand_o if isinstance(cand_o, dict) else {}
    cand_sha = str(cand.get("sha256") or "").lower()

    if not cand:
        blocked.append("blocked_m32_claim_flags_inconsistent")
    elif not _is_hex64(cand_sha):
        blocked.append("blocked_candidate_checkpoint_sha_missing")
    else:
        ps = cand.get("promotion_status")
        if ps is not None and str(ps) != "not_promoted_candidate_only":
            blocked.append("blocked_candidate_checkpoint_not_candidate_only")
        if _is_hex64(exp) and cand_sha != exp:
            blocked.append("blocked_m32_claim_flags_inconsistent")

    return _blocked_sorted(blocked)


def _non_claim_bools_probe(*, success: bool) -> dict[str, bool]:
    return {
        "training_performed": False,
        "benchmark_passed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "scorecard_execution_performed": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_or_t3_authorized": False,
        "long_gpu_run_authorized": False,
        "seventy_two_hour_run_authorized": False,
        "checkpoint_blob_io_performed": success,
        "candidate_model_loaded": success,
        "cuda_probe_performed": False,
        "inference_probe_performed": success,
    }


def seal_m33_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m33_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_checkpoint_model_load_cuda_probe_report",
        "report_version": "m33",
        "milestone": MILESTONE_LABEL_M33,
        "contract_id": CONTRACT_ID_M33_PROBE,
        "profile": PROFILE_M33_PROBE,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "probe_status": sealed.get("probe_status"),
        "blocked_reasons": sealed.get("blocked_reasons"),
    }


def build_m33_checklist_md(sealed: dict[str, Any]) -> str:
    br = sealed.get("blocked_reasons") or []
    st = str(sealed.get("probe_status", ""))
    ok = st == STATUS_PROBE_COMPLETED
    mk = "[x]" if ok else "[ ]"
    br_txt = ", ".join(str(x) for x in br) if br else "(none)"
    nc_raw = sealed.get("non_claims") or []
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return (
        "# V15-M33 — candidate checkpoint model-load / CUDA probe checklist\n\n"
        f"**`probe_status`:** `{st}`  \n"
        f"**`blocked_reasons`:** `{br_txt}`\n\n"
        "| Gate | Check |\n"
        "| --- | --- |\n"
        f"| P0 — M32 execution JSON valid + claim flags | {mk} |\n"
        f"| P1 — Checkpoint blob SHA matches expected | {mk} |\n"
        f"| P2 — Model load (M28/M29 checkpoint format) | {mk} |\n"
        f"| P3 — CUDA / inference probe (per device) | {mk} |\n\n"
        "## Non-claims\n\n"
        f"{nc_lines}\n\n"
        "M33 proves wiring only — not strength, benchmark pass, or promotion.\n"
    )


def build_fixture_m33_body() -> dict[str, Any]:
    nc = _non_claim_bools_probe(success=False)
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M33_PROBE,
        "milestone": MILESTONE_LABEL_M33,
        "profile": PROFILE_M33_PROBE,
        "emitter_module": EMITTER_MODULE_M33,
        "fixture_ci": True,
        "probe_status": STATUS_FIXTURE_SCHEMA_ONLY,
        "blocked_reasons": [],
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        "m32_execution_binding": {
            "binding_status": "fixture_ci_skipped_no_m32_file",
        },
        "candidate_checkpoint_sha256": "",
        "candidate_checkpoint_promotion_status": "",
        "checkpoint_blob_sha256_verified": False,
        "device_requested": "",
        "device_observed": "",
        "torch_version": "",
        "cuda_available": None,
        "cuda_device_name": "",
        "non_claims": list(NON_CLAIMS_M33),
        **nc,
    }
    return body


def _build_sequential_from_m28_state_dict(sd: dict[str, Any]) -> tuple[Any, list[str]]:
    """Rebuild `nn.Sequential` from M28 `model_state_dict` save format."""
    try:
        from torch import nn
    except ImportError:
        return None, ["blocked_torch_import_failed"]

    errs: list[str] = []
    w0 = sd.get("0.weight")
    b0 = sd.get("0.bias")
    w2 = sd.get("2.weight")
    b2 = sd.get("2.bias")
    if w0 is None or b0 is None or w2 is None or b2 is None:
        return None, ["blocked_checkpoint_format_unsupported"]
    if not all(hasattr(x, "shape") for x in (w0, b0, w2, b2)):
        return None, ["blocked_checkpoint_format_unsupported"]

    try:
        in_f = int(w0.shape[1])
        hid = int(w0.shape[0])
        if int(w2.shape[1]) != hid or int(w2.shape[0]) != 1:
            return None, ["blocked_checkpoint_format_unsupported"]
    except (TypeError, ValueError, IndexError):
        return None, ["blocked_missing_model_architecture_metadata"]

    model = nn.Sequential(
        nn.Linear(in_f, hid),
        nn.Tanh(),
        nn.Linear(hid, 1),
    )
    try:
        model.load_state_dict(sd)
    except Exception:
        return None, ["blocked_model_load_failed"]
    return model, errs


def run_torch_cuda_inference_probe(
    checkpoint_path: Path,
    *,
    device_requested: str,
) -> tuple[
    dict[str, Any],
    list[str],
]:
    """Load `.pt` blob (M28 format), run one forward pass; honor device."""
    telemetry: dict[str, Any] = {
        "torch_version": "",
        "cuda_available": None,
        "cuda_device_name": "",
        "device_requested": device_requested,
        "device_observed": "",
    }
    blockers: list[str] = []

    try:
        import torch
    except ImportError as exc:
        telemetry["device_observed"] = "torch_import_failed"
        blockers.append("blocked_torch_import_failed")
        telemetry["torch_version"] = f"import_error:{exc}"
        return telemetry, blockers

    telemetry["torch_version"] = str(getattr(torch, "__version__", ""))
    telemetry["cuda_available"] = bool(torch.cuda.is_available())
    if telemetry["cuda_available"]:
        try:
            telemetry["cuda_device_name"] = str(torch.cuda.get_device_name(0))
        except Exception:
            telemetry["cuda_device_name"] = "unknown"

    dev_req = str(device_requested or "cuda").lower()
    if dev_req == "cuda":
        if not torch.cuda.is_available():
            blockers.append("blocked_cuda_unavailable")
            telemetry["device_observed"] = "cuda_unavailable"
            return telemetry, blockers
        device = torch.device("cuda:0")
        telemetry["device_observed"] = "cuda"
    elif dev_req == "cpu":
        device = torch.device("cpu")
        telemetry["device_observed"] = "cpu"
    else:
        blockers.append("blocked_model_load_failed")
        telemetry["device_observed"] = f"unsupported_device:{dev_req}"
        return telemetry, blockers

    try:
        blob = torch.load(str(checkpoint_path), map_location="cpu", weights_only=True)
    except TypeError:
        blob = torch.load(str(checkpoint_path), map_location="cpu")
    except Exception:
        blockers.append("blocked_model_load_failed")
        return telemetry, blockers

    if not isinstance(blob, dict):
        blockers.append("blocked_checkpoint_format_unsupported")
        return telemetry, blockers
    sd = blob.get("model_state_dict")
    if not isinstance(sd, dict):
        blockers.append("blocked_checkpoint_format_unsupported")
        return telemetry, blockers

    model, err_list = _build_sequential_from_m28_state_dict(sd)
    if model is None:
        blockers.extend(err_list)
        return telemetry, blockers

    model = model.to(device=device, dtype=torch.float32)
    model.eval()
    lin0 = model[0]
    in_f = int(getattr(lin0, "in_features", 0))
    if in_f < 1:
        blockers.append("blocked_missing_model_architecture_metadata")
        return telemetry, blockers
    try:
        with torch.no_grad():
            x = torch.zeros(1, in_f, device=device, dtype=torch.float32)
            y = model(x)
            if y.shape != (1, 1):
                blockers.append("blocked_inference_probe_failed")
    except Exception:
        blockers.append("blocked_inference_probe_failed")

    return telemetry, _blocked_sorted(blockers)


def emit_m33_candidate_checkpoint_model_load_cuda_probe_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], Path, Path, Path]:
    body_pre = build_fixture_m33_body()
    sealed = seal_m33_body(redact_paths_in_value(body_pre))

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    rep = build_m33_report(sealed)
    chk = build_m33_checklist_md(sealed)

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M33 fixture emission leaked path patterns")

    return sealed, p_main, p_rep, p_chk


def emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
    output_dir: Path,
    *,
    m32: dict[str, Any],
    candidate_checkpoint_path: Path,
    expected_candidate_sha256: str,
    device_requested: str,
) -> tuple[dict[str, Any], Path, Path, Path]:
    blockers: list[str] = []

    exp = str(expected_candidate_sha256 or "").lower()
    blockers.extend(validate_m32_for_m33(m32, expected_candidate_sha256=exp))

    ck_path = candidate_checkpoint_path.resolve()
    sha_verified = False
    if not ck_path.is_file():
        blockers.append("blocked_candidate_checkpoint_missing")
    elif _is_hex64(exp):
        file_sha = sha256_hex_file(ck_path).lower()
        sha_verified = file_sha == exp
        if not sha_verified:
            blockers.append("blocked_candidate_checkpoint_sha_mismatch")

    m32_sha = str(m32.get(GATE_ARTIFACT_DIGEST_FIELD) or "").lower()
    m32_st = str(m32.get("execution_status") or "")
    cand_o = m32.get("candidate_checkpoint")
    cand: dict[str, Any] = cand_o if isinstance(cand_o, dict) else {}
    cand_promo = str(cand.get("promotion_status") or "not_promoted_candidate_only")

    telem: dict[str, Any] = {
        "torch_version": "",
        "cuda_available": None,
        "cuda_device_name": "",
        "device_requested": device_requested,
        "device_observed": "",
    }

    cuda_probe_done = False
    if not blockers:
        telem, run_block = run_torch_cuda_inference_probe(
            ck_path, device_requested=device_requested
        )
        blockers.extend(run_block)
        cuda_probe_done = (
            str(device_requested).lower() == "cuda"
            and not run_block
            and str(telem.get("device_observed")) == "cuda"
        )

    ready = len(blockers) == 0
    nc = _non_claim_bools_probe(success=ready)
    nc["cuda_probe_performed"] = bool(cuda_probe_done)
    if not ready:
        nc["checkpoint_blob_io_performed"] = False
        nc["candidate_model_loaded"] = False
        nc["inference_probe_performed"] = False

    if ready:
        probe_status = STATUS_PROBE_COMPLETED
        rec = RECOMMENDED_NEXT_SUCCESS
    else:
        probe_status = STATUS_REFUSED_BLOCKERS
        if (
            "blocked_checkpoint_format_unsupported" in blockers
            or "blocked_model_load_failed" in blockers
        ):
            rec = RECOMMENDED_NEXT_LOADER_REMEDIATION
        else:
            rec = RECOMMENDED_NEXT_SUCCESS

    body_pre: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M33_PROBE,
        "milestone": MILESTONE_LABEL_M33,
        "profile": PROFILE_M33_PROBE,
        "emitter_module": EMITTER_MODULE_M33,
        "fixture_ci": False,
        "probe_status": probe_status,
        "blocked_reasons": _blocked_sorted(blockers),
        "recommended_next": rec,
        "m32_execution_binding": {
            "artifact_sha256": m32_sha,
            "execution_status": m32_st,
            "profile": PROFILE_M32_BOUNDED,
            "m32_json_path_note": "operator_supplied_path_redacted",
        },
        "candidate_checkpoint_sha256": exp,
        "candidate_checkpoint_promotion_status": cand_promo,
        "checkpoint_blob_sha256_verified": sha_verified,
        "device_requested": device_requested,
        "device_observed": str(telem.get("device_observed") or ""),
        "torch_version": str(telem.get("torch_version") or ""),
        "cuda_available": telem.get("cuda_available"),
        "cuda_device_name": str(telem.get("cuda_device_name") or ""),
        "non_claims": list(NON_CLAIMS_M33),
        **nc,
    }

    red_body = redact_paths_in_value(body_pre)
    if not isinstance(red_body, dict):
        raise TypeError("redacted body must be dict")
    sealed = seal_m33_body(red_body)
    dump_probe = canonical_json_dumps(sealed) + canonical_json_dumps(build_m33_report(sealed))
    if emission_has_private_path_patterns(dump_probe):
        blockers2 = _blocked_sorted([*blockers, "blocked_private_path_leak_detected"])
        body_fail = dict(body_pre)
        body_fail["blocked_reasons"] = blockers2
        body_fail["probe_status"] = STATUS_REFUSED_BLOCKERS
        for k, v in _non_claim_bools_probe(success=False).items():
            body_fail[k] = v
        body_fail["cuda_probe_performed"] = False
        red_fail = redact_paths_in_value(body_fail)
        if not isinstance(red_fail, dict):
            raise TypeError("expected dict")
        sealed = seal_m33_body(red_fail)

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    rep = build_m33_report(sealed)
    chk = build_m33_checklist_md(sealed)

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M33 operator emission leaked path patterns")

    return sealed, p_main, p_rep, p_chk
