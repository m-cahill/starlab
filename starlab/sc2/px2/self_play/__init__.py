"""PX2-M03 — industrial self-play campaign surfaces (contract through slice 16)."""

from __future__ import annotations

from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE4,
    EXECUTION_KIND_SLICE5,
    EXECUTION_KIND_SLICE6,
    EXECUTION_KIND_SLICE7,
    EXECUTION_KIND_SLICE8,
    EXECUTION_KIND_SLICE9,
    EXECUTION_KIND_SLICE10,
    EXECUTION_KIND_SLICE11,
    EXECUTION_KIND_SLICE12,
    EXECUTION_KIND_SLICE13,
    EXECUTION_KIND_SLICE13_REANCHOR,
    EXECUTION_KIND_SLICE14,
    EXECUTION_KIND_SLICE15,
    EXECUTION_KIND_SLICE16,
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
from starlab.sc2.px2.self_play.continuation_run import (
    CONTINUATION_RUN_JSON,
    SLICE11_CAMPAIGN_PROFILE_ID,
    SLICE13_SECOND_HOP_CAMPAIGN_PROFILE_ID,
    run_bounded_continuation_run_consuming_current_candidate,
    validate_current_candidate_for_continuation_run,
)
from starlab.sc2.px2.self_play.continuation_run_record import (
    CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB,
    CONTINUATION_RULE_SECOND_HOP_CONSUME_CURRENT_CANDIDATE_STUB,
    CONTINUATION_RUN_RECORD_VERSION_SLICE13,
    PX2_SELF_PLAY_CONTINUATION_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_CONTINUATION_RUN_REPORT_CONTRACT_ID,
    build_px2_self_play_continuation_run_artifacts,
)
from starlab.sc2.px2.self_play.current_candidate import (
    DEFAULT_SLICE10_CAMPAIGN_ID,
    load_px2_self_play_current_candidate,
    next_run_preflight_hints_from_current_candidate,
    run_bounded_operator_local_session_transition_with_current_candidate,
)
from starlab.sc2.px2.self_play.current_candidate_reanchor import (
    CURRENT_CANDIDATE_REANCHOR_JSON,
    SLICE12_CAMPAIGN_PROFILE_ID,
    run_bounded_current_candidate_reanchor_after_continuation,
    run_bounded_current_candidate_reanchor_after_second_hop,
)
from starlab.sc2.px2.self_play.current_candidate_reanchor_record import (
    PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_CONTRACT_ID,
    PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_REPORT_CONTRACT_ID,
    REANCHOR_RULE_POST_CONTINUATION_STUB,
    REANCHOR_RULE_POST_SECOND_HOP_STUB,
    build_px2_self_play_current_candidate_reanchor_artifacts,
)
from starlab.sc2.px2.self_play.current_candidate_record import (
    CURRENT_CANDIDATE_RECORD_VERSION_SLICE12,
    CURRENT_CANDIDATE_RECORD_VERSION_SLICE13,
    CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB,
    CURRENT_CANDIDATE_RULE_REANCHOR_FROM_CONTINUATION_STUB,
    CURRENT_CANDIDATE_RULE_REANCHOR_FROM_SECOND_HOP_STUB,
    PX2_SELF_PLAY_CURRENT_CANDIDATE_CONTRACT_ID,
    PX2_SELF_PLAY_CURRENT_CANDIDATE_REPORT_CONTRACT_ID,
    build_px2_self_play_current_candidate_artifacts,
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
from starlab.sc2.px2.self_play.handoff_anchored_run import (
    HANDOFF_ANCHORED_RUN_JSON,
    run_bounded_handoff_anchored_operator_local_run,
    verify_loaded_pointer_seeded_handoff_self_seal,
)
from starlab.sc2.px2.self_play.handoff_anchored_run_record import (
    ANCHOR_SEMANTICS_DECLARED_FROM_SLICE15_HANDOFF_JSON_V1,
    HANDOFF_ANCHORED_RUN_RULE_ANCHOR_ON_SLICE15_HANDOFF_STUB,
    PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_REPORT_CONTRACT_ID,
    build_px2_self_play_handoff_anchored_run_artifacts,
)
from starlab.sc2.px2.self_play.operator_local_real_run import (
    DEFAULT_SLICE7_CAMPAIGN_ID,
    run_bounded_operator_local_real_run,
)
from starlab.sc2.px2.self_play.operator_local_real_run_record import (
    PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_REPORT_CONTRACT_ID,
    build_px2_self_play_operator_local_real_run_artifacts,
)
from starlab.sc2.px2.self_play.operator_local_session import (
    DEFAULT_SLICE8_CAMPAIGN_ID,
    run_bounded_operator_local_session,
)
from starlab.sc2.px2.self_play.operator_local_session_record import (
    PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_CONTRACT_ID,
    PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_REPORT_CONTRACT_ID,
    build_px2_self_play_operator_local_session_artifacts,
)
from starlab.sc2.px2.self_play.operator_local_session_transition import (
    DEFAULT_SLICE9_CAMPAIGN_ID,
    run_bounded_operator_local_session_with_transition,
)
from starlab.sc2.px2.self_play.operator_local_session_transition_record import (
    PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_CONTRACT_ID,
    PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_REPORT_CONTRACT_ID,
    build_px2_self_play_operator_local_session_transition_artifacts,
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
from starlab.sc2.px2.self_play.pointer_seeded_handoff import (
    POINTER_SEEDED_HANDOFF_JSON,
    run_bounded_pointer_seeded_handoff,
    verify_loaded_pointer_seeded_run_self_seal,
)
from starlab.sc2.px2.self_play.pointer_seeded_handoff_record import (
    DECLARED_NEXT_STEP_FROM_SLICE14_POINTER_SEEDED_V1,
    POINTER_SEEDED_HANDOFF_RULE_AFTER_SLICE14_STUB,
    PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_CONTRACT_ID,
    PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_REPORT_CONTRACT_ID,
    build_px2_self_play_pointer_seeded_handoff_artifacts,
)
from starlab.sc2.px2.self_play.pointer_seeded_run import (
    POINTER_SEEDED_RUN_JSON,
    run_bounded_pointer_seeded_operator_local_run,
    verify_loaded_current_candidate_self_seal,
)
from starlab.sc2.px2.self_play.pointer_seeded_run_record import (
    POINTER_SEEDED_RUN_RULE_SEED_FROM_CURRENT_CANDIDATE_STUB,
    PX2_SELF_PLAY_POINTER_SEEDED_RUN_CONTRACT_ID,
    PX2_SELF_PLAY_POINTER_SEEDED_RUN_REPORT_CONTRACT_ID,
    SEED_SEMANTICS_DECLARED_FROM_LATEST_CURRENT_CANDIDATE_V1,
    build_px2_self_play_pointer_seeded_run_artifacts,
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
from starlab.sc2.px2.self_play.second_hop_continuation import (
    FIRST_HOP_CONTINUATION_SNAPSHOT_JSON,
    SECOND_HOP_CONTINUATION_JSON,
    SLICE12_REANCHOR_SNAPSHOT_JSON,
    run_bounded_second_hop_continuation_after_slice12,
    validate_post_slice12_state_for_second_hop,
)
from starlab.sc2.px2.self_play.second_hop_continuation_record import (
    PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_CONTRACT_ID,
    PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_REPORT_CONTRACT_ID,
    build_px2_self_play_second_hop_continuation_artifacts,
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
    "EXECUTION_KIND_SLICE7",
    "EXECUTION_KIND_SLICE8",
    "EXECUTION_KIND_SLICE9",
    "EXECUTION_KIND_SLICE10",
    "EXECUTION_KIND_SLICE11",
    "EXECUTION_KIND_SLICE12",
    "EXECUTION_KIND_SLICE13",
    "EXECUTION_KIND_SLICE13_REANCHOR",
    "EXECUTION_KIND_SLICE14",
    "EXECUTION_KIND_SLICE15",
    "EXECUTION_KIND_SLICE16",
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
    "PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_CONTRACT_ID",
    "PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_CURRENT_CANDIDATE_CONTRACT_ID",
    "PX2_SELF_PLAY_CURRENT_CANDIDATE_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_CONTINUATION_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_CONTINUATION_RUN_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_CONTRACT_ID",
    "PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_POINTER_SEEDED_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_POINTER_SEEDED_RUN_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_CONTRACT_ID",
    "PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_REPORT_CONTRACT_ID",
    "HANDOFF_ANCHORED_RUN_RULE_ANCHOR_ON_SLICE15_HANDOFF_STUB",
    "ANCHOR_SEMANTICS_DECLARED_FROM_SLICE15_HANDOFF_JSON_V1",
    "POINTER_SEEDED_HANDOFF_RULE_AFTER_SLICE14_STUB",
    "DECLARED_NEXT_STEP_FROM_SLICE14_POINTER_SEEDED_V1",
    "POINTER_SEEDED_HANDOFF_JSON",
    "HANDOFF_ANCHORED_RUN_JSON",
    "POINTER_SEEDED_RUN_JSON",
    "POINTER_SEEDED_RUN_RULE_SEED_FROM_CURRENT_CANDIDATE_STUB",
    "SEED_SEMANTICS_DECLARED_FROM_LATEST_CURRENT_CANDIDATE_V1",
    "CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB",
    "CONTINUATION_RULE_SECOND_HOP_CONSUME_CURRENT_CANDIDATE_STUB",
    "CONTINUATION_RUN_RECORD_VERSION_SLICE13",
    "CONTINUATION_RUN_JSON",
    "SLICE11_CAMPAIGN_PROFILE_ID",
    "SLICE13_SECOND_HOP_CAMPAIGN_PROFILE_ID",
    "CURRENT_CANDIDATE_REANCHOR_JSON",
    "SLICE12_CAMPAIGN_PROFILE_ID",
    "PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_CONTRACT_ID",
    "PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_REPORT_CONTRACT_ID",
    "REANCHOR_RULE_POST_CONTINUATION_STUB",
    "REANCHOR_RULE_POST_SECOND_HOP_STUB",
    "CURRENT_CANDIDATE_RECORD_VERSION_SLICE12",
    "CURRENT_CANDIDATE_RECORD_VERSION_SLICE13",
    "CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB",
    "CURRENT_CANDIDATE_RULE_REANCHOR_FROM_CONTINUATION_STUB",
    "CURRENT_CANDIDATE_RULE_REANCHOR_FROM_SECOND_HOP_STUB",
    "PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID",
    "PX2_SELF_PLAY_PROMOTION_RECEIPT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID",
    "PX2_SELF_PLAY_ROLLBACK_RECEIPT_REPORT_CONTRACT_ID",
    "PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID",
    "PX2_SELF_PLAY_SMOKE_RUN_REPORT_CONTRACT_ID",
    "PREFLIGHT_SEAL_VERSION",
    "PolicyRuntimeBridgeReceipt",
    "bootstrap_policy_runtime_step",
    "build_px2_self_play_operator_local_real_run_artifacts",
    "build_px2_self_play_operator_local_session_artifacts",
    "build_px2_self_play_operator_local_session_transition_artifacts",
    "build_px2_self_play_current_candidate_artifacts",
    "build_px2_self_play_continuation_run_artifacts",
    "build_px2_self_play_current_candidate_reanchor_artifacts",
    "build_px2_self_play_second_hop_continuation_artifacts",
    "build_px2_self_play_pointer_seeded_run_artifacts",
    "build_px2_self_play_pointer_seeded_handoff_artifacts",
    "build_px2_self_play_handoff_anchored_run_artifacts",
    "run_bounded_pointer_seeded_operator_local_run",
    "run_bounded_pointer_seeded_handoff",
    "run_bounded_handoff_anchored_operator_local_run",
    "verify_loaded_current_candidate_self_seal",
    "verify_loaded_pointer_seeded_run_self_seal",
    "verify_loaded_pointer_seeded_handoff_self_seal",
    "build_default_opponent_pool_stub",
    "build_px2_self_play_campaign_root_manifest_artifacts",
    "build_slice5_opponent_pool",
    "build_policy_operator_local",
    "build_slice4_continuity_manifest",
    "build_preflight_seal_basis",
    "build_px2_self_play_campaign_artifacts",
    "build_px2_self_play_smoke_run_artifacts",
    "default_operator_local_campaign_root_subdirs",
    "DEFAULT_SLICE7_CAMPAIGN_ID",
    "DEFAULT_SLICE8_CAMPAIGN_ID",
    "DEFAULT_SLICE9_CAMPAIGN_ID",
    "DEFAULT_SLICE10_CAMPAIGN_ID",
    "corpus_root_logical_posix",
    "default_operator_local_slice4_subdirs",
    "ensure_operator_local_campaign_root_layout",
    "ensure_operator_local_slice4_layout",
    "opponent_battle_ref_ids",
    "opponent_pool_identity_sha256",
    "output_dir_logical_posix",
    "resolve_canonical_campaign_root",
    "run_bounded_operator_local_real_run",
    "run_bounded_operator_local_session",
    "run_bounded_operator_local_session_with_transition",
    "run_bounded_operator_local_session_transition_with_current_candidate",
    "run_bounded_continuation_run_consuming_current_candidate",
    "validate_current_candidate_for_continuation_run",
    "FIRST_HOP_CONTINUATION_SNAPSHOT_JSON",
    "SECOND_HOP_CONTINUATION_JSON",
    "SLICE12_REANCHOR_SNAPSHOT_JSON",
    "run_bounded_second_hop_continuation_after_slice12",
    "validate_post_slice12_state_for_second_hop",
    "run_bounded_current_candidate_reanchor_after_continuation",
    "run_bounded_current_candidate_reanchor_after_second_hop",
    "load_px2_self_play_current_candidate",
    "next_run_preflight_hints_from_current_candidate",
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
