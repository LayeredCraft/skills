# Validate the package in a consumer

## Build, test, and pack

Run the repository formatter first. These commands use the new-repo MTP
setup and example solution name. Keep the explicit package version the same
for build and pack.

```sh
solution=LayeredCraft.Example.slnx
scratch="$(mktemp -d)"
feed="$scratch/feed"
version="0.1.0-local.$(date -u +%Y%m%d%H%M%S)"
dotnet build "$solution" -c Release -p:Version="$version"
dotnet test --solution "$solution" -c Release --no-build --no-restore
dotnet pack "$solution" -c Release --no-build -o "$feed" -p:Version="$version"
```

Open each `.nupkg` as a ZIP and inspect the manifest, dependency versions,
assemblies or analyzer assets, and README. Compare the package IDs in the
feed with the IDs you intend to ship.

## Run the packaged API

1. Prefer an existing LayeredCraft consumer that exercises the package's
   normal use. Use a temporary checkout for that consumer. If no existing
   consumer fits, use a runnable sample or a small standalone project.
2. Use an exact-version `PackageReference` such as
   `Version="[0.1.0-local.20261125120000]"` in the consumer. If it uses central
   package management, make the temporary version change where the version is
   declared. Remove any project reference for the package under test. Include
   the local feed in the consumer's temporary NuGet config. If the repo uses
   source mapping, map the package IDs you are testing to the local feed and
   preserve sources for the other dependencies.
3. Restore with `dotnet restore <consumer-project> --packages "$scratch/packages"`
   and pass `--no-http-cache` if needed. For each relevant framework, inspect
   `obj/project.assets.json` to confirm the expected exact package version and
   that it resolved as a package. Mind the repo's lock-file policy in the
   temporary checkout. Build without restoring again.
4. Run the test, program, host, or framework integration with `--no-build` or
   `--no-restore` as appropriate to preserve the verified dependency graph. Exercise the
   intended behavior. For generators, compile from the packaged analyzer at
   the supported compiler floor and exercise its generated code. For an AOT
   claim, publish and execute a representative consumer.
5. Record the package IDs and versions, consumer repo or sample, target SDK and
   framework, and observed result. Keep local feed and version overrides out
   of committed files.

Compono and DynamoMapper give examples of package suites and generators whose
consumer behavior depends on the shipped package contents.
[Compono](https://github.com/LayeredCraft/compono),
[DynamoMapper](https://github.com/LayeredCraft/dynamo-mapper)
