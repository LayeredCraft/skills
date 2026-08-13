# Message Consumers

Use this reference for queue, topic, or stream handlers. Treat message receipt as a delivery edge:

```text
Message -> Consumer -> Operation -> DbContext / services / external clients
```

The consumer owns deserialization, message metadata, acknowledgement/settlement, delivery-attempt handling, correlation/trace propagation, and dead-letter or poison-message policy. The operation owns the use case and must not depend on broker SDK types.

```text
Features/
  Orders/
    OrderSubmitted.cs
    OrderSubmittedConsumer.cs
    StartFulfillment.cs
    OrdersMessagingModule.cs
```

Keep the broker adapter and contract at the consumer edge. Map the message to application input before calling the operation:

```csharp
public sealed record OrderSubmitted(Guid OrderId, string EventId);

public sealed class OrderSubmittedConsumer(
    MessageInbox inbox,
    StartFulfillment.Handler handler)
{
    // The broker adapter calls this method and acknowledges only after it succeeds.
    public async Task ConsumeAsync(OrderSubmitted message, CancellationToken ct)
    {
        var claim = await inbox.TryClaimAsync(message.EventId, ct);
        if (claim == MessageClaim.AlreadyCompleted)
            return; // Safe duplicate: acknowledge without running the operation again.

        try
        {
            await handler.HandleAsync(new StartFulfillment.Command(message.OrderId), ct);
            await inbox.CompleteAsync(message.EventId, ct);
        }
        catch
        {
            await inbox.ReleaseAsync(message.EventId, ct);
            throw; // The adapter applies the broker's retry or dead-letter policy.
        }
    }
}

public static class OrdersMessagingModule
{
    public static IServiceCollection AddOrdersMessaging(this IServiceCollection services)
    {
        services.AddScoped<StartFulfillment.Handler>();
        services.AddScoped<MessageInbox>();
        services.AddScoped<OrderSubmittedConsumer>();
        return services;
    }
}
```

Keep `MessageInbox` durable and protect its event ID with a uniqueness constraint. For a local database-only operation, persist the operation's state change and `CompleteAsync` in the same database transaction using the same scoped `DbContext`; otherwise a crash between the two can repeat the operation. If the operation includes an external side effect, do not keep that database transaction open around the call. Instead, make the side effect independently idempotent and reconcile it on retry, or use durable state plus an outbox. Make a claim lease recoverable after a crash; `TryClaimAsync` must return `AlreadyCompleted` only for a completed delivery, and may reclaim an expired in-progress delivery. For a broker SDK that invokes a singleton callback, create a scope per delivery there and resolve `OrderSubmittedConsumer` from that scope. The consumer above deliberately has no broker SDK types.

Assume at-least-once delivery unless the broker and its full processing path demonstrably guarantee otherwise. Make processing idempotent using a durable deduplication record, a unique business key, or a state transition that safely rejects repeats. Scope the idempotency key to the producer and message type where necessary.

Choose settlement deliberately:

- Acknowledge only after durable, successful processing.
- Retry transient failures with bounded attempts and backoff.
- Dead-letter malformed, unsupported, or repeatedly failing messages with useful diagnostics.
- Do not retry business rejections indefinitely; record or publish the expected outcome when the contract requires it.

Create a DI scope per delivery and keep `DbContext` work within that scope. Limit concurrent deliveries to the operation's database and downstream capacity. Do not hold a database transaction open while waiting on a slow external call unless its consistency and timeout costs are explicitly accepted.

For outgoing events that reflect a database write, persist the event in an outbox in the same transaction as the state change, then publish it asynchronously. A consumer may publish a follow-up event, but the broker message and database transaction are not atomically one operation without a specific transactional guarantee.

Version message contracts additively, preserve compatibility where the producer/consumer contract requires it, and keep broker schemas separate from HTTP contracts and EF entities. Split a consumer into its own deployable service only for independent ownership, scaling, data ownership, or failure isolation—not merely because it receives messages.

Test the operation separately from the broker. Add consumer tests for duplicate suppression, malformed-message handling, transient versus permanent failure classification, and acknowledgement/dead-letter behavior using the broker adapter's test seam. Run at least one integration test against the actual broker before relying on settlement or retry semantics in production.
