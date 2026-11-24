# Persistence and writes

**Summary.** Use EF Core inline, project queries into DTOs, and give each write one clear commit point. Add coordination where the operation needs it.

## Contents

- [Read and write paths](#read-and-write-paths)
- [Register a shared scoped context](#register-a-shared-scoped-context)
- [Give the write one owner](#give-the-write-one-owner)
- [Protect rules against concurrent writes](#protect-rules-against-concurrent-writes)
- [Add coordination when the operation needs it](#add-coordination-when-the-operation-needs-it)
- [Own retries and external effects](#own-retries-and-external-effects)

## Read and write paths

Use EF Core by default. Keep queries and persistence steps inline in the operation. A single scoped context is the default, including in a monolith. Split it when responsibilities or ownership make it unwieldy. Decide module write ownership independently of context count.

- Use separate command and query handlers over the same EF model and store. Call them directly in new designs. Keep an existing application pipeline when it owns needed validation or transactions. Add a separately maintained read model only after agreeing on the needs of the specific query, such as performance and acceptable staleness.
- Query only the fields needed and project directly into a serializable DTO before materializing. Bound collections and use no tracking for entity loads that won't be modified. An intentional response DTO can be returned unchanged by the entry point.
- In one project, inject the concrete context when that is the simplest choice. With separate Application and Infrastructure, expose needed EF sets and save operations through an Application-owned context interface. Register the interface to resolve the same scoped context instance. Keep provider setup, mapping, and interceptors in Infrastructure. Follow the project's schema change tooling and file placement.
- Use EF Core directly for writes and read queries. Keep the context and its tracking as the unit of work. Skip generic repositories and forwarding unit-of-work wrappers.
- Use handwritten SQL for a strong, concrete reason such as a provider feature or a measured query problem. Prefer EF Core's parameterized SQL APIs. Put the multiline raw string directly in the call and pass interpolated values through an API that parameterizes them. Keep dynamic identifiers out of interpolations.

```csharp
var shipments = await db.Database.SqlQuery<ShipmentSummary>(
    $"""
    SELECT Id, TrackingNumber
    FROM Shipments
    WHERE CustomerId = {customerId}
    """).ToListAsync(ct);
```

This example assumes a relational provider and identifiers that match its schema. Project the columns the DTO needs. Check translation and SQL behavior with the target provider. [EF Core SQL queries](https://learn.microsoft.com/en-us/ef/core/querying/sql-queries).

## Register a shared scoped context

`Application/Shipping/IShippingDbContext.cs` declares the EF operations the handlers need.

```csharp
public interface IShippingDbContext
{
    DbSet<Shipment> Shipments { get; }
    DbSet<Inventory> Inventory { get; }
    Task<int> SaveChangesAsync(CancellationToken ct);
}
```

`Infrastructure/Shipping/ShippingDbContext.cs` implements it with the concrete context. Register the interface through the concrete service so both resolve to the same instance in a scope.

```csharp
services.AddDbContext<ShippingDbContext>(options => options.UseSqlServer(connectionString));
services.AddScoped<IShippingDbContext>(sp => sp.GetRequiredService<ShippingDbContext>());
```

## Give the write one owner

Load the state needed for the rule, call domain behavior, stage the writes, and save once where possible. With a transactional provider, one `SaveChangesAsync` can commit all tracked changes together. Use a database uniqueness constraint for a uniqueness invariant, and handle the losing write. Define how optimistic concurrency conflicts should surface.

If `ReserveInventory` serves its own entry point, it can call `Inventory.TryReserve` and save. If `ShipOrder` must reserve inventory and record shipment together, call the same domain method, stage the shipment, and save both together. Repeat small query and orchestration steps if needed. A standalone handler that saves can commit all pending changes on a shared context. Keep save-mode flags out of handler signatures.

Use an explicit transaction when the operation needs several database steps to commit together. With a retrying execution strategy, run the whole explicit transaction through the strategy. Keep the transaction boundary and retry safety visible. [EF Core transactions](https://learn.microsoft.com/en-us/ef/core/saving/transactions).

## Protect rules against concurrent writes

One save keeps a shipment and its inventory update atomic. Two requests can still read the same available stock and both pass the domain rule. Configure a concurrency token or use a conditional update. For example, an application-managed token can live next to the domain change it protects:

```csharp
public sealed class Inventory
{
    public Guid Id { get; init; }
    public int Available { get; private set; }
    public Guid Version { get; private set; } = Guid.NewGuid();

    public static Inventory WithStock(Guid id, int available) =>
        new() { Id = id, Available = available };

    public bool TryReserve(int quantity)
    {
        if (quantity is <= 0 || quantity > Available)
            return false;

        Available -= quantity;
        Version = Guid.NewGuid();
        return true;
    }
}
```

Configure the property in Infrastructure. A tracked EF update checks the original token when it saves. Every writer that can change the protected state needs the same guard. For handwritten SQL or `ExecuteUpdate`, check the original token in the update predicate and advance an application-managed token. If the provider supports a generated token such as SQL Server `rowversion`, it can manage the token instead.

```csharp
modelBuilder.Entity<Inventory>().Property(x => x.Version).IsConcurrencyToken();
```

On `DbUpdateConcurrencyException`, return a conflict when the caller should choose what to do. If an automatic retry is safe, reload the affected state in a fresh context, rerun the domain rule, and retry the whole operation with a bound on attempts. An unchanged retry of the stale save cannot establish whether there is enough stock. Exercise two writes against the same inventory row in an integration test. [EF Core concurrency](https://learn.microsoft.com/en-us/ef/core/saving/concurrency).

## Add coordination when the operation needs it

Start with explicit calls for straightforward follow-up. A separate handler can own an independent operation. Use an event when several parts react to the same fact and the event makes ownership and flow easier to follow. Choose when local handlers run based on which work must share the commit.

When publishing an outgoing event must survive a crash after commit, write an outbox record in the same transaction as the business change. Publish after commit. Consumers should tolerate duplicate delivery. Use the outbox where that durability is required.

## Own retries and external effects

Give each failure one retry owner.

| Failure                                                | Default owner                                                                                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| A transient database error                             | The configured EF Core execution strategy retries the database unit. Keep external effects outside that retry block.                 |
| A retryable message delivery                           | The broker integration requests bounded redelivery. Each attempt uses a fresh scope.                                                 |
| A remote call times out after it may have taken effect | The application operation reconciles the outcome through the provider. Retry only under the provider's documented safety guarantees. |

For example, a carrier might accept a booking before its response times out. Save a stable booking key and request before the call when the application must recover after a restart. On replay, look up the booking by that key. If it exists, record the existing booking. If the state is still unknown, keep the operation pending for reconciliation. Repeat the same request with the same key only when the provider guarantees it is idempotent. Keep the database transaction short and the carrier call outside any EF retry block.

When both HTTP and SQS start work that must continue after the request, use a durable handoff to a worker that owns booking retries. Return HTTP `202` or acknowledge SQS once the handoff commits. An already-recorded handoff counts as accepted on replay. If the delivery itself owns retry and there is no durable handoff, keep it pending for bounded redelivery until the work completes or reaches a terminal outcome.

Test the timeout after acceptance with a provider double. Replay the operation, verify it uses the same key, and assert that the provider has one booking. [EF Core connection resiliency](https://learn.microsoft.com/en-us/ef/core/miscellaneous/connection-resiliency).
