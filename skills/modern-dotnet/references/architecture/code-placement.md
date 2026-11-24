# Code placement

**Summary.** Organize by business area. Keep simple operations together and split files or projects when doing so clarifies ownership or enforces a dependency rule.

## Contents

- [Choose the smallest boundary that fits](#choose-the-smallest-boundary-that-fits)
- [Folder examples](#folder-examples)
- [Name files and types for the operation](#name-files-and-types-for-the-operation)
- [Give logic an owner](#give-logic-an-owner)
- [Keep domain rules on the model](#keep-domain-rules-on-the-model)

## Choose the smallest boundary that fits

Use business names such as `Shipping` and `Billing`. Reuse the business area name across layers where it helps trace an operation. Start with shallow folders. Add subfolders when the files have become hard to scan.

| Situation                                                        | Shape                                                                                               |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Very small app with a simple single-entry operation              | One project. The adapter, handler, and operation-local types can share a file.                      |
| Several adapters call the same operation, or dependencies differ | Give each adapter its own file. Put the shared handler in an Application folder or project.         |
| Substantial business behavior needs a protected core             | Separate Domain, Application, and Infrastructure. Keep the entry point in the host.                 |
| Larger monolith                                                  | Give each layer a project. Add business module boundaries when ownership or contracts warrant them. |

Start with sibling files. Give a large operation its own folder if several related files benefit from being grouped. A file represents a coherent piece of work and can contain multiple types. Keep names such as `Features`, `UseCases`, `Commands`, and `Queries` optional.

With separate projects, Application references Domain. Infrastructure implements contracts owned by Application and can reference Domain. The host wires Application and Infrastructure together. Domain stays independent of transport and persistence. If Application sits in an API project and Infrastructure must implement an API-owned interface, check the references before wiring both projects together. Keep the implementation in the host or give the contract an independent Application project when needed.

## Folder examples

A small Minimal API can keep an endpoint and its handler together. Put the domain rule in the type that owns the state.

```text
Shipping.Api/
  Program.cs
  Shipping/
    GetShipment.cs        # Minimal API, query handler, and outcome cases
    CancelShipment.cs     # Minimal API, command handler, and outcome cases
    Shipment.cs           # Domain state and transitions
    ShippingDbContext.cs
```

When an endpoint and a listener share an operation in one host, split the files while keeping them in one project.

```text
Shipping.Host/
  Program.cs
  Api/Shipping/ShipOrderEndpoint.cs
  Listener/Shipping/ShipOrderListener.cs
  Application/Shipping/ShipOrder.cs
  Domain/Shipping/Shipment.cs
  Infrastructure/Shipping/ShippingDbContext.cs
```

A larger application can enforce its boundaries with projects. Each host maps its own request and calls the same operation.

```text
Warehouse.Api/Shipping/ShipOrderEndpoint.cs
Warehouse.Listener/Shipping/ShipOrderListener.cs
Warehouse.Application/Shipping/ShipOrder.cs
Warehouse.Application/Shipping/IShippingDbContext.cs
Warehouse.Domain/Shipping/Shipment.cs
Warehouse.Domain/Inventory/Inventory.cs
Warehouse.Infrastructure/Shipping/ShippingDbContext.cs
Warehouse.Infrastructure/Inventory/InventoryMapping.cs
Warehouse.Tests/Shipping/ShipOrderTests.cs
```

See [Minimal API examples](../delivery/api-feature-slices.md) for route mapping, [registration by project](../implementation/configuration-and-options.md#registration-by-project) for DI, and [persistence examples](persistence-and-writes.md) for the context and save boundary.

## Name files and types for the operation

Keep established names when extending an existing area. Use these defaults where there is no local convention.

| Role                           | Default                                                                                                                                             | When to split                                                                                                              |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Operation and handler          | `CancelShipment.cs`. Use `CancelShipment` as the standalone handler type, or `CancelShipment.Handler` when a small file also holds the entry point. | Give the handler an Application file when another adapter calls it or the transport dependencies need to stay separate.    |
| HTTP and message adapters      | `CancelShipmentEndpoint.cs` and `CancelShipmentListener.cs` when they have their own files.                                                         | Split by entry point. Keep each adapter's wire input beside it.                                                            |
| Operation-local DTO or outcome | Keep cases named for what they mean, such as `ShipmentNotFound`, beside the operation.                                                              | Move a type to its owner when it becomes a separately versioned contract or a stable concept shared by several operations. |

For example, adding SQS to a colocated `Shipping/CancelShipment.cs` creates two adapters and moves the handler to `Application/Shipping/CancelShipment.cs`. The domain stays in its current place. Use the same business operation name across all three files.

## Give logic an owner

- Keep a handler's orchestration, inputs, and output cases with the operation. Keep runtime request shapes and parsing with the adapter. Reuse a serializable application DTO as a public contract when that is its intended shape.
- Keep feature-local helpers and shared policies near their callers. Give a reusable cross-area capability a named home such as `Pricing`. A service earns its place when it implements a cohesive policy or capability.
- Put a provider client with its integration. Use a small contract at a real dependency boundary. Avoid forwarding services, catch-all folders, and interfaces created solely to mock an operation.
- Keep a shared domain type only when the meaning and ownership are actually shared. Similar fields alone are a poor reason to share a model.

A new entry point is a file boundary first. Split deployment, data ownership, or projects when there is a separate requirement such as scaling, failure isolation, or a dependency the compiler should enforce.

## Keep domain rules on the model

Use a plain value when its meaning is clear and it has no domain rules of its own. Use an immutable value object when a concept has its own validity rules or compares by value. For example, a shipment weight is a positive quantity in kilograms.

```csharp
public sealed record ShipmentWeight
{
    private ShipmentWeight(decimal kilograms) => Kilograms = kilograms;

    public decimal Kilograms { get; }

    public static ShipmentWeight? TryCreate(decimal kilograms) =>
        kilograms > 0 ? new ShipmentWeight(kilograms) : null;
}
```

Use an entity when identity persists as state changes. Give it methods named for the allowed transitions and keep protected state behind private setters. For example, [`Inventory.TryReserve`](persistence-and-writes.md#protect-rules-against-concurrent-writes) owns the stock rule. The application handler loads inventory, asks it to reserve stock, and decides which changes commit together.

Use the same validity rules on creation and updates. Keep EF Core mapping in Infrastructure and check that loading stored data preserves the model's invariants. Check existing rows before making a new rule mandatory.
