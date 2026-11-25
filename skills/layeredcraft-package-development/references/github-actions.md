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

| Caller under `.github/workflows/`                                                                                                      | Shared workflow       | Events and permissions                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`pr-title-check.yaml`](https://github.com/LayeredCraft/lambda-web-functions-dotnet/blob/main/.github/workflows/pr-title-check.yaml)   | `pr-title-check.yml`  | PR opened, edited, synchronized, reopened, or ready for review. Grant `pull-requests: read` and `statuses: write` to the metadata-only job.                                                                                                                  |
| [`release-drafter.yaml`](https://github.com/LayeredCraft/lambda-web-functions-dotnet/blob/main/.github/workflows/release-drafter.yaml) | `release-drafter.yml` | Main pushes, manual dispatch, and PR changes including `ready_for_review`. Pass `event_name: ${{ github.event_name }}` and `pr_draft: ${{ github.event.pull_request.draft == true }}`. Grant `contents: write` and `pull-requests: write` to the caller job. |

Start from the linked PR title and Release Drafter callers and align their
shared workflow pins with PR build. Keep `.github/release-drafter.yml` in the package repo. Match conventional PR
titles to release labels and use `v$RESOLVED_VERSION` for tags. Configure
`type: feat` for minor bumps and `type: fix` for patch bumps. Decide how
`breaking-change` affects pre-1.0 versions. Check that the version resolver and
release-note categories agree with the repo's policy. Compono has a concrete
[Release Drafter configuration](https://github.com/LayeredCraft/compono/blob/main/.github/release-drafter.yml).

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
publishes previews after merge. Release Drafter supplies the next version
and the preview workflow appends `-preview.<run-number>`. The tagged release
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
   check the observed results and confirm Release Drafter applies the
   intended version labels.
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
