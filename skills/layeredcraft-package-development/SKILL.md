---
name: layeredcraft-package-development
description: >-
  Creates and ships a new LayeredCraft .NET/NuGet package repository using proven
  organization conventions: repository blueprint, package metadata, testing,
  GitHub Actions from LayeredCraft/devops-templates, branch protection, first PR,
  preview and first release, and mandatory dogfooding with real LayeredCraft
  consumers. Use whenever creating, scaffolding, bootstrapping, publishing, or
  preparing a new LayeredCraft C#/.NET class library, NuGet package, source
  generator, analyzer, ASP.NET extension, integration package, or multi-package
  suite; also when standardizing its CI/release setup or planning its first
  release. Do not use for ordinary application repositories, non-LayeredCraft
  packages, or a narrow change to an existing package that does not affect setup
  or delivery.
---

# LayeredCraft package development

Create packages that fit LayeredCraft ecosystem. Existing packages are design
input, not optional inspiration. Reuse organization tooling and prove package in
real consumer. A green unit suite alone does not prove shipped `.nupkg` works.

## Operating rules

- Inspect current `LayeredCraft` package repos plus `LayeredCraft/devops-templates`
  before copying a convention. Pin workflow version only after reviewing matching
  reusable-workflow interface.
- Use `LayeredCraft/devops-templates`; do not recreate shared build, release, or
  NuGet publishing logic locally.
- Before adding a third-party dependency or rebuilding shared capability, search
  LayeredCraft packages. Use an existing organization package when it fits; record
  why it does not when it cannot.
- Use least-privilege GitHub Actions permissions. PR code never receives OIDC,
  cloud credentials, or write permission.
- Build one vertical slice before speculative package architecture.
- Dogfood each publishable package through a packed local feed. Use real
  LayeredCraft consumer when one exists. Repeat after every substantive package
  change before push.
- Never claim AOT/trim support without analyzer configuration and published
  consumer proof. Load `dotnet-aot-library-validation` for that work.
- Never create branch protection required checks until matching workflows exist
  and have produced successful check runs.
- Never enable Dependabot auto-merge without approved GitHub App credentials and
  owner confirmation.

## Intake

Read repo instructions and current state. Then collect or infer only facts needed:

1. Package type: runtime library, ASP.NET extension, source generator/analyzer,
   framework integration, or multi-package suite.
2. Package ID(s), target consumers, public API boundary, target frameworks, and
   first-release stability (`alpha`, `preview`, or stable).
3. Existing LayeredCraft consumer(s). Search org repos before proposing a throwaway
   sample.
4. Existing LayeredCraft package/component candidates. Check them before choosing
   external dependency or duplicating capability.
5. Compatibility claims: Native AOT, trimming, source-generator host SDK floor,
   supported framework/library versions.
6. Docs scope: README only, docs site, generated API reference.

When package type, consumer, public API, or compatibility promise is genuinely
unknown, ask before scaffolding. Do not invent a stable public API.

## Workflow

### 1. Choose shape

Load [package types](references/package-types.md). Choose smallest shape that
proves user problem. Record package graph before creating multi-package suite.

### 2. Build foundation

Load [repository blueprint](references/repository-blueprint.md). Create repository
layout, solution, project metadata, first public vertical slice, unit tests, and
consumer sample. Follow nearest existing LayeredCraft package for target
frameworks and tooling.

### 3. Prove packed package

Load [dogfooding](references/dogfooding.md). Pack source into unique local
prerelease version, restore consumer from local feed, assert resolved version,
and build/test consumer. This gate applies before first PR and every substantive
revision later.

### 4. Install delivery automation

Load [GitHub Actions](references/github-actions.md). Add caller workflows pinned
to one reviewed `devops-templates` version, Release Drafter config, Dependabot,
and initial governance. Run workflows before making checks required.

### 5. Land first PR and release

Load [delivery](references/delivery.md). Follow first-PR, preview, first-release,
and post-release runbooks. Verify NuGet trusted publishing before publishing any
release.

## Required output

For setup work, report:

```md
## Package decision

- Type:
- Package ID(s):
- Consumers:
- Compatibility/support policy:

## Repository plan

- Layout:
- Public API and tests:
- Docs:

## Automation

- Shared workflow pin:
- PR checks:
- Preview path:
- Release path:
- Repository settings still requiring owner action:

## Dogfood evidence

- Packed version:
- Consumer(s):
- Commands and result:

## First delivery checklist

- [ ] First PR
- [ ] Preview verification
- [ ] NuGet trusted publishing preflight
- [ ] First release
```

Report commands/results only when run. State unresolved owner-controlled GitHub
or NuGet configuration separately from repository changes.

## Reference map

| Need                                       | Read                                                       |
| ------------------------------------------ | ---------------------------------------------------------- |
| Directory layout, metadata, baseline files | [repository blueprint](references/repository-blueprint.md) |
| Package-specific architecture              | [package types](references/package-types.md)               |
| Shared workflows and governance            | [GitHub Actions](references/github-actions.md)             |
| Local-feed and external-consumer proof     | [dogfooding](references/dogfooding.md)                     |
| First PR, preview, and release             | [delivery](references/delivery.md)                         |
