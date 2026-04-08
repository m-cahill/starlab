"""Schema constants for canonical state frame + JSON Schema artifacts (M15)."""

from __future__ import annotations

# Governs the *contract* name (report + audit); distinct from per-document schema_version.
CANONICAL_STATE_CONTRACT = "starlab.canonical_state_schema.v1"
CANONICAL_STATE_PROFILE = "starlab.canonical_state_schema.m15.v1"

# Value of ``schema_version`` on each canonical state frame JSON document.
CANONICAL_STATE_FRAME_SCHEMA_VERSION = "starlab.canonical_state_frame.v1"

# JSON Schema document identity (emitted ``canonical_state_schema.json``).
CANONICAL_STATE_JSON_SCHEMA_ID = "starlab.canonical_state_frame.m15.v1.schema.json"

# Filenames for emitted artifacts (CLI / tests / governance).
CANONICAL_STATE_SCHEMA_FILENAME = "canonical_state_schema.json"
CANONICAL_STATE_SCHEMA_REPORT_FILENAME = "canonical_state_schema_report.json"

# M16 pipeline outputs (single state frame + report).
CANONICAL_STATE_ARTIFACT_FILENAME = "canonical_state.json"
CANONICAL_STATE_PIPELINE_REPORT_FILENAME = "canonical_state_report.json"
CANONICAL_STATE_PIPELINE_CONTRACT = "starlab.canonical_state_pipeline.v1"
CANONICAL_STATE_PIPELINE_PROFILE = "starlab.canonical_state_pipeline.m16.v1"
CANONICAL_STATE_PIPELINE_REPORT_VERSION = "starlab.canonical_state_report.v1"
