"""CLI: emit campaign + fixture self-play smoke JSON bundle (PX2-M03 slice 1)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.px2.self_play.smoke_run import run_px2_fixture_self_play_smoke


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Emit px2_self_play_campaign_contract.json, report, smoke_run, smoke_report "
            "using a PX2-M02-style corpus root (bundle directories)."
        )
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory to write all four JSON artifacts.",
    )
    p.add_argument(
        "--corpus-root",
        type=Path,
        required=True,
        help="Corpus directory (same layout as tests/fixtures/px2_m02/corpus).",
    )
    p.add_argument("--campaign-id", default="px2_m03_smoke_fixture_campaign_001")
    p.add_argument("--campaign-profile-id", default="px2_m03_slice1_fixture_smoke_v1")
    p.add_argument("--torch-seed", type=int, default=42)
    args = p.parse_args(argv)

    out = args.output_dir.resolve()
    corpus = args.corpus_root.resolve()
    out.mkdir(parents=True, exist_ok=True)

    campaign, campaign_report, smoke_run, smoke_report = run_px2_fixture_self_play_smoke(
        corpus_root=corpus,
        campaign_id=args.campaign_id,
        campaign_profile_id=args.campaign_profile_id,
        torch_seed=args.torch_seed,
    )
    (out / "px2_self_play_campaign_contract.json").write_text(
        canonical_json_dumps(campaign),
        encoding="utf-8",
    )
    (out / "px2_self_play_campaign_contract_report.json").write_text(
        canonical_json_dumps(campaign_report),
        encoding="utf-8",
    )
    (out / "px2_self_play_smoke_run.json").write_text(
        canonical_json_dumps(smoke_run),
        encoding="utf-8",
    )
    (out / "px2_self_play_smoke_run_report.json").write_text(
        canonical_json_dumps(smoke_report),
        encoding="utf-8",
    )
    print(f"wrote campaign + smoke artifacts under {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
