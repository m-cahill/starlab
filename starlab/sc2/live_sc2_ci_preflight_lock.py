"""Narrow advisory lock for M58 live-SC2 preflight (one output dir scope)."""

from __future__ import annotations

import json
import os
import socket
import sys
import time
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps

M58_LIVE_SC2_PREFLIGHT_LOCK_BASENAME: Final[str] = ".starlab_m58_live_sc2_preflight.lock"
M58_LOCK_KIND: Final[str] = "starlab.m58.live_sc2_preflight_lock.v1"


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


def _read_lock(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    return raw


def try_acquire_m58_live_sc2_preflight_lock(
    *,
    output_dir: Path,
) -> tuple[bool, Path, str]:
    """Return (ok, lock_path, message). Deny if another live PID holds the lock."""

    output_dir.mkdir(parents=True, exist_ok=True)
    lock_path = output_dir / M58_LIVE_SC2_PREFLIGHT_LOCK_BASENAME
    existing = _read_lock(lock_path)
    if existing is not None:
        try:
            pid = int(existing["pid"])
        except (KeyError, TypeError, ValueError):
            pid = -1
        if pid == os.getpid():
            return True, lock_path, "already_held_same_process"
        if _pid_exists(pid):
            return (
                False,
                lock_path,
                f"m58 preflight lock held by pid={pid} host={existing.get('hostname', '?')}",
            )
        try:
            lock_path.unlink()
        except OSError as e:
            return False, lock_path, f"stale lock present but could not remove: {e}"

    body: dict[str, Any] = {
        "command": "emit_live_sc2_in_ci_preflight",
        "hostname": socket.gethostname(),
        "lock_kind": M58_LOCK_KIND,
        "pid": os.getpid(),
        "started_at_unix_utc": time.time(),
    }
    try:
        lock_path.write_text(canonical_json_dumps(body), encoding="utf-8")
    except OSError as e:
        return False, lock_path, str(e)
    return True, lock_path, "acquired"


def release_m58_live_sc2_preflight_lock(lock_path: Path) -> None:
    try:
        if lock_path.is_file():
            lock_path.unlink()
    except OSError:
        pass
