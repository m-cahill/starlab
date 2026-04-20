"""PX2-M03 — industrial self-play campaign surfaces (contract through slice 3)."""

from __future__ import annotations

from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    PX2_SELF_PLAY_CAMPAIGN_REPORT_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
    seal_px2_self_play_campaign_body,
)
from starlab.sc2.px2.self_play.campaign_run import (
    PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_CAMPAIGN_RUN_REPORT_CONTRACT_ID,
    run_px2_campaign_execution_skeleton,
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
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import (
    PolicyRuntimeBridgeReceipt,
    bootstrap_policy_runtime_step,
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
    "EXECUTION_KIND_SLICE3",
    "WEIGHT_MODE_INIT_ONLY",
    "WEIGHT_MODE_WEIGHTS_FILE",
    "OpponentPoolStub",
    "PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID",
    "PX2_SELF_PLAY_CAMPAIGN_REPORT_CONTRACT_ID",
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
    "PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_SMOKE_RUN_REPORT_CONTRACT_ID",
    "PolicyRuntimeBridgeReceipt",
    "bootstrap_policy_runtime_step",
    "build_default_opponent_pool_stub",
    "build_policy_operator_local",
    "build_px2_self_play_campaign_artifacts",
    "build_px2_self_play_smoke_run_artifacts",
    "run_execution_preflight",
    "run_operator_local_campaign_smoke",
    "run_px2_campaign_execution_skeleton",
    "run_px2_fixture_self_play_smoke",
    "seal_px2_self_play_campaign_body",
    "select_opponent_ref",
    "sha256_hex_file",
]
