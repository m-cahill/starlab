"""Tests for V15-M61 release-lock proof pack and capture manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from starlab.v15.emit_v15_m60_showcase_evidence_lock_decision import main as emit_m60_main
from starlab.v15.emit_v15_m61_release_lock_proof_pack import main as emit_m61_main
from starlab.v15.m60_showcase_evidence_lock_decision_models import (
    FILENAME_DECISION_JSON as M60_DECISION,
)
from starlab.v15.m60_showcase_evidence_lock_decision_models import (
    PROFILE_FIXTURE_CI as M60_PROFILE_FIXTURE,
)
from starlab.v15.m61_release_lock_proof_pack_io import (
    declared_metadata_forbidden,
    validate_capture_manifest,
    validate_m60_lock_decision_for_m61,
)
from starlab.v15.m61_release_lock_proof_pack_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CAPTURE_STATUS_FIXTURE_NO_VIDEO,
    CAPTURE_STATUS_OPERATOR_CAPTURED,
    CONTRACT_ID,
    CONTRACT_ID_CAPTURE_MANIFEST,
    FILENAME_PROOF_PACK_JSON,
    FILENAME_PROOF_PACK_REPORT_JSON,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    PROFILE_OPERATOR_RELEASE_LOCK,
    RELEASE_LOCK_STATUS_PREFLIGHT,
)


def _synthetic_capture_manifest() -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID_CAPTURE_MANIFEST,
        "milestone": "V15-M61",
        "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        "capture_status": CAPTURE_STATUS_OPERATOR_CAPTURED,
        "capture_method": "replay_playback_screen_recording",
        "video_file": {
            "storage_posture": "operator_local_not_committed",
            "relative_or_redacted_path": "showcase_video/demo.mp4",
            "sha256": "a" * 64,
            "duration_seconds": "180",
            "format": "mp4",
        },
        "replay_file": {
            "storage_posture": "operator_local_not_committed",
            "relative_or_redacted_path": "showcase_video/demo.SC2Replay",
            "sha256": "b" * 64,
        },
        "sc2_context": {
            "map": "Waterfall",
            "opponent_or_baseline": "declared_smoke_opponent",
            "session_source": "existing_m57a_replay",
            "playback_speed": "0.5x",
            "slow_watchability_mode": True,
        },
        "non_claims": ["not_benchmark_execution"],
    }


def test_fixture_emits_contract_and_capture_status(tmp_path: Path) -> None:
    out = tmp_path / "o"
    assert emit_m61_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)]) == 0
    raw_pp = (out / FILENAME_PROOF_PACK_JSON).read_text(encoding="utf-8")
    blob = cast(dict[str, Any], json.loads(raw_pp))
    assert blob["contract_id"] == CONTRACT_ID
    sv = cast(dict[str, Any], blob["showcase_video"])
    assert sv["capture_status"] == CAPTURE_STATUS_FIXTURE_NO_VIDEO
    flags = cast(dict[str, Any], blob["claim_flags"])
    assert flags["benchmark_passed"] is False
    assert flags["strength_evaluated"] is False
    assert flags["checkpoint_promoted"] is False
    assert flags["seventy_two_hour_authorized"] is False
    assert flags["v2_authorized"] is False
    assert flags["release_lock_executed"] is False


def test_operator_declared_binds_manifest(tmp_path: Path) -> None:
    m60d = tmp_path / "m60"
    assert emit_m60_main(["--profile", M60_PROFILE_FIXTURE, "--output-dir", str(m60d)]) == 0
    m60_p = m60d / M60_DECISION
    man_p = tmp_path / "cap.json"
    man_p.write_text(json.dumps(_synthetic_capture_manifest()), encoding="utf-8")
    out = tmp_path / "out"
    rc = emit_m61_main(
        [
            "--profile",
            PROFILE_OPERATOR_DECLARED,
            "--output-dir",
            str(out),
            "--m60-lock-decision-json",
            str(m60_p),
            "--showcase-video-capture-manifest-json",
            str(man_p),
        ],
    )
    assert rc == 0
    raw_pp = (out / FILENAME_PROOF_PACK_JSON).read_text(encoding="utf-8")
    blob = cast(dict[str, Any], json.loads(raw_pp))
    assert blob["claim_flags"]["release_lock_executed"] is True
    sv = cast(dict[str, Any], blob["showcase_video"])
    assert "video_file_sha256" in sv
    assert sv["video_file_sha256"] == "a" * 64
    rl = cast(dict[str, Any], blob["release_lock"])
    assert rl["showcase_video_manifest_bound"] is True
    raw_rep = (out / FILENAME_PROOF_PACK_REPORT_JSON).read_text(encoding="utf-8")
    rep = cast(dict[str, Any], json.loads(raw_rep))
    assert "validated_m60_decision_canonical_sha256" in rep


def test_operator_release_lock_requires_dual_guards(tmp_path: Path) -> None:
    m60d = tmp_path / "m60"
    emit_m60_main(["--profile", M60_PROFILE_FIXTURE, "--output-dir", str(m60d)])
    man_p = tmp_path / "cap.json"
    man_p.write_text(json.dumps(_synthetic_capture_manifest()), encoding="utf-8")
    base = [
        "--profile",
        PROFILE_OPERATOR_RELEASE_LOCK,
        "--output-dir",
        str(tmp_path / "o"),
        "--m60-lock-decision-json",
        str(m60d / M60_DECISION),
        "--showcase-video-capture-manifest-json",
        str(man_p),
    ]
    assert emit_m61_main(base) == 2
    assert (
        emit_m61_main(
            base
            + [
                "--allow-operator-local-execution",
                "--authorize-v15-release-lock",
            ],
        )
        == 0
    )


def test_refuse_overclaim_in_manifest(tmp_path: Path) -> None:
    m60d = tmp_path / "m60"
    emit_m60_main(["--profile", M60_PROFILE_FIXTURE, "--output-dir", str(m60d)])
    bad = _synthetic_capture_manifest()
    bad["benchmark_passed"] = True
    man_p = tmp_path / "bad.json"
    man_p.write_text(json.dumps(bad), encoding="utf-8")
    assert (
        emit_m61_main(
            [
                "--profile",
                PROFILE_OPERATOR_DECLARED,
                "--output-dir",
                str(tmp_path / "o"),
                "--m60-lock-decision-json",
                str(m60d / M60_DECISION),
                "--showcase-video-capture-manifest-json",
                str(man_p),
            ],
        )
        == 2
    )


def test_invalid_m60_exit_2(tmp_path: Path) -> None:
    bad = tmp_path / "bad60.json"
    bad.write_text("{}", encoding="utf-8")
    man_p = tmp_path / "cap.json"
    man_p.write_text(json.dumps(_synthetic_capture_manifest()), encoding="utf-8")
    assert (
        emit_m61_main(
            [
                "--profile",
                PROFILE_OPERATOR_DECLARED,
                "--output-dir",
                str(tmp_path / "o"),
                "--m60-lock-decision-json",
                str(bad),
                "--showcase-video-capture-manifest-json",
                str(man_p),
            ],
        )
        == 2
    )


def test_operator_preflight_release_lock_not_executed(tmp_path: Path) -> None:
    m60d = tmp_path / "m60"
    emit_m60_main(["--profile", M60_PROFILE_FIXTURE, "--output-dir", str(m60d)])
    man_p = tmp_path / "cap.json"
    man_p.write_text(json.dumps(_synthetic_capture_manifest()), encoding="utf-8")
    out = tmp_path / "pf"
    assert (
        emit_m61_main(
            [
                "--profile",
                PROFILE_OPERATOR_PREFLIGHT,
                "--output-dir",
                str(out),
                "--m60-lock-decision-json",
                str(m60d / M60_DECISION),
                "--showcase-video-capture-manifest-json",
                str(man_p),
            ],
        )
        == 0
    )
    raw_pp = (out / FILENAME_PROOF_PACK_JSON).read_text(encoding="utf-8")
    blob = cast(dict[str, Any], json.loads(raw_pp))
    assert blob["claim_flags"]["release_lock_executed"] is False
    assert (
        cast(dict[str, Any], blob["release_lock"])["release_lock_status"]
        == RELEASE_LOCK_STATUS_PREFLIGHT
    )


def test_fixture_determinism(tmp_path_factory: pytest.TempPathFactory) -> None:
    digests: list[str] = []
    for lab in ("a", "b"):
        base = tmp_path_factory.mktemp(lab)
        emit_m61_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(base / "e")])
        path_pp = base / "e" / FILENAME_PROOF_PACK_JSON
        blob = cast(dict[str, Any], json.loads(path_pp.read_text(encoding="utf-8")))
        digests.append(json.dumps(blob, sort_keys=True))
    assert digests[0] == digests[1]


def test_validate_capture_fixture_ok() -> None:
    from starlab.v15.m61_release_lock_proof_pack_io import build_fixture_capture_manifest_body

    m = build_fixture_capture_manifest_body()
    assert validate_capture_manifest(m, require_operator_capture=False) == (True, "")
    assert validate_capture_manifest(m, require_operator_capture=True)[0] is False


def test_declared_metadata_forbidden_absolute_path() -> None:
    m = _synthetic_capture_manifest()
    m["video_file"]["relative_or_redacted_path"] = "/abs/secret/demo.mp4"
    assert declared_metadata_forbidden(m) is not None


def test_m60_validation_helper_fixture_roundtrip() -> None:
    from starlab.v15.m60_showcase_evidence_lock_decision_io import build_fixture_decision_body

    b = build_fixture_decision_body()
    assert validate_m60_lock_decision_for_m61(b) == (True, "")


def test_synthetic_manifest_json_valid() -> None:
    json.dumps(_synthetic_capture_manifest())
