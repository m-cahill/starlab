"""Assemble the M39 public flagship proof pack from governed fixtures (in-process)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Final

from starlab.evaluation.emit_baseline_evidence_pack import write_baseline_evidence_pack_artifacts
from starlab.evaluation.evidence_pack_models import (
    BASELINE_EVIDENCE_PACK_FILENAME,
    BASELINE_EVIDENCE_PACK_REPORT_FILENAME,
)
from starlab.evaluation.learned_agent_evaluation import write_learned_agent_evaluation_artifacts
from starlab.evaluation.learned_agent_models import (
    LEARNED_AGENT_EVALUATION_FILENAME,
    LEARNED_AGENT_EVALUATION_REPORT_FILENAME,
)
from starlab.explorer.replay_explorer_builder import build_replay_explorer_artifacts
from starlab.explorer.replay_explorer_io import (
    write_replay_explorer_report,
    write_replay_explorer_surface,
)
from starlab.explorer.replay_explorer_models import (
    DEFAULT_MAX_PANELS,
)
from starlab.explorer.replay_explorer_models import (
    REPORT_VERSION as M31_REPORT_VERSION,
)
from starlab.explorer.replay_explorer_models import (
    SURFACE_VERSION as M31_SURFACE_VERSION,
)
from starlab.flagship.models import (
    HASHES_FILENAME,
    PROOF_PACK_FILENAME,
    PROOF_PACK_REPORT_FILENAME,
    PROOF_PACK_REPORT_VERSION,
    PROOF_PACK_VERSION,
    PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

_BASELINE_DIR: Final[str] = "baseline"
_LEARNED_DIR: Final[str] = "learned"
_EXPLORER_DIR: Final[str] = "explorer"


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel_posix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def default_source_paths(repo_root: Path) -> dict[str, Path]:
    """Fixture-relative paths used to regenerate M25 / M28 / M31 surfaces for the proof pack."""

    return {
        "m25_scripted_suite": repo_root
        / "tests/fixtures/m21/expected_scripted_baseline_suite.json",
        "m25_heuristic_suite": repo_root
        / "tests/fixtures/m22/expected_heuristic_baseline_suite.json",
        "m25_tournament": repo_root / "tests/fixtures/m23/expected_evaluation_tournament.json",
        "m25_diagnostics": repo_root / "tests/fixtures/m24/expected_evaluation_diagnostics.json",
        "m28_benchmark_contract": repo_root / "tests/fixtures/m28/benchmark_contract_m28.json",
        "m28_baseline": repo_root / "tests/fixtures/m27/replay_imitation_baseline.json",
        "m28_dataset": repo_root / "tests/fixtures/m26/replay_training_dataset.json",
        "m28_bundle_dir": repo_root / "tests/fixtures/m16/bundle",
        "m31_bundle_dir": repo_root / "tests/fixtures/m31/bundle",
        "m31_agent": repo_root / "tests/fixtures/m30/replay_hierarchical_imitation_agent.json",
    }


def build_source_provenance(repo_root: Path, paths: dict[str, Path]) -> dict[str, Any]:
    """Structured provenance: repo-relative paths and SHA-256 of key governed inputs."""

    def entry(p: Path) -> dict[str, Any]:
        rel = _rel_posix(repo_root, p)
        return {"path": rel, "sha256": _file_sha256(p) if p.is_file() else None}

    m28_bundle = paths["m28_bundle_dir"]
    m31_bundle = paths["m31_bundle_dir"]
    prov: dict[str, Any] = {
        "m25_scripted_suite": entry(paths["m25_scripted_suite"]),
        "m25_heuristic_suite": entry(paths["m25_heuristic_suite"]),
        "m25_tournament": entry(paths["m25_tournament"]),
        "m25_diagnostics": entry(paths["m25_diagnostics"]),
        "m28_benchmark_contract": entry(paths["m28_benchmark_contract"]),
        "m28_replay_imitation_baseline": entry(paths["m28_baseline"]),
        "m28_replay_training_dataset": entry(paths["m28_dataset"]),
        "m28_bundle_directory": {
            "path": _rel_posix(repo_root, m28_bundle),
            "replay_bundle_manifest_sha256": _file_sha256(
                m28_bundle / "replay_bundle_manifest.json"
            ),
        },
        "m31_bundle_directory": {
            "path": _rel_posix(repo_root, m31_bundle),
            "replay_bundle_manifest_sha256": _file_sha256(
                m31_bundle / "replay_bundle_manifest.json"
            ),
        },
        "m31_hierarchical_agent": entry(paths["m31_agent"]),
    }
    return prov


def emit_m25_baseline_evidence_pack(
    *,
    output_baseline_dir: Path,
    paths: dict[str, Path],
) -> None:
    """Regenerate M25 from governed Phase-IV fixture JSON (deterministic across machines).

    Same inputs as ``test_happy_path_matches_golden`` in ``tests/test_baseline_evidence_pack.py``.
    A live M20–M24 chain from a contract would embed cwd-relative ``suite_path`` strings in the
    tournament artifact, which breaks stable hashes when intermediate directories differ; the
    checked-in fixtures are the canonical governed graph for reproducible evidence packaging.
    """

    output_baseline_dir.mkdir(parents=True, exist_ok=True)
    write_baseline_evidence_pack_artifacts(
        suite_paths=[paths["m25_scripted_suite"], paths["m25_heuristic_suite"]],
        tournament_path=paths["m25_tournament"],
        diagnostics_path=paths["m25_diagnostics"],
        output_dir=output_baseline_dir,
    )


def emit_m31_explorer(
    *,
    bundle_dir: Path,
    agent_path: Path,
    output_explorer_dir: Path,
) -> None:
    output_explorer_dir.mkdir(parents=True, exist_ok=True)
    surface, report = build_replay_explorer_artifacts(
        bundle_dir=bundle_dir.resolve(),
        agent_path=agent_path.resolve(),
        max_panels=DEFAULT_MAX_PANELS,
        slice_id_filter=None,
    )
    write_replay_explorer_surface(output_explorer_dir, surface)
    write_replay_explorer_report(output_explorer_dir, report)


def write_public_flagship_proof_pack(
    *,
    repo_root: Path,
    output_dir: Path,
    paths: dict[str, Path] | None = None,
) -> tuple[Path, Path, Path]:
    """Write baseline/, learned/, explorer/, pack, report, and hashes.json under ``output_dir``."""

    paths = paths or default_source_paths(repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    baseline_dir = output_dir / _BASELINE_DIR
    learned_dir = output_dir / _LEARNED_DIR
    explorer_dir = output_dir / _EXPLORER_DIR

    emit_m25_baseline_evidence_pack(
        output_baseline_dir=baseline_dir,
        paths=paths,
    )
    write_learned_agent_evaluation_artifacts(
        contract_path=paths["m28_benchmark_contract"],
        baseline_path=paths["m28_baseline"],
        dataset_path=paths["m28_dataset"],
        bundle_dirs=[paths["m28_bundle_dir"]],
        output_dir=learned_dir,
    )
    emit_m31_explorer(
        bundle_dir=paths["m31_bundle_dir"],
        agent_path=paths["m31_agent"],
        output_explorer_dir=explorer_dir,
    )

    artifact_paths = [
        output_dir / _BASELINE_DIR / BASELINE_EVIDENCE_PACK_FILENAME,
        output_dir / _BASELINE_DIR / BASELINE_EVIDENCE_PACK_REPORT_FILENAME,
        output_dir / _LEARNED_DIR / LEARNED_AGENT_EVALUATION_FILENAME,
        output_dir / _LEARNED_DIR / LEARNED_AGENT_EVALUATION_REPORT_FILENAME,
        output_dir / _EXPLORER_DIR / "replay_explorer_surface.json",
        output_dir / _EXPLORER_DIR / "replay_explorer_surface_report.json",
    ]
    artifact_roles = (
        "m25_baseline_evidence_pack",
        "m25_baseline_evidence_pack_report",
        "m28_learned_agent_evaluation",
        "m28_learned_agent_evaluation_report",
        "m31_replay_explorer_surface",
        "m31_replay_explorer_surface_report",
    )

    included_before_pack: list[dict[str, Any]] = []
    for p, role in zip(artifact_paths, artifact_roles, strict=True):
        rel = _rel_posix(output_dir, p)
        included_before_pack.append(
            {
                "relative_path": rel,
                "sha256": _file_sha256(p),
                "role": role,
            },
        )

    provenance = build_source_provenance(repo_root, paths)

    body_pre_hash: dict[str, Any] = {
        "proof_pack_version": PROOF_PACK_VERSION,
        "generation_commands": [
            "python -m starlab.flagship.emit_public_flagship_proof_pack --output-dir <OUTPUT_DIR>",
            "make flagship",
        ],
        "contract_references": [
            "docs/runtime/baseline_evidence_pack_v1.md",
            "docs/runtime/learned_agent_evaluation_harness_v1.md",
            "docs/runtime/replay_explorer_surface_v1.md",
            "docs/runtime/public_flagship_proof_pack_v1.md",
        ],
        "included_artifacts": included_before_pack,
        "source_provenance": provenance,
        "non_claims": sorted(PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1),
        "public_boundary_note": (
            "This pack is a public evidence index over governed, fixture-backed STARLAB surfaces. "
            "It does not disclose private operator data or crown-jewel internals; see "
            "docs/public_private_boundary.md and LICENSE."
        ),
        "deterministic_regeneration_note": (
            "Regeneration uses in-process emitters: M25 baseline evidence pack from the governed "
            "Phase-IV fixture graph (see test_happy_path_matches_golden), "
            "M28 learned-agent evaluation from fixtures + M16 bundle, M31 replay explorer "
            "surface from M31 bundle + M30 agent. Output JSON is canonicalized; byte-identical "
            "outputs assume a fixed repository tree."
        ),
    }

    proof_pack_sha256 = sha256_hex_of_canonical_json(body_pre_hash)
    proof_pack: dict[str, Any] = {**body_pre_hash, "proof_pack_sha256": proof_pack_sha256}

    pack_path = output_dir / PROOF_PACK_FILENAME
    pack_path.write_text(canonical_json_dumps(proof_pack), encoding="utf-8")

    baseline_pack = json.loads(
        (baseline_dir / BASELINE_EVIDENCE_PACK_FILENAME).read_text(encoding="utf-8"),
    )
    learned_eval = json.loads(
        (learned_dir / LEARNED_AGENT_EVALUATION_FILENAME).read_text(encoding="utf-8"),
    )

    report: dict[str, Any] = {
        "report_version": PROOF_PACK_REPORT_VERSION,
        "proof_pack_sha256": proof_pack_sha256,
        "subordinate_surface_versions": {
            "m25_evidence_pack_version": baseline_pack.get("evidence_pack_version"),
            "m28_evaluation_version": learned_eval.get("evaluation_version"),
            "m31_surface_version": M31_SURFACE_VERSION,
            "m31_report_version": M31_REPORT_VERSION,
        },
        "artifact_roles": [x["role"] for x in included_before_pack],
        "non_claims": sorted(PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1),
    }

    report_path = output_dir / PROOF_PACK_REPORT_FILENAME
    report_path.write_text(canonical_json_dumps(report), encoding="utf-8")

    hashes: dict[str, str] = {}
    for p in [*artifact_paths, pack_path, report_path]:
        rel = _rel_posix(output_dir, p)
        hashes[rel] = _file_sha256(p)

    hashes_sorted = dict(sorted(hashes.items()))
    hashes_path = output_dir / HASHES_FILENAME
    hashes_path.write_text(canonical_json_dumps(hashes_sorted), encoding="utf-8")

    return pack_path, report_path, hashes_path
