---
name: modern-python
description: Implement, review, or modernize Python server, library, and CLI code with current idioms, typed boundaries, safe concurrency, and deliberate compatibility. Do not use for data-science notebooks or legacy-only compatibility work unless asked.
---

# Modern Python

Match the repository's supported Python range and existing conventions. Prefer readable control flow and preserve public contracts unless change is authorized.

Write for the next maintainer: prefer direct names, ordinary control flow, small cohesive units, and obvious data flow over clever, compressed code. Comments and docstrings explain intent, invariants, and trade-offs—not code the reader can already see.

## Work

1. Read `pyproject.toml`, project guidance, and nearby code. Establish the minimum Python version; if unknown, use Python 3.10 syntax and state the assumption when it matters.
2. Type public and cross-module boundaries. Use built-in generics, `collections.abc`, unions, and honest interfaces. Keep validation, resource ownership, and error behavior explicit.
3. Before finishing a non-trivial change, run relevant configured tests, formatter, linter, and type checker; report actual results.

Load only the relevant reference:

- [Design and typing](references/design-and-typing.md): models, APIs, packaging, CLI, or type design.
- [Concurrency](references/concurrency.md): async work, threads, processes, deadlines, cancellation, or shutdown.
- [Quality and operations](references/quality-and-operations.md): tests, tooling, logging, performance, security, or deprecation.
- [Documentation](references/documentation.md): documentation or docstrings.

## Defaults

- Use dataclasses for owned records, `TypedDict` for external dict-shaped data, and small protocols for injected behavior. Use ABCs only for deliberate runtime hierarchies or shared implementation.
- Keep parsing and framework objects at the CLI edge; `main(argv=None) -> int` returns an exit status.
- Libraries do not configure global logging or perform import-time work.
- Related async tasks use `TaskGroup` on Python 3.11+ and always have an owner, cancellation path, deadline, and cleanup path.
- Follow existing tooling. New projects choose one formatter, Ruff as the usual linter, and one primary type checker.
- Use concise Google-style docstrings for public or non-obvious behavior, not trivial private code.
- Name for domain meaning, not implementation detail; avoid unexplained abbreviations and boolean mode flags.
- Keep mutation, I/O, retries, and caching visible at boundaries. Constructors and properties do not perform surprising work.
- Use an intermediate value or focused helper when it makes data flow, failures, or invariants clearer than a dense expression.

Review for readability: a reader can identify inputs, outputs, state changes, external effects, and failure behavior without tracing unrelated code.

Review exceptions to these defaults locally: `Any`, `cast`, ignores, broad catches, `shell=True`, unbounded tasks/caches, mutable globals, and unsafe deserialization.
