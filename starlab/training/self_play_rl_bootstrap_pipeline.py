"""M45: bootstrap rollouts via M44 + optional weighted sklearn re-fit."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from starlab.hierarchy.delegate_policy import DELEGATE_IDS, delegate_id_for_coarse_label
from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.hierarchy.hierarchical_training_models import (
    HIERARCHICAL_TRAINING_RUN_FILENAME,
    SKLEARN_BUNDLE_SCHEMA,
    WEIGHTS_ARTIFACT_BASENAME,
    WEIGHTS_SUBDIR,
)
from starlab.hierarchy.hierarchical_training_pipeline import TRAINER_CONFIG_V1
from starlab.hierarchy.m43_sklearn_runtime import (
    assert_workers_cover_delegates,
    load_hierarchical_sklearn_bundle,
)
from starlab.imitation.baseline_fit import collect_imitation_example_rows
from starlab.imitation.replay_imitation_training_pipeline import (
    parse_context_signature_to_feature_dict,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.local_live_play_validation_harness import run_local_live_play_validation
from starlab.sc2.local_live_play_validation_models import (
    LOCAL_LIVE_PLAY_VALIDATION_RUN_FILENAME,
    RuntimeMode,
)
from starlab.sc2.match_config import match_config_from_mapping, match_config_to_mapping
from starlab.training.self_play_rl_bootstrap_io import (
    minimal_report_from_run,
    seal_bootstrap_run_body,
    write_bootstrap_artifacts,
    write_bootstrap_dataset,
    write_episode_manifest,
)
from starlab.training.self_play_rl_bootstrap_models import (
    EPISODE_MANIFEST_VERSION,
    EPISODE_SEED_POLICY,
    NON_CLAIMS_V1,
    REWARD_POLICY_ID,
    SELF_PLAY_RL_BOOTSTRAP_RUN_VERSION,
    UPDATE_POLICY_ID,
    UPDATED_BUNDLE_BASENAME,
    UPDATED_POLICY_SUBDIR,
    BootstrapMode,
)


def _majority_label(counts: Counter[str]) -> str:
    if not counts:
        msg = "empty label counts for majority"
        raise ValueError(msg)
    best_n = max(counts.values())
    candidates = sorted([lab for lab, c in counts.items() if c == best_n])
    return candidates[0]


def resolve_bootstrap_mode(*, runtime_mode: RuntimeMode, mirror_self_play: bool) -> BootstrapMode:
    if mirror_self_play:
        return "mirror_self_play_local"
    if runtime_mode == "fixture_stub_ci":
        return "single_candidate_fixture_stub"
    return "single_candidate_local_live"


def compute_episode_reward_validation_outcome_v1(validation_run: dict[str, Any]) -> dict[str, Any]:
    """Deterministic heuristic reward from M44 validation (primary + small step shaping)."""

    me = validation_run.get("match_execution")
    if not isinstance(me, dict):
        me = {}
    final_status = str(me.get("final_status", ""))
    steps = validation_run.get("action_adapter_steps")
    n = len(steps) if isinstance(steps, list) else 0

    reward_primary = 1.0 if final_status == "ok" else 0.0
    shaping = min(0.05, 0.005 * float(n))
    reward_total = min(1.05, reward_primary + shaping)
    return {
        "final_status": final_status,
        "reward_policy_id": REWARD_POLICY_ID,
        "reward_primary": reward_primary,
        "reward_shaping_steps": shaping,
        "reward_total": reward_total,
        "step_count": n,
    }


def _weighted_refit_bundle(
    *,
    bundle: dict[str, Any],
    rows: list[tuple[str, str, str, str]],
    train_idx: list[int],
    bootstrap_xd: list[dict[str, str]],
    bootstrap_delegate: list[str],
    bootstrap_coarse: list[str],
    bootstrap_w: list[float],
    seed: int,
) -> dict[str, Any]:
    """Conservative weighted re-fit: original train rows (weight 1) + bootstrap pseudo-labels."""

    n_b = len(bootstrap_xd)
    if n_b != len(bootstrap_delegate) or n_b != len(bootstrap_coarse) or n_b != len(bootstrap_w):
        msg = "internal: bootstrap parallel lists length mismatch"
        raise ValueError(msg)

    vectorizer = bundle["dict_vectorizer"]
    x_dicts_train = [parse_context_signature_to_feature_dict(rows[i][3]) for i in train_idx]
    y_coarse_train = [rows[i][2] for i in train_idx]
    y_delegate_train = [delegate_id_for_coarse_label(lab) for lab in y_coarse_train]

    x_train_m = vectorizer.transform(x_dicts_train)
    x_boot_m = vectorizer.transform(bootstrap_xd)
    x_mgr = np.vstack([x_train_m, x_boot_m])

    w_train = np.ones(len(train_idx), dtype=float)
    w_boot = np.array(bootstrap_w, dtype=float)
    w_mgr = np.concatenate([w_train, w_boot])

    y_del_combined = list(y_delegate_train) + list(bootstrap_delegate)

    uniq_del = set(y_del_combined)
    manager_clf: LogisticRegression | None = None
    manager_label_encoder: LabelEncoder | None = None
    manager_constant_delegate: str | None = None

    if len(uniq_del) >= 2:
        manager_label_encoder = LabelEncoder()
        y_m_enc = manager_label_encoder.fit_transform(y_del_combined)
        manager_clf = LogisticRegression(
            max_iter=int(TRAINER_CONFIG_V1["max_iter"]),
            random_state=seed,
            solver=str(TRAINER_CONFIG_V1["solver"]),
        )
        manager_clf.fit(x_mgr, y_m_enc, sample_weight=w_mgr)
    else:
        manager_constant_delegate = _majority_label(Counter(y_del_combined))

    train_coarse_all = [rows[i][2] for i in train_idx]
    global_majority_label = _majority_label(Counter(train_coarse_all))

    worker_entries: dict[str, Any] = {}
    for did in DELEGATE_IDS:
        counts_by_split: dict[str, int] = {}
        for sp in ("train", "validation", "test"):
            counts_by_split[sp] = sum(
                1
                for j, r in enumerate(rows)
                if r[1] == sp and delegate_id_for_coarse_label(r[2]) == did
            )

        x_parts: list[Any] = []
        y_coarse_parts: list[str] = []
        w_parts: list[float] = []

        for j in range(len(train_idx)):
            if y_delegate_train[j] != did:
                continue
            xd = x_dicts_train[j]
            x_parts.append(vectorizer.transform([xd]))
            y_coarse_parts.append(y_coarse_train[j])
            w_parts.append(1.0)

        for k in range(n_b):
            if bootstrap_delegate[k] != did:
                continue
            x_parts.append(vectorizer.transform([bootstrap_xd[k]]))
            y_coarse_parts.append(bootstrap_coarse[k])
            w_parts.append(bootstrap_w[k])

        if not x_parts:
            worker_entries[did] = {
                "classifier": None,
                "label_encoder": None,
                "fallback_label": global_majority_label,
                "coverage": {
                    "counts_by_split": counts_by_split,
                    "trained_worker": False,
                    "fallback_active": True,
                    "fallback_reason": "zero_rows_after_bootstrap",
                },
            }
            continue

        x_sub = np.vstack(x_parts)
        w_sub = np.array(w_parts, dtype=float)

        uniq_labs = set(y_coarse_parts)
        if len(uniq_labs) < 2:
            const_lab = _majority_label(Counter(y_coarse_parts))
            worker_entries[did] = {
                "classifier": None,
                "label_encoder": None,
                "fallback_label": const_lab,
                "coverage": {
                    "counts_by_split": counts_by_split,
                    "trained_worker": False,
                    "fallback_active": True,
                    "fallback_reason": "single_class_train",
                },
            }
            continue

        w_enc = LabelEncoder()
        y_w = w_enc.fit_transform(y_coarse_parts)
        w_clf = LogisticRegression(
            max_iter=int(TRAINER_CONFIG_V1["max_iter"]),
            random_state=seed,
            solver=str(TRAINER_CONFIG_V1["solver"]),
        )
        w_clf.fit(x_sub, y_w, sample_weight=w_sub)
        worker_entries[did] = {
            "classifier": w_clf,
            "label_encoder": w_enc,
            "fallback_label": None,
            "coverage": {
                "counts_by_split": counts_by_split,
                "trained_worker": True,
                "fallback_active": False,
                "fallback_reason": None,
            },
        }

    sklearn_bundle: dict[str, Any] = {
        "delegate_policy_id": bundle["delegate_policy_id"],
        "dict_vectorizer": vectorizer,
        "encoding_policy_id": bundle["encoding_policy_id"],
        "feature_policy_id": bundle["feature_policy_id"],
        "global_majority_label": global_majority_label,
        "manager": {
            "classifier": manager_clf,
            "constant_delegate_id": manager_constant_delegate,
            "label_encoder": manager_label_encoder,
        },
        "schema_version": SKLEARN_BUNDLE_SCHEMA,
        "workers": {
            did: {
                "classifier": worker_entries[did]["classifier"],
                "fallback_label": worker_entries[did]["fallback_label"],
                "label_encoder": worker_entries[did]["label_encoder"],
            }
            for did in DELEGATE_IDS
        },
    }
    assert_workers_cover_delegates(sklearn_bundle)
    return sklearn_bundle


def run_self_play_rl_bootstrap(
    *,
    hierarchical_training_run_dir: Path,
    match_config_path: Path,
    output_dir: Path,
    runtime_mode: RuntimeMode,
    episodes: int,
    seed: int,
    dataset_path: Path | None,
    bundle_dirs: list[Path] | None,
    weights_path: Path | None = None,
    emit_updated_bundle: bool = False,
    mirror_self_play: bool = False,
) -> dict[str, Any]:
    """Run M44 rollouts; record bootstrap data; optional weighted re-fit + local joblib."""

    if mirror_self_play:
        msg = "mirror_self_play_local is not implemented in M45 v1"
        raise NotImplementedError(msg)

    if episodes < 1:
        msg = "episodes must be >= 1"
        raise ValueError(msg)

    hr_path = hierarchical_training_run_dir / HIERARCHICAL_TRAINING_RUN_FILENAME
    training_run = json.loads(hr_path.read_text(encoding="utf-8"))
    if not isinstance(training_run, dict):
        msg = "hierarchical training run root must be an object"
        raise ValueError(msg)
    tr_ver = training_run.get("training_run_version")
    if tr_ver != "starlab.hierarchical_training_run.v1":
        msg = f"unsupported hierarchical training_run_version: {tr_ver!r}"
        raise ValueError(msg)

    training_run_sha256 = training_run.get("training_run_sha256")
    if not isinstance(training_run_sha256, str):
        msg = "hierarchical_training_run.json missing training_run_sha256"
        raise ValueError(msg)
    stripped = {k: v for k, v in training_run.items() if k != "training_run_sha256"}
    if sha256_hex_of_canonical_json(stripped) != training_run_sha256:
        msg = "hierarchical_training_run.json training_run_sha256 does not match content"
        raise ValueError(msg)

    wpath = weights_path
    if wpath is None:
        wpath = hierarchical_training_run_dir / WEIGHTS_SUBDIR / WEIGHTS_ARTIFACT_BASENAME
    if not wpath.is_file():
        msg = f"M43 joblib weights not found at {wpath}"
        raise ValueError(msg)

    bundle = load_hierarchical_sklearn_bundle(wpath)
    assert_workers_cover_delegates(bundle)

    bootstrap_mode = resolve_bootstrap_mode(
        runtime_mode=runtime_mode, mirror_self_play=mirror_self_play
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    episodes_dir = output_dir / "episodes"
    episodes_dir.mkdir(parents=True, exist_ok=True)

    base_match_raw = json.loads(match_config_path.read_text(encoding="utf-8"))
    if not isinstance(base_match_raw, dict):
        msg = "match config root must be a JSON object"
        raise ValueError(msg)

    episode_rows: list[dict[str, Any]] = []
    bootstrap_xd: list[dict[str, str]] = []
    bootstrap_delegate: list[str] = []
    bootstrap_coarse: list[str] = []
    bootstrap_w: list[float] = []

    for ep in range(episodes):
        ep_dir = episodes_dir / f"e{ep:03d}"
        ep_dir.mkdir(parents=True, exist_ok=True)
        episode_seed = int(seed) + int(ep)
        ep_cfg_dict = dict(base_match_raw)
        ep_cfg_dict["seed"] = episode_seed
        ep_cfg = match_config_from_mapping(ep_cfg_dict)
        ep_match_path = ep_dir / "bootstrap_match_config.json"
        ep_match_path.write_text(
            canonical_json_dumps(match_config_to_mapping(ep_cfg)),
            encoding="utf-8",
        )
        res = run_local_live_play_validation(
            hierarchical_training_run_dir=hierarchical_training_run_dir,
            match_config_path=ep_match_path,
            output_dir=ep_dir,
            runtime_mode=runtime_mode,
            weights_path=wpath,
        )
        vr = res.validation_run
        vpath = ep_dir / LOCAL_LIVE_PLAY_VALIDATION_RUN_FILENAME
        reward_ep = compute_episode_reward_validation_outcome_v1(vr)
        steps = vr.get("action_adapter_steps")
        step_list = steps if isinstance(steps, list) else []
        n_steps = max(1, len(step_list))
        per_step_w = float(reward_ep["reward_total"]) / float(n_steps)

        for st in step_list:
            if not isinstance(st, dict):
                continue
            sig = st.get("context_signature")
            pd = st.get("predicted_delegate_id")
            pc = st.get("predicted_coarse_label")
            if not isinstance(sig, str) or not isinstance(pd, str) or not isinstance(pc, str):
                continue
            bootstrap_xd.append(parse_context_signature_to_feature_dict(sig))
            bootstrap_delegate.append(pd)
            bootstrap_coarse.append(pc)
            bootstrap_w.append(per_step_w)

        episode_rows.append(
            {
                "episode_index": ep,
                "episode_seed": episode_seed,
                "relative_dir": f"episodes/e{ep:03d}",
                "run_id": vr.get("run_id"),
                "validation_run_sha256": vr.get("validation_run_sha256"),
                "local_live_play_validation_run_path": str(vpath.resolve()),
                "reward": reward_ep,
            },
        )

    reward_totals = [float(er["reward"]["reward_total"]) for er in episode_rows]
    mean_r = sum(reward_totals) / float(len(reward_totals)) if reward_totals else 0.0

    sha256_values = []
    for er in episode_rows:
        h = er.get("validation_run_sha256")
        if isinstance(h, str) and len(h) == 64:
            sha256_values.append(str(h))
    distinct_validation_run_sha256 = len(set(sha256_values))
    run_id_values = [str(er["run_id"]) for er in episode_rows if isinstance(er.get("run_id"), str)]
    distinct_run_id = len(set(run_id_values))

    updated_sidecar: dict[str, Any] | None = None
    warnings: list[str] = []

    if episodes > 1 and distinct_validation_run_sha256 < episodes:
        warnings.append(
            "m47_episode_validation_run_sha256_collapsed: "
            f"configured_episodes={episodes} "
            f"distinct_validation_run_sha256={distinct_validation_run_sha256}"
        )
    if episodes > 1 and distinct_run_id < episodes and len(run_id_values) == episodes:
        warnings.append(
            "m47_episode_run_id_collapsed: "
            f"configured_episodes={episodes} distinct_run_id={distinct_run_id}"
        )

    manifest = {
        "bootstrap_base_seed": seed,
        "distinct_episode_identities": {
            "distinct_run_id_count": distinct_run_id,
            "distinct_validation_run_sha256_count": distinct_validation_run_sha256,
        },
        "episode_manifest_version": EPISODE_MANIFEST_VERSION,
        "episode_seed_policy": EPISODE_SEED_POLICY,
        "episodes": episode_rows,
        "runtime_mode": runtime_mode,
        "bootstrap_mode": bootstrap_mode,
    }
    write_episode_manifest(body=manifest, episodes_dir=episodes_dir)

    if emit_updated_bundle:
        if dataset_path is None or not bundle_dirs:
            msg = "--emit-updated-bundle requires --dataset and at least one --bundle-dir"
            raise ValueError(msg)
        raw_ds = json.loads(dataset_path.read_text(encoding="utf-8"))
        if not isinstance(raw_ds, dict):
            msg = "dataset JSON root must be an object"
            raise ValueError(msg)
        dsha = raw_ds.get("dataset_sha256")
        src = training_run.get("source_dataset")
        if isinstance(src, dict):
            expected = src.get("dataset_sha256")
            if isinstance(expected, str) and len(expected) == 64 and isinstance(dsha, str):
                if dsha != expected:
                    msg = (
                        "--dataset dataset_sha256 does not match "
                        "hierarchical_training_run source_dataset"
                    )
                    raise ValueError(msg)

        rows, _row_warnings = collect_imitation_example_rows(
            dataset=raw_ds, bundle_dirs=bundle_dirs
        )
        train_idx = [i for i, r in enumerate(rows) if r[1] == "train"]
        if not train_idx:
            msg = "no training examples (split=train) for weighted re-fit"
            raise ValueError(msg)
        if not bootstrap_xd:
            msg = "no bootstrap rows collected from M44 episodes; cannot re-fit"
            raise ValueError(msg)

        new_bundle = _weighted_refit_bundle(
            bootstrap_coarse=bootstrap_coarse,
            bootstrap_delegate=bootstrap_delegate,
            bootstrap_w=bootstrap_w,
            bootstrap_xd=bootstrap_xd,
            bundle=bundle,
            rows=rows,
            seed=seed,
            train_idx=train_idx,
        )
        upd_dir = output_dir / UPDATED_POLICY_SUBDIR
        upd_dir.mkdir(parents=True, exist_ok=True)
        out_joblib = upd_dir / UPDATED_BUNDLE_BASENAME
        joblib.dump(new_bundle, out_joblib)
        updated_sidecar = {
            "artifact_sha256": sha256_hex_file(out_joblib),
            "byte_size": int(out_joblib.stat().st_size),
            "format": "joblib",
            "relative_path": f"{UPDATED_POLICY_SUBDIR}/{UPDATED_BUNDLE_BASENAME}",
            "schema": SKLEARN_BUNDLE_SCHEMA,
            "update_policy_id": UPDATE_POLICY_ID,
        }
    else:
        if not bootstrap_xd:
            warnings.append("no_action_adapter_steps_collected_check_m44_outputs")

    contract_sha = training_run["training_program_contract_sha256"]
    contract_ver = training_run["training_program_contract_version"]

    identity_payload = {
        "bootstrap_mode": bootstrap_mode,
        "candidate": {
            "hierarchical_training_run_sha256": training_run_sha256,
            "training_run_id": training_run["run_id"],
        },
        "episode_count_configured": episodes,
        "episode_seed_policy": EPISODE_SEED_POLICY,
        "m44_runtime_mode": runtime_mode,
        "reward_policy_id": REWARD_POLICY_ID,
        "seed": seed,
        "training_program_contract_sha256": contract_sha,
        "update_policy_id": UPDATE_POLICY_ID,
    }
    derived_run_id = sha256_hex_of_canonical_json(identity_payload)

    dataset_summary: dict[str, Any] = {
        "bootstrap_row_count": len(bootstrap_xd),
        "episode_count": episodes,
        "reward_policy_id": REWARD_POLICY_ID,
        "update_policy_id": UPDATE_POLICY_ID,
    }

    caveats = [
        "ci_validates_fixture_stub_bootstrap_only",
        "m45_bootstrap_not_benchmark_integrity",
        "updated_policy_local_sidecar_only_not_in_repo",
    ]

    body_pre: dict[str, Any] = {
        "bootstrap_dataset_summary": dataset_summary,
        "bootstrap_mode": bootstrap_mode,
        "candidate": {
            "hierarchical_training_run_path": str(hr_path.resolve()),
            "hierarchical_training_run_sha256": training_run_sha256,
            "interface_trace_schema_version": training_run["interface_trace_schema_version"],
            "delegate_policy_id": training_run["delegate_policy_id"],
            "joblib_weights_path": str(wpath.resolve()),
            "joblib_weights_sha256": sha256_hex_file(wpath),
            "training_program_contract_sha256": contract_sha,
            "training_program_contract_version": contract_ver,
            "training_run_id": training_run["run_id"],
        },
        "caveats": caveats,
        "episode_count_configured": episodes,
        "episode_distinctness": {
            "bootstrap_base_seed": seed,
            "configured_episode_count": episodes,
            "distinct_run_id_count": distinct_run_id,
            "distinct_validation_run_sha256_count": distinct_validation_run_sha256,
            "episode_manifest_version": EPISODE_MANIFEST_VERSION,
            "episode_seed_policy": EPISODE_SEED_POLICY,
        },
        "m44_substrate": {
            "local_live_play_validation_contract": "starlab.local_live_play_validation_run.v1",
            "semantic_live_action_adapter_policy_id": "starlab.m44.semantic_live_action_adapter.v1",
        },
        "non_claims": sorted(NON_CLAIMS_V1),
        "reward_policy_id": REWARD_POLICY_ID,
        "reward_summary": {
            "episode_rewards_total": reward_totals,
            "mean_episode_reward_total": mean_r,
        },
        "run_id": derived_run_id,
        "runtime_mode": runtime_mode,
        "self_play_rl_bootstrap_run_version": SELF_PLAY_RL_BOOTSTRAP_RUN_VERSION,
        "sklearn_version": sklearn.__version__,
        "update_policy_id": UPDATE_POLICY_ID,
        "updated_policy_bundle": updated_sidecar,
        "warnings": warnings,
    }

    run = seal_bootstrap_run_body(body_pre)
    report = minimal_report_from_run(run)
    write_bootstrap_artifacts(output_dir=output_dir, report_body=report, run_body=run)

    ds_body = {
        "bootstrap_dataset_version": "starlab.m45.bootstrap_dataset.v1",
        "episodes_dir": "episodes",
        "manifest": manifest,
        "reward_policy_id": REWARD_POLICY_ID,
        "rows_ingested_for_refit": len(bootstrap_xd),
    }
    write_bootstrap_dataset(body=ds_body, output_dir=output_dir)

    return run
