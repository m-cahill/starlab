"""Concrete ``s2protocol`` adapter — **only** module that imports parser libraries (M08)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.replays.parser_interfaces import (
    AdapterAvailability,
    AdapterFailure,
    AdapterOutcome,
    AdapterSuccess,
    RawEventStreams,
    RawParseSections,
    ReplayParserAdapter,
)


def _try_import_s2protocol() -> tuple[Any, Any, Any] | None:
    try:
        from mpyq import MPQArchive  # noqa: PLC0415
        from s2protocol.versions import build, latest  # noqa: PLC0415
    except ImportError:
        return None
    return MPQArchive, build, latest


def _read_mpq_file(archive: Any, name: str) -> bytes | None:
    data = archive.read_file(name)
    return data if data else None


class S2ProtocolReplayAdapter:
    """Replay decoder using Blizzard ``s2protocol`` (+ ``mpyq`` MPQ reader)."""

    def __init__(self) -> None:
        self._imports = _try_import_s2protocol()
        try:
            import s2protocol as s2  # noqa: PLC0415
        except ImportError:
            self._s2_version = "unknown"
        else:
            self._s2_version = str(getattr(s2, "__version__", "unknown"))

    def dependency_available(self) -> bool:
        return self._imports is not None

    def parser_family(self) -> str:
        return "s2protocol"

    def parser_version(self) -> str:
        return self._s2_version

    def parse_replay_file(self, replay_path: Path) -> AdapterOutcome:
        if self._imports is None:
            return AdapterFailure(
                kind="parser_unavailable",
                message="s2protocol and/or mpyq import failed; install starlab[replay-parser]",
            )

        MPQArchive, build, latest = self._imports

        try:
            archive = MPQArchive(str(replay_path))
        except Exception as exc:  # noqa: BLE001 — boundary: surface as parse_failed
            return AdapterFailure(
                kind="parse_failed",
                message=f"failed to open MPQ archive: {exc}",
            )

        try:
            contents = archive.header["user_data_header"]["content"]
            header = latest().decode_replay_header(contents)
        except Exception as exc:  # noqa: BLE001
            return AdapterFailure(
                kind="parse_failed",
                message=f"failed to decode replay header: {exc}",
            )

        base_build = header["m_version"]["m_baseBuild"]
        protocol_context: dict[str, Any] = {
            "m_baseBuild": int(base_build),
            "m_dataBuild": int(header["m_version"].get("m_dataBuild", 0)),
            "m_revision": int(header["m_version"].get("m_revision", 0)),
        }

        try:
            protocol = build(base_build)
        except Exception as exc:  # noqa: BLE001
            return AdapterFailure(
                kind="unsupported_protocol",
                message=f"no protocol for base build {base_build!r}: {exc}",
            )

        details_bin = _read_mpq_file(archive, "replay.details")
        init_bin = _read_mpq_file(archive, "replay.initData")
        attr_bin = _read_mpq_file(archive, "replay.attributes.events")
        game_bin = _read_mpq_file(archive, "replay.game.events")
        msg_bin = _read_mpq_file(archive, "replay.message.events")
        trk_bin = _read_mpq_file(archive, "replay.tracker.events")

        if details_bin is None or init_bin is None:
            return AdapterFailure(
                kind="parse_failed",
                message="replay.details or replay.initData missing from archive",
            )

        try:
            details = protocol.decode_replay_details(details_bin)
            init_data = protocol.decode_replay_initdata(init_bin)
        except Exception as exc:  # noqa: BLE001
            return AdapterFailure(
                kind="parse_failed",
                message=f"decode replay details/initData failed: {exc}",
            )

        attribute_events: dict[str, Any] | None = None
        if attr_bin is not None:
            try:
                attribute_events = protocol.decode_replay_attributes_events(attr_bin)
            except Exception as exc:  # noqa: BLE001
                return AdapterFailure(
                    kind="parse_failed",
                    message=f"decode replay.attributes.events failed: {exc}",
                )

        tracker_ok = bool(trk_bin is not None and hasattr(protocol, "decode_replay_tracker_events"))

        availability = AdapterAvailability(
            attribute_events_available=attr_bin is not None,
            game_events_available=game_bin is not None,
            message_events_available=msg_bin is not None,
            tracker_events_available=tracker_ok,
        )

        game_events: list[dict[str, Any]] | None
        if game_bin is not None:
            try:
                game_events = list(protocol.decode_replay_game_events(game_bin))
            except Exception as exc:  # noqa: BLE001 — boundary: surface as parse_failed
                return AdapterFailure(
                    kind="parse_failed",
                    message=f"decode replay.game.events failed: {exc}",
                )
        else:
            game_events = None

        message_events: list[dict[str, Any]] | None
        if msg_bin is not None:
            try:
                message_events = list(protocol.decode_replay_message_events(msg_bin))
            except Exception as exc:  # noqa: BLE001
                return AdapterFailure(
                    kind="parse_failed",
                    message=f"decode replay.message.events failed: {exc}",
                )
        else:
            message_events = None

        tracker_events: list[dict[str, Any]] | None
        if tracker_ok and trk_bin is not None:
            try:
                decode_trk = getattr(protocol, "decode_replay_tracker_events")
                tracker_events = list(decode_trk(trk_bin))
            except Exception as exc:  # noqa: BLE001
                return AdapterFailure(
                    kind="parse_failed",
                    message=f"decode replay.tracker.events failed: {exc}",
                )
        else:
            tracker_events = None

        return AdapterSuccess(
            protocol_context=protocol_context,
            raw_sections=RawParseSections(
                attribute_events=attribute_events,
                details=details,
                header=header,
                init_data=init_data,
            ),
            availability=availability,
            raw_event_streams=RawEventStreams(
                game_events=game_events,
                message_events=message_events,
                tracker_events=tracker_events,
            ),
        )


def default_adapter() -> ReplayParserAdapter:
    """Factory for the canonical STARLAB adapter instance."""

    return S2ProtocolReplayAdapter()
