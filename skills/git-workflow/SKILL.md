---
name: git-workflow
description: >-
  Git workflow automation for committing, branching, and opening pull requests.
  Use this whenever the user asks to commit their work, create a branch, or
  create/open/draft a PR.
---

# Git Workflow

Use this skill whenever the user asks to:

- commit these changes
- create a commit
- save my work
- stage and commit
- commit current work
- create a branch
- start a feature branch
- make a branch for this work
- start working on a change
- create a PR
- open a PR
- draft a PR
- prepare a pull request
- commit and open a PR
- create a branch and PR
- submit the current work

______________________________________________________________________

## Commit-only fast path

When the user only asks to commit, stage and commit, save current work, or
otherwise create a commit without asking for a branch, push, or PR, keep the
workflow compact:

1. Do not load PR, branch, template, release note, or example files.
2. Do not load shared references unless compact git inspection leaves real
   ambiguity.
3. Inspect with `git status --short`, `git diff --name-status`, and
   `git diff --stat` first.
4. Avoid full `git diff` unless the commit message cannot be inferred from
   file names and diff stats.
5. Stage all user-modified files except obvious junk, local config, generated
   build/cache output, and secrets.
6. Create a concise conventional commit.
7. Report only the commit message, files committed, and any exclusions.

For branch and PR requests, load only the workflow doc selected below. Let that
doc identify any extra references needed for the requested workflow.

______________________________________________________________________

## Intent routing

Based on the user's request, load exactly one workflow doc:

| User intent                                     | Load                             |
| ----------------------------------------------- | -------------------------------- |
| Commit work, save changes, stage and commit     | [docs/commit.md](docs/commit.md) |
| Create a branch, start a feature branch         | [docs/branch.md](docs/branch.md) |
| Create/open/draft a PR, submit the current work | [docs/pr.md](docs/pr.md)         |

When intent is ambiguous, prefer the more complete workflow. If the user says "commit and open a PR", load `docs/pr.md` — it covers the full lifecycle including commit and branch.
