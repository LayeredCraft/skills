---
name: commit-work
description: Stage all user-modified files, create a conventional commit message, and commit the changes. Use this when the user asks to commit their work.
---

# Commit Work

Use this skill whenever the user asks to:

- commit these changes
- create a commit
- save my work
- stage and commit
- commit current work

## Goal

Create a commit representing the user's current working changes using a conventional commit format.

## Commit Format

<type>(<scope>): <description>

If no scope applies:

<type>: <description>

### Valid types

- feat
- fix
- docs
- refactor
- test
- chore
- ci

## File Inclusion Policy

Treat the working tree as the user's intent.

Include all:

- modified files
- staged files
- unstaged files
- untracked files
- deleted files

Never omit a user-modified file just because it appears unrelated.

### Allowed exclusions

Only exclude files that are clearly not intended for source control:

- .DS_Store
- editor swap files
- temporary files
- build output
- cache folders
- machine-local configuration
- secrets

If unsure whether a file should be committed, include it.

If any file is excluded automatically, report which file and why.

## Scope Detection

When possible infer scope from folder structure.

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

1. Inspect repository status
2. Identify modified files
3. Stage all user-modified files
4. Exclude only obvious junk artifacts
5. Generate conventional commit message
6. Create commit

## Safety

Never:

- rewrite history
- force push
- fabricate results
- omit user-modified files silently

## Output

Report:

- commit message
- files committed
- any files excluded