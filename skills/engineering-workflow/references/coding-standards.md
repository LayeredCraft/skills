# Coding standards

Explicit current project policy and accepted architecture records are source of
truth. Discover conventions from instruction files, formatters, linters, compiler
settings, nearby production code, and tests before writing code. Treat existing
code as precedent evidence, not authority: do not copy defects, obsolete patterns,
or insecure behavior merely because they already exist.

## General defaults

Use these only where project has no stronger rule:

- Keep changes scoped to request. Avoid drive-by refactors.
- Prefer clear names and small units with one coherent responsibility.
- Match existing file, module, namespace/package, and public API organization.
- Use narrow visibility and expose only intentional compatibility surfaces.
- Preserve nullability, type-safety, ownership, and mutability conventions.
- Prefer immutable data where mutation is unnecessary; encapsulate mutable state.
- Inject dependencies explicitly. Avoid hidden global state and service-locator
  patterns unless framework or established architecture requires them.
- Keep asynchronous work async end-to-end. Propagate cancellation/timeouts where
  ecosystem supports them; do not block on async operations.
- Treat expected domain outcomes as explicit values when that matches local
  patterns. Reserve exceptions/errors for exceptional or boundary failures.
- Catch only failures caller can handle. Preserve original error context and do
  not silently swallow failures.
- Avoid boolean mode flags and long parameter lists when separate operations or
  parameter objects express intent better.
- Depend on abstractions at module boundaries when it improves substitutability;
  do not add abstraction without concrete value.
- Optimize only with evidence. Prefer readable correct code before speculative
  complexity.
- Keep generated code deterministic, collision-safe, and clearly separated from
  hand-written source when generators are involved.

## Public API changes

Before changing externally consumed interfaces:

1. Identify compatibility guarantees and release policy.
2. Search known consumers and docs.
3. Prefer additive changes when backward compatibility matters.
4. Document migration and breaking impact when compatibility cannot be kept.
5. Add contract tests or representative consumer verification where practical.

## New patterns

Before introducing library, framework, architectural pattern, or coding style:

1. Search repository for precedent.
2. Confirm existing tools cannot solve need consistently.
3. Compare maintenance, security, performance, and migration costs.
4. Record decision at level required by `design-decisions.md`.

Do not copy stack-specific rules from another repository without validating they
fit current language, runtime, and product constraints.
