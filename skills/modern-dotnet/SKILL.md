---
name: modern-dotnet
description: >-
  Implement, review, or modernize .NET 8+ application, worker, and library code with
  current idioms, pragmatic delivery shapes, and only the complexity the operations
  require. Use for any .NET or ASP.NET Core work: where code belongs, how delivery
  and configuration are shaped, and whether a heavier pattern or layer is justified.
  Do not use for class-library Native AOT or trim compatibility work.
---

# Modern .NET

The organization's default answer to "how should this be built?" in .NET: the smallest architecture that makes the operations clear, with a layer added only for a concrete problem you can name.

## Routing

This file is the only one loaded automatically. Read the one reference that matches the task, then apply the rules below and stop. Paths here are relative to this skill's directory.

| The task is                                                | Read                                                                                |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| An HTTP endpoint or Minimal API                            | [API feature slices](references/delivery/api-feature-slices.md)                     |
| A background worker, scheduled job, or hosted service      | [Workers](references/delivery/workers.md)                                           |
| A queue, topic, or stream consumer                         | [Consumers](references/delivery/consumers.md)                                       |
| Where a service, client, model, or helper belongs          | [Code placement](references/architecture/code-placement.md)                         |
| Configuration, options, validation, or startup composition | [Configuration and options](references/implementation/configuration-and-options.md) |

The folders group the references by kind, not by step. For structure — whether to add a layer, module, project, or service boundary — read **How much structure to add** below; to review or simplify what already exists, read **Reviewing and evolving**. If a task spans rows, load both and let the flow decide ownership. A reference rarely needs another; when it does, it links to it directly, and each ends with its own testing guidance.

## How it flows

One flow, whatever the trigger:

```text
Trigger -> Edge -> Operation -> Data and capabilities
```

The edge owns transport only: binding and status codes, schedule, acknowledgement, correlation, and coarse authorization. The operation owns one use case, its inputs and outputs, and its transaction and side-effect boundaries, and never depends on the edge's framework, so the same operation can be driven by an endpoint, a worker, or a consumer. Data is the `DbContext`, its queries, and the unit of work.

## How much structure to add

Move up only in the affected feature. For each proposed layer, name the concrete problem it solves and the first operation that needs it. If that answer is not specific, stay at the current level.

| Level                   | Use it when                                                                  | Add                                                                          |
| ----------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1. Feature slice        | Typical CRUD or modest operation                                             | Edge, operation, scoped `DbContext`                                          |
| 2. Shared capability    | Several operations use real logic or an integration                          | Named service or typed client                                                |
| 3. Complex workflow     | Transactional state, policies, side effects, or retries matter               | Domain types, explicit outcomes, idempotency/outbox/transaction where needed |
| 4. Module boundary      | A feature has clear ownership, a public internal contract, or multiple edges | Module boundary; separate projects only if they protect it                   |
| 5. Distributed boundary | Independent deployment and data ownership are required                       | Service contract, integration events, separate data, operational resilience  |

A different process, host, or queue does not by itself justify a level 4 or 5 boundary; naming, scaling, data ownership, reliability, or failure isolation does.

## Universal rules

These apply to every task, so they are here rather than in a reference.

- Inject `DbContext` directly into an operation for ordinary EF Core work. Do not wrap routine queries or `SaveChangesAsync` in repositories.
- Add a service for a reusable capability or cohesive policy, not as a pass-through for an entity.
- Register operations as concrete types. Do not create handler interfaces or generic handler abstractions unless multiple implementations must be selected at runtime or a proven module boundary requires the contract; testing alone is not a reason.
- Keep transport contracts local to the edge. Do not expose tracked EF entities or reuse a transport contract as application data merely because fields match.
- Keep request-shape validation at the edge; enforce business invariants in the operation, domain type, or service.
- Make write boundaries and external side effects explicit. Add idempotency, an outbox, retries, or a transaction only when the operation's guarantees require them.
- Put cross-cutting protocol concerns at the edge. Do not create a hidden application pipeline.

## Reviewing and evolving

Inspect the target framework, entry points, feature ownership, data store, delivery guarantees, integrations, and tests before recommending change. Preserve coherent local conventions.

State the selected shape and complexity level, the evidence for them, and the smallest next change. Recommend simplification before a rewrite.
