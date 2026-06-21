# COLM Paper Workspace

This directory contains the draft body for an anonymized COLM-style paper.
The official COLM 2026 style files still need to be added from:

https://github.com/COLM-org/Template/releases/tag/2026

The current draft is intentionally conservative. It reports the completed
Qwen3.5-35B romanization experiment and automatic evaluation, but does not
claim native-speaker quality or metric-human divergence without human ratings.

## Files

- `paper.tex`: draft entry point to replace or merge into the official template.
- `sections/`: modular paper sections.
- `references.bib`: verified references used by the current draft.

## Local compilation

After adding the official COLM style files:

```bash
latexmk -pdf paper.tex
```

## Overleaf Git integration

Overleaf Git integration is a premium feature. In an Overleaf project, open
**Integrations > Git**, copy the project Git URL, then add it locally:

```bash
git remote add overleaf https://git.overleaf.com/PROJECT_ID
git push overleaf main
```

Use an Overleaf Git authentication token when prompted, not the account
password.
