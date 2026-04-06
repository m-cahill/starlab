# Security

## Reporting

Report security issues **privately** to the repository owner (Michael Cahill) via a non-public channel (e.g. GitHub private security advisory if enabled, or agreed contact).

Do **not** open public issues for undisclosed vulnerabilities.

## Secrets

Never commit:

- API keys, tokens, or passwords
- `.env` files containing secrets
- Provider credentials (Netlify, Render, etc.)

Use provider-managed secrets and local environment variables only.

## Scope

This repository is in early governance bootstrap. There is no production deployment in M00; surface area is documentation and CI.
