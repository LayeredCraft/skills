# Documentation

Use Google-style docstrings for public APIs and behavior that is not clear from names and types. Skip simple private helpers, tests, trivial properties, and unchanged overrides.

Start with one summary sentence. Add only useful sections:

- `Args:` for semantic constraints, ownership, or units—not repeated types.
- `Returns:` or `Yields:` for meaningful result behavior.
- `Raises:` for public, recoverable exceptions.
- `Attributes:` or `Example:` when they clarify use.

Document class responsibility and invariants. Keep implementation comments beside the relevant code rather than turning them into public docstrings.
