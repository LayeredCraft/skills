---
description: Create a branch if needed, commit current changes using a
  conventional commit message, push the branch, and create a pull
  request using the local PR template. Use this whenever the user asks
  to create, open, draft, or prepare a PR.
name: open-pr
---

# Open PR

Use this skill whenever the user asks to:

-   create a PR
-   open a PR
-   draft a PR
-   prepare a pull request
-   commit and open a PR
-   create a branch and PR
-   submit the current work

This skill performs the **entire workflow**, not just writing PR text.

------------------------------------------------------------------------

# Goal

Prepare the current work for review and create a pull request that
includes:

-   a correctly named branch
-   a conventional commit message
-   a PR title following the required format
-   a PR body generated from the local template

Template location:

`templates/pull-request-template.md`

------------------------------------------------------------------------

# Required PR Title Format

`<type>(<scope>): <description>`

Example:

`feat(core): add automated PR workflow`

------------------------------------------------------------------------

# Valid `<type>` Values

-   feat
-   fix
-   docs
-   refactor
-   test
-   chore
-   ci

------------------------------------------------------------------------

# Valid `<scope>` Values

Scope is optional.

-   host
-   envelopes
-   abstractions
-   opentelemetry
-   source-generators
-   deps
-   build
-   ci
-   github
-   core
-   docs
-   testing
-   tests

If no scope clearly applies, omit the scope.

------------------------------------------------------------------------

# File Inclusion Policy (Critical)

When preparing commits and PRs, **treat the working tree as the user's
intent**.

## Default behavior

Include **all user-modified files** in the commit and PR:

-   modified files
-   staged files
-   unstaged files
-   untracked files
-   deleted files

If the user changed a file, assume the change is intentional.

Do **not** exclude files merely because they appear unrelated to the
inferred task.

------------------------------------------------------------------------

## Allowed automatic exclusions

Files may only be excluded if they are clearly not intended for source
control, such as:

-   `.DS_Store`
-   editor swap files
-   temporary files
-   build output folders
-   cache folders
-   machine-local configuration files
-   secret files that should never be committed

Example patterns:

    .DS_Store
    *.swp
    *.tmp
    bin/
    obj/
    node_modules/
    .vscode/*

------------------------------------------------------------------------

## Ambiguity rule

If there is **any uncertainty** about whether a file should be
committed:

**Include the file.**

Never silently omit a user-modified file.

------------------------------------------------------------------------

## Transparency rule

If the skill excludes any files automatically, it must explicitly
report:

-   which files were excluded
-   the reason they were excluded

------------------------------------------------------------------------

# Branch Rules

## When to create a branch

Create a new branch if:

-   the current branch is `main`
-   the repository is in detached `HEAD`

If already on a feature branch, use the current branch.

------------------------------------------------------------------------

## Branch naming

`<type>/<scope>-<short-description>`

If no scope:

`<type>/<short-description>`

Rules:

-   lowercase only
-   hyphen separated
-   concise and descriptive
-   remove punctuation

Examples:

-   `feat/core-add-pr-automation`
-   `fix/github-handle-detached-head`
-   `docs/update-readme`
-   `ci/github-improve-release-workflow`

------------------------------------------------------------------------

# Commit Rules

Before committing:

1.  Inspect repository status
2.  Inspect changed files
3.  Stage **all user-modified files by default**
4.  Exclude only clearly temporary/generated artifacts
5.  Create a conventional commit message

Commit format:

`<type>(<scope>): <description>`

If scope does not apply:

`<type>: <description>`

Never create an empty commit.

If there are no changes to commit, skip commit creation.

------------------------------------------------------------------------

# Automatic Scope Detection

When possible, infer scope based on the folders that contain the
majority of the changes.

Examples:

  Folder                          Scope
  ------------------------------- -------------------
  `.github/workflows`             github
  `src/Core`                      core
  `src/Abstractions`              abstractions
  `src/SourceGenerators`          source-generators
  `src/OpenTelemetry`             opentelemetry
  `tests`                         tests
  `test`                          testing
  `docs`                          docs
  `build`                         build
  dependency or package updates   deps

If multiple folders are involved, prioritize the **primary concern of
the change**.

If no mapping clearly applies, omit the scope.

------------------------------------------------------------------------

# PR Generation Rules

Load the PR template from:

`templates/pull-request-template.md`

Populate the template using the current changes.

Guidelines:

-   summarize the actual change
-   explain why the change is needed
-   include important implementation details
-   do not invent issue numbers
-   do not mark checklist items complete unless confirmed
-   highlight risky areas or follow-up work for reviewers

------------------------------------------------------------------------

# Execution Flow

Follow this sequence.

## 1 Inspect repository

Determine:

-   current branch
-   whether HEAD is detached
-   git status
-   modified files
-   diff summary

------------------------------------------------------------------------

## 2 Infer metadata

Determine:

-   PR type
-   optional scope
-   short description
-   PR title
-   branch name

------------------------------------------------------------------------

## 3 Prepare branch

If on `main` or detached `HEAD`:

Create a new branch and switch to it.

Otherwise remain on the current branch.

------------------------------------------------------------------------

## 4 Commit work

Stage all user-modified files.

Exclude only obvious junk artifacts.

Create a commit using the conventional title.

Skip if nothing to commit.

------------------------------------------------------------------------

## 5 Push branch

Push branch to origin.

Set upstream if necessary.

------------------------------------------------------------------------

## 6 Generate PR body

Load template:

`templates/pull-request-template.md`

Fill:

-   Summary
-   Changes
-   Related Issues
-   Reviewer Notes

------------------------------------------------------------------------

## 7 Create PR

Create a pull request using:

-   generated title
-   generated body
-   current branch

------------------------------------------------------------------------

# Safety Rules

Never:

-   rewrite history
-   force push
-   silently omit user-modified files
-   invent issue numbers
-   fabricate test results
-   mark checklist items complete without evidence

If the repository state is ambiguous, choose the safest non-destructive
option.

------------------------------------------------------------------------

# Output Expectations

At the end report:

-   branch name
-   whether a branch was created
-   commit message
-   whether a commit was created
-   PR title
-   PR body
-   any excluded files
-   any assumptions or blockers
