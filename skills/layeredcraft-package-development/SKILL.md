---
name: layeredcraft-package-development
description: >-
  Create, package, and prepare to release .NET libraries for the LayeredCraft
  GitHub organization. Use for a new LayeredCraft NuGet package or package repo,
  class library, source generator, analyzer, framework integration, or
  multi-package suite. Also use for adding a publishable project to an existing
  LayeredCraft repo, setting up its GitHub Actions with LayeredCraft/devops-templates,
  or preparing its first preview or stable release. Ordinary .NET app development
  and unrelated package changes are outside this skill.
---

# LayeredCraft package development

1. Read the target repo's instructions and build files. Turn the brief into the
   package ID, consumers, supported targets, and first public operation. Check
   nearby LayeredCraft libraries for reusable code and conventions. Ask when a
   missing answer would materially change the public API or supported consumers.
   Use the brief and repo precedent for routine choices and proceed.
2. Follow [repository standards](references/repository-standards.md). For a
   new repo, create the solution, library, test project, README, and package
   metadata using the starter configuration. In an existing repo, extend its
   solution and build files. Choose the CI SDK separately from the library's
   target frameworks.
3. Implement the requested library behavior through its public API. Add tests
   for the main use and meaningful failure cases. Put a runnable usage example
   and the exact install command in the README. Use
   `dotnet-aot-library-validation` when the package promises trimming or
   Native AOT support.
4. Run the formatter, Release build, and tests. Then [pack and run a consumer](references/consumer-validation.md)
   against the exact local package version. Fix build, test, package, and
   consumer failures before calling the library ready.
5. Wire the standard [GitHub Actions callers](references/github-actions.md)
   and Release Drafter configuration for a new package repo. In an existing
   repo, include the new project in the solution the workflows already use.
   Confirm the workflow commands use
   the same SDK, test runner, and solution as local validation. Set up or
   publish a remote release when the brief includes it.

Deliver the working source, tests, installable package, README, and workflow
files. Report package IDs and supported targets, the shared workflow revision,
and the checks actually run. Call out any pending owner-side publishing setup.
