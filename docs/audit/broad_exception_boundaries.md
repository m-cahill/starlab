# Broad `except Exception` boundaries (DIR-005)

**Purpose:** Record where **`except Exception`** with **`# noqa: BLE001`** remains intentional at **untrusted or adapter boundaries**.  
**Authority:** Subordinate to `docs/starlab.md`.

## M34 validation summary

A repo-wide search of `starlab/` found **`except Exception`** only in:

| Location | Role |
| -------- | ---- |
| `starlab/replays/s2protocol_adapter.py` | Blizzard / `s2protocol` adapter surface; failures become structured parse/receipt outcomes. |
| `starlab/replays/metadata_io.py` | Extraction boundary; failures surface as `extraction_failed` / advisory strings. |
| `starlab/sc2/harness.py` | SC2 / adapter harness; failures return `HarnessResult` messages to CLI. |

No bare `except:` or `except BaseException` appeared in `starlab/` or `tests/` at M34 closeout.

## Resolution posture (DIR-005)

**DIR-005** is closed as **documentation / validation closure**: all remaining broad catches are **approved boundary** handlers (not internal-only control flow). Narrowing would risk hiding real adapter failures without improving STARLAB-owned artifact contracts.
