---
name: modern-python
description: Implement, review, or modernize Python server, library, and CLI code with current idioms, typed boundaries, safe concurrency, and deliberate compatibility. Do not use for data-science notebooks or legacy-only compatibility work unless asked.
---

# Modern Python

Write maintainable Python that fits the repository's supported interpreter range. Prefer ordinary, readable control flow over compact tricks. Preserve established public APIs unless the request authorizes a compatibility change.

## First pass

1. Read the project's `pyproject.toml`, contribution guidance, existing tool configuration, and nearby code before choosing syntax or tools.
2. Identify the minimum supported Python version. Do not introduce parser-level features above that floor. If it is not stated and cannot be inferred, use broadly modern Python 3.10 syntax and call out the assumption when it affects the result.
3. Keep public functions, cross-module data, callbacks, and meaningful state typed. Let clear local variables be inferred.
4. Use built-in generics, `collections.abc` interfaces, and `X | None` / `X | Y` where the version permits. Avoid spreading `Any`; use `object` and narrow untrusted values instead.
5. Keep validation at trust boundaries, expose intentional public APIs, and make cleanup and error behavior explicit.

Choose the smallest applicable reference. Do not load all references by default.

## Route by task

- For type design, data models, public library APIs, package structure, or CLI boundaries, read [references/design-and-typing.md](references/design-and-typing.md).
- For `asyncio`, threads, processes, cancellation, timeouts, resource ownership, or concurrent-error handling, read [references/concurrency.md](references/concurrency.md).
- For testing, formatting, linting, static analysis, profiling, logging, security, or compatibility/deprecation work, read [references/quality-and-operations.md](references/quality-and-operations.md).
- For public API documentation or docstring review, read [references/documentation.md](references/documentation.md).

## Default decisions

- Use a `dataclass` for owned record-like values; use `TypedDict` for dictionary-shaped external data; use a small `Protocol` for injected behavior. Use an ABC only for intentional runtime hierarchy or shared implementation.
- Keep CLI parsing at the edge. Pass ordinary typed values into application code; have `main(argv: Sequence[str] | None = None) -> int` return an exit status.
- Keep libraries free of global logging configuration and import-time side effects.
- In async code, make each task's owner, cancellation path, deadline, and cleanup path clear. Prefer `TaskGroup` for sibling work belonging to one operation.
- Use formatter, linter, and type checker settings already present in the repository. For a new project, choose one formatter, Ruff as the usual linter, and one primary type checker.
- Document public and non-obvious behavior with concise Google-style docstrings; do not add boilerplate docstrings to self-explanatory private code.

## Review focus

Treat these as deliberate exceptions that need a local reason: `Any`, `cast`, type/lint ignores, broad exception catches, `shell=True`, unbounded task creation or caches, mutable global state, and unsafe deserialization.

Do not modernize spelling, APIs, or dependencies solely for fashion. Prefer changes that improve a concrete contract, safety property, or maintenance cost.
