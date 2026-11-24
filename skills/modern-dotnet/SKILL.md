---
name: modern-dotnet
description: >-
  Use whenever asked to write, add, or change code in a C#/.NET application,
  even for a single new class, method, endpoint, handler, or business rule.
  Also use when creating a new application, feature, service, worker, listener,
  Lambda, or CLI, or when designing, reviewing, or changing .NET architecture,
  layering, project structure, folders, or code placement. Covers C# 15+
  application patterns, ASP.NET Core Minimal APIs, EF Core, domain modeling,
  typed outcomes, dependency injection, configuration, and integration and
  component tests. The request or repository context can
  establish that the work is .NET. Architecture terminology is optional.
  For standalone syntax explanations use language guidance.
  For class-library trimming or Native AOT compatibility use
  dotnet-aot-library-validation.
---

# Modern .NET

Target C# 15 or later. Check the SDK and deployment runtime. If the project is pinned to an older version, recommend upgrading. Read nearby code and tests, then use the simplest design that makes the operation and its owner clear.

## Apply the skill

1. For any application code change or architecture decision, start with [Code placement](references/architecture/code-placement.md). Identify the business area and the type or file that should own the change.
2. Open only the additional references that match the work. Start with their summaries and contents, then jump to the sections you need.
3. Use ASP.NET Core Minimal APIs for new HTTP endpoints. Call handlers directly in new designs. For scoped changes, follow established names and preserve the existing public contract, authorization, validation, and transaction behavior. Name the concrete reason for each new boundary.

## References

| Task                                                | Reference                                                                           |
| --------------------------------------------------- | ----------------------------------------------------------------------------------- |
| EF Core, CQRS, inline SQL, commits, events          | [Persistence and writes](references/architecture/persistence-and-writes.md)         |
| Unions, Result, Option, pattern matching            | [Expected outcomes](references/implementation/expected-outcomes.md)                 |
| Implementing or composing Map, Bind, and Tap        | [Functional helpers](references/implementation/functional-helpers.md)               |
| HTTP and Minimal APIs                               | [HTTP endpoints](references/delivery/api-feature-slices.md)                         |
| Worker, scheduled job, or CLI                       | [Workers and jobs](references/delivery/workers.md)                                  |
| Queue, stream, event listener, or Lambda            | [Event listeners and Lambda](references/delivery/consumers.md)                      |
| Startup, dependency injection, settings, or options | [Configuration and options](references/implementation/configuration-and-options.md) |
| Test design or shared fixtures                      | [Integration and component tests](references/implementation/testing.md)             |

Every reference, including every new page, must start with a brief summary and a linked table of contents directly after its title, before the detailed guidance. Keep the contents in sync with the page's sections.
