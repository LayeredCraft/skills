---
name: create-branch
description: Create and switch to a new branch for the current work using inferred conventional naming.
---

# Create Branch

Use this skill whenever the user asks to:

- create a branch
- start a feature branch
- make a branch for this work
- start working on a change

## Goal

Create a properly named branch for the current work based on inferred change intent.

## Branch Naming Format

<type>/<scope>-<short-description>

If no scope applies:

<type>/<short-description>

Examples:

- feat/core-add-pr-automation
- fix/github-handle-detached-head
- docs/update-readme
- ci/github-improve-release-workflow

## Valid Types

- feat
- fix
- docs
- refactor
- test
- chore
- ci

## Scope Detection

Infer scope based on folders changed.

| Folder | Scope |
|------|------|
| .github/workflows | github |
| src/Core | core |
| src/Abstractions | abstractions |
| src/SourceGenerators | source-generators |
| src/OpenTelemetry | opentelemetry |
| tests | tests |
| test | testing |
| docs | docs |
| build | build |
| dependency updates | deps |

If no mapping applies, omit scope.

## Workflow

1. Inspect repository status and changed files
2. Infer change type
3. Infer optional scope
4. Generate branch name
5. Create branch
6. Switch to the branch

## Safety Rules

Never:

- overwrite existing branches
- delete branches automatically
- force push

If a branch with the same name exists, append a short suffix.

## Output

Report:

- branch name created
- branch switched to