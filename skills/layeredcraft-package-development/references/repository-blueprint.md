# Repository blueprint

Use nearest current LayeredCraft library as template. `lambda-web-functions-dotnet`
shows lean v11 workflows; `compono` shows multi-package, package-validation, AOT,
and consumer-proof patterns; `dynamo-mapper`/`decoweaver` show generator layouts.
Do not copy legacy `permissions: write-all` callers into new repositories.

## Default runtime-library layout

```text
<repo>/
├── .config/dotnet-tools.json             # only when local tools are needed
├── .github/
│   ├── workflows/
│   │   ├── pr-build.yaml
│   │   ├── pr-title-check.yaml
│   │   ├── release-drafter.yaml
│   │   ├── publish-preview.yaml
│   │   └── publish-release.yaml
│   ├── dependabot.yml
│   └── release-drafter.yml
├── src/
│   └── LayeredCraft.<Package>/
│       └── LayeredCraft.<Package>.csproj
├── tests/
│   └── LayeredCraft.<Package>.Tests/
├── samples/
│   └── LayeredCraft.<Package>.Sample/    # real public-API consumer
├── Directory.Build.props
├── Directory.Build.targets                # only for genuine shared late props
├── Directory.Packages.props               # only when central package management helps
├── global.json
├── <repo>.slnx
├── README.md
├── LICENSE
├── .editorconfig
└── AGENTS.md
```

Source generator shape:

```text
src/
├── LayeredCraft.<Package>/                # package facade/runtime, if needed
└── LayeredCraft.<Package>.Generators/     # netstandard Roslyn host project
tests/
├── LayeredCraft.<Package>.Generators.Tests/
└── LayeredCraft.<Package>.PackageSmokeTest/
```

Multi-package shape:

```text
src/
├── LayeredCraft.<Package>/
├── LayeredCraft.<Package>.<IntegrationA>/
└── LayeredCraft.<Package>.<IntegrationB>/
tests/
├── LayeredCraft.<Package>.Tests/
├── LayeredCraft.<Package>.<IntegrationA>.Tests/
└── LayeredCraft.<Package>.SampleTests/    # consumes packed packages
```

Keep sample/test projects `IsPackable=false`. One publishable project must have
one intentional `PackageId`; do not accidentally pack test helpers or generator
implementation projects.

## Baseline project metadata

Set shared metadata in `Directory.Build.props`, then override only where package
needs it:

```xml
<Project>
  <PropertyGroup>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
    <Authors>LayeredCraft</Authors>
    <Company>LayeredCraft</Company>
    <RepositoryUrl>https://github.com/LayeredCraft/<repo></RepositoryUrl>
    <RepositoryType>git</RepositoryType>
    <PackageProjectUrl>https://github.com/LayeredCraft/<repo></PackageProjectUrl>
    <PackageRequireLicenseAcceptance>false</PackageRequireLicenseAcceptance>
    <PublishRepositoryUrl>true</PublishRepositoryUrl>
    <EmbedUntrackedSources>true</EmbedUntrackedSources>
    <IncludeSymbols>true</IncludeSymbols>
    <SymbolPackageFormat>snupkg</SymbolPackageFormat>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.SourceLink.GitHub">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime;build;native;contentfiles;analyzers;buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>
</Project>
```

In each publishable `.csproj`, make package identity visible:

```xml
<PropertyGroup>
  <PackageId>LayeredCraft.<Package></PackageId>
  <Description>...</Description>
  <PackageTags>...</PackageTags>
  <PackageReadmeFile>README.md</PackageReadmeFile>
  <PackageIcon>icon.png</PackageIcon> <!-- only when icon exists -->
</PropertyGroup>
<ItemGroup>
  <None Include="..\..\README.md" Pack="true" PackagePath="" Visible="false" />
  <None Include="..\..\icon.png" Pack="true" PackagePath="" Visible="false" />
</ItemGroup>
```

Do not suppress package analysis as default. Fix package metadata warnings or
make narrow documented exception after inspecting emitted package.

## First vertical slice

Before adding integrations, extensions, or abstractions:

1. Define one public operation with XML documentation.
2. Add focused unit test for success and meaningful failure boundary.
3. Add sample that uses public API only.
4. Pack project.
5. Run sample/test from packed local feed, not project reference.
6. Put same minimal usage in README; compile or execute it where practical.

## AOT and compatibility

Only promise Native AOT/trimming after evidence. For supported `net8.0+` targets,
use conditional `IsAotCompatible` and validation app. Load
`dotnet-aot-library-validation`; do not use this blueprint as substitute.

For multi-target libraries, select target framework floor from actual consumers.
`netstandard2.0` adds support cost; source generators commonly target it for
Roslyn host compatibility. State support matrix in README.
