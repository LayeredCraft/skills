# Documentation and docstrings

Use Google-style docstrings for public APIs and code whose behavior, side effects, invariants, or failure modes are not obvious from its signature and name.

Do not require docstrings for straightforward private helpers, simple tests, trivial properties, or overrides that add no behavior. Do not repeat information already conveyed clearly by types and names.

## Content

- Start with a concise summary sentence describing what the object does or represents.
- Add a short explanation only when it clarifies behavior, ownership, lifecycle, ordering, mutation, caching, security, or compatibility.
- Use `Args:`, `Returns:`, `Yields:`, `Raises:`, `Attributes:`, and `Example:` only when the section adds useful information.
- Describe semantic constraints and outcomes rather than restating types. A type hint already documents `timeout: float | None`; explain what timeout means and what happens when it expires.
- Document public exceptions callers can reasonably handle. Do not enumerate incidental implementation exceptions.

```python
def fetch_user(user_id: UserId, *, timeout: float | None = None) -> User:
    """Return the current user record from the remote service.

    Args:
        user_id: Identifier assigned by the account service.
        timeout: Maximum time to wait for the remote response. `None` uses the
            client's configured deadline.

    Raises:
        UserNotFoundError: If no user exists for `user_id`.
        ServiceUnavailableError: If the service cannot respond before the
            deadline.
    """
```

For classes, document the class's responsibility and invariants; document constructor arguments in `__init__` only when the constructor is the public API and the class docstring would otherwise be unclear. Keep internal implementation comments close to the code they explain rather than turning them into public-facing docstrings.
