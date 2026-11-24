# Event listeners and Lambda

**Summary.** Keep delivery behavior in the adapter. Define how broker, Lambda, and in-process consumers receive and finish work.

## Contents

- [Keep the listener at the entry point](#keep-the-listener-at-the-entry-point)
- [Example of a shared cancellation handler](#example-of-a-shared-cancellation-handler)
- [Decide what happens to a delivery](#decide-what-happens-to-a-delivery)
- [In-process delivery](#in-process-delivery)
- [AWS Lambda](#aws-lambda)
- [Verify delivery behavior](#verify-delivery-behavior)

## Keep the listener at the entry point

A queue handler, topic subscription, stream consumer, or Lambda is an entry point. Keep its event envelope, deserialization, correlation, acknowledgement, retry behavior, and host-specific types at the adapter. Map to application input. Call the handler directly in new designs and use an existing application pipeline when it owns required validation or transactions.

When HTTP and a listener share an operation, use separate adapter files and put the shared handler in Application. For example, `Api/Shipping/ShipOrderEndpoint.cs` and `Listener/Shipping/ShipOrderListener.cs` can both call `Application/Shipping/ShipOrder.cs`. Each maps its own contract. Compare behavior before sharing a handler. Accepting an order and starting fulfillment are different operations even if their inputs look alike.

## Example of a shared cancellation handler

`Listener/Shipping/CancelShipmentListener.cs` calls the same `CancelShipment` as the [Minimal API write endpoint](api-feature-slices.md#example-of-a-write-endpoint). It accepts a decoded message and resolves the handler in a scope for the delivery.

```csharp
public sealed record CancelShipmentMessage(Guid ShipmentId);
public enum CancellationDisposition { Complete, TerminalRejection, Retry }

public sealed class CancelShipmentListener(IServiceScopeFactory scopes)
{
    public async Task<CancellationDisposition> ConsumeAsync(
        CancelShipmentMessage message, CancellationToken ct)
    {
        await using var scope = scopes.CreateAsyncScope();
        var handler = scope.ServiceProvider.GetRequiredService<CancelShipment>();
        var outcome = await handler.HandleAsync(message.ShipmentId, ct);

        return outcome switch
        {
            Cancelled => CancellationDisposition.Complete,
            ShipmentMissing or AlreadyShipped => CancellationDisposition.TerminalRejection,
            CancellationConflict => CancellationDisposition.Retry
        };
    }
}
```

The broker integration settles `Complete` after the handler returns. This example assumes missing and shipped are terminal for the message contract. Record a terminal rejection before settling when required. Apply bounded redelivery to `Retry`. Each attempt gets a fresh scope, so a repeated cancellation can succeed and a shipment that won the dispatch race can be rejected. Technical failures follow the configured retry or dead-letter policy. If an absent shipment can be created by a message still in flight, the contract may allow a retry instead.

## Decide what happens to a delivery

| Outcome                                                 | Adapter action                                                               |
| ------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Work committed or the delivery was already processed    | Acknowledge or advance the checkpoint when safe.                             |
| Expected business outcome that redelivery cannot change | Settle according to the message contract and record the outcome when needed. |
| Transient failure                                       | Apply bounded retry with backoff.                                            |
| Invalid input, permanent failure, or exhausted attempts | Use the configured dead-letter or quarantine policy with useful diagnostics. |

Create a scope per independent delivery and resolve the handler inside it. Limit concurrency to the operation's dependencies. Confirm the broker's semantics before mapping results. RabbitMQ settles deliveries, Service Bus can redeliver after a lock is lost, and Kafka checkpoints are positions within a partition. Keep a checkpoint behind earlier failed records when they must be retried.

A database commit can succeed before settlement fails. Prefer a repeat-safe domain transition or a unique business key. When a durable receipt is required, commit the receipt and business write together. Make external effects repeat-safe with a provider idempotency key and reconciliation where applicable. Use an outbox only when an outgoing notification must survive a crash after commit. An outbox does not replace inbound duplicate handling.

When a worker owns completion after a durable handoff, acknowledge once that handoff commits. Use redelivery if the handoff itself fails transiently. See [retry ownership](../architecture/persistence-and-writes.md#own-retries-and-external-effects).

## In-process delivery

- Route events by type before enqueueing. A worker that publishes back into a full queue it alone drains can stall. Give each independent effect its own queue. Readers doing the same job can share a queue.
- Decide what happens when a queue fills and whether a slow consumer may delay the others. Decide which failures skip an item, retry safely, or stop the host.
- If shutdown must drain pending work, stop intake and drain stages in producer-to-consumer order within a deadline.
- In-memory queues lose pending work when the process exits. If work must survive restart, advance the source cursor only after the required work completes or is durably queued. Plan for duplicate effects on replay.

## AWS Lambda

The Lambda function handler maps the event and calls the Application handler. Configure the function and dependency injection at its entry point. Reuse compatible SDK clients and the root service provider across warm invocations. Scope EF Core and mutable state to the work. Keep a separate context for each independent record processed concurrently. Verify language and runtime availability for the deployment.

SQS delivery can repeat. When independent retry is appropriate, enable `ReportBatchItemFailures` on the event source mapping and return each failed record's `MessageId` as its `ItemIdentifier`. Throwing from the function fails the whole batch. With FIFO, stop after the first failure and return failed and unprocessed records to preserve ordering. Check the event source and invocation mode for their retry behavior. [Lambda C# handlers](https://docs.aws.amazon.com/lambda/latest/dg/csharp-handler.html), [SQS batch failure handling](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html).

With a self-hosted SQS poller, delete a completed delivery using its current receipt handle. Keep retryable deliveries for redelivery and configure visibility timeout and redrive for the operation's needs. [SQS DeleteMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessage.html).

## Verify delivery behavior

Test delivery through the real broker where settlement or retries are important. Exercise duplicates and loss of settlement after commit. For Lambda, cover envelope mapping locally and verify event source setup, IAM, and retry behavior with a deployed integration test. [AWS Lambda testing](https://docs.aws.amazon.com/lambda/latest/dg/testing-guide.html).
