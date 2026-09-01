# Concurrency and async services

Use this reference for any code that starts, awaits, cancels, limits, or shuts down concurrent work.

## Choose by workload

- Use ordinary synchronous code for simple flows and low concurrency.
- Use `asyncio` for many concurrent I/O operations with async-capable dependencies.
- Use threads for blocking I/O and synchronous-library adapters; bound executor/offload concurrency.
- Use processes for CPU-heavy or isolated work that can tolerate startup and serialization costs.
- Do not assume free-threaded CPython is available. Write shared-state code that is correct under concurrent scheduling regardless of the interpreter build.

## Ownership and lifecycle

- Application boundaries may own a loop with `asyncio.run()`. Reusable libraries must not call it internally.
- Prefer `asyncio.TaskGroup` for sibling tasks that belong to one operation. Use `gather()` only when its ordered result behavior and failure semantics match the need.
- Never fire-and-forget a task without a strong reference, failure reporting, and a defined shutdown owner.
- Use `async with` and `try`/`finally` for resources and cleanup. Use `AsyncExitStack` for a dynamic resource set.
- Treat cancellation as normal control flow. Perform bounded cleanup in `finally`, then propagate `CancelledError`; do not swallow it casually.

## Limits and failures

- Put deadlines around external waits and make end-to-end timeout budgets explicit when needed.
- Apply admission control with semaphores, bounded queues, worker pools, or equivalent limits. Async syntax does not create unlimited sockets, memory, or upstream capacity.
- Keep blocking calls out of the event loop, using `asyncio.to_thread()` or a controlled executor where appropriate. Remember that cancelling the await does not generally cancel the underlying blocking work.
- Let concurrent sibling failures propagate naturally as exception groups. Handle with `except*` only where independent failure categories genuinely need separate recovery.
- Catch broad `Exception` only at containment boundaries that record, isolate, or convert an unexpected failure. Keep lower-level `try` blocks narrow.
