"""Tests for replay explorer / operator evidence surface (M31)."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.explorer.emit_replay_explorer_surface import main as emit_main
from starlab.explorer.replay_explorer_builder import build_replay_explorer_artifacts
from starlab.explorer.replay_explorer_io import (
    write_replay_explorer_report,
    write_replay_explorer_surface,
)
from starlab.explorer.replay_explorer_models import DEFAULT_NON_CLAIMS
from starlab.explorer.replay_explorer_selection import (
    ordered_slices_for_explorer,
    slice_anchor_gameloop,
)
from starlab.hierarchy.hierarchical_interface_schema import validate_hierarchical_trace_document
from starlab.runs.json_util import canonical_json_dumps

REPO_ROOT = Path(__file__).resolve().parents[1]
M31_FIX = REPO_ROOT / "tests" / "fixtures" / "m31"
BUNDLE_FIX = M31_FIX / "bundle"
M30_AGENT = REPO_ROOT / "tests" / "fixtures" / "m30" / "replay_hierarchical_imitation_agent.json"

M31_EXPLORER_MODULES = (
    "replay_explorer_models.py",
    "replay_explorer_selection.py",
    "replay_explorer_builder.py",
    "replay_explorer_io.py",
    "emit_replay_explorer_surface.py",
)


@pytest.mark.smoke
def test_slice_anchor_midpoint() -> None:
    assert slice_anchor_gameloop(0, 260) == 130
    assert slice_anchor_gameloop(40, 360) == 200


@pytest.mark.smoke
def test_selection_order_independent_of_input_order() -> None:
    slices_json = json.loads((BUNDLE_FIX / "replay_slices.json").read_text(encoding="utf-8"))
    raw = slices_json["slices"]
    assert isinstance(raw, list)
    shuffled = {"slices": list(reversed(raw))}
    a = ordered_slices_for_explorer(slices_json, slice_id_filter=None, max_panels=5)
    b = ordered_slices_for_explorer(shuffled, slice_id_filter=None, max_panels=5)
    assert [x.get("slice_id") for x in a] == [x.get("slice_id") for x in b]


@pytest.mark.smoke
def test_bounded_excerpt_counts() -> None:
    surface, _rep = build_replay_explorer_artifacts(
        bundle_dir=BUNDLE_FIX,
        agent_path=M30_AGENT,
        max_panels=2,
        slice_id_filter=None,
    )
    for p in surface["panels"]:
        assert len(p["timeline_excerpt"]) <= 8
        assert len(p["economy_excerpt"]) <= 6
        assert len(p["combat_scouting_excerpt"]) <= 6


@pytest.mark.smoke
def test_trace_m29_compatible() -> None:
    surface, _rep = build_replay_explorer_artifacts(
        bundle_dir=BUNDLE_FIX,
        agent_path=M30_AGENT,
        max_panels=3,
        slice_id_filter=None,
    )
    for p in surface["panels"]:
        doc = p.get("hierarchical_trace_document")
        if doc is None:
            assert any("materialization_failed" in w for w in p.get("warnings", []))
            continue
        errs = validate_hierarchical_trace_document(doc)
        assert errs == [], errs


@pytest.mark.smoke
def test_io_deterministic_roundtrip(tmp_path: Path) -> None:
    surface, rep = build_replay_explorer_artifacts(
        bundle_dir=BUNDLE_FIX,
        agent_path=M30_AGENT,
        max_panels=2,
        slice_id_filter=None,
    )
    d1 = tmp_path / "o1"
    d2 = tmp_path / "o2"
    d1.mkdir()
    d2.mkdir()
    write_replay_explorer_surface(d1, surface)
    write_replay_explorer_report(d1, rep)
    write_replay_explorer_surface(d2, surface)
    write_replay_explorer_report(d2, rep)
    assert (d1 / "replay_explorer_surface.json").read_text() == (
        d2 / "replay_explorer_surface.json"
    ).read_text()


@pytest.mark.smoke
def test_report_reconciles_with_surface() -> None:
    surface, rep = build_replay_explorer_artifacts(
        bundle_dir=BUNDLE_FIX,
        agent_path=M30_AGENT,
        max_panels=5,
        slice_id_filter=None,
    )
    assert rep["panel_count"] == len(surface["panels"])
    df = rep["delegate_frequency"]
    assert isinstance(df, dict)
    wf = rep["worker_label_frequency"]
    assert isinstance(wf, dict)
    assert sum(df.values()) <= rep["panel_count"]
    assert sum(wf.values()) <= rep["panel_count"]


def test_non_claims_preserved() -> None:
    surface, rep = build_replay_explorer_artifacts(
        bundle_dir=BUNDLE_FIX,
        agent_path=M30_AGENT,
        max_panels=1,
        slice_id_filter=None,
    )
    assert surface["non_claims"] == list(DEFAULT_NON_CLAIMS)
    assert rep["non_claims"] == list(DEFAULT_NON_CLAIMS)


@pytest.mark.smoke
def test_golden_fixture_snapshot(tmp_path: Path) -> None:
    rc = emit_main(
        [
            "--bundle-dir",
            str(BUNDLE_FIX),
            "--agent-path",
            str(M30_AGENT),
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert rc == 0
    exp_s = json.loads(
        (M31_FIX / "expected_replay_explorer_surface.json").read_text(encoding="utf-8")
    )
    got_s = json.loads((tmp_path / "replay_explorer_surface.json").read_text(encoding="utf-8"))
    assert canonical_json_dumps(got_s) == canonical_json_dumps(exp_s)
    exp_r = json.loads(
        (M31_FIX / "expected_replay_explorer_surface_report.json").read_text(encoding="utf-8")
    )
    got_r = json.loads(
        (tmp_path / "replay_explorer_surface_report.json").read_text(encoding="utf-8")
    )
    assert canonical_json_dumps(got_r) == canonical_json_dumps(exp_r)


@pytest.mark.smoke
def test_cli_module_invocation(tmp_path: Path) -> None:
    out = tmp_path / "cli_out"
    out.mkdir()
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.explorer.emit_replay_explorer_surface",
            "--bundle-dir",
            str(BUNDLE_FIX),
            "--agent-path",
            str(M30_AGENT),
            "--output-dir",
            str(out),
            "--max-panels",
            "1",
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    assert (out / "replay_explorer_surface.json").is_file()


@pytest.mark.parametrize("name", M31_EXPLORER_MODULES)
def test_explorer_modules_forbid_replays_sc2_s2protocol(name: str) -> None:
    path = REPO_ROOT / "starlab" / "explorer" / name
    tree = ast.parse(path.read_text(encoding="utf-8"))
    bad: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = (alias.name or "").split(".", 1)[0]
                if base in ("starlab", "s2protocol"):
                    if alias.name.startswith("starlab.replays") or alias.name.startswith(
                        "starlab.sc2"
                    ):
                        bad.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("starlab.replays") or node.module.startswith("starlab.sc2"):
                bad.append(node.module)
            if node.module == "s2protocol" or node.module.startswith("s2protocol."):
                bad.append(node.module)
    assert bad == [], f"forbidden imports in {name}: {bad}"


def test_e2e_copy_bundle_deterministic(tmp_path: Path) -> None:
    """Duplicate bundle under another path; same artifacts."""

    b2 = tmp_path / "bundle2"
    shutil.copytree(BUNDLE_FIX, b2)
    s1, r1 = build_replay_explorer_artifacts(
        bundle_dir=BUNDLE_FIX,
        agent_path=M30_AGENT,
        max_panels=2,
        slice_id_filter=None,
    )
    s2, r2 = build_replay_explorer_artifacts(
        bundle_dir=b2,
        agent_path=M30_AGENT,
        max_panels=2,
        slice_id_filter=None,
    )
    assert canonical_json_dumps(s1) == canonical_json_dumps(s2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)
