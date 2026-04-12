# M40 Plan — Agent Training Program Charter & Artifact Contract

**Milestone:** M40  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Status:** In progress — see `docs/starlab.md` §7 / §11.

---

## Intent

Recharter STARLAB after M39 so the active program is a **governed training track** (M40–M45), not the former Phase VI substrate/platform review stubs. M40 delivers:

1. **Roadmap recharter** in `docs/starlab.md` — **46 milestones (M00–M45)**; former **SC2 Substrate Review** and **Platform Boundary Review** ideas recorded as **deferred** (§19).
2. **Training-program contract** — deterministic `agent_training_program_contract.json` / report under `out/training_program/`, `starlab.training` emitters, `docs/runtime/agent_training_program_contract_v1.md`.
3. **Stub milestones** M41–M45 (plan + toolcalls only).

No model training, no weights, no live SC2 in CI, no benchmark-integrity claims.

---

## Out of scope

- Training implementation (M41+)
- RL / self-play logic
- CI changes that weaken gates

---

## Deliverables

- Updated ledger, README, architecture (where referenced)
- `tests/test_m40_agent_training_program_contract.py`
- Governance tests: M39 complete row, arc 46, M42–M45 stub folders
