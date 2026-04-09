"""M18 perceptual bridge prototype tests (canonical state JSON only; no replay, no s2protocol)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.observation.observation_surface_inputs import (
    load_canonical_state,
    load_canonical_state_report,
)
from starlab.observation.observation_surface_pipeline import (
    materialize_observation_surface,
)
from starlab.observation.observation_surface_schema import validate_observation_surface_frame
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m18"


def test_materialize_matches_golden() -> None:
    state, err = load_canonical_state(FIX / "canonical_state.json")
    assert err is None and state is not None
    rep, rerr2 = load_canonical_state_report(FIX / "canonical_state_report.json")
    assert rerr2 is None and rep is not None

    obs, mat_report, _w = materialize_observation_surface(
        canonical_state=state,
        perspective_player_index=0,
        canonical_state_report=rep,
    )

    exp_o = json.loads(
        (FIX / "expected_observation_surface.json").read_text(encoding="utf-8"),
    )
    exp_r = json.loads(
        (FIX / "expected_observation_surface_report.json").read_text(encoding="utf-8"),
    )
    assert json.loads(canonical_json_dumps(obs)) == exp_o
    assert json.loads(canonical_json_dumps(mat_report)) == exp_r


def test_deterministic_repeat_emission() -> None:
    state, _ = load_canonical_state(FIX / "canonical_state.json")
    rep, _ = load_canonical_state_report(FIX / "canonical_state_report.json")
    assert state is not None and rep is not None
    o1, r1, _ = materialize_observation_surface(
        canonical_state=state,
        perspective_player_index=0,
        canonical_state_report=rep,
    )
    o2, r2, _ = materialize_observation_surface(
        canonical_state=state,
        perspective_player_index=0,
        canonical_state_report=rep,
    )
    assert sha256_hex_of_canonical_json(o1) == sha256_hex_of_canonical_json(o2)
    assert sha256_hex_of_canonical_json(r1) == sha256_hex_of_canonical_json(r2)


def test_invalid_perspective_raises() -> None:
    state, _ = load_canonical_state(FIX / "canonical_state.json")
    rep, _ = load_canonical_state_report(FIX / "canonical_state_report.json")
    assert state is not None and rep is not None
    with pytest.raises(ValueError, match="perspective_player_index"):
        materialize_observation_surface(
            canonical_state=state,
            perspective_player_index=99,
            canonical_state_report=rep,
        )


def test_report_hash_mismatch_raises() -> None:
    state, _ = load_canonical_state(FIX / "canonical_state.json")
    rep, _ = load_canonical_state_report(FIX / "canonical_state_report.json")
    assert state is not None and rep is not None
    bad = dict(rep)
    bad["canonical_state_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        materialize_observation_surface(
            canonical_state=state,
            perspective_player_index=0,
            canonical_state_report=bad,
        )


def test_materialize_without_canonical_state_report() -> None:
    state, _ = load_canonical_state(FIX / "canonical_state.json")
    assert state is not None
    obs, rep, _ = materialize_observation_surface(
        canonical_state=state,
        perspective_player_index=0,
        canonical_state_report=None,
    )
    assert validate_observation_surface_frame(obs) == []
    assert rep["provenance_crosscheck"]["canonical_state_report_supplied"] is False
    assert rep["provenance_crosscheck"]["canonical_state_report_hash_match"] is False
    assert rep["warnings"] == []


def test_emitted_observation_validates_schema() -> None:
    state, _ = load_canonical_state(FIX / "canonical_state.json")
    rep, _ = load_canonical_state_report(FIX / "canonical_state_report.json")
    assert state is not None and rep is not None
    obs, _, _ = materialize_observation_surface(
        canonical_state=state,
        perspective_player_index=0,
        canonical_state_report=rep,
    )
    assert validate_observation_surface_frame(obs) == []


def test_emit_cli_success(tmp_path: Path) -> None:
    from starlab.observation.emit_observation_surface import main

    out = tmp_path / "out"
    code = main(
        [
            "--canonical-state",
            str(FIX / "canonical_state.json"),
            "--perspective-player-index",
            "0",
            "--output-dir",
            str(out),
            "--canonical-state-report",
            str(FIX / "canonical_state_report.json"),
        ],
    )
    assert code == 0
    assert (out / "observation_surface.json").is_file()
    assert (out / "observation_surface_report.json").is_file()


def test_emit_cli_failure_bad_perspective(tmp_path: Path) -> None:
    from starlab.observation.emit_observation_surface import main

    out = tmp_path / "out2"
    code = main(
        [
            "--canonical-state",
            str(FIX / "canonical_state.json"),
            "--perspective-player-index",
            "7",
            "--output-dir",
            str(out),
        ],
    )
    assert code == 2


def test_m18_observation_modules_have_no_replay_imports() -> None:
    """Governance: M18 observation modules must not import replay stack."""

    repo = Path(__file__).resolve().parents[1]
    names = (
        "observation_surface_inputs.py",
        "observation_surface_derivation.py",
        "observation_surface_pipeline.py",
        "emit_observation_surface.py",
    )
    banned = ("starlab.replays", "s2protocol", "replay_raw_parse")
    for n in names:
        p = repo / "starlab" / "observation" / n
        text = p.read_text(encoding="utf-8")
        for b in banned:
            assert b not in text, f"{n} must not reference {b}"
