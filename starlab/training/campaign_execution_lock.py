"""M50: PID-based output-dir and execution-tree locks (cross-platform, inspectable)."""

from __future__ import annotations

import json
import os
import socket
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps
from starlab.training.industrial_hidden_rollout_models import (
    CAMPAIGN_EXECUTION_LOCK_VERSION,
    CAMPAIGN_OUTPUT_LOCK_VERSION,
)

CAMPAIGN_OUTPUT_LOCK_BASENAME: Final[str] = ".starlab_campaign_output.lock"
CAMPAIGN_EXECUTION_LOCK_BASENAME: Final[str] = ".campaign_execution.lock"


def _pid_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes

        kernel32 = ctypes.windll.kernel32
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    else:
        return True


@dataclass(frozen=True, slots=True)
class CampaignLockInfo:
    """Parsed lockfile contents."""

    pid: int
    hostname: str
    started_at_unix_utc: float
    execution_id: str | None
    command: str
    lock_version: str
    raw: dict[str, Any]


def read_lock_file(path: Path) -> CampaignLockInfo | None:
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    try:
        pid = int(raw["pid"])
        hostname = str(raw["hostname"])
        started = float(raw["started_at_unix_utc"])
        cmd = str(raw.get("command", ""))
        lv = str(raw.get("lock_version", ""))
        ex = raw.get("execution_id")
        ex_id = str(ex) if ex is not None else None
    except (KeyError, TypeError, ValueError):
        return None
    return CampaignLockInfo(
        command=cmd,
        execution_id=ex_id,
        hostname=hostname,
        lock_version=lv,
        pid=pid,
        raw=raw,
        started_at_unix_utc=started,
    )


def lock_is_stale(info: CampaignLockInfo) -> bool:
    """True if lock PID is not running (safe to break after operator review)."""

    return not _pid_exists(info.pid)


def try_acquire_campaign_output_lock(
    *,
    campaign_root: Path,
    execution_id: str,
    command: str,
) -> tuple[bool, Path, str]:
    """Acquire exclusive lock on campaign output directory (``campaign_root``).

    Returns (ok, lock_path, message).
    """

    campaign_root.mkdir(parents=True, exist_ok=True)
    lock_path = campaign_root / CAMPAIGN_OUTPUT_LOCK_BASENAME
    if lock_path.is_file():
        info = read_lock_file(lock_path)
        if info is not None and not lock_is_stale(info):
            return (
                False,
                lock_path,
                f"campaign output dir locked by pid={info.pid} host={info.hostname} "
                f"execution_id={info.execution_id!r}",
            )
        if info is not None and lock_is_stale(info):
            try:
                lock_path.unlink()
            except OSError as e:
                return False, lock_path, f"stale lock present but could not remove: {e}"

    body: dict[str, Any] = {
        "command": command,
        "execution_id": execution_id,
        "hostname": socket.gethostname(),
        "lock_version": CAMPAIGN_OUTPUT_LOCK_VERSION,
        "pid": os.getpid(),
        "started_at_unix_utc": time.time(),
    }
    try:
        lock_path.write_text(canonical_json_dumps(body), encoding="utf-8")
    except OSError as e:
        return False, lock_path, str(e)
    return True, lock_path, "acquired"


def release_lock(lock_path: Path) -> None:
    try:
        if lock_path.is_file():
            lock_path.unlink()
    except OSError:
        pass


def try_acquire_execution_tree_lock(
    *,
    execution_dir: Path,
    execution_id: str,
    command: str,
) -> tuple[bool, Path, str]:
    """Lock a single execution tree under ``campaign_runs/<execution_id>/``."""

    execution_dir.mkdir(parents=True, exist_ok=True)
    lock_path = execution_dir / CAMPAIGN_EXECUTION_LOCK_BASENAME
    if lock_path.is_file():
        info = read_lock_file(lock_path)
        if info is not None and not lock_is_stale(info):
            return (
                False,
                lock_path,
                f"execution tree locked by pid={info.pid} host={info.hostname}",
            )
        if info is not None and lock_is_stale(info):
            try:
                lock_path.unlink()
            except OSError as e:
                return False, lock_path, f"stale lock could not be removed: {e}"

    body: dict[str, Any] = {
        "command": command,
        "execution_id": execution_id,
        "hostname": socket.gethostname(),
        "lock_version": CAMPAIGN_EXECUTION_LOCK_VERSION,
        "pid": os.getpid(),
        "started_at_unix_utc": time.time(),
    }
    try:
        lock_path.write_text(canonical_json_dumps(body), encoding="utf-8")
    except OSError as e:
        return False, lock_path, str(e)
    return True, lock_path, "acquired"
