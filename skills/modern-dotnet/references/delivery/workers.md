# Workers and jobs

**Summary.** Keep scheduling, dependency scopes, and shutdown in the host. A worker, scheduled job, or CLI invokes an Application operation.

## Contents

- [Choose the host](#choose-the-host)
- [Example of a scoped worker](#example-of-a-scoped-worker)
- [Handle failures and verify behavior](#handle-failures-and-verify-behavior)
- [Example of an in-process event pipeline](#example-of-an-in-process-event-pipeline)

## Choose the host

Treat a scheduled job, polling worker, or CLI command as an entry point. Translate the trigger to application input and call the handler directly in a new design. Use the existing application entry point when it owns required validation or transactions. Keep the loop, schedule, shutdown, concurrency limits, and exit behavior with the host. Keep business rules and the commit with the operation and its domain types.

- Use a run-once executable when an external scheduler starts the job. Pass the logical processing window when a retry needs to process the same work. Define overlap and catch-up behavior with the scheduler.
- Use `BackgroundService` for a long-running loop in a .NET host. Registering with `AddHostedService` gives the worker a singleton lifetime. Resolve the handler and context inside a scope for each independent run or work item. Give parallel operations separate contexts.
- A CLI owns arguments, output, and exit codes. It can use the same handler as a scheduled job when both execute the same operation.

## Example of a scoped worker

```csharp
public sealed class BillingWorker(IServiceScopeFactory scopes) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(TimeSpan.FromMinutes(5));

        while (await timer.WaitForNextTickAsync(stoppingToken))
        {
            await using var scope = scopes.CreateAsyncScope();
            var handler = scope.ServiceProvider.GetRequiredService<ReconcileInvoices>();
            await handler.HandleAsync(stoppingToken);
        }
    }
}
```

## Handle failures and verify behavior

This loop runs one operation at a time. Unexpected failures reach the host. Choose backoff and retry only for work that can safely repeat. Keep permanent failures visible. Use a checkpoint when restarting a long or multi-step job would otherwise lose progress or repeat effects. For an external call, use the provider's idempotency support when available and reconcile an unknown outcome before repeating the effect.

Keep a small worker in the existing host if its lifecycle and resource needs fit. Deploy it separately when scaling, ownership, or failure isolation requires it. Use a controllable trigger in component tests and a real database for persistence behavior. [.NET worker services](https://learn.microsoft.com/en-us/dotnet/core/extensions/workers), [Scoped hosted services](https://learn.microsoft.com/en-us/dotnet/core/extensions/scoped-service).

## Example of an in-process event pipeline

A long-running console app polls a forum for new topics. The poller owns the cursor and sends `NewTopic` to the fetch worker. The fetch worker loads the post and sends `PostFetched` to the archive, log, and notification workers. Each owns its own effect. The host wires the routes and owns shutdown and the exit code.

Call the next operation directly when it can share the caller's timing and failure behavior. Use a [bounded queue](consumers.md#in-process-delivery) when a stage needs its own backlog or concurrency.

To test the routing, use a fetch queue with capacity one and pause the first fetch. Fill the queue with the next topic, then let the first fetch finish. Verify that it can publish its result and begin the next fetch.
