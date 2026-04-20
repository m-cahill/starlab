"""CLI: emit ``px2_self_play_campaign_contract*.json`` (PX2-M03 slice 1)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.px2.self_play.campaign_contract import build_px2_self_play_campaign_artifacts
from starlab.sc2.px2.self_play.snapshot_pool import build_default_opponent_pool_stub


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Emit PX2 self-play campaign contract + report JSON.")
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory to write px2_self_play_campaign_contract.json and report.",
    )
    p.add_argument("--campaign-id", default="px2_m03_default_campaign_001")
    p.add_argument("--campaign-profile-id", default="px2_m03_slice1_default_v1")
    p.add_argument("--torch-seed", type=int, default=42)
    args = p.parse_args(argv)

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pool = build_default_opponent_pool_stub()
    contract, report = build_px2_self_play_campaign_artifacts(
        campaign_id=args.campaign_id,
        campaign_profile_id=args.campaign_profile_id,
        opponent_pool=pool,
        torch_seed=args.torch_seed,
    )
    (out / "px2_self_play_campaign_contract.json").write_text(
        canonical_json_dumps(contract),
        encoding="utf-8",
    )
    (out / "px2_self_play_campaign_contract_report.json").write_text(
        canonical_json_dumps(report),
        encoding="utf-8",
    )
    print(f"wrote {out / 'px2_self_play_campaign_contract.json'}")
    print(f"wrote {out / 'px2_self_play_campaign_contract_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
