# Dogfooding

Dogfooding proves consumer experience of package artifact, not source tree.
Project references, unit tests, and `dotnet build` do not prove final `.nupkg`
contains correct assets, dependencies, metadata, analyzers, or transitive graph.

## Consumer selection

1. Use existing LayeredCraft consumer when it exercises intended package API.
2. Keep in-repo sample/sample-test as fast deterministic baseline.
3. Create temporary minimal consumer only when no real consumer exists.

Search organization before declaring no consumer. Record why selected consumer
covers package risk.

## Required local-feed loop

Run before first PR. Repeat after each substantive package, packaging, generated
output, public API, target-framework, or dependency change.

1. Clean prior local feed and restore artifacts.
2. Pack every changed publishable package under one unique prerelease version.
3. Make local feed highest-priority package source for consumer.
4. Override consumer package versions temporarily. Do not edit/commit consumer's
   real central package file for validation.
5. Restore consumer with caches isolated or cleared as needed.
6. Assert restore resolved exact packed version for every dogfooded package.
7. Build and test consumer; run host/application behavior when relevant.
8. Delete temp override/feed or use disposable worktree/directory.

Example shell outline. Adapt paths and version-management mechanism; do not copy
blindly:

```bash
version="0.1.0-dogfood.$(date +%s)"
feed="$(mktemp -d)"

dotnet pack src/LayeredCraft.Example/LayeredCraft.Example.csproj \
  -c Release -o "$feed" -p:Version="$version"

# In disposable consumer worktree: add temporary source/version override, then:
dotnet restore --no-cache
dotnet build --no-restore
dotnet test --no-build
```

Evidence must name package IDs, unique version, consumer commit/worktree, restore
proof, and command results. “Used local feed” without version-resolution proof is
not sufficient.

## Package-type proof

| Package type              | Required consumer evidence                                                            |
| ------------------------- | ------------------------------------------------------------------------------------- |
| Runtime library           | public API executes from packed package                                               |
| Source generator/analyzer | consumer compiles generated output and executes it; inspect analyzer/build assets     |
| Framework integration     | real framework runner/host discovers and exercises integration                        |
| ASP.NET/Lambda            | host boots from packed package; health or representative request succeeds             |
| AOT/trim promise          | consumer is packed, restored, published Native AOT, then executable runs              |
| Multi-package suite       | consumer resolves every relevant freshly packed package under same validation version |

## CI promotion

Start local. Promote stable, high-value consumer proof into repository CI after
it is deterministic and network/credentials requirements are understood.

Compono precedent: package-content checks, local-feed sample tests, AOT smoke
apps, and external-consumer script. Copy concept, not its package names or
assumptions. Do not make unrelated external repository availability a required PR
gate without fallback/owner agreement.
