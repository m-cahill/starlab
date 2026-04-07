"""Deterministic runtime smoke matrix artifact (M06)."""

from __future__ import annotations

SMOKE_MATRIX_SCHEMA_VERSION = "starlab.runtime_smoke_matrix.v1"

LATER_MILESTONES: tuple[str, ...] = (
    "M07 replay intake policy & provenance enforcement",
    "M08 replay parser substrate",
)

CI_PROFILE = "ci_fixture"
LOCAL_PROFILE = "local_optional"


def build_runtime_smoke_matrix(*, runtime_boundary_label: str) -> dict[str, object]:
    """Return deterministic ``runtime_smoke_matrix.json`` body."""

    return {
        "later_milestones": list(LATER_MILESTONES),
        "profiles": {
            CI_PROFILE: {
                "required_checks": [
                    "probe_schema_valid",
                    "runtime_boundary_label_present",
                ],
            },
            LOCAL_PROFILE: {
                "required_checks": [
                    "probe_schema_valid",
                    "runtime_boundary_label_present",
                ],
                "warning_checks": [
                    "adapter_name_present",
                    "base_build_captured",
                    "data_version_captured",
                ],
            },
        },
        "runtime_boundary_label": runtime_boundary_label,
        "schema_version": SMOKE_MATRIX_SCHEMA_VERSION,
    }
