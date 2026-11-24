# Minimal API endpoints

**Summary.** Use ASP.NET Core Minimal APIs for HTTP. Invoke the application operation and match its outcome inline. Return the projected DTO when it matches the public contract.

## Contents

- [Keep HTTP at the endpoint](#keep-http-at-the-endpoint)
- [Place validation and authorization](#place-validation-and-authorization)
- [Map HTTP responses consistently](#map-http-responses-consistently)
- [Example of a small read endpoint](#example-of-a-small-read-endpoint)
- [Example of a write endpoint](#example-of-a-write-endpoint)
- [Register and evolve the operation](#register-and-evolve-the-operation)
- [Add a route to an existing app](#add-a-route-to-an-existing-app)
- [Verify HTTP behavior](#verify-http-behavior)

## Keep HTTP at the endpoint

The endpoint owns routing, binding, input shape validation, transport authorization, and the HTTP response. It calls the Application handler directly in new designs. Pass actor data when the use case needs to enforce resource authorization. Keep HTTP types out of the handler.

Use `MapGet`, `MapPost`, and the other Minimal API route methods for new endpoints. Keep existing authorization, validation, and transaction behavior when introducing or migrating a route. Apply required policies to the new route or route group explicitly. Bind IDs as parameters by default so a malformed value returns 400. Use a route constraint such as `:guid` to disambiguate routes or preserve an existing contract that returns 404 when the route does not match.

## Place validation and authorization

| Owner                   | Checks                                                                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Minimal API or listener | Parse the input, validate its transport shape, establish a trusted caller, and apply the entry point's access policy.                   |
| Application             | Check permission for the specific operation and resource using the trusted caller and tenant. Apply these checks for every entry point. |
| Domain                  | Enforce rules about the object's state and allowed transitions.                                                                         |

For cancellation, bind a shipment ID and require the Shipping write policy in HTTP. Get the user and tenant from authenticated identity. In a listener, establish the caller and tenant from the trusted integration or service identity and its authorization rules. Pass that information explicitly when calling Application. Request fields can identify a requested resource. They cannot establish the caller's identity or authority.

Scope the shipment lookup to the tenant the caller is authorized to access. Return the same missing case for an absent shipment and a shipment the caller must not discover. Use a forbidden case if the caller can see the shipment and lacks permission to cancel it. Once authorized, call the domain cancellation rule. An already-shipped shipment is a domain outcome. [ASP.NET Core resource-based authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resource-based).

## Map HTTP responses consistently

Keep an existing endpoint's response contract. For a new API without a local convention, use the following defaults. Match the operation's outcome inline with `TypedResults`. Use a typed union of HTTP results when it makes the response contract clear.

| Outcome                                    | Default response                                                                                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Read succeeds                              | `200` with the projected DTO as the body.                                                                                             |
| Creates an addressable resource            | `201` with its location and a DTO when the client needs its representation.                                                           |
| Accepts work for later completion          | `202` after a durable handoff to a process that owns completion. Include a status location when clients can poll it.                  |
| Command succeeds with no response data     | `204`.                                                                                                                                |
| Malformed input or field validation fails  | `400`. Use validation problem details when returning field errors.                                                                    |
| Authentication or access fails             | Let the authentication and authorization middleware handle `401` or route-level `403`. Map a visible resource denial to `403` inline. |
| Resource is missing or must stay hidden    | `404` without a body by default.                                                                                                      |
| Valid request conflicts with current state | `409`. Include problem details when the client needs a stable reason or next action.                                                  |
| Unexpected failure                         | Use the host's exception handling and safe error response.                                                                            |

For example, this cancellation can return a bare `409` when the client just refreshes after contention. If the client must distinguish contention from a shipment that already left, give each conflict a stable problem type under the API's error convention. Keep the response mapping in the endpoint. [ASP.NET Core Minimal API responses](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/responses).

## Example of a small read endpoint

For a tiny, single-entry operation, keep the endpoint, handler, and local types in one file if it reads clearly. For example, `Shipping/GetShipment.cs` can contain:

```csharp
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;

public static class GetShipment
{
    public sealed record ShipmentDto(Guid Id, string TrackingNumber);
    public sealed record ShipmentNotFound(Guid Id);
    public union Outcome(ShipmentDto, ShipmentNotFound);

    public static void Map(IEndpointRouteBuilder endpoints)
    {
        endpoints.MapGet("/shipments/{id}", HandleHttpAsync);
    }

    private static async Task<Results<Ok<ShipmentDto>, NotFound>> HandleHttpAsync(
        Guid id, Handler handler, CancellationToken ct)
    {
        var outcome = await handler.HandleAsync(id, ct);

        return outcome switch
        {
            ShipmentDto dto => TypedResults.Ok(dto),
            ShipmentNotFound => TypedResults.NotFound()
        };
    }

    public sealed class Handler(ShippingDbContext db)
    {
        public async Task<Outcome> HandleAsync(Guid id, CancellationToken ct)
        {
            var shipment = await db.Shipments
                .Where(shipment => shipment.Id == id)
                .Select(shipment => new ShipmentDto(shipment.Id, shipment.TrackingNumber))
                .SingleOrDefaultAsync(ct);

            if (shipment is null)
                return new ShipmentNotFound(id);

            return shipment;
        }
    }
}
```

## Example of a write endpoint

When the operation has a second entry point, put each adapter in its own file. For example:

```text
Api/Shipping/CancelShipmentEndpoint.cs
Listener/Shipping/CancelShipmentListener.cs
Application/Shipping/CancelShipment.cs
Application/Shipping/IShippingDbContext.cs
Domain/Shipping/Shipment.cs
Infrastructure/Shipping/ShippingDbContext.cs
Infrastructure/Shipping/ShipmentMapping.cs
Tests/Shipping/CancelShipmentTests.cs
```

In this new design the handler returns initialized cases from its outcome union. Only the endpoint selects HTTP statuses.

```csharp
using Microsoft.AspNetCore.Http.HttpResults;

public static class CancelShipmentEndpoint
{
    public static void Map(IEndpointRouteBuilder endpoints)
    {
        endpoints.MapPost("/shipments/{id}/cancel", HandleAsync)
            .RequireAuthorization("ShippingWrite");
    }

    private static async Task<Results<NoContent, NotFound, Conflict>> HandleAsync(
        Guid id, CancelShipment handler, CancellationToken ct)
    {
        var outcome = await handler.HandleAsync(id, ct);

        return outcome switch
        {
            Cancelled => TypedResults.NoContent(),
            ShipmentMissing => TypedResults.NotFound(),
            AlreadyShipped or CancellationConflict => TypedResults.Conflict()
        };
    }
}
```

The host registers the `ShippingWrite` policy. The shared handler owns querying and saving through the context. Put the records and union beside the operation while they are local to it.

```csharp
using Microsoft.EntityFrameworkCore;

public sealed record Cancelled;
public sealed record ShipmentMissing(Guid Id);
public sealed record AlreadyShipped(Guid Id);
public sealed record CancellationConflict(Guid Id);
public union CancelShipmentOutcome(Cancelled, ShipmentMissing, AlreadyShipped, CancellationConflict);

public sealed class CancelShipment(IShippingDbContext db)
{
    public async Task<CancelShipmentOutcome> HandleAsync(Guid id, CancellationToken ct)
    {
        var shipment = await db.Shipments.AsTracking().SingleOrDefaultAsync(x => x.Id == id, ct);
        if (shipment is null)
            return new ShipmentMissing(id);

        if (!shipment.TryCancel())
            return new AlreadyShipped(id);

        try
        {
            await db.SaveChangesAsync(ct);
            return new Cancelled();
        }
        catch (DbUpdateConcurrencyException ex)
            when (ex.Entries.Count == 1 && ReferenceEquals(ex.Entries[0].Entity, shipment))
        {
            return new CancellationConflict(id);
        }
    }
}
```

The domain owns both transitions. Configure `Shipment.Version` in Infrastructure so dispatch and cancellation check the original version when saving. Apply a migration when adding the token to an existing schema. After a conflict, finish the scope without another save. A retry starts in a fresh context and evaluates the state again. See [context registration](../architecture/persistence-and-writes.md#register-a-shared-scoped-context), [concurrent writes](../architecture/persistence-and-writes.md#protect-rules-against-concurrent-writes), and [race tests](../implementation/testing.md#test-a-write-race).

```csharp
public Guid Version { get; private set; } = Guid.NewGuid();

public bool TryCancel()
{
    if (Status is ShipmentStatus.Dispatched or ShipmentStatus.Delivered)
        return false;

    if (Status == ShipmentStatus.Cancelled)
        return true;

    Status = ShipmentStatus.Cancelled;
    Version = Guid.NewGuid();
    return true;
}

public bool TryDispatch()
{
    if (Status is not ShipmentStatus.Pending)
        return false;

    Status = ShipmentStatus.Dispatched;
    Version = Guid.NewGuid();
    return true;
}
```

```csharp
modelBuilder.Entity<Shipment>().Property(x => x.Version).IsConcurrencyToken();
```

## Register and evolve the operation

Register the scoped context and `GetShipment.Handler` at startup and call `GetShipment.Map(app)`. Group registrations and route mappings by business area when the host starts accumulating them. Keep the route implementation with the operation. See [registration by project](../implementation/configuration-and-options.md#registration-by-project) for explicit DI in a layered app.

```csharp
// Program.cs, after registering the context and the ShippingWrite policy
builder.Services.AddScoped<GetShipment.Handler>();
builder.Services.AddScoped<CancelShipment>();

var app = builder.Build();
GetShipment.Map(app);
CancelShipmentEndpoint.Map(app);
app.Run();
```

Project directly to a serializable DTO. Return it as the response body when it is the intended contract. Use a separate wire shape when the public contract needs different fields or an independent lifetime. Keep domain objects and tracked entities out of the response body.

When another entry point needs the handler, give each adapter its own file and put the handler and its outcomes in an Application folder or project. The new adapter maps its own wire input and result. HTTP and message contracts can evolve separately.

## Add a route to an existing app

Add a Minimal API route even when other endpoints use controllers. MVC filters only run in MVC. Identify which authorization and request checks the old filter actually performs. Reuse that logic in an authorization requirement, service, or endpoint filter as appropriate. Apply the equivalent authentication schemes and policy to the route.

If the existing application operation depends on a validation or transaction pipeline, call its established entry point from the new adapter. For example, an app that already uses MediatR can keep this invocation inside its Minimal API route handler and match the returned outcome inline:

```csharp
var outcome = await sender.Send(new CancelShipmentCommand(id), ct);
```

Use the existing pipeline as the transaction owner when it already holds that responsibility. Register the operation and its required checks in each host. Pass a trusted actor or tenant from the adapter when required so application checks work outside HTTP. Cover unauthenticated and forbidden requests, invalid input, and rollback on a failed write before replacing a route.

## Verify HTTP behavior

Match expected outcomes inline next to the handler call. Use the host's error handling for unexpected failures and avoid returning technical details to clients. Use a component test for the route, authorization, and response contract. Use the production database engine for the query when practical. [ASP.NET Core Minimal API responses](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/responses?view=aspnetcore-10.0).
