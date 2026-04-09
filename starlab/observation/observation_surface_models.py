"""Schema constants for observation surface frame + JSON Schema artifacts (M17)."""

from __future__ import annotations

OBSERVATION_SURFACE_CONTRACT = "starlab.observation_surface.v1"
OBSERVATION_SURFACE_PROFILE = "starlab.observation_surface.m17.v1"

OBSERVATION_FRAME_SCHEMA_VERSION = "starlab.observation_frame.v1"

OBSERVATION_SURFACE_JSON_SCHEMA_ID = "starlab.observation_frame.m17.v1.schema.json"

OBSERVATION_SURFACE_SCHEMA_FILENAME = "observation_surface_schema.json"
OBSERVATION_SURFACE_SCHEMA_REPORT_FILENAME = "observation_surface_schema_report.json"

OBSERVATION_SURFACE_REPORT_VERSION = "starlab.observation_surface_report.v1"

# M18 materialization outputs (single observation frame + report; distinct from schema report).
OBSERVATION_SURFACE_ARTIFACT_FILENAME = "observation_surface.json"
OBSERVATION_SURFACE_MATERIALIZATION_REPORT_FILENAME = "observation_surface_report.json"

PERCEPTUAL_BRIDGE_PROTOTYPE_CONTRACT = "starlab.perceptual_bridge_prototype.v1"
PERCEPTUAL_BRIDGE_PROTOTYPE_PROFILE = "starlab.perceptual_bridge_prototype.m18.v1"
OBSERVATION_MATERIALIZATION_REPORT_VERSION = "starlab.observation_surface_materialization_report.v1"
