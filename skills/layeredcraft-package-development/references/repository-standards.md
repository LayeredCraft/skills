# Repository standards

## Pick a comparable repo

Use these examples to choose the package layout and tests. For new CI, start
with the v11-style callers described in [GitHub Actions](github-actions.md).
Several sibling repos still use earlier templates with broader permissions.

| Package shape                      | LayeredCraft examples                                                                                                   | What to verify                                                                                                                                                        |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Runtime library                    | [Compact JSON Formatter](https://github.com/LayeredCraft/compact-json-formatter)                                        | A small public entry point, a usage example, and a consumer test on the supported framework versions.                                                                 |
| ASP.NET Core or Lambda extension   | [Lambda Web Functions](https://github.com/LayeredCraft/lambda-web-functions-dotnet)                                     | Start the real host and make a representative request. Check a published executable when the package advertises Native AOT.                                           |
| Source generator or analyzer       | [DynamoMapper](https://github.com/LayeredCraft/dynamo-mapper), [DecoWeaver](https://github.com/LayeredCraft/decoweaver) | Test diagnostics, generated code, and the packaged analyzer on the oldest supported compiler and SDK.                                                                 |
| Package suite or framework adapter | [Compono](https://github.com/LayeredCraft/compono)                                                                      | Core works without the adapters. Each adapter depends on core and the framework it integrates with. Exercise the adapter through the actual framework runner or host. |

## Lay out the repository

- Use a lowercase, hyphenated repo name on GitHub and a clear package ID. New
  packages usually use `LayeredCraft.<Name>` or
  `LayeredCraft.<Area>.<Name>`. Preserve established IDs for existing packages
  and suites, such as `Compono`. Check NuGet.org for ID availability or
  ownership before committing to a new ID.
- Use a root solution, normally `.slnx` for a new repo, and put package projects
  under `src/`, tests under `test/` or `tests/`, and runnable examples under
  `samples/` or `examples/`. Add a root `README.md`, `LICENSE`,
  `.editorconfig`, and `.gitignore` for build outputs and local files.
  Document repo-specific build and format commands in
  `AGENTS.md` when useful.
- Put shared MSBuild settings and package metadata in `Directory.Build.props`
  when several projects use them. Keep package-specific metadata in the
  publishable project. Use `Directory.Packages.props` when managing dependency
  versions across projects.
- Use `global.json` to coordinate the SDK and test runner with CI. SDK version,
  package target frameworks, and a generator's compiler floor are independent
  choices. A generator often targets `netstandard2.0` for its compiler host.
  Keep a deliberate Roslyn version constraint when a higher dependency would
  prevent the packaged analyzer from loading on supported SDKs.
- Follow the repo's formatter and runner. Several current repos use xUnit v3
  with Microsoft Testing Platform. Match the xUnit packages to the selected MTP
  generation and match the workflow setting to the runner in `global.json`.
  Apply nullable reference types and the repo's warning policy.

## Start a new library

Use the package ID for the solution and library project. This example uses
`LayeredCraft.Example` and targets `net10.0`. Choose the actual target from the
brief and its consumers, and use an installed .NET 10 or later SDK that
supports all selected targets.

```sh
dotnet new sln -n LayeredCraft.Example --format slnx
dotnet new classlib -n LayeredCraft.Example -o src/LayeredCraft.Example -f net10.0 --no-restore
```

Create `tests/LayeredCraft.Example.Tests/LayeredCraft.Example.Tests.csproj`.
Use the organization's xUnit v3 and Microsoft Testing Platform v2 setup for new
libraries using the shared publishing workflows. Put
`"test": { "runner": "Microsoft.Testing.Platform" }` in the root
`global.json` beside the selected SDK version and roll-forward policy. The
version below is an example from
[Lambda Web Functions](https://github.com/LayeredCraft/lambda-web-functions-dotnet/blob/main/Directory.Packages.props).
Use the dependency versions and management style of the comparable repo.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <OutputType>Exe</OutputType>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="xunit.v3.mtp-v2" Version="4.0.2" />
    <ProjectReference Include="../../src/LayeredCraft.Example/LayeredCraft.Example.csproj" />
  </ItemGroup>
</Project>
```

```sh
dotnet sln LayeredCraft.Example.slnx add \
  src/LayeredCraft.Example/LayeredCraft.Example.csproj \
  tests/LayeredCraft.Example.Tests/LayeredCraft.Example.Tests.csproj
```

Replace the generated class with the first requested public operation. Keep
the test's project reference for quick development. Use a separate package
consumer for the final smoke test.

## Prepare the NuGet package

- Make the `PackageId`, description, authors, tags, repository URL, project URL,
  and license explicit in the evaluated project. MIT is common in the
  organization. Match the actual repository license. Include the README in
  the package and an icon if the project supplies one.
- Preserve the repo's Source Link and symbol policy. Check the emitted package
  for metadata, dependencies, and intended assemblies or analyzer assets.
  Mark tests, samples, and internal helper projects `IsPackable=false`.
- Show the exact install command, a runnable usage example, the supported
  frameworks and SDKs, and any compatibility promises in the README.
- Give each publishable project a reason to be installed independently. For a
  suite, document each ID, what it owns, what it depends on, and whether its
  version moves with the rest of the suite.

Set package metadata in the library project or shared props. This example
assumes the project is two levels below the repository root.

```xml
<PropertyGroup>
  <IsPackable>true</IsPackable>
  <PackageId>LayeredCraft.Example</PackageId>
  <Authors>LayeredCraft</Authors>
  <Description>Describe the operation the library provides.</Description>
  <PackageTags>example</PackageTags>
  <PackageLicenseExpression>MIT</PackageLicenseExpression>
  <RepositoryUrl>https://github.com/LayeredCraft/example</RepositoryUrl>
  <RepositoryType>git</RepositoryType>
  <PackageProjectUrl>$(RepositoryUrl)</PackageProjectUrl>
  <PackageReadmeFile>README.md</PackageReadmeFile>
  <PublishRepositoryUrl>true</PublishRepositoryUrl>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
<ItemGroup>
  <None Include="../../README.md" Pack="true" PackagePath="/" />
</ItemGroup>
```

Enable `EnablePackageValidation` for a multi-target runtime library to check
that compatible frameworks expose compatible APIs. When updating a stable
package, use `PackageValidationBaselineVersion` to compare with a prior stable
release. For a generator, inspect `analyzers/dotnet/cs/` in the package and
check that runtime dependencies land in the appropriate package and asset
groups. [SDK package validation](https://learn.microsoft.com/en-us/dotnet/fundamentals/package-validation/overview)
