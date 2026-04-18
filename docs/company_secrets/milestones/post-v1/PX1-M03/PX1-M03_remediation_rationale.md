# PX1-M03 — Remediation rationale

**PX1-M02** closed with **`no-candidate-selected`**: bounded protocol v2 evaluation showed the primary refit candidate did not meet frozen play-quality thresholds (0/10 wins in the authoritative series). Separately, the live BurnySc2 harness was effectively **observation-only** (`action_count` always zero), so “play” evidence was not semantically grounded in real SC2 commands.

**PX1-M03** exists to:

1. Preserve honest **PX1-M02** history — no reinterpretation.
2. Add a **small, audit-defensible** hybrid live surface: deterministic Terran macro essentials + narrow candidate-driven combat/scout choice.
3. Re-run evaluation under a **new frozen remediation protocol** with improved proof readability (categorized tallies, behavior summary).
4. Close with **`demo-ready-candidate-selected`** or **`no-demo-ready-candidate-within-scope`** — **not** opening **PX1-M04** or **v2** automatically.

Governed demo/video proof moves to **PX1-M04** only after explicit charter if **PX1-M03** justifies it.
