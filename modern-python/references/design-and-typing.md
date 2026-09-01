# Design and typing

- Python 3.10+: built-in generics, `X | Y`, pattern matching, `ParamSpec`, `TypeGuard`.
- Python 3.11+: `TaskGroup`, `Self`, `Required`, `NotRequired`, `ExceptionGroup`.
- Python 3.12+: PEP 695 type parameters only when the floor permits.
- Python 3.13+: prefer sound `TypeIs` predicates; use `TypeGuard` when narrowing is intentionally unsound.
- Python 3.14+: annotations are deferred. Do not rely on annotation side effects.
- For newer typing features on older supported Python, import only the needed construct from `typing_extensions` and declare the dependency.

Use the weakest honest interface (`Iterable`, `Collection`, `Sequence`, `Mapping`). Prefer ordinary narrowing over `cast`; `cast` is not validation. Use small `Protocol`s for structural dependencies and `NewType`, `Literal`, overloads, or `ParamSpec` only for real type relationships.

Use a dataclass by default; choose `frozen`, `kw_only`, or `slots` for a concrete reason. Use `default_factory` for mutable fields. `TypedDict` describes external dictionaries statically—validate before trusting it. `NamedTuple` is for intentional tuple semantics.

## Structure

Organize modules around one cohesive responsibility and clear dependency direction. Split a file when it mixes distinct concepts, layers, or reasons to change—not at an arbitrary line count. Keep related small types together; do not create a file per class.

Prefer functions for stateless transformations and one-off actions. Introduce a class when state, lifecycle, invariants, or a replaceable behavior belong together. Do not use classes as namespaces. Keep functions focused on one meaningful operation; extract a helper only when it has a clear name and responsibility. Avoid modules or classes that coordinate unrelated work.

Public APIs are typed, intentional, and stable. Use keyword-only evolving options, package `py.typed` for published inline-typed libraries, and translate errors only at abstraction boundaries with preserved causes. Deprecations name a replacement and removal point.

Keep CLI parsing at the edge; use `argparse` unless a framework earns its dependency. Public changes require type, exception, docstring, compatibility, and focused-test review. Test an installed artifact when packaging or import behavior changes.
