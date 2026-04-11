"""M37: targeted coverage for core I/O and replay/observation helpers (no s2protocol)."""

from __future__ import annotations

import json
import runpy
import shutil
import sys
from pathlib import Path

import pytest
from starlab._io import JSON_ROOT_MUST_BE_OBJECT, load_json_object_strict, parse_json_object_text
from starlab.baselines.emit_heuristic_baseline_suite import main as emit_heuristic_baseline_main
from starlab.baselines.emit_scripted_baseline_suite import main as emit_scripted_baseline_main
from starlab.benchmarks.emit_benchmark_contracts import main as emit_benchmark_contracts_main
from starlab.evaluation.emit_baseline_evidence_pack import main as emit_baseline_evidence_pack_main
from starlab.evaluation.emit_evaluation_diagnostics import main as emit_evaluation_diagnostics_main
from starlab.evaluation.emit_evaluation_tournament import main as emit_evaluation_tournament_main
from starlab.evaluation.emit_learned_agent_evaluation import (
    main as emit_learned_agent_evaluation_main,
)
from starlab.explorer.emit_replay_explorer_surface import main as emit_replay_explorer_surface_main
from starlab.imitation.emit_replay_imitation_baseline import (
    main as emit_replay_imitation_baseline_main,
)
from starlab.imitation.emit_replay_training_dataset import main as emit_replay_training_dataset_main
from starlab.observation.observation_reconciliation_pipeline import emit_reconciliation_artifacts
from starlab.replays.build_order_economy_io import (
    exit_code_for_build_order_economy_run,
    extract_build_order_economy_from_paths,
)
from starlab.replays.combat_scouting_visibility_io import (
    exit_code_for_combat_scouting_visibility_run,
    extract_combat_scouting_visibility_from_paths,
)
from starlab.replays.combat_scouting_visibility_models import (
    COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION,
)
from starlab.replays.intake_cli import main as intake_cli_main
from starlab.replays.metadata_extraction import (
    core_metadata_ok,
    extract_players,
    extract_protocol_fields,
    player_rows_complete,
    required_sections_non_null,
)
from starlab.replays.metadata_io import (
    exit_code_for_extraction_status,
    extract_from_paths,
    write_metadata_artifacts,
)
from starlab.replays.parser_io import exit_code_for_parse_status, write_parse_artifacts
from starlab.replays.replay_bundle_io import (
    collect_secondary_reports_from_dir,
    exit_code_for_replay_bundle_run,
    extract_replay_bundle_from_paths,
    write_replay_bundle_artifacts,
)
from starlab.replays.replay_slice_generation_helpers import (
    combat_window_id,
    hex_eq,
    max_gameloop_from_timeline,
    metadata_max_loops_optional,
    optional_report_hash_required,
    overlap_build_steps,
    overlap_visibility_windows,
    primary_anchor_id,
    scouting_observation_id,
    slice_identity_payload_for_hash,
    validate_csv_contract,
)
from starlab.replays.replay_slice_io import (
    exit_code_for_replay_slice_run,
    extract_replay_slices_from_paths,
)
from starlab.replays.replay_slice_models import SLICE_KIND_COMBAT, SLICE_KIND_SCOUTING
from starlab.replays.timeline_io import (
    exit_code_for_timeline_run,
    extract_timeline_from_paths,
    write_timeline_artifacts,
)
from starlab.runs.replay_binding import compute_replay_content_sha256
from starlab.sc2.env_probe import main as env_probe_main
from starlab.sc2.evaluate_environment_drift import main as evaluate_environment_drift_main

FIX13 = Path(__file__).resolve().parent / "fixtures" / "m13"
FIX09 = Path(__file__).resolve().parent / "fixtures" / "m09"
FIX19 = Path(__file__).resolve().parent / "fixtures" / "m19"
FIX14 = Path(__file__).resolve().parent / "fixtures" / "m14"


def _materialize_m14_bundle_directory(dest: Path) -> None:
    """Minimal governed M14 bundle dir (shared with M26/M27 harness tests)."""

    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        "replay_metadata.json",
        "replay_timeline.json",
        "replay_build_order_economy.json",
        "replay_combat_scouting_visibility.json",
        "replay_slices.json",
        "replay_metadata_report.json",
        "replay_slices_report.json",
    ):
        shutil.copy(FIX14 / name, dest / name)
    shutil.copy(
        FIX14 / "expected_replay_bundle_manifest.json", dest / "replay_bundle_manifest.json"
    )
    shutil.copy(FIX14 / "expected_replay_bundle_lineage.json", dest / "replay_bundle_lineage.json")
    shutil.copy(
        FIX14 / "expected_replay_bundle_contents.json", dest / "replay_bundle_contents.json"
    )


M07_REPLAY = Path(__file__).resolve().parent / "fixtures" / "replay_m07_sample.SC2Replay"
PROBE_M06 = Path(__file__).resolve().parent / "fixtures" / "probe_m06_valid.json"
BENCH_FIXTURE_ONLY = (
    Path(__file__).resolve().parent / "fixtures" / "m20" / "valid_benchmark_contract.json"
)
FIX_M21D = Path(__file__).resolve().parent / "fixtures" / "m21"
FIX_M22D = Path(__file__).resolve().parent / "fixtures" / "m22"
FIX_M23D = Path(__file__).resolve().parent / "fixtures" / "m23"
FIX_M24D = Path(__file__).resolve().parent / "fixtures" / "m24"
FIX_M26D = Path(__file__).resolve().parent / "fixtures" / "m26"
FIX_M27D = Path(__file__).resolve().parent / "fixtures" / "m27"
FIX_M31_BUNDLE = Path(__file__).resolve().parent / "fixtures" / "m31" / "bundle"
RUN_ID_M06 = (
    Path(__file__).resolve().parent / "fixtures" / "run_identity_m06_fingerprint_match.json"
)


def test_parse_json_object_text_and_strict(tmp_path: Path) -> None:
    obj, err = parse_json_object_text("{}")
    assert err is None and obj == {}

    obj2, err2 = parse_json_object_text("[]")
    assert obj2 is None and err2 == JSON_ROOT_MUST_BE_OBJECT

    bad = tmp_path / "x.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        load_json_object_strict(bad)

    bad2 = tmp_path / "arr.json"
    bad2.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON root must be an object"):
        load_json_object_strict(bad2)

    not_a_file = tmp_path / "dir_instead_of_json"
    not_a_file.mkdir()
    with pytest.raises(ValueError, match="dir_instead_of_json"):
        load_json_object_strict(not_a_file)


def test_emit_phase_iv_chain_mains_inprocess(tmp_path: Path) -> None:
    assert (
        emit_evaluation_tournament_main(
            [
                "--benchmark-contract",
                str(FIX_M21D / "valid_benchmark_contract.json"),
                "--suite",
                str(FIX_M21D / "expected_scripted_baseline_suite.json"),
                "--suite",
                str(FIX_M22D / "expected_heuristic_baseline_suite.json"),
                "--output-dir",
                str(tmp_path / "m23"),
            ],
        )
        == 0
    )
    assert (
        emit_evaluation_diagnostics_main(
            [
                "--tournament",
                str(FIX_M23D / "expected_evaluation_tournament.json"),
                "--output-dir",
                str(tmp_path / "m24"),
            ],
        )
        == 0
    )
    assert (
        emit_baseline_evidence_pack_main(
            [
                "--suite",
                str(FIX_M21D / "expected_scripted_baseline_suite.json"),
                "--suite",
                str(FIX_M22D / "expected_heuristic_baseline_suite.json"),
                "--tournament",
                str(FIX_M23D / "expected_evaluation_tournament.json"),
                "--diagnostics",
                str(FIX_M24D / "expected_evaluation_diagnostics.json"),
                "--output-dir",
                str(tmp_path / "m25"),
            ],
        )
        == 0
    )


def test_emit_baseline_suite_mains_inprocess(tmp_path: Path) -> None:
    assert (
        emit_scripted_baseline_main(
            ["--benchmark-contract", str(BENCH_FIXTURE_ONLY), "--output-dir", str(tmp_path / "sb")],
        )
        == 0
    )
    assert (
        emit_heuristic_baseline_main(
            ["--benchmark-contract", str(BENCH_FIXTURE_ONLY), "--output-dir", str(tmp_path / "hb")],
        )
        == 0
    )


def test_evaluate_environment_drift_main_inprocess(tmp_path: Path) -> None:
    out = tmp_path / "m06_out"
    rc = evaluate_environment_drift_main(
        ["--probe", str(PROBE_M06), "--output-dir", str(out)],
    )
    assert rc == 0
    assert (out / "runtime_smoke_matrix.json").is_file()

    out2 = tmp_path / "m06_out2"
    rc2 = evaluate_environment_drift_main(
        [
            "--probe",
            str(PROBE_M06),
            "--output-dir",
            str(out2),
            "--run-identity",
            str(RUN_ID_M06),
        ],
    )
    assert rc2 == 0


def test_evaluate_environment_drift_main_error_paths(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    assert (
        evaluate_environment_drift_main(
            ["--probe", str(bad), "--output-dir", str(tmp_path / "e1")],
        )
        == 1
    )

    arr = tmp_path / "arr.json"
    arr.write_text("[]", encoding="utf-8")
    assert (
        evaluate_environment_drift_main(
            ["--probe", str(arr), "--output-dir", str(tmp_path / "e2")],
        )
        == 1
    )

    rid = tmp_path / "rid.json"
    rid.write_text("{", encoding="utf-8")
    assert (
        evaluate_environment_drift_main(
            [
                "--probe",
                str(PROBE_M06),
                "--output-dir",
                str(tmp_path / "e3"),
                "--run-identity",
                str(rid),
            ],
        )
        == 1
    )


def test_emit_benchmark_contracts_main_inprocess(tmp_path: Path) -> None:
    assert emit_benchmark_contracts_main(["--output-dir", str(tmp_path / "m20")]) == 0
    assert (tmp_path / "m20" / "benchmark_contract_schema.json").is_file()


def test_emit_replay_training_dataset_main_missing_bundle(tmp_path: Path) -> None:
    assert (
        emit_replay_training_dataset_main(
            ["--bundle", str(tmp_path / "nope"), "--output-dir", str(tmp_path / "out")],
        )
        == 1
    )


def test_emit_replay_imitation_baseline_main_bad_dataset(tmp_path: Path) -> None:
    bdir = tmp_path / "bundle"
    _materialize_m14_bundle_directory(bdir)
    assert (
        emit_replay_imitation_baseline_main(
            [
                "--dataset",
                str(tmp_path / "missing_dataset.json"),
                "--bundle",
                str(bdir),
                "--output-dir",
                str(tmp_path / "m27"),
            ],
        )
        == 1
    )


def test_emit_learned_agent_evaluation_package_main_help(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["emit_learned_agent_evaluation", "--help"],
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module(
            "starlab.evaluation.emit_learned_agent_evaluation",
            run_name="__main__",
        )
    assert exc.value.code == 0


def test_emit_replay_explorer_surface_package_main_help(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["emit_replay_explorer_surface", "--help"],
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module(
            "starlab.explorer.emit_replay_explorer_surface",
            run_name="__main__",
        )
    assert exc.value.code == 0


def test_emit_learned_agent_evaluation_main_bad_contract(tmp_path: Path) -> None:
    assert (
        emit_learned_agent_evaluation_main(
            [
                "--contract",
                str(tmp_path / "no_contract.json"),
                "--baseline",
                str(FIX_M27D / "replay_imitation_baseline.json"),
                "--dataset",
                str(FIX_M26D / "replay_training_dataset.json"),
                "--bundle",
                str(FIX_M31_BUNDLE),
                "--output-dir",
                str(tmp_path / "m28"),
            ],
        )
        == 1
    )


def test_emit_replay_training_and_imitation_baseline_mains_inprocess(tmp_path: Path) -> None:
    bdir = tmp_path / "bundle"
    _materialize_m14_bundle_directory(bdir)
    m26_out = tmp_path / "m26"
    assert (
        emit_replay_training_dataset_main(
            ["--bundle", str(bdir), "--output-dir", str(m26_out)],
        )
        == 0
    )
    ds_path = m26_out / "replay_training_dataset.json"
    m27_out = tmp_path / "m27"
    assert (
        emit_replay_imitation_baseline_main(
            [
                "--dataset",
                str(ds_path),
                "--bundle",
                str(bdir),
                "--output-dir",
                str(m27_out),
            ],
        )
        == 0
    )
    assert (m27_out / "replay_imitation_baseline.json").is_file()


def test_env_probe_main_inprocess(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key in (
        "STARLAB_SC2_ROOT",
        "STARLAB_SC2_BIN",
        "STARLAB_SC2_MAPS_DIR",
        "STARLAB_SC2_REPLAYS_DIR",
        "STARLAB_SC2_BASE_BUILD",
        "STARLAB_SC2_DATA_VERSION",
    ):
        monkeypatch.delenv(key, raising=False)
    assert env_probe_main([]) == 0
    out = capsys.readouterr().out
    assert "interface_modes" in out and "s2protocol" in out


def test_emit_replay_explorer_surface_main_handles_build_error(tmp_path: Path) -> None:
    bad_agent = tmp_path / "bad_agent.json"
    bad_agent.write_text("{", encoding="utf-8")
    assert (
        emit_replay_explorer_surface_main(
            [
                "--bundle-dir",
                str(FIX_M31_BUNDLE),
                "--agent-path",
                str(bad_agent),
                "--output-dir",
                str(tmp_path / "m31_err"),
            ],
        )
        == 1
    )


def test_starlab_sc2_package_main_invokes_env_probe(monkeypatch: pytest.MonkeyPatch) -> None:
    """``python -m starlab.sc2`` delegates to env_probe (covers ``starlab.sc2.__main__``)."""

    monkeypatch.setattr(sys, "argv", ["starlab.sc2"])
    for key in (
        "STARLAB_SC2_ROOT",
        "STARLAB_SC2_BIN",
        "STARLAB_SC2_MAPS_DIR",
        "STARLAB_SC2_REPLAYS_DIR",
        "STARLAB_SC2_BASE_BUILD",
        "STARLAB_SC2_DATA_VERSION",
    ):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("starlab.sc2", run_name="__main__")
    assert exc.value.code == 0


def test_intake_cli_main_inprocess(tmp_path: Path) -> None:
    """Exercise `intake_cli.main` in-process (subprocess tests do not attribute coverage)."""
    meta = tmp_path / "meta.json"
    meta.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "download",
                "declared_origin_class": "external",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "m37-coverage",
                "expected_replay_content_sha256": compute_replay_content_sha256(M07_REPLAY),
            },
        ),
        encoding="utf-8",
    )
    out = tmp_path / "intake_out"
    rc = intake_cli_main(
        [
            "--replay",
            str(M07_REPLAY),
            "--metadata",
            str(meta),
            "--output-dir",
            str(out),
        ],
    )
    assert rc == 0
    assert (out / "replay_intake_receipt.json").is_file()


def test_intake_cli_package_main_sys_argv_slice(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``python -m starlab.replays.intake_cli`` passes ``sys.argv[1:]`` to ``main``."""
    meta = tmp_path / "meta.json"
    meta.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "download",
                "declared_origin_class": "external",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "m37-coverage",
                "expected_replay_content_sha256": compute_replay_content_sha256(M07_REPLAY),
            },
        ),
        encoding="utf-8",
    )
    out = tmp_path / "intake_out_main"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "intake_cli",
            "--replay",
            str(M07_REPLAY),
            "--metadata",
            str(meta),
            "--output-dir",
            str(out),
        ],
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("starlab.replays.intake_cli", run_name="__main__")
    assert exc.value.code == 0
    assert (out / "replay_intake_receipt.json").is_file()


def test_metadata_section_core_checks() -> None:
    assert required_sections_non_null(
        {"raw_sections": {"header": 1, "details": 1, "init_data": 1}},
    )
    assert not required_sections_non_null({"raw_sections": {"header": 1}})
    assert not required_sections_non_null({})
    assert core_metadata_ok(
        {
            "protocol": {"base_build": 1, "data_build": 2},
            "game": {"player_count": 2, "event_streams_available": {}},
        },
    )
    assert not core_metadata_ok({"protocol": {}})
    assert player_rows_complete(
        [
            {
                "player_index": 0,
                "player_kind": "human",
                "race_requested": "terran",
                "race_actual": "terran",
                "result": "win",
            },
        ],
    )
    assert not player_rows_complete([{"player_index": 0}])


def test_build_order_and_csv_io_extract_failures(tmp_path: Path) -> None:
    bad_tl = tmp_path / "tl.json"
    bad_tl.write_text("{", encoding="utf-8")
    st, _a, rep = extract_build_order_economy_from_paths(
        timeline_path=bad_tl,
        output_dir=tmp_path / "boe",
        raw_parse_path=None,
        timeline_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st == "extraction_failed"
    assert "timeline_load_failed" in rep["reason_codes"]
    assert exit_code_for_build_order_economy_run("completed") == 0
    assert exit_code_for_build_order_economy_run("extraction_failed") == 4
    assert exit_code_for_build_order_economy_run("source_contract_failed") == 5
    with pytest.raises(ValueError):
        exit_code_for_build_order_economy_run("nope")

    st2, _a2, rep2 = extract_combat_scouting_visibility_from_paths(
        timeline_path=bad_tl,
        build_order_economy_path=FIX13 / "replay_build_order_economy.json",
        output_dir=tmp_path / "csv",
        raw_parse_path=None,
        timeline_report_path=None,
        build_order_economy_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st2 == "extraction_failed"
    assert "timeline_load_failed" in rep2["reason_codes"]
    assert exit_code_for_combat_scouting_visibility_run("completed") == 0
    with pytest.raises(ValueError):
        exit_code_for_combat_scouting_visibility_run("nope")


def test_build_order_and_csv_lineage_load_failures(tmp_path: Path) -> None:
    tl = FIX13 / "replay_timeline.json"
    bad_raw = tmp_path / "raw.json"
    bad_raw.write_text("{", encoding="utf-8")
    st, _, rep = extract_build_order_economy_from_paths(
        timeline_path=tl,
        output_dir=tmp_path / "boe2",
        raw_parse_path=bad_raw,
        timeline_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st == "extraction_failed"
    assert "lineage_load_failed" in rep["reason_codes"]

    st2, _, rep2 = extract_combat_scouting_visibility_from_paths(
        timeline_path=tl,
        build_order_economy_path=FIX13 / "replay_build_order_economy.json",
        output_dir=tmp_path / "csv2",
        raw_parse_path=bad_raw,
        timeline_report_path=None,
        build_order_economy_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st2 == "extraction_failed"
    assert "lineage_load_failed" in rep2["reason_codes"]


def test_replay_bundle_io_extract_and_write(tmp_path: Path) -> None:
    assert exit_code_for_replay_bundle_run("completed") == 0
    assert exit_code_for_replay_bundle_run("lineage_failed") == 5
    assert exit_code_for_replay_bundle_run("load_failed") == 4
    with pytest.raises(ValueError):
        exit_code_for_replay_bundle_run("nope")  # type: ignore[arg-type]

    sec = collect_secondary_reports_from_dir(FIX14)
    assert "replay_metadata_report.json" in sec

    out = tmp_path / "bundle_out"
    st, err, man, lin, cont = extract_replay_bundle_from_paths(
        input_dir=FIX14,
        output_dir=out,
        optional_intake_receipt_path=None,
        optional_parse_receipt_path=None,
    )
    assert st == "completed" and err is None
    assert man and lin and cont
    assert (out / "replay_bundle_manifest.json").is_file()

    man_path, lin_path, cont_path = write_replay_bundle_artifacts(
        output_dir=tmp_path / "bw",
        manifest={"a": 1},
        lineage={"b": 2},
        contents={"c": 3},
    )
    assert man_path.is_file() and lin_path.is_file() and cont_path.is_file()


def test_parser_io_write_and_exit_codes(tmp_path: Path) -> None:
    rp, rpt, rawp = write_parse_artifacts(
        output_dir=tmp_path / "p8",
        receipt={"a": 1},
        report={"b": 2},
        raw_parse={"c": 3},
    )
    assert rp.is_file() and rpt.is_file() and rawp.is_file()
    assert exit_code_for_parse_status("parsed") == 0
    assert exit_code_for_parse_status("unsupported_protocol") == 2
    assert exit_code_for_parse_status("parser_unavailable") == 3
    assert exit_code_for_parse_status("parse_failed") == 4
    assert exit_code_for_parse_status("input_contract_failed") == 5
    with pytest.raises(ValueError):
        exit_code_for_parse_status("nope")  # type: ignore[arg-type]


def test_emit_reconciliation_artifacts_writes_m19_fixtures(tmp_path: Path) -> None:
    ap, rp, verdict = emit_reconciliation_artifacts(
        canonical_state_path=FIX19 / "canonical_state.json",
        observation_surface_path=FIX19 / "observation_surface.json",
        output_dir=tmp_path / "m19out",
        canonical_state_report_path=FIX19 / "canonical_state_report.json",
        observation_surface_report_path=FIX19 / "observation_surface_report.json",
    )
    assert ap.is_file() and rp.is_file()
    assert verdict in {"pass", "pass_with_warnings", "fail"}


def test_metadata_extraction_protocol_and_players(tmp_path: Path) -> None:
    proto = extract_protocol_fields(
        {
            "protocol_context": {"m_baseBuild": 1, "m_dataBuild": 2, "m_revision": 3},
            "raw_sections": {"header": {"m_version": {"m_baseBuild": 9}}},
        },
    )
    assert proto["base_build"] == 1
    assert proto["data_build"] == 2
    assert proto["data_version"] == 3

    proto2 = extract_protocol_fields({"raw_sections": {}})
    assert proto2["base_build"] == 0

    rows, amb = extract_players({"m_playerList": "nope"})
    assert rows == [] and amb is False

    rows2, amb2 = extract_players(
        {
            "m_playerList": [
                {"m_control": 99, "m_race": "X", "m_result": 1},
                "not-a-dict",
            ],
        },
    )
    assert amb2 is True
    assert len(rows2) == 1

    mp, rp = write_metadata_artifacts(
        output_dir=tmp_path / "meta_out",
        metadata={"replay_content_sha256": "a" * 64},
        report={"schema_version": "starlab.replay_metadata_report.v1"},
    )
    assert mp.is_file() and rp.is_file()


def test_timeline_io_extract_and_write(tmp_path: Path) -> None:
    bad_raw = tmp_path / "raw.json"
    bad_raw.write_text("{", encoding="utf-8")
    out = tmp_path / "t1"
    st, _tl, rep = extract_timeline_from_paths(
        raw_parse_path=bad_raw,
        output_dir=out,
        parse_receipt_path=None,
        parse_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st == "extraction_failed"
    assert "raw_parse_load_failed" in rep["reason_codes"]

    raw_ok = FIX09 / "replay_raw_parse_valid.json"
    bad_side = tmp_path / "side.json"
    bad_side.write_text("not json", encoding="utf-8")
    out2 = tmp_path / "t2"
    st2, _, rep2 = extract_timeline_from_paths(
        raw_parse_path=raw_ok,
        output_dir=out2,
        parse_receipt_path=bad_side,
        parse_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st2 == "extraction_failed"
    assert "lineage_load_failed" in rep2["reason_codes"]

    p1, p2 = write_timeline_artifacts(
        output_dir=tmp_path / "tw",
        timeline={"entries": [], "schema_version": "x"},
        report={"schema_version": "y"},
    )
    assert p1.is_file() and p2.is_file()

    st3, _tl3, _rep3 = extract_timeline_from_paths(
        raw_parse_path=FIX09 / "replay_raw_parse_valid.json",
        output_dir=tmp_path / "t3",
        parse_receipt_path=FIX09 / "replay_parse_receipt_valid.json",
        parse_report_path=FIX09 / "replay_parse_report_valid.json",
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st3 in ("completed", "extraction_failed", "source_contract_failed")


def test_exit_codes_replay_slice_and_timeline() -> None:
    assert exit_code_for_replay_slice_run("completed") == 0
    assert exit_code_for_replay_slice_run("extraction_failed") == 4
    assert exit_code_for_replay_slice_run("lineage_failed") == 5
    assert exit_code_for_replay_slice_run("source_contract_failed") == 5
    with pytest.raises(ValueError):
        exit_code_for_replay_slice_run("nope")  # type: ignore[arg-type]

    assert exit_code_for_timeline_run("completed") == 0
    assert exit_code_for_timeline_run("source_contract_failed") == 5
    assert exit_code_for_timeline_run("extraction_failed") == 4
    with pytest.raises(ValueError):
        exit_code_for_timeline_run("nope")


def test_exit_code_metadata_extraction_status() -> None:
    assert exit_code_for_extraction_status("extracted") == 0
    assert exit_code_for_extraction_status("partial") == 0
    assert exit_code_for_extraction_status("source_contract_failed") == 5
    assert exit_code_for_extraction_status("extraction_failed") == 4
    with pytest.raises(ValueError):
        exit_code_for_extraction_status("nope")  # type: ignore[arg-type]


def test_extract_from_paths_raw_parse_and_receipt_failures(tmp_path: Path) -> None:
    bad_raw = tmp_path / "raw.json"
    bad_raw.write_text("{", encoding="utf-8")
    out = tmp_path / "m1"
    st, _meta, rep = extract_from_paths(
        raw_parse_path=bad_raw,
        output_dir=out,
        parse_receipt_path=None,
        parse_report_path=None,
    )
    assert st == "extraction_failed"
    assert "raw_parse_load_failed" in rep["reason_codes"]

    raw_ok = FIX09 / "replay_raw_parse_valid.json"
    bad_rcpt = tmp_path / "rcpt.json"
    bad_rcpt.write_text("not json", encoding="utf-8")
    out2 = tmp_path / "m2"
    st2, _m2, rep2 = extract_from_paths(
        raw_parse_path=raw_ok,
        output_dir=out2,
        parse_receipt_path=bad_rcpt,
        parse_report_path=None,
    )
    assert st2 == "extraction_failed"
    assert "parse_receipt_load_failed" in rep2["reason_codes"]

    bad_rpt = tmp_path / "rpt.json"
    bad_rpt.write_text("not json", encoding="utf-8")
    out3 = tmp_path / "m3"
    st3, _m3, rep3 = extract_from_paths(
        raw_parse_path=raw_ok,
        output_dir=out3,
        parse_receipt_path=None,
        parse_report_path=bad_rpt,
    )
    assert st3 == "extraction_failed"
    assert "parse_report_load_failed" in rep3["reason_codes"]


def test_extract_replay_slices_from_paths_completed(tmp_path: Path) -> None:
    out = tmp_path / "slice_ok"
    st, body, rep = extract_replay_slices_from_paths(
        timeline_path=FIX13 / "replay_timeline.json",
        build_order_economy_path=FIX13 / "replay_build_order_economy.json",
        combat_scouting_visibility_path=FIX13 / "replay_combat_scouting_visibility.json",
        output_dir=out,
        timeline_report_path=None,
        build_order_economy_report_path=None,
        combat_scouting_visibility_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st == "completed"
    assert isinstance(body.get("slices"), list) and len(body["slices"]) >= 1
    assert rep.get("schema_version") == "starlab.replay_slices_report.v1"


def test_extract_replay_slices_timeline_load_failed(tmp_path: Path) -> None:
    bad = tmp_path / "tl.json"
    bad.write_text("not json", encoding="utf-8")
    out = tmp_path / "out"
    st, art, rep = extract_replay_slices_from_paths(
        timeline_path=bad,
        build_order_economy_path=FIX13 / "replay_build_order_economy.json",
        combat_scouting_visibility_path=FIX13 / "replay_combat_scouting_visibility.json",
        output_dir=out,
        timeline_report_path=None,
        build_order_economy_report_path=None,
        combat_scouting_visibility_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st == "extraction_failed"
    assert rep.get("reason_codes") == ["timeline_load_failed"]
    assert "slices" in art


def test_extract_replay_slices_boe_and_csv_load_failures(tmp_path: Path) -> None:
    tl = FIX13 / "replay_timeline.json"
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    out = tmp_path / "o1"
    st, _, rep = extract_replay_slices_from_paths(
        timeline_path=tl,
        build_order_economy_path=bad,
        combat_scouting_visibility_path=FIX13 / "replay_combat_scouting_visibility.json",
        output_dir=out,
        timeline_report_path=None,
        build_order_economy_report_path=None,
        combat_scouting_visibility_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st == "extraction_failed"
    assert rep.get("reason_codes") == ["build_order_economy_load_failed"]

    out2 = tmp_path / "o2"
    st2, _, rep2 = extract_replay_slices_from_paths(
        timeline_path=tl,
        build_order_economy_path=FIX13 / "replay_build_order_economy.json",
        combat_scouting_visibility_path=bad,
        output_dir=out2,
        timeline_report_path=None,
        build_order_economy_report_path=None,
        combat_scouting_visibility_report_path=None,
        metadata_path=None,
        metadata_report_path=None,
    )
    assert st2 == "extraction_failed"
    assert rep2.get("reason_codes") == ["combat_scouting_visibility_load_failed"]


def test_replay_slice_generation_helpers() -> None:
    assert max_gameloop_from_timeline({}) == 0
    assert max_gameloop_from_timeline({"entries": []}) == 0
    assert max_gameloop_from_timeline({"entries": [{"gameloop": 10}, {"gameloop": 5}]}) == 10
    assert max_gameloop_from_timeline({"entries": [{"gameloop": True}]}) == 0  # bool excluded

    ok, err = validate_csv_contract({"schema_version": "wrong"})
    assert ok is False and err is not None
    ok2, err2 = validate_csv_contract(
        {
            "schema_version": COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION,
            "combat_windows": [],
            "scouting_observations": [],
            "visibility_windows": [],
        },
    )
    assert ok2 is True and err2 is None

    assert hex_eq("Ab", "ab")
    assert not hex_eq("a", "b")

    good, msg = optional_report_hash_required(
        artifact_field="abc",
        report_path_provided=False,
        label="x",
    )
    assert good is False and msg is not None

    payload = slice_identity_payload_for_hash(
        slice_kind=SLICE_KIND_COMBAT,
        start_gameloop=1,
        end_gameloop=2,
        anchor_gameloop=3,
        anchor_ref={"k": "v"},
        subject_player_index=0,
        opponent_player_index=1,
        evidence_model="m",
    )
    assert payload["slice_kind"] == SLICE_KIND_COMBAT
    assert combat_window_id(2) == "combat_window:2"
    assert scouting_observation_id(1) == "scouting_observation:1"
    assert (
        primary_anchor_id(
            slice_kind=SLICE_KIND_COMBAT,
            window_index=0,
            observation_index=None,
        )
        == "cw-0"
    )
    assert (
        primary_anchor_id(
            slice_kind=SLICE_KIND_SCOUTING,
            window_index=None,
            observation_index=2,
        )
        == "so-2"
    )
    assert (
        primary_anchor_id(
            slice_kind=SLICE_KIND_SCOUTING,
            window_index=None,
            observation_index=None,
        )
        == "unknown"
    )

    steps = [{"step_index": 1, "gameloop": 5}, {"step_index": 2, "gameloop": 99}]
    assert overlap_build_steps(steps=steps, start_gameloop=4, end_gameloop=10) == ["1"]

    vw = [
        {
            "window_index": 0,
            "start_gameloop": 0,
            "end_gameloop": 100,
            "visibility_model": "observation_proxy",
        },
        {
            "window_index": 1,
            "start_gameloop": 0,
            "end_gameloop": 100,
            "visibility_model": "explicit_visibility",
        },
    ]
    ids, p, e = overlap_visibility_windows(
        visibility_windows=vw,
        start_gameloop=0,
        end_gameloop=50,
    )
    assert set(ids) == {"0", "1"} and p and e

    assert metadata_max_loops_optional(None) is None
    assert metadata_max_loops_optional({"metadata": {"game": {"game_length_loops": 123}}}) == 123
