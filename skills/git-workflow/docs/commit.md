# Commit Workflow

## Context budget

This is the lightweight workflow. Do not load shared references by default.
Consult them only when compact git inspection leaves real ambiguity:

- [Scope Detection](../shared/scope-detection.md) - when the scope is unclear
- [File Inclusion Policy](../shared/file-inclusion-policy.md) - when file
  inclusion is ambiguous
- [Safety Rules](../shared/safety-rules.md) - when repository state is unusual
- [Conventional Types](../shared/conventional-types.md) - when the type is
  unclear or the change may be breaking

---

## Goal

Create a commit representing the user's current working changes using a conventional commit format.

## Commit format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The description must immediately follow the colon and space. Scope is wrapped in parentheses when present: `feat(parser): add CSV support`.

For breaking changes, append `!` after the type/scope and/or include a `BREAKING CHANGE:` footer. See [Conventional Types](../shared/conventional-types.md) for details.

## Workflow

1. Inspect repository status with `git status --short`
2. Identify changed files with `git diff --name-status` and `git diff --stat`
3. Identify automatic exclusions first: obvious junk, local config, generated
   build/cache output, and secrets
4. Stage remaining user-modified files
5. Infer `<type>` and optional `<scope>` from filenames, paths, and stat output
6. Generate and create the commit

Use full `git diff` only when the compact status, names, and stats are not
enough to write an accurate commit message.

## Output

Report:

- commit message used
- files committed
- any files excluded and why
