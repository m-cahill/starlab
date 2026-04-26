"""Governance tests: ledger, CI wiring, and high-signal smoke checks."""

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m06_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M06" in v15
    assert "starlab.v15.human_panel_benchmark.v1" in v15
    assert "M06 non-claims" in v15
    assert "recruit" in v15 and "human participants" in v15
    assert "no** new real participant **rows**" in v15
    human_reg = (REPO_ROOT / "docs" / "human_benchmark_register.md").read_text(encoding="utf-8")
    assert "V15-M06" in human_reg
    assert "No rows" in human_reg or "*No rows.*" in human_reg
    rt = REPO_ROOT / "docs" / "runtime" / "v15_human_panel_benchmark_protocol_v1.md"
    assert rt.is_file()
    rtxt = rt.read_text(encoding="utf-8").lower()
    assert "protocol" in rtxt and ("fixture only" in rtxt or "protocol contract only" in rtxt)


@pytest.mark.smoke
def test_v15_m07_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M07" in v15
    assert "starlab.v15.training_run_receipt.v1" in v15
    assert "M07 non-claims" in v15
    assert "V15-M08" in v15 and "long" in v15.lower()
    rt = REPO_ROOT / "docs" / "runtime" / "v15_training_smoke_short_gpu_shakedown_v1.md"
    assert rt.is_file()
    rtxt = rt.read_text(encoding="utf-8").lower()
    assert "receipt" in rtxt and "shakedown" in rtxt
    mwr = (REPO_ROOT / "docs" / "model_weight_register.md").read_text(encoding="utf-8")
    car = (REPO_ROOT / "docs" / "checkpoint_asset_register.md").read_text(encoding="utf-8")
    tar = (REPO_ROOT / "docs" / "training_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M07" in mwr and "claim-critical" in mwr
    assert "V15-M07" in car
    assert "V15-M07" in tar


@pytest.mark.smoke
def test_v15_m08_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M08" in v15
    assert "starlab.v15.long_gpu_training_manifest.v1" in v15
    assert "starlab.v15.long_gpu_campaign_receipt.v1" in v15
    assert "M08 non-claims" in v15
    assert "implementation_ready_waiting_for_operator_run" in v15
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_long_gpu_campaign_execution_v1.md" in ledger
    rt = REPO_ROOT / "docs" / "runtime" / "v15_long_gpu_campaign_execution_v1.md"
    assert rt.is_file()
    rtxt = rt.read_text(encoding="utf-8").lower()
    assert "preflight" in rtxt and "double" in rtxt and "guard" in rtxt


@pytest.mark.smoke
def test_v15_m09_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M09" in v15
    assert "starlab.v15.checkpoint_evaluation.v1" in v15
    assert "starlab.v15.checkpoint_promotion_decision.v1" in v15
    assert "M09 non-claims" in v15
    assert "blocked_missing_m08_campaign_receipt" in v15 or "governance routing" in v15
    car = (REPO_ROOT / "docs" / "checkpoint_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M09" in car and "no" in car.lower() and "public" in car
    mwr = (REPO_ROOT / "docs" / "model_weight_register.md").read_text(encoding="utf-8")
    assert "V15-M09" in mwr
    tar = (REPO_ROOT / "docs" / "training_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M09" in tar
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M09" in rights
    rt = REPO_ROOT / "docs" / "runtime" / "v15_checkpoint_evaluation_promotion_v1.md"
    assert rt.is_file()
    rtxt = rt.read_text(encoding="utf-8").lower()
    assert "checkpoint" in rtxt and "promotion" in rtxt


@pytest.mark.smoke
def test_v15_m11_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M11" in v15
    assert "PR #137" in v15
    assert "24945588527" in v15
    assert "24945647654" in v15
    assert "468d90fc" in v15
    assert "V15-M11" in v15
    assert "— **closed**" in v15 or "closed** on `main`" in v15
    assert "starlab.v15.human_panel_execution.v1" in v15
    assert "starlab.v15.human_benchmark_claim_decision.v1" in v15
    assert "M11 non-claims" in v15
    assert "recruit human participants" in v15
    human_reg = (REPO_ROOT / "docs" / "human_benchmark_register.md").read_text(encoding="utf-8")
    assert "V15-M11" in human_reg
    assert "No rows" in human_reg or "*No rows.*" in human_reg
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M11" in rights
    car = (REPO_ROOT / "docs" / "checkpoint_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M11" in car
    mwr = (REPO_ROOT / "docs" / "model_weight_register.md").read_text(encoding="utf-8")
    assert "V15-M11" in mwr
    xai = (REPO_ROOT / "docs" / "xai_evidence_register.md").read_text(encoding="utf-8")
    assert "V15-M11" in xai
    rt = REPO_ROOT / "docs" / "runtime" / "v15_human_panel_bounded_benchmark_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert ("h0" in rtx and "fixture" in rtx) or "blocked" in rtx


@pytest.mark.smoke
def test_v15_m12_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M12" in v15
    assert "PR #138" in v15
    assert "24946748829" in v15
    assert "24946807747" in v15
    assert "1182b1bc" in v15
    assert "starlab.v15.showcase_agent_release_pack.v1" in v15
    assert "M12 non-claims" in v15
    assert "does not train a checkpoint" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_showcase_agent_release_pack_v1.md"
    assert rt.is_file()
    rtxt = rt.read_text(encoding="utf-8").lower()
    assert "release pack" in rtxt
    human_reg = (REPO_ROOT / "docs" / "human_benchmark_register.md").read_text(encoding="utf-8")
    assert "V15-M12" in human_reg
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M12" in rights
    car = (REPO_ROOT / "docs" / "checkpoint_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M12" in car
    mwr = (REPO_ROOT / "docs" / "model_weight_register.md").read_text(encoding="utf-8")
    assert "V15-M12" in mwr
    xai = (REPO_ROOT / "docs" / "xai_evidence_register.md").read_text(encoding="utf-8")
    assert "V15-M12" in xai
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_showcase_agent_release_pack_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m13_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M13" in v15
    assert "PR #139" in v15
    assert "24948284106" in v15
    assert "24948356222" in v15
    assert "starlab.v15.v2_go_no_go_decision.v1" in v15
    assert "v15-m13-v2-go-no-go-decision" in v15
    assert "does not authorize v2" in v15.lower() or "does not authorize v2" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_v2_go_no_go_decision_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "v2" in rtx and ("no-go" in rtx or "go / no-go" in rtx)
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M13" in rights
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_v2_go_no_go_decision_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m14_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M14" in v15
    assert "starlab.v15.evidence_remediation_plan.v1" in v15
    assert "M14 non-claims" in v15
    assert "emit_v15_evidence_remediation_plan" in v15
    assert "V15-M15" in v15 and "V15-M21" in v15
    # M16+ remain proposed on the public authority doc; M15 may be opened/implementation
    assert "V15-M16" in v15
    assert "proposed" in v15.lower() and "not started" in v15.lower()
    rt = REPO_ROOT / "docs" / "runtime" / "v15_evidence_remediation_operator_acquisition_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "remediation" in rtx and "m13" in rtx
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M14" in rights
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_evidence_remediation_operator_acquisition_v1.md" in ledger
    assert "v2" in ledger.lower() and "not" in ledger.lower()


@pytest.mark.smoke
def test_v15_m15_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M15" in v15
    assert "starlab.v15.operator_evidence_collection_preflight.v1" in v15
    assert "M15 non-claims" in v15
    assert "emit_v15_operator_evidence_collection_preflight" in v15
    assert "V15-M16" in v15 and "V15-M21" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_operator_evidence_collection_preflight_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "preflight" in rtx and "p0" in rtx and "s0" in rtx
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M15" in rights
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_operator_evidence_collection_preflight_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m10_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M10" in v15
    assert "PR #136" in v15
    assert "24943450910" in v15
    assert "24943955088" in v15
    assert "starlab.v15.replay_native_xai_demonstration.v1" in v15
    assert "M10 non-claims" in v15
    xai_reg = (REPO_ROOT / "docs" / "xai_evidence_register.md").read_text(encoding="utf-8")
    assert "V15-M10" in xai_reg
    assert "No rows" in xai_reg or "*No rows.*" in xai_reg
    car = (REPO_ROOT / "docs" / "checkpoint_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M10" in car
    mwr = (REPO_ROOT / "docs" / "model_weight_register.md").read_text(encoding="utf-8")
    assert "V15-M10" in mwr
    tar = (REPO_ROOT / "docs" / "training_asset_register.md").read_text(encoding="utf-8")
    assert "V15-M10" in tar
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M10" in rights
    rt = REPO_ROOT / "docs" / "runtime" / "v15_replay_native_xai_demonstration_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "m04" in rtx and "governed" in rtx


@pytest.mark.smoke
def test_docs_company_secrets_tree_not_tracked_by_git() -> None:
    proc = subprocess.run(
        ["git", "ls-files", "--", "docs/company_secrets"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0:
        pytest.skip("git ls-files unavailable (not a git checkout)")
    tracked = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    assert not tracked, f"docs/company_secrets/ must not be tracked; got {tracked[:10]}"


@pytest.mark.smoke
def test_ledger_header_points_to_v15_authority_doc() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    head = text.split("---", 1)[0]
    assert "docs/starlab-v1.5.md" in head


@pytest.mark.smoke
def test_ledger_quick_scan_px1_m03_current_px1_m02_closed_threshold_met() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    scan = text.split("## Current truth (quick scan)")[1].split("##")[0]
    assert "| Current milestone |" in scan
    assert "**`V15-M15`**" in scan
    assert "**`V15-M14`**" in scan
    assert "PR #140" in scan or "pull/140" in scan
    assert "PR #139" in scan or "pull/139" in scan
    assert "PR #137" in scan
    assert "PR #136" in scan
    assert "**`V15-M10`**" in scan
    assert "**`V15-M09`**" in scan
    assert "PR #135" in scan or "pull/135" in scan
    assert "**`V15-M08`**" in scan and "**`V15-M07`**" in scan and "**`V15-M06`**" in scan
    assert "PR #116" in scan and "PR #125" in scan and "PR #127" in scan and "PR #129" in scan
    assert "PR #133" in scan or "pull/133" in scan
    assert "PR #116–#120" in scan or "PR #120" in scan
    assert "**`V15-M01`**" in scan and "**`V15-M02`**" in scan
    assert "docs/starlab-v1.5.md" in scan
    assert "v1.5" in scan or "**V15" in scan
    assert "px2_industrial_self_play_campaign_readiness_v1.md" in scan
    assert "px2_industrial_self_play_campaign_v1.md" in scan
    assert "slice 2" in scan.lower() or "execution skeleton" in scan.lower()
    assert "slice 3" in scan.lower() or "preflight" in scan.lower()
    assert "slice 4" in scan.lower() or "continuity" in scan.lower()
    assert "slice 5" in scan.lower() or "campaign-root" in scan.lower()
    assert (
        "slice 6" in scan.lower()
        or "preflight seal" in scan.lower()
        or "canonical operator-local" in scan.lower()
    )
    assert "slice 7" in scan.lower() or "real-run" in scan.lower() or "real run" in scan.lower()
    assert "slice 8" in scan.lower() or "multi-run session" in scan.lower()
    assert (
        "slice 9" in scan.lower()
        or "session transition" in scan.lower()
        or "promotion/rollback execution" in scan.lower()
    )
    assert (
        "slice 10" in scan.lower()
        or "current-candidate" in scan.lower()
        or "current candidate" in scan.lower()
    )
    assert (
        "slice 11" in scan.lower()
        or "continuation run" in scan.lower()
        or "current-candidate consumption" in scan.lower()
    )
    assert (
        "slice 12" in scan.lower()
        or "slice 13" in scan.lower()
        or "slice 14" in scan.lower()
        or "slice 15" in scan.lower()
        or "slice 16" in scan.lower()
        or "re-anchor" in scan.lower()
        or "reanchor" in scan.lower()
        or "second-hop" in scan.lower()
        or "second_hop" in scan.lower()
        or "pointer-seeded" in scan.lower()
        or "pointer_seeded" in scan.lower()
        or "handoff" in scan.lower()
        or "handoff-anchored" in scan.lower()
    )
    assert "| Last closed milestone (PX2 arc) |" in scan
    assert "PX2-M02" in scan and "PX2-M01" in scan and "PX2-M00" in scan
    assert "PX1-M04" in scan and "**closed**" in scan
    assert "PX1-M03" in scan and "**closed**" in scan
    assert "PX1-M01" in scan and "**closed**" in scan
    assert "threshold-met" in scan
    assert "px1_full_industrial_campaign_execution_evidence_v1.md" in scan
    assert "**PX1-M00**" in scan and "**closed**" in scan
    assert "pull/83" in scan
    assert "**PV1-M04**" in scan
    assert "pull/81" in scan
    assert "| PV1 campaign outcome (bounded, operator-local) |" in scan
    assert "**PV1-M03**" in scan
    assert "pull/77" in scan
    assert "threshold-not-met" in scan
    assert "tranche_b_operator_note.md" in scan or "PV1 execution evidence" in scan
    assert "| Post-PV1 (PX1) |" in scan
    assert "| Post-PX1 (PX2) |" in scan
    assert (
        "After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded "
        "substantive execution, still below industrial scale"
    ) in scan
    assert "px2_autonomous_full_game_agent_charter_v1.md" in scan
    assert "| Last closed milestone (PX1 arc) |" in scan
    assert "| PX1 industrial run status (PX1-M01) |" in scan
    assert "v2" in scan.lower() and "defer" in scan.lower()


@pytest.mark.smoke
def test_starlab_ledger_exists() -> None:
    ledger = REPO_ROOT / "docs" / "starlab.md"
    assert ledger.is_file()


@pytest.mark.smoke
def test_m47_recharter_and_m48_deferral_documented() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Governance recharter (2026-04-13 — user-directed)" in text
    assert "Bootstrap Episode Distinctness & Operator Ergonomics" in text
    assert (
        "**M47 — Bootstrap Episode Distinctness & Operator Ergonomics:** **closed** on `main`"
    ) in text
    m48_closed = "**M48 — Learned-agent comparison contract-path alignment:** **closed** on `main`"
    assert m48_closed in text
    assert "62 milestones (M00–M61)" in text or "62 milestones (M00-M61)" in text


@pytest.mark.smoke
def test_ledger_names_deployment_targets() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Netlify" in text
    assert "Render" in text


@pytest.mark.smoke
def test_milestone_m00_directory_exists() -> None:
    m00 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M00"
    if not m00.is_dir():
        pytest.skip("Private docs/company_secrets/ tree not in workspace (gitignored).")
    assert m00.is_dir()


@pytest.mark.smoke
def test_rights_register_exists() -> None:
    path = REPO_ROOT / "docs" / "rights_register.md"
    assert path.is_file()


@pytest.mark.smoke
def test_ci_workflow_exists() -> None:
    wf = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert wf.is_file()


@pytest.mark.smoke
def test_pyproject_exists() -> None:
    assert (REPO_ROOT / "pyproject.toml").is_file()


@pytest.mark.smoke
def test_ledger_has_m01_runtime_title_and_m32_map() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "SC2 Runtime Surface Decision & Environment Lock" in text
    assert "M32" in text
    assert "46 milestones" in text
    assert "M00–M45" in text or "M00-M45" in text
    assert (
        "62 milestones" in text or "M00–M61" in text or "M00-M61" in text or "53 milestones" in text
    )
    assert "Audit Closure I" in text
    assert "Platform Boundary Review" in text
    assert "Governance, Runtime Surface, and Deterministic Run Substrate" in text


@pytest.mark.smoke
def test_ledger_canonical_corpus_promotion_rule() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Canonical corpus promotion" in text
    assert "canonical STARLAB corpus" in text


@pytest.mark.smoke
def test_od005_resolved_row() -> None:
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("| OD-005"):
            assert "Resolved" in stripped
            assert "s2client-proto" in stripped or "s2client" in stripped.lower()
            return
    raise AssertionError("OD-005 row not found in ledger")


@pytest.mark.smoke
def test_ledger_post_pv1_px1_section() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "## Post-PV1 (PX1) — Full Industrial Run & Demonstration Proof" in text
    assert "| `PX1-M00` |" in text
    assert "| `PX1-M01` |" in text
    assert "| `PX1-M02` |" in text
    assert "| `PX1-M03` |" in text
    assert "| `PX1-M04` |" in text
    assert "| `PX1-M05` |" in text
    assert "Candidate Strengthening & Demo Readiness Remediation" in text
    assert "Governed Demo Proof Pack" in text
    assert "Full Industrial Run & Demonstration Charter | **closed**" in text
    assert "Full Industrial Campaign Execution Evidence | **closed**" in text
    assert "Play-Quality Evaluation & Demo Candidate Selection | **closed**" in text
    assert "pull/83" in text
    assert "docs/runtime/px1_full_industrial_run_demo_charter_v1.md" in text
    assert "docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md" in text
    assert (REPO_ROOT / "docs" / "runtime" / "px1_full_industrial_run_demo_charter_v1.md").is_file()
    px1_m01_rt = (
        REPO_ROOT / "docs" / "runtime" / "px1_full_industrial_campaign_execution_evidence_v1.md"
    )
    assert px1_m01_rt.is_file()
    assert (
        REPO_ROOT / "docs" / "runtime" / "px1_play_quality_demo_candidate_selection_v1.md"
    ).is_file()
    assert (
        REPO_ROOT / "docs" / "runtime" / "px1_candidate_strengthening_demo_readiness_v1.md"
    ).is_file()
    assert (REPO_ROOT / "docs" / "runtime" / "px1_governed_demo_proof_pack_v1.md").is_file()


@pytest.mark.smoke
def test_ledger_post_px1_px2_section() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "## Post-PX1 (PX2) — Autonomous Full-Game Skill Development" in text
    assert "PX1 proved demo-proof packaging and bounded remediation" in text
    assert "| `PX2-M00` |" in text
    px2_m00_row = next(
        line for line in text.splitlines() if line.strip().startswith("| `PX2-M00` |")
    )
    assert "**closed**" in px2_m00_row
    assert "| `PX2-M01` |" in text
    px2_m01_row = next(
        line for line in text.splitlines() if line.strip().startswith("| `PX2-M01` |")
    )
    assert "**closed**" in px2_m01_row
    assert "pull/95" in px2_m01_row
    assert "px2_full_terran_runtime_action_surface_v1.md" in text
    assert "px2_neural_bootstrap_from_replays_v1.md" in text
    assert "| `PX2-M02` |" in text
    px2_m02_row = next(
        line for line in text.splitlines() if line.strip().startswith("| `PX2-M02` |")
    )
    assert "**closed**" in px2_m02_row
    assert "pull/96" in px2_m02_row
    px2_m03_row = next(
        line for line in text.splitlines() if line.strip().startswith("| `PX2-M03` |")
    )
    assert "**closed**" in px2_m03_row
    assert "| `PX2-M03` |" in text
    assert "| `PX2-M04` |" in text
    assert "| `PX2-M05` |" in text
    assert "Full Terran Runtime & Action Surface" in text
    assert "Neural Bootstrap from Replays" in text
    assert "Industrial Self-Play Campaign" in text
    assert "docs/runtime/px2_autonomous_full_game_agent_charter_v1.md" in text
    assert "### Phase boundary matrix (post-v1 phases)" in text
    px2_charter = REPO_ROOT / "docs" / "runtime" / "px2_autonomous_full_game_agent_charter_v1.md"
    assert px2_charter.is_file()
    px2_m01_rt = REPO_ROOT / "docs" / "runtime" / "px2_full_terran_runtime_action_surface_v1.md"
    assert px2_m01_rt.is_file()
    assert (REPO_ROOT / "docs" / "runtime" / "px2_neural_bootstrap_from_replays_v1.md").is_file()
    px2_m03_ready = (
        REPO_ROOT / "docs" / "runtime" / "px2_industrial_self_play_campaign_readiness_v1.md"
    )
    assert px2_m03_ready.is_file()
    px2_m03_campaign_v1 = REPO_ROOT / "docs" / "runtime" / "px2_industrial_self_play_campaign_v1.md"
    assert px2_m03_campaign_v1.is_file()
    assert "px2_industrial_self_play_campaign_v1.md" in text


@pytest.mark.smoke
def test_ledger_post_v1_pv1_section() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "## Post-v1 (PV1) — Long Industrial Campaign & Scaling Evidence" in text
    assert "| `PV1-M00` |" in text
    assert "### PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria" in text
    assert "### PV1 evidence surfaces (PV1-M01 — inspection helpers)" in text
    assert "### PV1 evidence surfaces (PV1-M02 — Tranche A operator-local execution)" in text
    assert "tranche_checkpoint_receipt.json" in text
    assert "campaign_observability_index.json" in text
    assert "| `PV1-M01` |" in text
    assert "| `PV1-M02` |" in text
    assert "| `PV1-M03` |" in text
    assert "| `PV1-M04` |" in text
    assert "Post-Campaign Analysis / Comparative Readout | **closed**" in text
    assert "pull/81" in text
    assert "### PV1 evidence surfaces (PV1-M03 — Tranche B / full-run threshold)" in text
    assert "### Canonical PV1 operator artifacts (campaign root)" in text
    assert "[PR #74](https://github.com/m-cahill/starlab/pull/74)" in text
    assert "[PR #76](https://github.com/m-cahill/starlab/pull/76)" in text
    assert "[PR #77](https://github.com/m-cahill/starlab/pull/77)" in text


@pytest.mark.smoke
def test_current_milestone_section_covers_m47_and_closed_phase_vi() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    section = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "**`V15-M01`**" in section
    assert "**`V15-M00`**" in section
    assert "docs/starlab-v1.5.md" in section
    assert "v15_training_scale_provenance_asset_registers_v1.md" in section
    assert "px2_industrial_self_play_campaign_readiness_v1.md" in section
    assert "px2_industrial_self_play_campaign_v1.md" in section
    assert (
        "### V15-M01 — Training-Scale Provenance and Asset Registers — **closed** on `main`"
        in section
    )
    assert "v15_xai_evidence_contract_v1.md" in section
    assert "v15_strong_agent_benchmark_protocol_v1.md" in section
    assert "v15_human_panel_benchmark_protocol_v1.md" in section
    assert "### V15-M05 — *Strong-Agent Benchmark Protocol* — **closed**" in section
    m08_heading = (
        "### V15-M08 — *Long GPU Campaign Execution* — **closed** on `main` "
        "(**implementation surface**; **`implementation_ready_waiting_for_operator_run`**)"
    )
    assert m08_heading in section
    m09_heading = (
        "### V15-M09 — *Checkpoint Evaluation and Promotion* — **closed** on `main` "
        "(implementation [PR #135](https://github.com/m-cahill/starlab/pull/135); "
        "**closeout** **`blocked_missing_m08_campaign_receipt`**)"
    )
    assert m09_heading in section
    m10_heading = "### V15-M10 — *Replay-Native XAI Demonstration* — **closed** on `main`"
    assert m10_heading in section
    m11_heading = (
        "### V15-M11 — *Human Panel / Bounded Human Benchmark* — **closed** on `main` "
        "(implementation [PR #137](https://github.com/m-cahill/starlab/pull/137); merge `468d90fc"
    )
    assert m11_heading in section
    m12_heading = (
        "### V15-M12 — *Showcase Agent Release Pack* — **closed** on `main` "
        "(implementation [PR #138](https://github.com/m-cahill/starlab/pull/138); merge `1182b1bc"
    )
    assert m12_heading in section
    m13_heading = (
        "### V15-M13 — *v2 Go / No-Go Decision* — **closed** on `main` (implementation [PR #139]"
    )
    assert m13_heading in section
    assert "v15_showcase_agent_release_pack_v1.md" in section
    assert "v15_v2_go_no_go_decision_v1.md" in section
    assert "v15_human_panel_bounded_benchmark_v1.md" in section
    assert "implementation [PR #137]" in section
    assert "implementation [PR #136]" in section
    assert "v15_replay_native_xai_demonstration_v1.md" in section
    assert "v15_long_gpu_campaign_execution_v1.md" in section
    assert "### V15-M07 — *Training Smoke and Short GPU Shakedown* — **closed**" in section
    assert "### V15-M06 — *Human Panel Benchmark Protocol* — **closed**" in section
    assert "**`V15-M05`**" in section
    assert "### V15-M04 — *XAI Evidence Contract v1* — **closed**" in section
    assert "### V15-M03 — *Checkpoint Lineage and Resume Discipline* — **closed**" in section
    assert "**`V15-M03`**" in section
    assert "**`V15-M04`**" in section
    assert "### V15-M02 — Long GPU Run Environment Lock — **closed**" in section
    assert "### V15-M00 — v1.5 Training Readiness Charter and Long GPU Run Gate" in section
    assert "### PX2-M03 — Industrial Self-Play Campaign — **closed**" in section
    assert "### PX2-M02 — Neural Bootstrap from Replays — **closed** on `main`" in section
    assert "### PX2-M01 — Full Terran Runtime & Action Surface — **closed** on `main`" in section
    assert (
        "### PX2-M00 — Autonomous Full-Game Agent Charter & Success Criteria — **closed** (`main`)"
        in section
    )
    assert (
        "### PX1-M04 — Governed Demo Proof Pack & Winning Video — **closed** (`main`)"
    ) in section
    assert (
        "### PX1-M03 — Candidate Strengthening & Demo Readiness Remediation — **closed** (`main`)"
    ) in section
    assert (
        "### PX1-M02 — Play-Quality Evaluation & Demo Candidate Selection — **closed**"
    ) in section
    assert "### PX1-M01 — Full Industrial Campaign Execution Evidence — **closed**" in section
    assert "px1_full_industrial_campaign_execution_evidence_v1.md" in section
    assert "### PX1-M00 — Full Industrial Run & Demonstration Charter — **closed**" in section
    assert "px1_full_industrial_run_demo_charter_v1.md" in section
    assert "### PV1-M04 — Post-Campaign Analysis / Comparative Readout — **closed**" in section
    assert "### PV1-M03 — Tranche B / Full-Run Completion Evidence — **closed**" in section
    assert "### PV1-M02 — Tranche A Execution Evidence — **closed**" in section
    assert "### PV1-M01 — Campaign Observability & Checkpoint Discipline — **closed**" in section
    assert "PV1-M00" in section
    assert "M47" in section
    assert "M50" in section
    assert "M51" in section
    assert "M52" in section
    assert "M53" in section
    assert "Bootstrap Episode Distinctness" in section or "Operator Ergonomics" in section
    assert "M46" in section
    assert "M45" in section
    assert "Self-Play" in section or "RL" in section
    assert "M44" in section
    assert "Local Live-Play Validation" in section
    assert section.lower().count("closed") >= 2


@pytest.mark.smoke
def test_ledger_milestone_table_m37_m45_rows() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    sec = text.split("## 7. Milestone table")[1].split("## 8")[0]
    assert "| M37 |" in sec and "Audit Closure VI" in sec and "Coverage Margin Recovery" in sec
    assert "| M38 |" in sec and "Audit Closure VII" in sec and "Public Face Refresh" in sec
    assert "| M39 |" in sec and "Public Flagship Proof Pack" in sec
    assert "| M40 |" in sec and "Agent Training Program Charter" in sec
    assert "| M41 |" in sec and "Replay-Imitation Training Pipeline" in sec and "Complete" in sec
    assert "| M42 |" in sec and "Learned-Agent Comparison" in sec and "Complete" in sec
    assert "| M43 |" in sec and "Hierarchical Training Pipeline" in sec and "Complete" in sec
    assert "| M44 |" in sec and "Local Live-Play Validation" in sec and "Complete" in sec
    assert "| M45 |" in sec and "Self-Play" in sec
    m48_line = next(line for line in sec.splitlines() if line.strip().startswith("| M48 |"))
    assert "Learned-Agent Comparison Contract-Path" in m48_line and "Complete" in m48_line
    assert "| M49 |" in sec and "Full Local Training" in sec and "Complete" in sec
    m50_line = next(line for line in sec.splitlines() if line.strip().startswith("| M50 |"))
    assert "Industrial-scale hidden rollout" in m50_line and "Complete" in m50_line
    m51_line = next(line for line in sec.splitlines() if line.strip().startswith("| M51 |"))
    assert "post-bootstrap" in m51_line and "Complete" in m51_line and "v0.0.51-m51" in m51_line


@pytest.mark.smoke
def test_od007_deferred_beyond_active_arc() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("| OD-007 |"):
            assert "Deferred" in line
            assert "Beyond active arc" in line or "beyond" in line.lower()
            return
    raise AssertionError("OD-007 row not found in docs/starlab.md")


def test_m01_changelog_entry_present() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### 2026-04-06 — M01 closeout" in text
    assert "OD-005" in text
    assert "### 2026-04-20 — **PX2-M02** closeout" in text
    assert "24645967129" in text
    assert "24646072791" in text
    assert "3b16c73fc3dd1cd4c5fbd73dd33c6bb0b2e486db" in text
    assert "### 2026-04-23 — **PX2** transition closeout" in text
    assert "### 2026-04-20 — **PX2-M03** opening" in text
    assert "px2_industrial_self_play_campaign_readiness_v1.md" in text
    assert "### 2026-04-19 — **PX2-M03** first implementation slice" in text
    assert "### 2026-04-19 — **PX2-M03** second implementation slice" in text
    assert "### 2026-04-20 — **PX2-M03** third implementation slice" in text
    assert "### 2026-04-19 — **PX2-M03** fifth implementation slice" in text
    assert "### 2026-04-20 — **PX2-M03** fourth implementation slice" in text
    assert "px2_industrial_self_play_campaign_v1.md" in text
    assert "### 2026-04-19 — **PX2-M02** opening" in text
    assert "### 2026-04-19 — **PX2-M01** closeout" in text
    assert "24643980874" in text
    assert "24644245868" in text
    assert "24644285043" in text
    assert "dd5ce04a5ab531326ebf2b6a65951edea49e5813" in text
