"""PX2-M03 — industrial self-play campaign surfaces (contract through slice 6)."""

from __future__ import annotations

from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE4,
    EXECUTION_KIND_SLICE5,
    EXECUTION_KIND_SLICE6,
    PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID,
    PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_REPORT_CONTRACT_ID,
    run_operator_local_campaign_continuity,
)
from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    PX2_SELF_PLAY_CAMPAIGN_REPORT_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
    seal_px2_self_play_campaign_body,
)
from starlab.sc2.px2.self_play.campaign_root import (
    default_operator_local_campaign_root_subdirs,
    ensure_operator_local_campaign_root_layout,
    recommended_operator_out_campaign_root_path,
    run_slice5_operator_local_campaign,
)
from starlab.sc2.px2.self_play.campaign_root_manifest import (
    PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_CONTRACT_ID,
    PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_REPORT_CONTRACT_ID,
    build_px2_self_play_campaign_root_manifest_artifacts,
)
from starlab.sc2.px2.self_play.campaign_run import (
    PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_CAMPAIGN_RUN_REPORT_CONTRACT_ID,
    run_px2_campaign_execution_skeleton,
)
from starlab.sc2.px2.self_play.canonical_operator_local_run import (
    resolve_canonical_campaign_root,
    run_canonical_operator_local_campaign_root_smoke,
)
from starlab.sc2.px2.self_play.checkpoint_receipts import (
    PX2_SELF_PLAY_CHECKPOINT_RECEIPT_CONTRACT_ID,
    PX2_SELF_PLAY_CHECKPOINT_RECEIPT_REPORT_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.evaluation_receipts import (
    PX2_SELF_PLAY_EVALUATION_RECEIPT_CONTRACT_ID,
    PX2_SELF_PLAY_EVALUATION_RECEIPT_REPORT_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.execution_preflight import (
    PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID,
    PX2_SELF_PLAY_EXECUTION_PREFLIGHT_REPORT_CONTRACT_ID,
    run_execution_preflight,
)
from starlab.sc2.px2.self_play.operator_local_smoke import (
    EXECUTION_KIND_SLICE3,
    PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_CONTRACT_ID,
    PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_REPORT_CONTRACT_ID,
    run_operator_local_campaign_smoke,
)
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_FROZEN_SEED,
    OPPONENT_SELECTION_ROUND_ROBIN,
    OPPONENT_SELECTION_SELF_SNAPSHOT,
    OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.path_identity import (
    PREFLIGHT_SEAL_VERSION,
    build_preflight_seal_basis,
    corpus_root_logical_posix,
    output_dir_logical_posix,
    weights_path_logical_posix,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import (
    PolicyRuntimeBridgeReceipt,
    bootstrap_policy_runtime_step,
)
from starlab.sc2.px2.self_play.promotion_receipts import (
    PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID,
    PX2_SELF_PLAY_PROMOTION_RECEIPT_REPORT_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.rollback_receipts import (
    PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID,
    PX2_SELF_PLAY_ROLLBACK_RECEIPT_REPORT_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.run_artifacts import (
    build_slice4_continuity_manifest,
    default_operator_local_slice4_subdirs,
    ensure_operator_local_slice4_layout,
)
from starlab.sc2.px2.self_play.smoke_run import (
    PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_SMOKE_RUN_REPORT_CONTRACT_ID,
    build_px2_self_play_smoke_run_artifacts,
    run_px2_fixture_self_play_smoke,
)
from starlab.sc2.px2.self_play.snapshot_pool import (
    OpponentPoolStub,
    build_default_opponent_pool_stub,
    build_slice5_opponent_pool,
    opponent_battle_ref_ids,
    opponent_pool_identity_sha256,
)
from starlab.sc2.px2.self_play.weight_loading import (
    WEIGHT_MODE_INIT_ONLY,
    WEIGHT_MODE_WEIGHTS_FILE,
    build_policy_operator_local,
    sha256_hex_file,
)

__all__ = [
    "OPPONENT_SELECTION_FROZEN_SEED",
    "OPPONENT_SELECTION_ROUND_ROBIN",
    "OPPONENT_SELECTION_SELF_SNAPSHOT",
    "OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB",
    "EXECUTION_KIND_SLICE3",
    "EXECUTION_KIND_SLICE4",
    "EXECUTION_KIND_SLICE5",
    "EXECUTION_KIND_SLICE6",
    "WEIGHT_MODE_INIT_ONLY",
    "WEIGHT_MODE_WEIGHTS_FILE",
    "OpponentPoolStub",
    "PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_RUN_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_CHECKPOINT_RECEIPT_CONTRACT_ID",
    "PX2_SELF_PLAY_CHECKPOINT_RECEIPT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_EVALUATION_RECEIPT_CONTRACT_ID",
    "PX2_SELF_PLAY_EVALUATION_RECEIPT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID",
    "PX2_SELF_PLAY_EXECUTION_PREFLIGHT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID",
    "PX2_SELF_PLAY_PROMOTION_RECEIPT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID",
    "PX2_SELF_PLAY_ROLLBACK_RECEIPT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_SMOKE_RUN_REPORT_CONTRACT_ID",
    "PREFLIGHT_SEAL_VERSION",
    "PolicyRuntimeBridgeReceipt",
    "bootstrap_policy_runtime_step",
    "build_default_opponent_pool_stub",
    "build_px2_self_play_campaign_root_manifest_artifacts",
    "build_slice5_opponent_pool",
    "build_policy_operator_local",
    "build_slice4_continuity_manifest",
    "build_preflight_seal_basis",
    "build_px2_self_play_campaign_artifacts",
    "build_px2_self_play_smoke_run_artifacts",
    "default_operator_local_campaign_root_subdirs",
    "corpus_root_logical_posix",
    "default_operator_local_slice4_subdirs",
    "ensure_operator_local_campaign_root_layout",
    "ensure_operator_local_slice4_layout",
    "opponent_battle_ref_ids",
    "opponent_pool_identity_sha256",
    "output_dir_logical_posix",
    "resolve_canonical_campaign_root",
    "run_canonical_operator_local_campaign_root_smoke",
    "run_execution_preflight",
    "recommended_operator_out_campaign_root_path",
    "run_operator_local_campaign_continuity",
    "run_slice5_operator_local_campaign",
    "run_operator_local_campaign_smoke",
    "run_px2_campaign_execution_skeleton",
    "run_px2_fixture_self_play_smoke",
    "seal_px2_self_play_campaign_body",
    "select_opponent_ref",
    "sha256_hex_file",
    "weights_path_logical_posix",
]
