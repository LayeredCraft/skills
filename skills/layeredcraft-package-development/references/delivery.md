# First PR and first release

## First PR

First PR proves repository can ship one coherent public slice.

1. Branch from current `main`; follow repository git workflow.
2. Implement one documented public operation plus focused tests.
3. Add executable sample or sample tests using public API.
4. Pack and inspect package artifacts.
5. Dogfood from local feed; save exact evidence.
6. Run build, tests, formatter, and package-specific proof.
7. Open non-draft PR with semantic title, normally:

   ```text
   feat(<scope>): add <package>
   ```

8. Confirm title check, PR build, extra gates, and Release Drafter autolabel.
9. Obtain required review, squash merge, then confirm draft release and preview
   workflow behavior.

First PR is incomplete when package builds only through project references.

## Preview verification

After merge to `main`:

1. Inspect preview workflow run; confirm version follows current Release Drafter
   policy.
2. Download preview package or verify configured publish destination.
3. Restore clean consumer against preview package.
4. Execute same real behavior proven in local dogfood.
5. Confirm draft GitHub Release title, tag, labels, and notes describe actual
   package change.

Current shared workflow documentation and implementation can drift. Verify chosen
workflow tag's real inputs and behavior before relying on version strategy.

## First-release preflight

Before publishing GitHub Release, confirm all:

- [ ] Package ID is owned/available on NuGet.org.
- [ ] NuGet Trusted Publishing trusts exact LayeredCraft repo and release workflow.
- [ ] Shared workflow expected `NUGET_USER` secret exists.
- [ ] Release Drafter version/tag matches intended initial policy.
- [ ] README install command and minimum example are correct.
- [ ] `.nupkg` contains runtime/analyzer/build assets, XML docs, readme, icon as configured.
- [ ] Symbols package exists when configured.
- [ ] Local-feed consumer proof passed on current merged commit.
- [ ] AOT consumer proof passed if claim made.
- [ ] No secrets or local feeds remain in committed files.

## Publish and verify

1. Review Release Drafter draft; edit notes only for accuracy.
2. Publish GitHub Release with resolved tag. Do not hand-create alternate tag
   unless policy deliberately changes.
3. Watch release build/push workflow through completion.
4. Verify package appears on NuGet.org: version, README, license, repository,
   dependencies, symbols, and deprecation state.
5. Create clean temporary consumer using NuGet.org only; restore/build/test/run.
6. Record release URL/version and any deferred follow-up.

If publishing fails after GitHub Release publishes, stop. Diagnose workflow,
NuGet trusted-publishing binding, or package collision before retrying. Do not
rotate credentials into repository as workaround.

## Post-release

- Confirm new Release Drafter draft starts from released tag.
- Confirm Dependabot and required checks still run.
- File issues for adoption, docs, compatibility, or telemetry work outside first
  vertical slice.
- Do not call package stable merely because first version reached NuGet; stability
  follows declared support and compatibility policy.
