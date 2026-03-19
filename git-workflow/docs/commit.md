# Commit Workflow

## Shared references

Load before executing:

- [Scope Detection](../shared/scope-detection.md)
- [File Inclusion Policy](../shared/file-inclusion-policy.md)
- [Safety Rules](../shared/safety-rules.md)
- [Conventional Types](../shared/conventional-types.md)

---

## Goal

Create a commit representing the user's current working changes using a conventional commit format.

## Commit format

```
<type>(<scope>): <description>
```

If no scope applies:

```
<type>: <description>
```

## Workflow

1. Inspect repository status
2. Identify all modified files
3. Stage all user-modified files (see [File Inclusion Policy](../shared/file-inclusion-policy.md))
4. Exclude only obvious junk artifacts
5. Infer `<type>` and `<scope>` (see [Conventional Types](../shared/conventional-types.md) and [Scope Detection](../shared/scope-detection.md))
6. Generate and create the commit

## Output

Report:

- commit message used
- files committed
- any files excluded and why
