# Quality, operations, security, and compatibility

Use this reference for tool setup, tests, diagnostics, performance work, security-sensitive code, or public migration policy.

## Tooling

- Follow existing repository configuration. Do not add overlapping tools without a concrete gap.
- For new projects, choose exactly one formatter (Ruff formatter or Black), use Ruff as the usual linter, and choose one primary type checker (mypy or Pyright).
- Set each tool's target version to the actual minimum supported Python version.
- Start typed code with reasonably strict checking. Keep suppressions local and explain non-obvious ones.

## Tests and diagnostics

- Keep pure transformations separate from I/O where useful. Inject clocks, randomness, clients, subprocess runners, or filesystem roots only when tests need control of those effects.
- Prefer small fakes that satisfy a `Protocol`; use constrained/autospecced mocks when mocks are necessary.
- Test CLI core behavior separately from parsing. Test async cancellation and shutdown with synchronization primitives, not arbitrary sleeps.
- Use module loggers (`logging.getLogger(__name__)`). Libraries must not call `basicConfig()` or set global handlers. Use parameterized log calls and log a traceback once at the layer responsible for recording it.
- Never log credentials, tokens, or raw sensitive payloads.

## Performance

- Measure before optimizing. Use `cProfile` for CPU profile shape, `timeit` for narrow microbenchmarks, and `tracemalloc` for Python allocation growth.
- Improve algorithms, I/O count, data movement, and allocation behavior before source-level tricks.
- Use generators for one-pass streams, bounded caches for retained data, and slotted records only when measurement supports them.
- Avoid global GC tuning unless a measured, deployment-specific case requires it.

## Security

- Validate, normalize, and limit untrusted input at the boundary: size, time, queue depth, concurrency, and output are all resources.
- Never unpickle untrusted data.
- Use `subprocess` argument sequences with `shell=False` by default. Do not use f-strings to assemble SQL, shell, HTML, or another language from untrusted values; use that target's parameterized/escaping API.
- Use `secrets` for security tokens and `compare_digest` for sensitive comparisons when applicable. Use `tempfile` APIs instead of inventing temporary names.
- Static types aid review; they never replace runtime enforcement at a trust boundary.
