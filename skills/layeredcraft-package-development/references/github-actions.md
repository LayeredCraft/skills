# GitHub Actions and publishing

Use [LayeredCraft/devops-templates](https://github.com/LayeredCraft/devops-templates)
for shared build and release logic. Use one reviewed revision across callers and
the NuGet action. Check the files at that revision for input names, job names,
permissions, and artifact names. Use a full commit SHA when the repo requires
immutable pins.

## Pull request checks and release notes

This example uses v11.2 and matches the new-library starter. Replace the
solution and SDK with the target repo's values.

```yaml
name: PR Build
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened, ready_for_review]
permissions:
  contents: read
jobs:
  build:
    uses: LayeredCraft/devops-templates/.github/workflows/pr-build.yaml@v11.2
    with:
      solution: LayeredCraft.Example.slnx
      dotnetVersion: 10.0.x
      hasTests: true
      useMtpRunner: true
```

For v11.2 the shared .NET job is named `dotnet`, so this caller normally emits
`build / dotnet`. Use the observed check name when setting branch protection.
An existing repository may already use an aggregate check such as
`build / build`. Preserve that check when migrating and make it depend on every
required job. Add local jobs for repo-specific checks such as package validation,
AOT smoke tests, or a formatter the template cannot run. Keep PR build jobs
read-only and free of secrets. Set `useMtpRunner` only for MTP projects and use a
matching `global.json`. The shared v11 PR build defaults to no CDK deployment.

Use the [PR title caller](https://github.com/LayeredCraft/cdk-constructs/blob/main/.github/workflows/pr-title-check.yaml)
on PR open, edit, synchronize, reopen, and ready for review. Align its pin with
PR build. The v11.2 title check accepts `feat`, `fix`, `docs`, `refactor`,
`test`, `chore`, `ci`, and `revert`. Scope is optional and the subject starts
with a lowercase letter. The check uses `pull-requests: read` and `statuses: write`.
[Shared PR title check](https://github.com/LayeredCraft/devops-templates/blob/v11.2/.github/workflows/pr-title-check.yml)

## Release Drafter

Add both files when setting up a new package repository.

- Copy the [starter configuration](../assets/release-drafter.yml) to
  `.github/release-drafter.yml`. This controls PR labels, release notes,
  and version resolution.
- Start from the [CDK Constructs caller](https://github.com/LayeredCraft/cdk-constructs/blob/main/.github/workflows/release-drafter.yaml)
  for `.github/workflows/release-drafter.yaml`. Keep the shared workflow pin
  aligned with PR and publish workflows. Grant `contents: write` and
  `pull-requests: write` to the caller and pass
  `event_name: ${{ github.event_name }}` and
  `pr_draft: ${{ github.event.pull_request.draft == true }}`.

The shared workflow labels non-draft PRs on open, edit, synchronize, reopen,
and ready for review. It updates the draft release on pushes to `main` and
manual dispatch. The preview workflow reads the same config in dry-run mode
to calculate the next package version.

The starter matches the label names and release sections used across the
organization. For example, `feat(api): add batching` gets `type: feat` and
`fix(api)!: remove the old overload` gets `type: fix` and `breaking-change`.
The highest eligible bump wins. Breaking changes bump major, features bump
minor, and the other included types default to patch. The `internal` and
`skip-changelog` labels remove a PR from both notes and version calculation.
The release name and tag use `v$RESOLVED_VERSION`. Check the resolved first
version against the brief. If the project explicitly stays on a `0.x` line,
set its breaking-change rule accordingly.

The starter uses category rules supported by Release Drafter v7.7.0, which
the v11.2 shared workflows pin. Compono and Minimal Lambda use this format.
Older package configs can contain top-level `version-resolver`, `include-labels`,
and `exclude-labels`. Check the action version before reusing a config from
another repo. Keep a repository's existing version policy when updating its
workflow. DynamoDB EF Core Provider uses separate configs for independent
major-version lines.
[Compono config](https://github.com/LayeredCraft/compono/blob/main/.github/release-drafter.yml),
[Minimal Lambda config](https://github.com/LayeredCraft/minimal-lambda/blob/main/.github/release-drafter.yml),
[DynamoDB EF Core 11 config](https://github.com/LayeredCraft/dynamodb-efcore-provider/blob/main/.github/release-drafter-ef11.yml),
[Release Drafter v7.7.0](https://github.com/release-drafter/release-drafter/blob/v7.7.0/README.md#version-resolver)

## Dependency updates

Use weekly Dependabot updates for NuGet and GitHub Actions when setting up a
new package repo. Group minor and patch updates if it suits the repo. Preserve
compiler compatibility constraints, and add SDK updates if the repo tracks its
SDK that way.
[Dependabot example](https://github.com/LayeredCraft/lambda-web-functions-dotnet/blob/main/.github/dependabot.yml)

## Preview and tagged release

Both v11.2 publishing workflows build, test, pack, and upload `.nupkg`
artifacts. Their test command is `dotnet test --solution`, which expects
Microsoft Testing Platform mode. The new-library test project and
`global.json` in [repository standards](repository-standards.md) use this
mode. Run that same command locally before wiring publishing.

Use this as `.github/workflows/publish-release.yaml`.

```yaml
name: Publish Release
on:
  release:
    types: [published]
permissions:
  contents: read
jobs:
  build:
    permissions:
      contents: write
    uses: LayeredCraft/devops-templates/.github/workflows/publish-release.yml@v11.2
    with:
      solution: LayeredCraft.Example.slnx
      dotnetVersion: 10.0.x
      hasTests: true
  push:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: LayeredCraft/devops-templates/.github/actions/nuget-push@v11.2
        with:
          nuget_user: ${{ secrets.NUGET_USER }}
```

For `.github/workflows/publish-preview.yaml`, use the same job layout with
`publish-preview.yml` and add `pull-requests: write` to the build job. Use
`workflow_dispatch` and run it from `main`. Add pushes to `main` if the repo
publishes previews after merge. Most existing package callers do this and
skip docs-only pushes. Release Drafter supplies the next version and the
preview workflow appends `-preview.<run-number>`. The tagged release
takes its version from the GitHub release tag. Both use the `nuget-packages`
artifact by default.

The composite action runs in the caller job. This gives NuGet the caller's
workflow identity during the OIDC exchange. Keep OIDC permission on the push
job and avoid forwarding secrets to the build. For each publishing caller,
have the package owner configure NuGet Trusted Publishing with the exact
repository, workflow filename, and environment if used. Scope it to the
intended IDs and allow new packages for the first push. Set `NUGET_USER` to
the NuGet username of the policy creator. Use the workflow file's basename
when entering it in NuGet.org.
[NuGet Trusted Publishing](https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing)

## First PR and release

1. Verify the local build, tests, and packed consumer. When the PR runs,
   verify the title check and confirm Release Drafter applies the intended
   labels. After merge, check the draft's notes and proposed `vX.Y.Z` tag
   before the first publish.
2. When preview publishing is authorized, run the preview caller. Verify the
   artifact, wait for the exact package version to appear on NuGet.org, and
   restore it into the consumer.
3. For an authorized release, review the draft notes and version, confirm that
   the tag points to the intended commit, and publish the GitHub release. Check
   that the release caller succeeds and that the intended IDs and versions
   restore from NuGet.org.

Use the tagged template files to verify exact inputs. Use the package repo
callers as examples of how the jobs fit together.
[Shared workflows at v11.2](https://github.com/LayeredCraft/devops-templates/tree/v11.2/.github/workflows),
[Lambda Web Functions callers](https://github.com/LayeredCraft/lambda-web-functions-dotnet/tree/main/.github/workflows)
