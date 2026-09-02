# Graphify Developer Tooling

Graphify is an **optional local developer tool** for codebase navigation. It is not part of the bootstrap runtime, not a CI dependency, and not required to use or release `server-bootstrap`.

## Purpose

Graphify builds a queryable knowledge graph from repository code and documentation to help agents and developers navigate the project without repeatedly grepping large trees.

Official project: https://github.com/Graphify-Labs/graphify

Official PyPI package: `graphifyy` (CLI command: `graphify`)

## Policy for this repository

- Install Graphify in an isolated user tool environment (`uv tool install` or `pipx install`), pinned to a reviewed release.
- Use project-scoped Cursor integration only (`graphify cursor install --project`).
- Build graphs in **code-only / local** mode so repository content is not sent to external models.
- Do **not** install Graphify git hooks or global aliases as part of Phase 0.
- Do **not** add Graphify to `requirements-dev.txt` or CI gates.

## Initial setup

```bash
uv tool install graphifyy==0.9.53
graphify cursor install --project
graphify extract . --code-only
```

Refresh after significant structural changes:

```bash
graphify update . --code-only
```

## Tracked artifacts

Portable graph artifacts may be committed under `graphify-out/` when reviewed safe:

- `graph.json`
- `GRAPH_REPORT.md`
- `graph.html`

Ignore local-only artifacts:

```text
graphify-out/cost.json
```

## Review before commit

Before tracking generated Graphify output, verify:

- no secrets or credentials,
- no private hostnames or customer data,
- no unnecessary absolute paths,
- reasonable repository size impact.

## Removal

```bash
graphify cursor uninstall --project
```

To remove generated output:

```bash
graphify uninstall --project --purge
```
