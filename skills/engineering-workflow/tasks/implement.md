# Task: Implement

Use for feature work, meaningful bug fixes, or implementation of accepted design.
For unresolved high-impact design, run [Design](design.md) first.

## Load first

Always:

- [Coding standards](../references/coding-standards.md)
- [Testing](../references/testing.md)
- [Documentation](../references/documentation.md)

As relevant:

- [Design decisions](../references/design-decisions.md)
- [Security](../references/security.md)
- [Contributing](../references/contributing.md)

## Procedure

1. Inspect repository instructions and working-tree state. Inventory pre-existing
   changes and preserve unrelated user work. Read accepted decision and re-read
   plan from disk when either exists.
2. Confirm scope, completion criteria, affected contracts, and required validation.
3. Inspect nearby implementation/tests before editing; follow local patterns.
4. Implement smallest coherent change. Avoid unrelated cleanup and new dependencies
   unless necessary and justified.
5. Add or update tests while building. Include regression, boundary, integration,
   or consumer tests matching actual risks.
6. Keep plan/checklist current as implementation diverges or completes.
7. Update docs, examples, changelog, migrations, or public API references required
   by behavior change.
8. Inspect unfamiliar validation scripts before execution. Ask before running
   commands that install software, access network or credentials, mutate external
   systems, or may be destructive. Then run applicable formatter/linter,
   build/type-check, tests, and realistic boundary verification. Record evidence.
9. Review final diff for scope, secrets, generated artifacts, accidental debug
   code, compatibility, and incomplete plan items.
10. Report changed files, validation, and residual risks. Commit/push/open PR only
    when requested or repository workflow explicitly includes it.

## Output

Working change matching agreed scope, tests and docs updated, validation evidence
reported, and plan status accurate. Clearly state anything not verified.
