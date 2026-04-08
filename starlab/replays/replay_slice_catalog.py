"""Slice family catalog and tag vocabulary (M13).

Classification is explicit and auditable; extraction logic lives in replay_slice_generation.py.
"""

from __future__ import annotations

from starlab.replays.replay_slice_models import SLICE_KIND_COMBAT, SLICE_KIND_SCOUTING

CATALOG_NAME = "starlab.replay_slice_catalog.m13.v1"

SLICE_FAMILIES_V1: tuple[str, ...] = (SLICE_KIND_COMBAT, SLICE_KIND_SCOUTING)

# Low-cardinality tag strings; overlap-derived tags are added only in the artifact record,
# not in slice_id identity (see contract doc).
TAG_COMBAT = "combat"
TAG_SCOUTING = "scouting"
TAG_PROXY_VISIBILITY_OVERLAP = "proxy_visibility_overlap"
TAG_EXPLICIT_VISIBILITY_OVERLAP = "explicit_visibility_overlap"
