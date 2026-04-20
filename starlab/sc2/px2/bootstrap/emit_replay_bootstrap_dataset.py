"""Emit ``px2_replay_bootstrap_dataset*.json`` from governed bundle directories (PX2-M02)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from starlab.sc2.px2.bootstrap.dataset_contract import (
    DatasetExampleRecord,
    build_dataset_artifacts,
    split_assignment_for_replay,
    write_dataset_outputs,
)
from starlab.sc2.px2.bootstrap.feature_adapter import (
    observation_dict_to_feature_tensor,
    observation_feature_dim,
    pad_or_trunc,
)
from starlab.sc2.px2.bootstrap.game_state_presets import preset_snapshot_for_supervised_action
from starlab.sc2.px2.bootstrap.replay_labeler import (
    label_examples_from_bundle_directory,
    load_observation_surface,
    patch_observation_gameloop,
)


def emit_from_corpus(
    corpus_root: Path,
    output_dir: Path,
    *,
    split_salt: str = "px2_m02_replay_split_v1",
) -> tuple[Path, Path]:
    """Walk one level of child bundle directories and emit dataset + report."""

    examples: list[DatasetExampleRecord] = []
    bundle_ids: list[str] = []

    for bundle_dir in sorted(corpus_root.iterdir()):
        if not bundle_dir.is_dir():
            continue
        manifest_path = bundle_dir / "replay_bundle_manifest.json"
        if not manifest_path.is_file():
            continue
        labeled, _skips = label_examples_from_bundle_directory(bundle_dir)
        obs = load_observation_surface(bundle_dir)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bundle_ids.append(str(manifest.get("bundle_id", bundle_dir.name)))

        for lab in labeled:
            po = patch_observation_gameloop(obs, lab.gameloop)
            feat_t = pad_or_trunc(observation_dict_to_feature_tensor(po), observation_feature_dim())
            gs = preset_snapshot_for_supervised_action(lab.action_id)
            split = split_assignment_for_replay(
                source_replay_identity=lab.source_replay_identity,
                split_salt=split_salt,
            )
            examples.append(
                DatasetExampleRecord(
                    example_id=f"{lab.source_replay_identity[:8]}_{lab.example_id}",
                    source_replay_identity=lab.source_replay_identity,
                    gameloop=lab.gameloop,
                    label_action_id=lab.action_id,
                    label_arguments=dict(lab.arguments),
                    game_state_snapshot=gs,
                    feature_vector=[float(x) for x in feat_t.tolist()],
                    split=split,
                    observation_surface=po,
                ),
            )

    ds, rp = build_dataset_artifacts(
        examples=examples,
        upstream_bundle_ids=bundle_ids,
        split_salt=split_salt,
    )
    # attach skip stats from labeler passes — omitted for brevity in M02 minimal emitter
    return write_dataset_outputs(output_dir, dataset=ds, report=rp)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Emit PX2 replay-bootstrap dataset JSON artifacts.")
    p.add_argument("--corpus-root", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--split-salt", default="px2_m02_replay_split_v1")
    args = p.parse_args(argv)
    dp, rp = emit_from_corpus(args.corpus_root, args.output_dir, split_salt=args.split_salt)
    print(f"wrote {dp}")
    print(f"wrote {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
