"""M08 parser pipeline tests (fixture adapters; no optional replay-parser in CI)."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.parser_interfaces import (
    AdapterAvailability,
    AdapterFailure,
    AdapterOutcome,
    AdapterSuccess,
    RawEventStreams,
    RawParseSections,
)
from starlab.replays.parser_io import run_replay_parse
from starlab.replays.parser_models import PARSE_CHECK_IDS, RAW_PARSE_SCHEMA_VERSION_V2
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.runs.replay_binding import (
    build_replay_binding_record,
    build_replay_reference,
)
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
OPAQUE_REPLAY = FIXTURE_DIR / "replay_m07_generated.SC2Replay"


class _SuccessAdapter:
    """Returns minimal decoded sections (fixture)."""

    def parser_family(self) -> str:
        return "fixture"

    def parser_version(self) -> str:
        return "0.0.test"

    def dependency_available(self) -> bool:
        return True

    def parse_replay_file(self, replay_path: Path) -> AdapterOutcome:
        return AdapterSuccess(
            availability=AdapterAvailability(
                attribute_events_available=False,
                game_events_available=False,
                message_events_available=False,
                tracker_events_available=False,
            ),
            protocol_context={"m_baseBuild": 12345},
            raw_sections=RawParseSections(
                attribute_events=None,
                details={"m_playerList": []},
                header={"m_version": {"m_baseBuild": 12345}},
                init_data={
                    "m_syncLobbyState": {"m_gameDescription": {"m_cacheHandles": []}},
                },
            ),
        )


class _UnavailableAdapter:
    def parser_family(self) -> str:
        return "s2protocol"

    def parser_version(self) -> str:
        return "n/a"

    def dependency_available(self) -> bool:
        return False

    def parse_replay_file(self, replay_path: Path) -> AdapterOutcome:
        raise AssertionError("unreachable")


class _UnsupportedProtocolAdapter:
    def parser_family(self) -> str:
        return "fixture"

    def parser_version(self) -> str:
        return "0.0.test"

    def dependency_available(self) -> bool:
        return True

    def parse_replay_file(self, replay_path: Path) -> AdapterOutcome:
        return AdapterFailure(
            kind="unsupported_protocol",
            message="no protocol for build",
        )


def test_check_order_matches_constants() -> None:
    _, _, report, _ = run_replay_parse(
        adapter=_SuccessAdapter(),
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    ids = [c["check_id"] for c in report["check_results"]]
    assert ids == list(PARSE_CHECK_IDS)


def test_parsed_status_and_raw_sections() -> None:
    status, receipt, report, raw_parse = run_replay_parse(
        adapter=_SuccessAdapter(),
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    assert status == "parsed"
    assert report["parse_status"] == "parsed"
    assert raw_parse["schema_version"] == "starlab.replay_raw_parse.v1"
    assert raw_parse["raw_sections"]["header"] is not None
    assert receipt["raw_parse_sha256"] == sha256_hex_of_canonical_json(raw_parse)


def test_parser_unavailable_path() -> None:
    status, _, report, _ = run_replay_parse(
        adapter=_UnavailableAdapter(),
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    assert status == "parser_unavailable"
    assert report["parse_status"] == "parser_unavailable"


def test_unsupported_protocol_status() -> None:
    status, _, report, _ = run_replay_parse(
        adapter=_UnsupportedProtocolAdapter(),
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    assert status == "unsupported_protocol"
    assert "unsupported_protocol" in report["reason_codes"]


def test_intake_receipt_hash_mismatch(tmp_path: Path) -> None:
    ir = tmp_path / "replay_intake_receipt.json"
    ir.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_receipt.v1",
                "replay_content_sha256": "0" * 64,
            },
        ),
        encoding="utf-8",
    )
    status, _, report, _ = run_replay_parse(
        adapter=_SuccessAdapter(),
        intake_receipt_path=ir,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    assert status == "input_contract_failed"
    assert "intake_receipt_hash_mismatch" in report["reason_codes"]


def test_binding_hash_mismatch(tmp_path: Path) -> None:
    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    rb = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256="1" * 64,
        replay_reference=build_replay_reference(OPAQUE_REPLAY),
        run_spec_id=ri["run_spec_id"],
    )
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(rb_path, rb)
    status, _, _, _ = run_replay_parse(
        adapter=_SuccessAdapter(),
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=rb_path,
        replay_path=OPAQUE_REPLAY,
    )
    assert status == "input_contract_failed"


class _StreamsAdapter:
    """Fixture adapter with M10 raw_event_streams (v2 parse artifact)."""

    def parser_family(self) -> str:
        return "fixture"

    def parser_version(self) -> str:
        return "0.0.test"

    def dependency_available(self) -> bool:
        return True

    def parse_replay_file(self, replay_path: Path) -> AdapterOutcome:
        return AdapterSuccess(
            availability=AdapterAvailability(
                attribute_events_available=False,
                game_events_available=True,
                message_events_available=False,
                tracker_events_available=False,
            ),
            protocol_context={"m_baseBuild": 12345},
            raw_event_streams=RawEventStreams(
                game_events=[{"_event": "NNet.Game.SCmdEvent", "_gameloop": 1, "_eventid": 27}],
                message_events=None,
                tracker_events=None,
            ),
            raw_sections=RawParseSections(
                attribute_events=None,
                details={"m_playerList": []},
                header={"m_version": {"m_baseBuild": 12345}},
                init_data={
                    "m_syncLobbyState": {"m_gameDescription": {"m_cacheHandles": []}},
                },
            ),
        )


def test_parsed_status_emits_v2_when_streams_present() -> None:
    status, _, _, raw_parse = run_replay_parse(
        adapter=_StreamsAdapter(),
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    assert status == "parsed"
    assert raw_parse["schema_version"] == RAW_PARSE_SCHEMA_VERSION_V2
    assert "raw_event_streams" in raw_parse
    assert (
        raw_parse["raw_event_streams"]["raw_event_streams_schema"] == "starlab.raw_event_streams.v1"
    )


def test_deterministic_repeat_run() -> None:
    a = _SuccessAdapter()
    s1 = run_replay_parse(
        adapter=a,
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    s2 = run_replay_parse(
        adapter=a,
        intake_receipt_path=None,
        intake_report_path=None,
        replay_binding_path=None,
        replay_path=OPAQUE_REPLAY,
    )
    assert s1[1] == s2[1] and s1[2] == s2[2] and s1[3] == s2[3]
