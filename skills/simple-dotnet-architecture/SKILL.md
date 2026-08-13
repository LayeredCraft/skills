---
name: simple-dotnet-architecture
description: Design, implement, review, or simplify .NET 8+ Minimal APIs, background workers, and message consumers using pragmatic feature slices and only the complexity the application needs. Use when choosing boundaries between delivery code, operations, EF Core, services, clients, workers, or consumers; restructuring a .NET application; or deciding whether repositories, CQRS, MediatR, Clean Architecture, modules, or distributed-service boundaries are justified.
---

# Simple .NET Architecture

Choose the smallest architecture that makes the application's operations clear. Start with a feature slice, direct dependencies, and local contracts. Do not add Clean Architecture, CQRS/MediatR, repositories, or interfaces by default.

## Select the delivery shape

Identify the application's entry point, then load only its reference:

| Shape | Delivery edge | Load |
| --- | --- | --- |
| HTTP API | ASP.NET Core Minimal API endpoint | [API feature slices](references/api-feature-slices.md) |
| Background worker | `BackgroundService`, scheduled job, or hosted service | [Workers](references/workers.md) |
| Message consumer | Queue, topic, or stream consumer | [Consumers](references/consumers.md) |

The delivery edge owns its protocol: HTTP binding/status codes, job scheduling/lifecycle, or message acknowledgement/metadata. The operation it calls owns the use case and does not depend on the delivery framework. Share an operation between edges only when they truly perform the same work.

When deciding whether to extract a service, client, or model—and where it belongs—load [Shared code and capabilities](references/shared-code.md).

## Choose the lowest suitable level

| Level | Use it when | Add |
| --- | --- | --- |
| 1. Feature slice | Typical CRUD or modest operation | Delivery edge, operation handler, scoped `DbContext` |
| 2. Shared capability | Several operations use real logic or an integration | Named service or typed client |
| 3. Complex workflow | Transactional state, policies, side effects, or retries matter | Domain types, explicit outcomes, idempotency/outbox/transaction where needed |
| 4. Module boundary | A feature has clear ownership, a public internal contract, or multiple delivery edges | Module boundary; separate projects only if they protect it |
| 5. Distributed boundary | Independent deployment and data ownership are required | A service contract, integration events, separate data, operational resilience |

Move up only in the affected feature. For each proposed layer, name the concrete problem it solves and the first operation that needs it. If that answer is not specific, remain at the current level.

## Universal rules

- Inject `DbContext` directly into an operation handler for ordinary EF Core work. Do not wrap routine queries or `SaveChangesAsync` in repositories.
- Add a service for a reusable capability or cohesive policy, not as a pass-through for an entity.
- Register operation handlers as concrete types. Do not create handler interfaces or generic handler abstractions unless multiple implementations must be selected at runtime or a proven module boundary requires the contract; testing alone is not a reason.
- Keep transport contracts local to the delivery edge. Do not expose tracked EF entities or reuse a transport contract as application data merely because fields match.
- Keep request-shape validation at the edge; enforce business invariants in the operation, domain type, or service.
- Make write boundaries and external side effects explicit. Add idempotency, an outbox, retries, or a transaction only when the operation's guarantees require them.
- Put cross-cutting protocol concerns at the edge. Do not create a hidden application pipeline.

## Review and evolve

Inspect the target framework, entry points, feature ownership, data store, delivery guarantees, integrations, and tests before recommending change. Preserve coherent local conventions.

State the selected shape and complexity level, the evidence for them, and the smallest next change. Recommend simplification before a rewrite.
