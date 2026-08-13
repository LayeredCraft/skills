# Workers

Use this reference for `BackgroundService`, `IHostedService`, scheduled jobs, polling loops, and long-running processes. Treat the worker as a delivery edge, not as the location for business logic:

```text
Schedule / trigger -> Worker -> Operation -> DbContext / services / external clients
```

The worker owns host lifecycle, scheduling or polling, concurrency limits, cancellation, and observability. The operation owns one unit of work and must not depend on `BackgroundService`, service-provider scope management, or host lifecycle APIs.

Create a DI scope per unit of work; resolve scoped dependencies inside it. Do not inject a scoped `DbContext` into a singleton hosted service. Honor the stopping token, propagate cancellation, and avoid overlapping runs unless the operation is explicitly concurrency-safe.

```text
Features/
  Billing/
    RunOverdueInvoices.cs
    BillingWorker.cs
    BillingModule.cs
```

```csharp
public sealed class BillingWorker(
    IServiceScopeFactory scopeFactory,
    ILogger<BillingWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(TimeSpan.FromMinutes(5));

        while (await timer.WaitForNextTickAsync(stoppingToken))
        {
            await using var scope = scopeFactory.CreateAsyncScope();
            var operation = scope.ServiceProvider
                .GetRequiredService<RunOverdueInvoices.Handler>();

            await operation.HandleAsync(stoppingToken);
            logger.LogInformation("Overdue-invoice run completed");
        }
    }
}

public static class BillingModule
{
    public static IServiceCollection AddBilling(this IServiceCollection services)
    {
        services.AddScoped<RunOverdueInvoices.Handler>();
        services.AddHostedService<BillingWorker>();
        return services;
    }
}
```

Keep scheduling in `BillingWorker`; make `RunOverdueInvoices.Handler` a normal scoped operation that accepts only its input and `CancellationToken`. For a one-off or queue-triggered item, create one scope per item rather than per timer tick.

For recurring work, define the trigger, selection criteria, work-item claim or lock strategy, retry/backoff policy, and maximum parallelism. Make a run safe after restart: use durable state, an idempotency key, or a claim/checkpoint where duplicate execution is possible.

Use a worker in the web host for small, coupled work. Move it to a separately deployed worker only when its scaling, reliability, operational ownership, or failure isolation differs from the API. A different process does not automatically require a different domain model or service boundary.

For work that calls external systems, persist local state before the side effect where possible. If a crash can occur between the external call and local update, use an idempotency key with the provider and reconcile on retry. Use a transactional outbox when reliably publishing a follow-up message is required.

Keep job-specific request and result models local to the worker. Reuse an operation only when a worker and another edge perform the identical use case; do not make HTTP request/response contracts the worker's application contract.

Test the operation's selection, state transitions, and retry-safe behavior independently. Add a focused host test only for registration, schedule/trigger behavior, cancellation, or concurrency wiring that an operation test cannot cover. Use a controllable clock or trigger in tests; do not wait for real timer intervals.
