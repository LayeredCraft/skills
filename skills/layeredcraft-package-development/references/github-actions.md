# GitHub Actions and governance

`LayeredCraft/devops-templates` owns shared CI/CD behavior. Inspect current
reusable workflow inputs at chosen tag before writing callers. Reuse one reviewed
version across every workflow; pin immutable commit SHA when organization policy
requires supply-chain pinning. Do not mix v10/v11 callers in new repo.

## Required caller workflows

New NuGet library starts with:

```text
.github/workflows/
├── pr-build.yaml
├── pr-title-check.yaml
├── release-drafter.yaml
├── publish-preview.yaml
└── publish-release.yaml
```

Optional only with need: docs deploy, AOT smoke validation, package/API
compatibility validation, coverage reporting, Dependabot auto-merge.

## PR build

Keep PR code credential-free. New v11-style caller:

```yaml
name: PR Build
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  application-build:
    uses: LayeredCraft/devops-templates/.github/workflows/pr-build.yaml@<reviewed-pin>
    with:
      solution: LayeredCraft.<Package>.slnx
      dotnetVersion: <reviewed-sdk-channel-or-version>
      hasTests: true
      useMtpRunner: true # only when repository uses Microsoft Testing Platform
      runCdk: false
```

Add local jobs only for proof shared workflow cannot express: AOT publish/run,
package API validation, packed-consumer validation, or repository formatter. Add
final aggregate `build / build` job if branch protection needs one stable check
name across multiple jobs.

Never grant `id-token: write`, cloud roles, package credentials, or `write-all`
to PR build. Never use `pull_request_target` to execute PR code.

## PR title and Release Drafter

Add semantic PR-title check using shared workflow. Add Release Drafter caller on
main pushes, non-draft PR changes, and manual dispatch. Keep config local because
release-note categories and version rules are package policy.

Baseline labels:

```text
breaking-change
internal
skip-changelog
type: feat | fix | docs | refactor | test | chore | ci | revert
```

Baseline version policy:

```text
breaking-change or !  -> major
feat                  -> minor
fix/other labeled work -> patch
```

For pre-1.0 package, explicitly decide whether breaking changes remain minor.
Do not let Release Drafter choose policy by accident.

## Preview and release publishing

Preview caller triggers on non-doc `main` pushes if preview packages are desired.
It calls shared `publish-preview.yml`, packs/tests, and uploads artifact. A
separate push job publishes with shared `nuget-push` action:

```yaml
permissions:
  id-token: write
  contents: read
```

Release caller triggers only on GitHub `release: [published]`, calls shared
`publish-release.yml`, then same OIDC push action. Release workflow rebuilds
from release/tag source. Never promote arbitrary preview artifact as stable
release unless shared workflow deliberately implements that contract.

Required owner-controlled prerequisites:

- NuGet.org package ID ownership.
- NuGet Trusted Publishing policy bound to correct repository/workflow.
- `NUGET_USER` secret expected by shared action.
- GitHub Actions enabled for repository.

Do not put NuGet API key in repository, Actions secret, sample, or log.

## Dependabot

Add `dependabot.yml` for NuGet and GitHub Actions, normally weekly. Keep grouped
minor/patch updates if existing org package precedent uses them. Preserve explicit
ignores for intentionally constrained compiler/tooling dependencies.

Dependabot auto-merge is optional. It needs GitHub App ID/private-key secrets and
approved policy. Do not add workflow or claim it works until owner confirms both.

## Repository settings after first successful checks

Owner/admin action, not source-file change:

- Default branch `main`.
- Squash merge allowed; merge/rebase commits disabled.
- Auto-merge and delete-head-branch enabled.
- Main protection: PR required, one approval, dismiss stale approvals, code-owner
  approval if `CODEOWNERS` exists, linear history, conversation resolution.
- Require observed stable check names, normally `build / build`; add package/AOT
  gate only after successful real run.

Do not protect `main` against checks that have never been emitted. GitHub leaves
missing required checks pending forever.
