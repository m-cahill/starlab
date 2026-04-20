"""Conservative replay-derived labeling into PX2 Terran core v1 (PX2-M02)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab._io import load_json_object

# --- Conservative BOE entity_name → (action_id | skip) ---------------------------------

_SKIP = None


def _map_structure_started(entity_name: str) -> tuple[str, dict[str, Any]] | None:
    m: dict[str, tuple[str, dict[str, Any]]] = {
        "Barracks": ("build_barracks", {"build_slot": 0}),
        "Factory": ("build_factory", {"build_slot": 0}),
        "Starport": ("build_starport", {"build_slot": 0}),
        "SupplyDepot": ("build_supply_depot", {"build_slot": 0}),
        "EngineeringBay": ("build_engineering_bay", {"build_slot": 0}),
        "Refinery": ("build_refinery", {"expansion_slot": 0}),
    }
    if entity_name not in m:
        return _SKIP
    aid, args = m[entity_name]
    return (aid, dict(args))


def _map_unit_completed(entity_name: str) -> tuple[str, dict[str, Any]] | None:
    m: dict[str, tuple[str, dict[str, Any]]] = {
        "Marine": ("train_marine", {"producer_key": "barracks_0"}),
        "Marauder": ("train_marauder", {"producer_key": "barracks_0"}),
        "SiegeTank": ("train_siege_tank", {"producer_key": "factory_0"}),
        "Medivac": ("train_medivac", {"producer_key": "starport_0"}),
        "Viking": ("train_viking", {"producer_key": "starport_0"}),
    }
    if entity_name not in m:
        return _SKIP
    aid, args = m[entity_name]
    return (aid, dict(args))


@dataclass(frozen=True, slots=True)
class LabelingSkip:
    """Explicit skip with reason (high-precision path)."""

    reason: str
    detail: str


@dataclass(frozen=True, slots=True)
class LabeledExample:
    example_id: str
    source_replay_identity: str
    gameloop: int
    player_index: int
    action_id: str
    arguments: dict[str, Any]


def _terr_perspective_player(canonical_state: dict[str, Any]) -> int | None:
    players = canonical_state.get("players")
    if not isinstance(players, list):
        return None
    for p in players:
        if not isinstance(p, dict):
            continue
        if str(p.get("race_actual")) == "Terran":
            return int(p["player_index"])
    return None


def label_build_order_step(
    *,
    step: dict[str, Any],
    terran_player_index: int,
) -> LabeledExample | LabelingSkip:
    """Map one M11 BOE step for the Terran player only."""

    try:
        pidx = int(step["player_index"])
    except (KeyError, TypeError, ValueError):
        return LabelingSkip("bad_step", "missing_or_invalid_player_index")
    if pidx != terran_player_index:
        return LabelingSkip("other_player", "non_terran_perspective_player")

    entity_name = str(step.get("entity_name", ""))
    phase = str(step.get("phase", ""))
    try:
        gameloop = int(step["gameloop"])
    except (KeyError, TypeError, ValueError):
        return LabelingSkip("bad_step", "missing_gameloop")

    if phase == "started" and str(step.get("entity_kind")) == "structure":
        mapped = _map_structure_started(entity_name)
        if mapped is None:
            return LabelingSkip("unsupported_structure", entity_name)
        aid, args = mapped
    elif phase == "completed" and str(step.get("entity_kind")) == "unit":
        mapped = _map_unit_completed(entity_name)
        if mapped is None:
            if entity_name in {"SCV", "Reaper", "MULE"}:
                return LabelingSkip("unsupported_or_ambiguous_unit", entity_name)
            return LabelingSkip("unsupported_unit", entity_name)
        aid, args = mapped
    else:
        return LabelingSkip("unsupported_step_shape", f"{phase}:{step.get('entity_kind')}")

    src = step.get("source_timeline_index")
    eid = f"gl{gameloop}_tl{src}"
    return LabeledExample(
        example_id=eid,
        source_replay_identity="",
        gameloop=gameloop,
        player_index=pidx,
        action_id=aid,
        arguments=args,
    )


def label_examples_from_bundle_directory(
    bundle_dir: Path,
) -> tuple[list[LabeledExample], list[tuple[str, str]]]:
    """Load governed JSON from a bundle directory and emit labeled examples + skips.

    Expected files: ``replay_bundle_manifest.json``, ``replay_build_order_economy.json``,
    ``canonical_state.json``, and ``observation_surface.json`` for M18 features.
    """

    manifest_p = bundle_dir / "replay_bundle_manifest.json"
    boe_p = bundle_dir / "replay_build_order_economy.json"
    cs_p = bundle_dir / "canonical_state.json"

    manifest, e1 = load_json_object(manifest_p)
    boe, e2 = load_json_object(boe_p)
    canonical, e3 = load_json_object(cs_p)
    for err, label in (
        (e1, manifest_p),
        (e2, boe_p),
        (e3, cs_p),
    ):
        if err:
            msg = f"failed to load {label}: {err}"
            raise ValueError(msg)

    assert manifest is not None and boe is not None and canonical is not None

    replay_id = str(manifest.get("source_replay_identity", ""))
    terran_pi = _terr_perspective_player(canonical)
    if terran_pi is None:
        msg = "no Terran player in canonical_state — cannot label for PX2 Terran core v1"
        raise ValueError(msg)

    steps = boe.get("build_order_steps")
    if not isinstance(steps, list):
        msg = "replay_build_order_economy.json missing build_order_steps"
        raise ValueError(msg)

    out: list[LabeledExample] = []
    skips: list[tuple[str, str]] = []
    for step in steps:
        if not isinstance(step, dict):
            skips.append(("bad_step", "non_object_step"))
            continue
        res = label_build_order_step(step=step, terran_player_index=terran_pi)
        if isinstance(res, LabelingSkip):
            skips.append((res.reason, res.detail))
            continue
        out.append(
            LabeledExample(
                example_id=res.example_id,
                source_replay_identity=replay_id,
                gameloop=res.gameloop,
                player_index=res.player_index,
                action_id=res.action_id,
                arguments=res.arguments,
            ),
        )
    return out, skips


def load_observation_surface(bundle_dir: Path) -> dict[str, Any]:
    p = bundle_dir / "observation_surface.json"
    raw, err = load_json_object(p)
    if err or raw is None:
        msg = f"failed to load observation_surface.json: {err}"
        raise ValueError(msg)
    if not isinstance(raw, dict):
        msg = "observation_surface.json must be a JSON object"
        raise ValueError(msg)
    return raw


def patch_observation_gameloop(obs: dict[str, Any], gameloop: int) -> dict[str, Any]:
    """Return a shallow-ish copy with metadata.gameloop updated (deterministic fixture aid)."""

    o = json.loads(json.dumps(obs))
    meta = o.get("metadata")
    if isinstance(meta, dict):
        meta["gameloop"] = gameloop
    if not isinstance(o, dict):
        msg = "internal error: observation clone must be dict"
        raise TypeError(msg)
    return o
