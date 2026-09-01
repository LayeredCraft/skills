# Concurrency

Use synchronous code when sufficient; `asyncio` for concurrent I/O; threads for blocking I/O adapters; processes for isolated CPU work. Do not assume a free-threaded build.

- Only application boundaries call `asyncio.run()`.
- Prefer `TaskGroup` for sibling work. `gather()` is for its specific ordered-result and failure behavior.
- Every background task has a retained reference, failure reporting, and shutdown owner.
- Use `async with` and `try`/`finally` for cleanup. Propagate `CancelledError` after bounded cleanup.
- Put deadlines around external waits; use bounded queues, semaphores, or pools for admission control.
- Keep blocking calls off the event loop; cancellation usually cannot stop the underlying blocking operation.
- Handle `ExceptionGroup` with `except*` only for distinct concurrent recovery paths. Catch broad `Exception` only at containment boundaries.
