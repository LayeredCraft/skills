# Package types

Choose one primary package type. Use existing LayeredCraft packages as precedent;
do not mix shapes because future ideas might need them.

## Runtime library

Examples: `structured-logging`, `compact-json-formatter`,
`dynamodb-distributed-lock`.

- Keep public API small and documented.
- Test public behavior, cancellation/error boundaries, and dependency interactions.
- Include executable sample or sample tests using package public API.
- Pack and run consumer against local feed.

## ASP.NET or Lambda extension

Examples: `lambda-aspnetcore-hosting-extensions`,
`lambda-web-functions-dotnet`.

- Expose configuration extensions only after real setting exists.
- Add host-level integration test, not only extension-method unit tests.
- Sample boots host and hits health/representative endpoint.
- Preserve trimming/AOT behavior when advertised; publish/run real host consumer.

## Source generator or analyzer

Examples: `decoweaver`, `dynamo-mapper`, `optimized-enums`.

- Generator host normally targets `netstandard2.0`; verify supported compiler/SDK
  floor before choosing Roslyn dependencies.
- Keep generator implementation separate from shipped package facade/runtime when
  that makes package boundaries clear.
- Add diagnostic and generated-source tests. Snapshot tests supplement behavioral
  assertions; they do not replace consumer compilation.
- Pack generated/analyzer assets, then build and execute a separate consumer.
- Inspect `.nupkg` analyzer/build assets explicitly. A project-reference test can
  hide broken package layout.

## Framework integration package

Examples: Compono integrations for xUnit, NUnit, TUnit, logging, HTTP, options.

- Core package must not depend on optional integration package.
- Integration owns framework-specific public surface and compatibility matrix.
- Test supported upstream versions/runners where practical.
- Consumer proof uses real framework runner or host, not hand-constructed internals.

## Multi-package suite

Examples: `compono`, `aws-secrets-manager-provider`.

Before creating second publishable package, write package graph:

| Package     | Owns                        | Depends on                | Consumer proof   |
| ----------- | --------------------------- | ------------------------- | ---------------- |
| Core        | stable abstractions/runtime | BCL only if possible      | core sample      |
| Integration | adapter/extensions          | Core + upstream framework | framework sample |

Rules:

- Each package owns a coherent public boundary.
- Avoid cycles and accidental transitive dependency coupling.
- Pack every publishable package in CI.
- Dogfood exact package set each consumer restores.
- Give release/versioning policy for every package before first release.

## Admission questions

Answer before adding package/integration:

1. Does distinct install boundary solve real consumer need?
2. Can core remain independent from optional framework?
3. What exact consumer proves value?
4. Which framework/SDK versions are supported?
5. Does addition change AOT, trimming, package size, or dependency policy?
6. Can first release ship single vertical slice instead?
