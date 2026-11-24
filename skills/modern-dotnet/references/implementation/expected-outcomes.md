# Expected outcomes

**Summary.** Return expected states as union cases, use a generic Result for data or a typed error, and handle outcomes inline at the entry point.

## Contents

- [Choose the outcome shape](#choose-the-outcome-shape)
- [Match outcomes at the entry point](#match-outcomes-at-the-entry-point)
- [Compose results](#compose-results)
- [Check exhaustiveness](#check-exhaustiveness)

## Choose the outcome shape

Use C# 15 unions to model the outcomes the caller can act on. Name cases in business terms. An absent shipment is an expected state. An endpoint can map it to HTTP 404 without treating absence as a failure inside the application.

| Shape                                                           | Use it for                                              |
| --------------------------------------------------------------- | ------------------------------------------------------- |
| A plain value                                                   | One meaningful outcome                                  |
| [Option or Maybe](functional-helpers.md#model-ordinary-absence) | A value or ordinary absence                             |
| Generic Result                                                  | Data or a typed error                                   |
| An operation-specific union                                     | Named states such as found, missing, or already shipped |

A `Try` method can express an attempted operation with an expected outcome. Prefer an explicit case when callers need to know which state occurred. Put domain rules on the type that owns the state. Use property, type, and tuple patterns to express rules when they are easy to read.

## Match outcomes at the entry point

Match outcomes inline at the entry point. An HTTP endpoint chooses the status and serializes the intended DTO. A listener chooses how to settle the delivery. A CLI chooses output and an exit code. Keep transport SDK types out of the handler result.

```csharp
public sealed record ShipmentDto(Guid Id, string TrackingNumber);
public sealed record ShipmentNotFound(Guid Id);

public union GetShipmentOutcome(ShipmentDto, ShipmentNotFound);
```

## Compose results

Use distinct success and failure cases in a reusable `Result<T, TError>`. This keeps cases distinct even when both payload types are the same or one is assignable to the other. Reuse the application's existing helpers. See [Functional helpers](functional-helpers.md) for C# 15 implementations of `Map`, `Bind`, and `Tap`.

## Check exhaustiveness

Match every case. Omit a fallback when the handler always returns an initialized case and the contents are non-null. Account for `null` if nullable cases or default-initialized unions can reach the switch. Reserve exceptions for unexpected failures. [C# union exhaustiveness](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/union#union-exhaustiveness).
