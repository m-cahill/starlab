"""V15-M61 — release-lock proof-pack and showcase video capture manifest IO."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.m60_showcase_evidence_lock_decision_models import (
    DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED,
    LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY,
    NEXT_ROUTE_M61_RELEASE_LOCK,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
)
from starlab.v15.m61_release_lock_proof_pack_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CAPTURE_STATUS_FIXTURE_NO_VIDEO,
    CAPTURE_STATUS_OPERATOR_CAPTURED,
    CONTRACT_ID,
    CONTRACT_ID_CAPTURE_MANIFEST,
    CONTRACT_ID_REPORT,
    FILENAME_CAPTURE_CHECKLIST_MD,
    FILENAME_CAPTURE_MANIFEST_JSON,
    FILENAME_PROOF_PACK_JSON,
    FILENAME_PROOF_PACK_MD,
    FILENAME_PROOF_PACK_REPORT_JSON,
    FIXTURE_PLACEHOLDER_SHA256,
    MILESTONE,
    NON_CLAIMS,
    PROFILE_ID,
    RELEASE_LOCK_STATUS_FIXTURE,
    SCOPE_BOUNDED_SHOWCASE,
    SESSION_SOURCES_ALLOWED,
    STRONGEST_ALLOWED_CLAIM,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")

_OVERCLAIM_KEYS: Final[frozenset[str]] = frozenset(
    (
        "benchmark_passed",
        "strength_evaluated",
        "checkpoint_promoted",
        "v2_authorized",
        "v2_recharter_authorized",
        "seventy_two_hour_authorized",
        "human_panel_claim_authorized",
        "ladder_public_performance_claim_authorized",
    )
)

_FORBIDDEN_METADATA: Final[tuple[str, ...]] = (
    "checkpoint_path",
    "private_path",
    "operator_absolute_path",
    "company_secrets",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _norm_sha(s: str) -> str:
    return str(s or "").strip().lower()


def validate_hex64(label: str, value: object) -> tuple[bool, str]:
    v = _norm_sha(str(value or ""))
    if not _HEX64.match(v):
        return False, f"{label} must be a 64-char lowercase hex SHA-256"
    return True, ""


def scan_overclaim_true(obj: object) -> str | None:
    """Return error if any overclaim key is truthy in nested structure."""

    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k) in _OVERCLAIM_KEYS and v is True:
                return f"overclaim forbidden: {k!r} must not be true"
            err = scan_overclaim_true(v)
            if err:
                return err
    elif isinstance(obj, list):
        for item in obj:
            err = scan_overclaim_true(item)
            if err:
                return err
    return None


def declared_metadata_forbidden(blob: dict[str, Any]) -> str | None:
    def walk(o: object) -> str | None:
        if isinstance(o, dict):
            for k, v in o.items():
                lk = str(k).lower()
                if any(fk in lk for fk in _FORBIDDEN_METADATA):
                    return f"forbidden key in metadata: {k!r}"
                err = walk(v)
                if err:
                    return err
        elif isinstance(o, list):
            for it in o:
                err = walk(it)
                if err:
                    return err
        elif isinstance(o, str):
            low = o.lower()
            if "company_secrets" in low:
                return "metadata must not reference company_secrets"
            if "docs/company_secrets" in low:
                return "metadata must not reference docs/company_secrets"
            if "\\company_secrets" in low.replace("/", "\\"):
                return "metadata must not reference company_secrets paths"
            if "..\\" in o or "../" in o:
                return "metadata must not contain path traversal"
            if _looks_absolute_or_unc_path(o):
                return "paths must be redacted or relative, not absolute"
        return None

    return walk(blob)


def _looks_absolute_or_unc_path(s: str) -> bool:
    t = s.strip()
    if not t:
        return False
    if t.startswith("\\\\"):
        return True
    if len(t) >= 2 and t[1] == ":" and t[0].isalpha():
        return True
    if t.startswith("/") and not t.startswith("//"):
        # Unix absolute — disallow (operator should use relative/redacted)
        return True
    return False


def validate_m60_lock_decision_for_m61(blob: dict[str, Any]) -> tuple[bool, str]:
    if str(blob.get("contract_id") or "") != "starlab.v15.m60.showcase_evidence_lock_decision.v1":
        return False, "m60 contract_id mismatch"
    if str(blob.get("decision_status") or "") != DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED:
        return False, "m60 decision_status must be showcase_lock_recommended"
    ld = blob.get("lock_decision")
    if not isinstance(ld, dict):
        return False, "m60 lock_decision missing"
    if str(ld.get("lock_scope") or "") != LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY:
        return False, "m60 lock_scope must be bounded_showcase_evidence_package_only"
    if str(ld.get("next_route") or "") != NEXT_ROUTE_M61_RELEASE_LOCK:
        return False, "m60 next_route must be route_to_v15_m61_release_lock_proof_pack_update"
    if str(ld.get("next_route_status") or "") != ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED:
        return False, "m60 next_route_status must be recommended_not_executed"
    return True, ""


def load_m60_path(path: Path) -> tuple[bool, str, dict[str, Any] | None]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, str(exc), None
    if not isinstance(raw, dict):
        return False, "m60 json root must be object", None
    ok, err = validate_m60_lock_decision_for_m61(raw)
    if not ok:
        return False, err, None
    return True, "", raw


def _m60_upstream_summary(m60: dict[str, Any]) -> dict[str, Any]:
    raw_ld = m60.get("lock_decision")
    ld: dict[str, Any] = raw_ld if isinstance(raw_ld, dict) else {}
    return {
        "status": "closed",
        "decision_status": m60.get("decision_status"),
        "lock_scope": ld.get("lock_scope"),
        "next_route": ld.get("next_route"),
        "route_status": ld.get("next_route_status"),
    }


def _fixture_upstream_m60() -> dict[str, Any]:
    return {
        "status": "closed",
        "decision_status": DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED,
        "lock_scope": LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY,
        "next_route": NEXT_ROUTE_M61_RELEASE_LOCK,
        "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    }


def _evidence_chain() -> dict[str, Any]:
    return {
        "m53_training_execution": "closed_training_execution_evidence_only",
        "m54_package_readiness": "closed_package_readiness_only",
        "m55_m56_preflight_readout": "closed_bounded_readout_only",
        "m57a_visual_watch": "closed_watchability_observation_only",
        "m58_adapter_smoke": "closed_bounded_adapter_smoke_only",
        "m59_overclaim_refusal": "closed_benchmark_overclaim_refusal",
        "m60_lock_decision": "closed_showcase_lock_recommended",
    }


def _fixture_claim_flags(*, release_lock_executed: bool) -> dict[str, bool]:
    return {
        "release_lock_executed": release_lock_executed,
        "benchmark_passed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "ladder_public_performance_claim_authorized": False,
        "human_panel_claim_authorized": False,
        "seventy_two_hour_authorized": False,
        "v2_authorized": False,
        "v2_recharter_authorized": False,
    }


def build_fixture_capture_manifest_body() -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID_CAPTURE_MANIFEST,
        "milestone": MILESTONE,
        "capture_status": CAPTURE_STATUS_FIXTURE_NO_VIDEO,
        "capture_method": "fixture_schema_only_no_video",
        "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        "video_file": {
            "storage_posture": "operator_local_not_committed",
            "relative_or_redacted_path": "fixture/no_video",
            "sha256": FIXTURE_PLACEHOLDER_SHA256,
            "duration_seconds": "n/a_fixture",
            "format": "mp4",
        },
        "replay_file": {
            "storage_posture": "operator_local_not_committed",
            "relative_or_redacted_path": "fixture/no_replay",
            "sha256": FIXTURE_PLACEHOLDER_SHA256,
        },
        "sc2_context": {
            "map": "Waterfall",
            "opponent_or_baseline": "fixture_only",
            "session_source": "fixture_ci",
            "playback_speed": "n/a_fixture",
            "slow_watchability_mode": True,
        },
        "non_claims": [
            "not_benchmark_execution",
            "not_benchmark_pass_fail",
            "not_strength_evaluation",
            "not_checkpoint_promotion",
            "not_ladder_claim",
            "not_human_panel_claim",
            "not_v2_authorization",
        ],
    }


def validate_capture_manifest(
    blob: dict[str, Any],
    *,
    require_operator_capture: bool,
) -> tuple[bool, str]:
    if str(blob.get("contract_id") or "") != CONTRACT_ID_CAPTURE_MANIFEST:
        return False, "capture manifest contract_id mismatch"
    if str(blob.get("milestone") or "") != MILESTONE:
        return False, "capture manifest milestone mismatch"
    cand = _norm_sha(str(blob.get("candidate_checkpoint_sha256") or ""))
    if cand != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        return False, "candidate_checkpoint_sha256 mismatch"
    oc = scan_overclaim_true(blob)
    if oc:
        return False, oc
    fm = declared_metadata_forbidden(blob)
    if fm:
        return False, fm

    cap = str(blob.get("capture_status") or "")
    if cap == CAPTURE_STATUS_FIXTURE_NO_VIDEO:
        if require_operator_capture:
            return False, "operator path requires capture_status operator_video_captured"
        return True, ""

    if cap != CAPTURE_STATUS_OPERATOR_CAPTURED:
        return False, "invalid capture_status"

    vf = blob.get("video_file")
    rf = blob.get("replay_file")
    if not isinstance(vf, dict) or not isinstance(rf, dict):
        return False, "video_file and replay_file must be objects"
    vsha = vf.get("sha256")
    rsha = rf.get("sha256")
    ok, err = validate_hex64("video_file.sha256", vsha)
    if not ok:
        return False, err
    ok, err = validate_hex64("replay_file.sha256", rsha)
    if not ok:
        return False, err
    if vsha == FIXTURE_PLACEHOLDER_SHA256 or rsha == FIXTURE_PLACEHOLDER_SHA256:
        return False, "operator capture must not use fixture placeholder hashes"
    if str(vf.get("storage_posture") or "") != "operator_local_not_committed":
        return False, "video_file.storage_posture must be operator_local_not_committed"
    if str(rf.get("storage_posture") or "") != "operator_local_not_committed":
        return False, "replay_file.storage_posture must be operator_local_not_committed"

    sc = blob.get("sc2_context")
    if not isinstance(sc, dict):
        return False, "sc2_context must be object"
    ss = str(sc.get("session_source") or "")
    if require_operator_capture:
        if ss not in SESSION_SOURCES_ALLOWED:
            return False, "sc2_context.session_source must be an allowed operator value"
    elif ss:
        extended = set(SESSION_SOURCES_ALLOWED) | {"fixture_ci"}
        if ss not in extended:
            return False, "sc2_context.session_source not in allowed vocabulary"

    return True, ""


def summarize_showcase_from_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    raw_vf = manifest.get("video_file")
    raw_rf = manifest.get("replay_file")
    raw_sc = manifest.get("sc2_context")
    vf: dict[str, Any] = raw_vf if isinstance(raw_vf, dict) else {}
    rf: dict[str, Any] = raw_rf if isinstance(raw_rf, dict) else {}
    sc: dict[str, Any] = raw_sc if isinstance(raw_sc, dict) else {}
    return {
        "capture_manifest_contract_id": CONTRACT_ID_CAPTURE_MANIFEST,
        "capture_status": manifest.get("capture_status"),
        "video_artifact_status": "operator_local_not_committed",
        "video_file_sha256": vf.get("sha256"),
        "replay_sha256": rf.get("sha256"),
        "capture_method": manifest.get("capture_method"),
        "playback_speed": sc.get("playback_speed"),
        "watchability_pacing": "human_watchable",
        "session_source": sc.get("session_source"),
        "map": sc.get("map"),
    }


def build_proof_pack_body(
    *,
    upstream_m60: dict[str, Any],
    capture_manifest: dict[str, Any],
    release_lock_executed: bool,
    release_lock_status: str,
) -> dict[str, Any]:
    summ = summarize_showcase_from_manifest(capture_manifest)
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_ID,
        "milestone": MILESTONE,
        "upstream_m60": upstream_m60,
        "release_lock": {
            "release_lock_status": release_lock_status,
            "release_lock_scope": SCOPE_BOUNDED_SHOWCASE,
            "proof_pack_updated": True,
            "showcase_video_manifest_bound": True,
        },
        "candidate": {
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "promotion_status": "not_promoted_candidate_only",
        },
        "evidence_chain": _evidence_chain(),
        "showcase_video": summ,
        "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM,
        "claim_flags": _fixture_claim_flags(release_lock_executed=release_lock_executed),
        "non_claims": list(NON_CLAIMS),
    }


def build_fixture_proof_pack_body() -> dict[str, Any]:
    cap = build_fixture_capture_manifest_body()
    body = build_proof_pack_body(
        upstream_m60=_fixture_upstream_m60(),
        capture_manifest=cap,
        release_lock_executed=False,
        release_lock_status=RELEASE_LOCK_STATUS_FIXTURE,
    )
    return body


def build_proof_pack_report(
    body: dict[str, Any],
    *,
    emitter_profile: str | None = None,
    m60_digest: str | None = None,
    manifest_digest: str | None = None,
) -> dict[str, Any]:
    rep: dict[str, Any] = {
        "contract_id": CONTRACT_ID_REPORT,
        "milestone": MILESTONE,
        "emitter_profile": emitter_profile,
        "summary": {
            "release_lock": body.get("release_lock"),
            "showcase_video": body.get("showcase_video"),
            "claim_flags": body.get("claim_flags"),
            "strongest_allowed_claim": body.get("strongest_allowed_claim"),
        },
        "non_claims": body.get("non_claims"),
        "proof_pack_canonical_sha256": sha256_hex_of_canonical_json(body),
    }
    if m60_digest:
        rep["validated_m60_decision_canonical_sha256"] = m60_digest
    if manifest_digest:
        rep["validated_capture_manifest_canonical_sha256"] = manifest_digest
    return rep


def render_proof_pack_markdown(body: dict[str, Any]) -> str:
    raw_sv = body.get("showcase_video")
    sv: dict[str, Any] = raw_sv if isinstance(raw_sv, dict) else {}
    lines = [
        "# V15-M61 — v1.5 Release-Lock / Showcase Video Proof Pack",
        "",
        f"**Milestone:** `{body.get('milestone')}`",
        f"**Contract:** `{body.get('contract_id')}`",
        "",
        "## Candidate",
        "",
        f"- **Checkpoint SHA-256:** `{CANONICAL_CANDIDATE_CHECKPOINT_SHA256}`",
        "- **Promotion:** not promoted (candidate only)",
        "",
        "## Evidence chain (summary)",
        "",
        "- **M53:** 12-hour training execution evidence (closed)",
        "- **M54:** package / evaluation readiness (closed)",
        "- **M55/M56:** bounded preflight and readout (closed)",
        "- **M57A/M58:** watchability / bounded adapter smoke (closed)",
        "- **M59:** benchmark overclaim refusal (closed)",
        "- **M60:** showcase lock recommended (closed)",
        "",
        "## Showcase video evidence",
        "",
        f"- **Capture status:** `{sv.get('capture_status')}`",
        f"- **Capture method:** `{sv.get('capture_method')}`",
        f"- **Session source:** `{sv.get('session_source')}`",
        f"- **Map:** `{sv.get('map')}`",
        f"- **Video SHA-256:** `{sv.get('video_file_sha256')}`",
        f"- **Replay SHA-256:** `{sv.get('replay_sha256')}`",
        "- **Storage posture:** operator-local / not committed to Git",
        "",
        "### Non-claims (video)",
        "",
        (
            "Demonstration evidence only. Not benchmark pass/fail. Not ladder claim. "
            "Not strength evaluation. Candidate checkpoint not promoted by this video."
        ),
        "",
        "## Strongest allowed claim",
        "",
        str(body.get("strongest_allowed_claim") or ""),
        "",
        "## Explicit non-claims",
        "",
    ]
    for nc in body.get("non_claims") or []:
        lines.append(f"- {nc}")
    lines.extend(
        [
            "",
            "## Next options",
            "",
            (
                "- **V15-M62+:** decision fork — 72-hour charter vs v2 recharter "
                "(not opened automatically)."
            ),
            "- Not framed as “first 12-hour run.” Not automatic execution.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def render_capture_checklist() -> str:
    return """# V15-M61 — Showcase video capture checklist (operator)

1. Use the latest candidate checkpoint SHA:
   `7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90`
2. Run or reuse a governed visual/watchability session that saves replay metadata.
3. Open the replay in SC2 (preferred: replay-first capture).
4. Set playback speed to a human-watchable pace.
5. Record 2–5 minutes of curated video (screen recording).
6. Include title and/or end card with non-claims.
7. Hash the video file: `sha256sum <video.mp4>` or PowerShell
   `Get-FileHash <video.mp4> -Algorithm SHA256`.
8. Hash the replay file similarly.
9. Emit the V15-M61 capture manifest and proof pack
   (`operator_declared` or `operator_release_lock`).
10. Do **not** commit raw video, replay blobs, large checkpoints, or `docs/company_secrets/` to Git.

**Classification:** showcase video capture only — not benchmark execution, not strength
evaluation, not new training, not checkpoint promotion.
"""


def write_m61_artifacts(
    output_dir: Path,
    *,
    body: dict[str, Any],
    capture_manifest: dict[str, Any],
    emitter_profile: str | None = None,
    m60_digest: str | None = None,
    manifest_digest: str | None = None,
) -> tuple[Path, Path, Path, Path, Path]:
    out = output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pp = out / FILENAME_PROOF_PACK_JSON
    pr = out / FILENAME_PROOF_PACK_REPORT_JSON
    pm = out / FILENAME_PROOF_PACK_MD
    cm = out / FILENAME_CAPTURE_MANIFEST_JSON
    ck = out / FILENAME_CAPTURE_CHECKLIST_MD
    pp.write_text(canonical_json_dumps(body), encoding="utf-8")
    pr.write_text(
        canonical_json_dumps(
            build_proof_pack_report(
                body,
                emitter_profile=emitter_profile,
                m60_digest=m60_digest,
                manifest_digest=manifest_digest,
            )
        ),
        encoding="utf-8",
    )
    pm.write_text(render_proof_pack_markdown(body), encoding="utf-8")
    cm.write_text(canonical_json_dumps(capture_manifest), encoding="utf-8")
    ck.write_text(render_capture_checklist(), encoding="utf-8")
    return pp, pr, pm, cm, ck
