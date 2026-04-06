# Environment matrix

Reserved for future operational use. M00 seeds structure only; most cells are **not yet active**.

| Dimension | local | ci | preview | production |
|-----------|-------|-----|---------|------------|
| **Frontend target** | reserved (future Netlify) | N/A | reserved | reserved |
| **Backend target** | reserved (future Render) | N/A | reserved | reserved |
| **Secrets source** | local env / not committed | GitHub Actions secrets (future) | provider | provider |
| **Allowed data** | dev-only; no unclear-rights corpus in canonical paths | test fixtures only | TBD | TBD |
| **Notes** | No production claim | Governance CI only in M00 | Netlify deploy previews when enabled | Netlify + Render when enabled |

**Rule:** Until a milestone explicitly enables hosting, no row implies a live system.
