"""Split-governance control entries for the M55 benchmark integrity charter."""

from __future__ import annotations

from typing import Any

from starlab.benchmark_integrity.benchmark_integrity_models import (
    CONTROL_FAMILY_ORDER,
    CONTROL_IDS_ORDERED,
)


def split_governance_controls() -> list[dict[str, Any]]:
    """Six top-level controls — one per family, deterministic order."""

    specs: list[tuple[str, str, str, str, list[str], list[str], list[str]]] = [
        (
            CONTROL_IDS_ORDERED[0],
            CONTROL_FAMILY_ORDER[0],
            (
                "Owns the versioned benchmark contract identity and score semantics: "
                "what constitutes a valid benchmark subject class and how primary metrics are "
                "interpreted under M20-style contracts."
            ),
            "M20 benchmark contract + scorecard schemas; benchmark-facing CLI/doc surfaces that "
            "bind contract ids and scoring_role semantics.",
            [
                "Runners, tournament harnesses, or report layers silently redefining "
                "benchmark score semantics outside the contracted benchmark definition.",
                "Treating ad hoc JSON or diagnostics as if they were the governed benchmark "
                "contract without an explicit contract id/version linkage.",
            ],
            [
                "Recorded benchmark_contract_id / schema linkage for a benchmark-grade run.",
                "Explicit score semantics ownership aligned to the benchmark contract, not "
                "inferred from downstream tooling.",
            ],
            [
                "Does not prove that any particular benchmark run is repeatable or comparable "
                "across hosts (M56).",
            ],
        ),
        (
            CONTROL_IDS_ORDERED[1],
            CONTROL_FAMILY_ORDER[1],
            (
                "Governs replay/map/label provenance posture, intake status, redistribution "
                "constraints, and whether material is eligible for canonical-review promotion."
            ),
            "M07 replay intake receipts; M14 bundle lineage; rights/provenance registers; "
            "canonical corpus policy statements.",
            [
                "Silently treating local-only, quarantined, or non-redistributable material as "
                "benchmark-grade canonical corpus.",
                "Promoting assets into a canonical corpus without explicit provenance and intake "
                "posture aligned to STARLAB governance rules.",
            ],
            [
                "Provenance records adequate for corpus promotion decisions.",
                "Intake/eligibility posture visible at aggregation and publication time.",
            ],
            [
                "Does not perform corpus promotion or relabel datasets in M55 (charter only).",
            ],
        ),
        (
            CONTROL_IDS_ORDERED[2],
            CONTROL_FAMILY_ORDER[2],
            (
                "Binds baseline vs candidate identity and freezes training/evaluation artifact "
                "versions when comparing subjects under a benchmark contract."
            ),
            "M02/M03/M04 identity JSON; M40–M42 program and comparison harness linkage; bundle "
            "hashes and run seals where applicable.",
            [
                "Silent substitution of a different model artifact, weights path, or bundle "
                "while preserving the same nominal benchmark row.",
                "Comparing candidates without a recorded contract or lineage linkage sufficient "
                "to reconstruct what was evaluated.",
            ],
            [
                "Subject identity records tied to contract and run hashes / deterministic ids.",
                "Explicit freeze markers for artifacts participating in a comparison.",
            ],
            [
                "Does not verify that stored hashes match unpacked artifact bytes (M56 evidence).",
            ],
        ),
        (
            CONTROL_IDS_ORDERED[3],
            CONTROL_FAMILY_ORDER[3],
            (
                "Separates fixture-only, local-first, bounded live-local, and "
                "unavailable-by-design evaluation surfaces; forbids misrepresenting harness "
                "posture as live evidence."
            ),
            "M02/M44 runtime_mode distinctions; CI fixture tiers; environment lock and smoke/drift "
            "surfaces documented as non-benchmark proof.",
            [
                "Representing fixture-only or stubbed execution as equivalent to full live SC2 "
                "evidence for benchmark claims.",
                "Claiming CI-default CPU fixture paths prove live SC2-in-CI benchmark integrity.",
            ],
            [
                "Execution posture declared on benchmark-facing receipts where such receipts "
                "exist (future M56).",
                "Explicit unavailable_by_design handling for surfaces omitted by contract.",
            ],
            [
                "Does not introduce live SC2 in CI or change default CI merge proof posture (M55).",
            ],
        ),
        (
            CONTROL_IDS_ORDERED[4],
            CONTROL_FAMILY_ORDER[4],
            (
                "Defines who owns aggregation semantics and who may summarize or publicize "
                "benchmark results; prevents diagnostics layers from inventing stronger claims "
                "than the benchmark contract allows."
            ),
            "M23–M25 evaluation and diagnostics artifacts; flagship or operator-facing packs "
            "that summarize tournament rows.",
            [
                "Rankings or headlines that disagree with the governed primary metric under the "
                "benchmark contract.",
                "Diagnostics or failure-view JSON presented as if it were a new benchmark "
                "contract or pass/fail verdict.",
            ],
            [
                "Reproducible aggregation steps from raw score rows to published summaries.",
                "Explicit separation between interpretive diagnostics and contract-authorized "
                "claims.",
            ],
            [
                "Does not prove statistical significance or leaderboard validity (M56 and beyond).",
            ],
        ),
        (
            CONTROL_IDS_ORDERED[5],
            CONTROL_FAMILY_ORDER[5],
            (
                "Separates who may describe benchmark integrity status from enforced repository "
                "or merge gates; M55 introduces no benchmark acceptance verdict."
            ),
            "Public ledger (`docs/starlab.md`); future M56 gate vocabulary; descriptive "
            "operator language only where explicitly allowed.",
            [
                "Charter or report JSON silently treated as a repository merge gate for "
                "benchmark integrity.",
                "Descriptive language in auxiliary reports read as formal acceptance without an "
                "explicit gate family (reserved for M56).",
            ],
            [
                "Clear acceptance authority boundaries when M56 introduces gate packs.",
                "Separation between governance narrative and enforced automation.",
            ],
            [
                "M55 emits charter_only status — no benchmark integrity acceptance verdict.",
            ],
        ),
    ]

    rows: list[dict[str, Any]] = []
    for (
        control_id,
        control_family,
        purpose,
        owned_surface,
        prohibited_conflations,
        required_evidence_later,
        residual_non_claims,
    ) in specs:
        rows.append(
            {
                "control_id": control_id,
                "control_family": control_family,
                "purpose": purpose,
                "owned_surface": owned_surface,
                "prohibited_conflations": prohibited_conflations,
                "required_evidence_later": required_evidence_later,
                "residual_non_claims": residual_non_claims,
            }
        )
    return rows
