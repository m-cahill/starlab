"""Allow ``python -m starlab.sc2`` to run the environment probe CLI."""

from __future__ import annotations

import sys

from starlab.sc2.env_probe import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
