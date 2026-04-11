# M38 Plan — Audit Closure VII — Public Face Refresh, Governance Rationalization, and Code-Health Tightening

**Milestone:** M38  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Status:** In progress (implementation on branch `m38-public-face-governance-code-health`)

---

## Milestone intent

Small, corrective, enterprise-grade milestone: improve **public readability**, reduce **governance friction** (without diluting audits), and tighten **high-value code-health** edges. Does **not** overlap M39 flagship proof-pack work.

---

## Objective

Produce a **cleaner, more legible, lower-noise repo surface** while preserving claims and CI truthfulness.

---

## Slices (this PR)

### Slice A — Public front door

- **Primary:** `README.md` — current program arc (**42 milestones M00–M41**), **M37** closed, **M38** current, **M39** planned flagship, proved vs not proved, where to start in under five minutes, **~85% coverage as stretch not claim**.
- **Supporting:** `docs/architecture.md` only if needed; existing doc retained as pointer from README.
- **Ledger:** compact **“Current truth (quick scan)”** table near top of `docs/starlab.md` for navigation; **no** removal of authoritative evidence in §1 / §18.

### Slice B — Governance rationalization

- Remove redundant **`test_planned_program_arc_is_42_milestones`** (overlap with `test_ledger_has_m01_runtime_title_and_m32_map`).
- Add **M07** and **M37** to `test_governance_milestones.py` milestone-table row checks (closes gap vs §7).

### Slice C — Code-health

- **`tests/runpy_helpers.py`:** `run_module_as_main` suppresses benign `runpy` `RuntimeWarning` (“found in sys.modules…”) in tests; all `runpy.run_module(..., __main__)` call sites in tests use helper.
- **`tests/test_runpy_helpers.py`:** regression test that the sys-modules warning does not surface.

---

## Out of scope

- M39 public flagship proof-pack product work  
- New benchmark-integrity claims  
- Live SC2 in CI  
- Operating manual v1 promotion  
- Broad architecture reshaping  
- Large refactors  

---

## Deliverables (closeout, post–green CI)

- `M38_summary.md`, `M38_audit.md`, `M38_run1.md` (if applicable)  
- Ledger update with PR number, SHAs, authoritative CI runs  
- Next milestone stubs (**M39** plan + toolcalls) after merge permission  

---

## Acceptance criteria

1. README materially reflects current truth.  
2. At least one governance duplication reduced without weakening gates.  
3. At least one code-health fix with tests.  
4. CI green; no weakened checks.  
5. `docs/starlab.md` truthful for M38.  

---

## Branch / PR

- **Branch:** `m38-public-face-governance-code-health`  
- **PR title:** `M38: public face refresh, governance rationalization, and code-health tightening`  
