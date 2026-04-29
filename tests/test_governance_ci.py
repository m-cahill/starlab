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
def test_v15_m16_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M16" in v15
    assert "PR #142" in v15
    assert "24968275296" in v15
    assert "24968604458" in v15
    assert "closed on `main`" in v15 or "closed** on `main`" in v15
    assert "starlab.v15.short_gpu_environment_evidence.v1" in v15
    assert "M16 non-claims" in v15
    assert "emit_v15_short_gpu_environment_evidence" in v15
    assert "V15-M17" in v15 and "V15-M21" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_short_gpu_environment_evidence_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "milestone" in rtx and "g0" in rtx and "contract" in rtx
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M16" in rights
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_short_gpu_environment_evidence_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m18_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M18" in v15
    assert "starlab.v15.checkpoint_evaluation_readiness.v1" in v15
    assert "M18 non-claims" in v15
    assert "emit_v15_checkpoint_evaluation_readiness" in v15
    assert "25023439537" in v15
    assert "25023582158" in v15
    assert "V15-M19" in v15 and "V15-M21" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_checkpoint_evaluation_readiness_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "contract id" in rtx and "readiness" in rtx and "refusal" in rtx
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_checkpoint_evaluation_readiness_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m19_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M19" in v15
    assert "PR #151" in v15
    assert "25025083247" in v15
    assert "25025427887" in v15
    assert "closed" in v15
    assert "starlab.v15.candidate_checkpoint_evaluation_package.v1" in v15
    assert "M19 non-claims" in v15
    assert "emit_v15_candidate_checkpoint_evaluation_package" in v15
    assert "recommended_m20_fork" in v15
    assert "V15-M20" in v15 and "V15-M21" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_candidate_checkpoint_evaluation_package_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "contract" in rtx and "package" in rtx and "p0" in rtx
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_candidate_checkpoint_evaluation_package_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m20_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M20" in v15
    assert "PR #152" in v15
    assert "25027412708" in v15
    assert "25027870414" in v15
    assert "starlab.v15.real_candidate_checkpoint_production_gate.v1" in v15
    assert "fixture_no_operator_run" in v15
    assert "merge CI" in v15 or "merge ci" in v15.lower()
    assert "emit_v15_real_candidate_checkpoint_production_gate" in v15
    assert "run_v15_t1_30min_candidate_checkpoint_gate" in v15
    assert "V15-M21" in v15 and "starlab.v15.operator_t1_30min_gpu_run_execution.v1" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_real_candidate_checkpoint_production_gate_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "contract id" in rtx and "t1" in rtx and "30" in rtx
    assert "status" in rtx and "closed" in rtx
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_real_candidate_checkpoint_production_gate_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m21_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M21" in v15
    assert "PR #153" in v15
    assert "25029512815" in v15
    assert "25029902265" in v15
    assert "starlab.v15.operator_t1_30min_gpu_run_execution.v1" in v15
    assert "M21 non-claims" in v15
    assert "emit_v15_operator_t1_30min_gpu_run_execution" in v15
    assert "run_v15_m21_t1_30min_gpu_run_execution" in v15
    assert "run_v15_t1_30min_candidate_checkpoint_gate" in v15
    assert "t1_30min_run_not_started" in v15
    assert "dry-run preflight" in v15.lower()
    assert "full operator-local T1 30-minute GPU run was not performed" in v15.replace("\n", " ")
    assert "V15-M22" in v15
    assert "PR #154" in v15
    assert "25031597888" in v15
    assert "25031726394" in v15
    assert (
        "operator_preflight_blocked" in v15
        or "torch_cuda_unavailable" in v15
        or ("proposed" in v15 and "V15-M22" in v15)
    )
    rt = REPO_ROOT / "docs" / "runtime" / "v15_operator_t1_30min_gpu_run_execution_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "contract id" in rtx and "t1" in rtx and "30" in rtx
    assert "status" in rtx and "closed" in rtx
    assert "dry-run preflight" in rtx or "preflight" in rtx
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_operator_t1_30min_gpu_run_execution_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m23_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M23" in v15
    assert "CUDA PyTorch Operator Environment Remediation" in v15
    assert "v15-m23-cuda-pytorch-operator-env-remediation" in v15
    assert "PR #156" in v15
    assert "PR #157" in v15
    assert "25032909816" in v15
    assert "25033137726" in v15
    assert "7ceb750a" in v15
    assert "closed" in v15 and "V15-M23" in v15
    assert "M23 non-claims block" in v15
    assert "torch_cuda_unavailable" in v15
    assert "V15-M24" in v15
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M23" in ledger
    assert "v15-m23-cuda-pytorch-operator-env-remediation" in ledger
    assert "PR #156" in ledger
    assert "25032909816" in ledger
    assert "**`V15-M24`**" in ledger


@pytest.mark.smoke
def test_v15_m24_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M24" in v15
    assert "operator_preflight_blocked" in v15
    assert "missing_private_manifest_inputs" in v15
    assert "M24 non-claims block" in v15
    low = v15.lower()
    assert "not strength evaluation" in low or "not_strength_evaluation" in low
    assert "not checkpoint promotion" in low or "not_checkpoint_promotion" in low
    m24_nc = v15.split("M24 non-claims block", 1)[1][:1200].lower()
    assert "v2" in m24_nc
    assert ".venv" in v15
    assert "v15-m24-real-t1-30min-gpu-attempt" in v15
    assert "V15-M25" in v15
    assert "merge PR pending" not in v15
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M24" in ledger
    assert "V15-M25" in ledger
    assert "operator_preflight_blocked" in ledger
    assert "missing_private_manifest_inputs" in ledger


@pytest.mark.smoke
def test_v15_m26_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    low = v15.lower()
    assert "V15-M26" in v15
    assert "PR #162" in v15
    assert "M26 non-claims block" in v15
    assert "t1_30min_completed_without_candidate_checkpoint" in v15
    assert "t1_30min_checkpoint_produced_package_ready" in v15
    assert "t1_checkpoint_plumbing_completed_but_sc2_training_not_yet_meaningful" in v15
    assert "t1_30min_completed_with_candidate_checkpoint" in v15
    assert "no_pytorch_checkpoint_artifact_under_execution_root" in v15
    assert "not meaningful sc2 agent training" in low or "meaningful sc2" in low
    assert "synthetic cuda" in low
    assert "sc2 rollout path" in low
    assert "not yet meaningful sc2 training" in low or "not meaningful sc2 training" in low
    assert "cb375b77a92f6f07b406d8579a60f3539568be12877808d600826c049e146e78" in v15
    compact_v15 = v15.replace("*", "").lower()
    assert "no promotion" in compact_v15
    assert "V15-M27" in v15
    assert "SC2 Rollout Duration and Training-Loop Integration Fix" in v15
    assert "v15-m26-real-t1-30min-gpu-run" in v15
    assert "393adb7f" in v15
    assert "25046959088" in v15
    assert "25047132158" in v15
    assert "9d877da2" in v15
    assert "closed on `main`" in v15.lower() or "closed** on `main`" in v15
    assert "open** on [PR #162]" not in v15
    assert "dry_run_preflight_performed" in low or "non-dry-run" in v15.lower()
    assert "not strength" in low or "not_strength" in low
    assert "not checkpoint promotion" in low or "not_checkpoint_promotion" in low
    assert "merge PR pending" not in v15
    assert "sc2-harness" in low or "sc2-harness" in v15
    narrative = (
        "M26 completed T1 checkpoint-production plumbing and produced a candidate checkpoint "
        "via synthetic CUDA, but the SC2 rollout path remained bounded smoke/bootstrap only "
        "and is not yet meaningful SC2 training."
    )
    assert narrative in v15.replace("\n", " ")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    led_low = ledger.lower()
    assert "V15-M26" in ledger
    assert "V15-M27" in ledger
    assert "PR #162" in ledger
    assert "t1_30min_completed_without_candidate_checkpoint" in ledger
    assert "t1_30min_checkpoint_produced_package_ready" in ledger
    assert "t1_checkpoint_plumbing_completed_but_sc2_training_not_yet_meaningful" in ledger
    assert "synthetic cuda" in led_low
    assert "sc2 rollout path" in led_low
    assert "not yet meaningful sc2 training" in led_low or "not meaningful sc2 training" in led_low
    assert "cb375b77a92f6f07b406d8579a60f3539568be12877808d600826c049e146e78" in ledger
    assert "no promotion" in ledger.replace("*", "").lower()
    assert "SC2 Rollout Duration and Training-Loop Integration Fix" in ledger
    assert "393adb7f" in ledger
    assert "25046959088" in ledger or "25047132158" in ledger
    assert narrative in ledger.replace("\n", " ")


@pytest.mark.smoke
def test_v15_m27_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M27" in v15
    assert "V15-M27" in ledger
    assert "SC2 Rollout Duration and Training-Loop Integration Fix" in v15
    assert "starlab.v15.sc2_rollout_training_loop_integration.v1" in v15
    assert "v15_m27_nontrivial_macro_smoke_policy_v1" in v15
    assert "sc2_rollout_training_loop_integration_completed" in v15
    assert "sc2_rollout_training_loop_integration_completed" in ledger
    assert "PR #163" in ledger
    assert "25078974410" in ledger
    assert "25079150705" in ledger
    assert "sc2_rollout_fixture_only" in v15
    assert "action_count" in v15
    assert "training_loop_binding" in v15 or "training_update_executed" in v15
    assert "PR #163" in v15
    assert "25078974410" in v15
    assert "25079150705" in v15
    assert "960f925a" in v15.lower() or "960f925afb2d1913055fe3ae18dc0b76a4c0951f" in v15.lower()
    assert "d3c53b1c" in v15.lower() or "d3c53b1cb322f2080d2ed3991a80ddcc7968425f" in v15.lower()
    assert "25079519363" in v15
    low = v15.lower()
    assert "m27 non-claims" in low
    assert "not strength" in low or "not benchmark" in low
    assert ("integration_smoke" in low) or ("integration-smoke" in v15)
    assert ("not strength evaluation" in low) or ("not strength" in low)
    assert "not v2" in low or "not_v2" in low
    rt = REPO_ROOT / "docs" / "runtime" / "v15_sc2_rollout_training_loop_integration_v1.md"
    assert rt.is_file()


@pytest.mark.smoke
def test_v15_m28_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M28" in v15
    assert "V15-M28" in ledger
    assert "SC2-Backed T1 Candidate Training Attempt" in v15
    assert "starlab.v15.sc2_backed_t1_candidate_training.v1" in v15
    assert "run_v15_m28_sc2_backed_t1_candidate_training" in v15
    assert "f9c2ca5aca7a3b15df0567358c1f207f99e112cd8d816f5ac1a1c6ff04022227" in v15
    assert "sc2_backed_candidate_training_completed_with_candidate_checkpoint" in v15
    assert "sc2_backed_features_used" in v15.lower()
    assert "fixture_only" in v15.lower()
    assert "71897cfff94fba7209e667dd44e040eabc705e686c6a579cd26e13015f00ecc8" in v15
    assert "PR #164" in v15
    assert "25083196925" in v15
    assert "25083354466" in v15
    assert "40550e64" in v15.lower() or "40550e6481c6f5988cd72e210e2a17d16f533e81" in v15.lower()
    assert "35d59f11" in v15.lower() or "35d59f11e64b5b8fcb2c2937572478bfa9f37863" in v15.lower()
    low = v15.lower()
    assert "m28 non-claims" in low
    assert "not strength evaluation" in low or "not_strength_evaluation" in low
    assert "not benchmark pass" in low or "not_benchmark_pass" in low
    assert "not checkpoint promotion" in low or "not_checkpoint_promotion" in low
    assert "not v2" in low or "not_v2_authorization" in low
    rt28 = REPO_ROOT / "docs" / "runtime" / "v15_sc2_backed_t1_candidate_training_v1.md"
    assert rt28.is_file()


@pytest.mark.smoke
def test_v15_m29_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M29" in v15
    assert "V15-M29" in ledger
    assert "Full 30-Minute SC2-Backed T1 Candidate Run" in v15 or "full 30-minute" in v15.lower()
    assert "V15-M30" in v15
    assert "starlab.v15.full_30min_sc2_backed_t1_run.v1" in v15
    assert "run_v15_m29_full_30min_sc2_backed_t1_run" in v15
    low = v15.lower().replace("`", "")
    assert "observed_wall_clock_seconds" in low or "full_wall_clock_satisfied" in low
    assert "m29 non-claims" in low
    assert "not benchmark pass" in low or "not_benchmark_pass" in low
    assert "not strength" in low
    rt29 = REPO_ROOT / "docs" / "runtime" / "v15_full_30min_sc2_backed_t1_run_v1.md"
    assert rt29.is_file()


@pytest.mark.smoke
def test_v15_m30_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M30" in v15
    assert "V15-M30" in ledger
    assert "starlab.v15.candidate_checkpoint_evaluation_package.v1" in v15
    assert "emit_v15_m30_sc2_backed_candidate_checkpoint_evaluation_package" in v15
    low = v15.lower().replace("`", "")
    assert (
        "m30 non-claims" in low or "assembly/binding" in low or "not_promoted_candidate_only" in low
    )
    rt30 = (
        REPO_ROOT
        / "docs"
        / "runtime"
        / "v15_sc2_backed_candidate_checkpoint_evaluation_package_v1.md"
    )
    assert rt30.is_file()


@pytest.mark.smoke
def test_v15_m31_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M31" in v15
    assert "V15-M31" in ledger
    assert "starlab.v15.candidate_checkpoint_evaluation_harness_gate.v1" in v15
    assert "emit_v15_m31_candidate_checkpoint_evaluation_harness_gate" in v15.replace("\n", " ")
    low = v15.lower().replace("`", "")
    assert "m31 non-claims" in low or "evaluation_harness_ready" in low
    rt31 = REPO_ROOT / "docs" / "runtime" / "v15_candidate_checkpoint_evaluation_harness_gate_v1.md"
    assert rt31.is_file()


@pytest.mark.smoke
def test_v15_m32_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M32" in v15
    assert "V15-M32" in ledger
    assert "starlab.v15.candidate_checkpoint_evaluation_execution.v1" in v15
    assert "emit_v15_m32_candidate_checkpoint_evaluation_execution" in v15.replace("\n", " ")
    low = v15.lower().replace("`", "")
    assert "m32 non-claims" in low
    assert "not benchmark pass" in low or "not_benchmark_pass" in low
    assert "v15-m33" in low or "V15-M33" in v15
    rt32 = REPO_ROOT / "docs" / "runtime" / "v15_candidate_checkpoint_evaluation_execution_v1.md"
    assert rt32.is_file()


@pytest.mark.smoke
def test_v15_m33_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M33" in v15
    assert "V15-M33" in ledger
    assert "starlab.v15.candidate_checkpoint_model_load_cuda_probe.v1" in v15
    assert "emit_v15_m33_candidate_checkpoint_model_load_cuda_probe" in v15.replace("\n", " ")
    low = v15.lower().replace("`", "")
    assert "m33 non-claims" in low
    assert "seventy_two" in low or "72-hour" in low or "72" in low
    assert "v15-m34" in low or "V15-M34" in v15
    rt33 = REPO_ROOT / "docs" / "runtime" / "v15_candidate_checkpoint_model_load_cuda_probe_v1.md"
    assert rt33.is_file()


@pytest.mark.smoke
def test_v15_m34_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M34" in v15
    assert "V15-M34" in ledger
    assert "PR #170" in v15
    low = v15.lower().replace("`", "")
    assert "m34 non-claims" in low
    assert "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26" in v15
    assert "candidate_model_load_cuda_probe_completed" in v15
    assert "v15-m35" in low or "V15-M35" in v15


@pytest.mark.smoke
def test_v15_m35_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M35" in v15
    assert "V15-M35" in ledger
    assert "PR #171" in v15
    assert "25129363401" in v15
    assert "25129578504" in v15
    assert "3bf3fa46" in v15
    assert "PR #171" in ledger
    assert "starlab.v15.candidate_checkpoint_smoke_benchmark_readiness.v1" in v15
    assert "emit_v15_m35_candidate_checkpoint_smoke_benchmark_readiness" in v15.replace("\n", " ")
    low = v15.lower().replace("`", "")
    assert "m35 non-claims" in low
    assert "fixture_schema_only_no_benchmark_execution" in low
    assert "v15-m37" in low or "V15-M37" in v15
    rt35 = REPO_ROOT / "docs/runtime/v15_candidate_checkpoint_smoke_benchmark_readiness_v1.md"
    assert rt35.is_file()
    rt35_text = rt35.read_text(encoding="utf-8")
    assert "PR #171" in rt35_text
    assert "25129363401" in rt35_text


@pytest.mark.smoke
def test_v15_m36_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M36" in v15
    assert "V15-M36" in ledger
    assert "PR #172" in v15
    assert "PR #172" in ledger
    assert "25131688817" in v15
    assert "25131917336" in v15
    assert "aa0adba4" in v15
    assert "starlab.v15.smoke_benchmark_execution.v1" in v15
    assert "emit_v15_m36_smoke_benchmark_execution" in v15.replace("\n", " ")
    low = v15.lower().replace("`", "")
    assert "m36 non-claims" in low
    assert "fixture_schema_only_no_candidate_execution" in low
    assert "v15-m37" in low or "V15-M37" in v15
    rt36 = REPO_ROOT / "docs/runtime/v15_smoke_benchmark_execution_surface_v1.md"
    assert rt36.is_file()
    rt_body = rt36.read_text(encoding="utf-8")
    rt_text = rt_body.lower()
    assert "PR #172" in rt_body
    assert "not a 2-hour run" in rt_text or "2-hour" in rt_text


@pytest.mark.smoke
def test_v15_m37_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    rt37 = REPO_ROOT / "docs/runtime/v15_two_hour_run_blocker_discovery_v1.md"
    assert rt37.is_file()
    rt_body = rt37.read_text(encoding="utf-8")
    assert "starlab.v15.two_hour_run_blocker_discovery.v1" in rt_body
    assert "fixture_schema_only_no_operator_audit" in rt_body.lower()
    assert "PR #" not in rt_body
    assert "V15-M37" in v15
    assert "V15-M37" in ledger
    assert "two_hour_run_blocker_discovery" in v15.replace("\n", " ")
    assert "emit_v15_m37_two_hour_run_blocker_discovery" in v15.replace("\n", " ")
    assert "PR #173" in v15
    assert "25136254104" in v15
    assert "25136423879" in v15
    assert "291aa417" in v15
    low = v15.lower().replace("`", "")
    assert "m37 non-claims" in low
    assert "v15-m38" in low or "V15-M38" in v15
    assert "PR #174" in v15
    assert "blocker-discovery/readiness-audit" in v15.replace("\n", " ").lower()
    assert "PR #173" in ledger
    assert "PR #174" in ledger
    assert "25136254104" in ledger
    assert "25136423879" in ledger
    assert "blocker discovery" in ledger.lower() or "2-hour" in ledger.lower()


@pytest.mark.smoke
def test_v15_m38_governance_surface() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    rt38 = REPO_ROOT / "docs/runtime/v15_two_hour_run_remediation_launch_rehearsal_v1.md"
    assert rt38.is_file()
    rt_body = rt38.read_text(encoding="utf-8")
    assert "starlab.v15.two_hour_run_remediation_launch_rehearsal.v1" in rt_body
    assert "PR #" not in rt_body
    assert "5843bbdf" in rt_body
    assert "9cf2944d" in rt_body
    assert "V15-M38" in v15
    assert "V15-M38" in ledger
    assert "emit_v15_m38_two_hour_run_remediation_launch_rehearsal" in v15.replace("\n", " ")
    assert "V15-M39" in v15
    assert "V15-M39" in ledger
    assert "PR #174" in v15
    assert "25138210391" in v15
    assert "25138442045" in v15
    assert "9cf2944d" in v15
    assert "5843bbdf" in v15
    assert "PR #174" in ledger
    assert "25138210391" in ledger
    assert "25138442045" in ledger
    low = v15.lower().replace("`", "")
    assert "m38 non-claims" in low
    assert "fixture_schema_only_no_operator_rehearsal" in rt_body.lower()
    assert "v15-m39" in low or "V15-M39" in v15


def test_v15_m25_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M25" in v15
    assert "25039367953" in v15
    assert "e4ecc95e" in v15
    assert "m21_dry_run_preflight_passed" in v15
    assert "ready_for_v15_m26_t1_attempt" in v15
    assert "M25 non-claims block" in v15
    assert "fixture_ci" in v15.lower()
    low = v15.lower()
    assert "dry-run-preflight-only" in low or "--dry-run-preflight-only" in low.replace("`", "")
    assert "real t1" in low and "not" in low
    assert "no checkpoint" in low or ("candidate checkpoint" in low and "not" in low)
    assert "merge PR pending" not in v15
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "V15-M25" in ledger
    assert "V15-M26" in ledger
    assert "PR #160" in ledger
    assert "25039367953" in ledger


@pytest.mark.smoke
def test_v15_m17_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M17" in v15
    assert "PR #143" in v15
    assert "24971298575" in v15
    assert "24971687346" in v15
    assert "closed on `main`" in v15 or "closed** on `main`" in v15
    assert "starlab.v15.long_gpu_campaign_evidence.v1" in v15
    assert "M17 non-claims" in v15
    assert "emit_v15_long_gpu_campaign_evidence" in v15
    assert "V15-M18" in v15 and "V15-M21" in v15
    rt = REPO_ROOT / "docs" / "runtime" / "v15_long_gpu_campaign_evidence_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "milestone" in rtx and "l0" in rtx and "contract" in rtx
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M17" in rights
    ledger = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "v15_long_gpu_campaign_evidence_v1.md" in ledger


@pytest.mark.smoke
def test_v15_m15_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M15" in v15
    assert "PR #141" in v15
    assert "24966701437" in v15
    assert "24967008755" in v15
    assert "closed on `main`" in v15 or "closed** on `main`" in v15
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
    assert "**`V15-M17`**" in scan
    assert "**`V15-M18`**" in scan
    assert "**`V15-M19`**" in scan
    assert "**`V15-M20`**" in scan
    assert "**`V15-M21`**" in scan
    assert "**`V15-M22`**" in scan
    assert "**`V15-M23`**" in scan
    assert "**`V15-M24`**" in scan
    assert "**`V15-M25`**" in scan
    assert "**`V15-M26`**" in scan
    assert "**`V15-M27`**" in scan
    assert "**`V15-M28`**" in scan
    assert "**`V15-M29`**" in scan
    assert "**`V15-M30`**" in scan
    assert "**`V15-M31`**" in scan
    assert "**`V15-M32`**" in scan
    assert "PR #142" in scan or "pull/142" in scan
    assert "PR #141" in scan or "pull/141" in scan
    assert "**`V15-M14`**" in scan
    assert "PR #140" in scan or "pull/140" in scan
    assert "PR #139" in scan or "pull/139" in scan
    assert "PR #137" in scan
    assert "PR #136" in scan
    assert "**`V15-M10`**" in scan
    assert "**`V15-M09`**" in scan
    assert "PR #135" in scan or "pull/135" in scan
    assert "**`V15-M08`**" in scan and "**`V15-M07`**" in scan and "**`V15-M06`**" in scan
    assert "PR #133" in scan or "pull/133" in scan
    assert "PR #152" in scan or "pull/152" in scan
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
    assert "**`V15-M22`**" in section
    assert "**`V15-M23`**" in section
    assert "**`V15-M24`**" in section
    assert "**`V15-M25`**" in section
    assert "**`V15-M26`**" in section
    assert "**`V15-M27`**" in section
    assert "**`V15-M28`**" in section
    assert "**`V15-M31`**" in section
    assert "**`V15-M32`**" in section
    assert "**`V15-M21`**" in section
    assert "**`V15-M20`**" in section
    assert "**`V15-M19`**" in section
    assert "**`V15-M18`**" in section
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
