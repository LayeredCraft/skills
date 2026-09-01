# Design, typing, and interfaces

Use this reference for type boundaries, data models, library design, package structure, and CLI code.

## Version-aware language choices

- Python 3.10+: use `list[str]`, `dict[str, bytes]`, `collections.abc` interfaces, `T | None`, structural pattern matching where shape-driven dispatch helps, `ParamSpec`, and `TypeGuard`.
- Python 3.11+: prefer `asyncio.TaskGroup` for related async work; `Self`, `Required`, `NotRequired`, `assert_never`, and `ExceptionGroup` are available.
- Python 3.12+: use PEP 695 type-parameter syntax (`def first[T](...)`) only when the project floor is 3.12 or higher.
- Python 3.13+: use `typing.TypeIs` when a custom predicate soundly narrows a subtype. Keep `TypeGuard` for unsound-but-useful cases such as invariant mutable containers.
- Python 3.14+: deferred annotation evaluation changes runtime introspection. Do not depend on annotation evaluation side effects; retain a compatibility approach for older supported versions.

## Contracts and types

- Accept the weakest honest interface: `Iterable` for one pass, `Collection` for length/containment, `Sequence` for indexing, and `Mapping` when mutation is unnecessary.
- Prefer normal narrowing (`isinstance`, `is not None`, early return, raise) over `cast`. A cast records static knowledge; it never validates runtime data.
- Use `Protocol` for small consumer-owned structural interfaces, especially adapters and test fakes. Use `@runtime_checkable` only for coarse capability checks.
- Use `NewType` for distinct scalar IDs where mixing values would be a bug. Use `Literal` or overloads when inputs and outputs genuinely correlate.
- Use `ParamSpec` for decorators/adapters that preserve a callable signature. Use a callable protocol when keyword-only details matter.

## Models and ownership

- Use `@dataclass` as the normal owned model. Consider `frozen=True` for value objects, `kw_only=True` for evolving constructors, and `slots=True` when measured instance count or deliberate API rigidity justifies it.
- Never use mutable field defaults; use `field(default_factory=...)`.
- Use `TypedDict` for JSON/config/request-like dictionaries. It is static only, so validate untrusted data before treating it as trusted. Prefer field-level `Required`, `NotRequired`, and `ReadOnly` when they express the schema.
- Use `NamedTuple` only where tuple semantics—unpacking and positional order—are part of the contract.
- Copy or wrap mutable inputs at ownership boundaries, not indiscriminately.

## Public APIs and packaging

- Type public parameters, returns, yielded values, callbacks, and important attributes. Make sync/async distinctions explicit.
- Prefer keyword-only policy options that will likely grow. Use positional-only parameters only when parameter names should deliberately remain non-contractual.
- Keep top-level exports intentional and implementation modules private by convention. For published inline-typed packages, ship `py.typed`.
- Prefer `pyproject.toml`; use a `src/` layout for distributable packages unless the existing project has a sound, established alternative.
- Translate low-level exceptions only at an abstraction boundary, preserving the cause with `raise PublicError(...) from exc`.
- Deprecate established contracts with a replacement, expected removal point, and appropriate warning/static metadata. Do not break users merely to change style.

## CLI boundary

- Use `argparse` when standard-library portability matters; use a framework such as Typer only when its dependency is justified by the CLI.
- Keep parser/framework objects out of domain code. Send requested output to stdout; send diagnostics to stderr or logging.
- Keep `__main__.py` as a small wrapper around the same entry point used by the installed script.
