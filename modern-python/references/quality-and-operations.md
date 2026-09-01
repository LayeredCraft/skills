# Quality and operations

Follow repository tooling. New projects use one formatter, Ruff, and one type checker; target the minimum supported Python. Applications use the project's reproducible lock/install workflow; libraries keep supported dependency ranges deliberate. Keep suppressions local and explained.

Separate pure logic from I/O where useful. Inject effects tests must control. Test observable behavior; pair defect fixes with focused regressions. Prefer protocol-based fakes to deep mocks; test CLI core separately and async cancellation without arbitrary sleeps. Libraries use module loggers and never configure global logging. Do not log secrets.

Measure before optimizing: `cProfile` for execution shape, `timeit` for microbenchmarks, `tracemalloc` for allocations. Improve algorithms and data movement first; bound caches.

Validate and limit untrusted input. Never unpickle it. Use `subprocess` argument lists with `shell=False`, plus `check=True` and a timeout when appropriate. Parameterize target languages instead of interpolating untrusted data. Use `secrets`, `compare_digest`, and `tempfile` for their intended security cases. Types do not enforce runtime security.
