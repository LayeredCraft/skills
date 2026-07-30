# Task: Implement

Use for feature work, meaningful bug fixes, or implementation of accepted design.
For unresolved high-impact design, run [Design](design.md) first.

## Load first

Always:

- [Coding standards](../references/coding-standards.md)

As relevant:

- [Testing](../references/testing.md) — behavior or tests change
- [Documentation](../references/documentation.md) — docs, examples, comments, or
  public contracts change
- [Design decisions](../references/design-decisions.md) — decision or plan exists
  or change introduces a meaningful design choice
- [Security](../references/security.md) — trust boundary or sensitive data changes
- [Contributing](../references/contributing.md) — preparing contribution artifacts

## Procedure

1. Inspect repository instructions and working-tree state. Inventory pre-existing
   changes and preserve unrelated user work. Read accepted decision and re-read
   plan from disk when either exists.
2. Confirm scope, completion criteria, affected contracts, and required validation.
3. Inspect nearby implementation/tests before editing; follow local patterns.
4. Implement smallest coherent change. Avoid unrelated cleanup and new dependencies
   unless necessary and justified.
5. When behavior changes or identified risk warrants coverage, add or update tests
   while building. Include regression, boundary, integration, or consumer tests
   matching actual risks. For test-only work, avoid unrelated production or doc
   changes.
6. Keep an existing plan/checklist current as implementation diverges or completes.
7. Update docs, examples, changelog, migrations, or public API references when
   behavior, public contracts, or repository policy requires it. For docs-only
   work, do not invent unrelated tests or code changes.
8. Inspect unfamiliar validation scripts before execution. Ask before running
   commands that install software, access network or credentials, mutate external
   systems, or may be destructive. Then run applicable formatter/linter,
   build/type-check, tests, and realistic boundary verification. Record evidence.
9. Review final diff for scope, secrets, generated artifacts, accidental debug
   code, compatibility, and incomplete plan items.
10. Report changed files, validation, and residual risks. Commit/push/open PR only
    when requested or repository workflow explicitly includes it.

## Output

Working change matching agreed scope; applicable tests, docs, and plan state
updated; validation evidence reported. Clearly state anything not verified and
why an update was not applicable when that might otherwise be ambiguous.
