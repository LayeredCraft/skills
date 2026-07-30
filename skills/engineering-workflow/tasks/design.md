# Task: Design

Use for new features, architecture changes, cross-cutting refactors, or “how
should this be structured?” requests. Produce agreed direction before application
code when decision cost warrants it.

## Load first

Always:

- [Design decisions](../references/design-decisions.md)
- [Documentation](../references/documentation.md)

As relevant:

- [Coding standards](../references/coding-standards.md)
- [Testing](../references/testing.md)
- [Security](../references/security.md)

## Procedure

1. Read repository instructions, relevant code/docs, existing ADRs/plans, issues,
   and nearby precedent.
2. Restate problem, desired outcome, non-goals, constraints, and success criteria.
3. Classify decision as inline, light, or deep using reversibility, ambiguity,
   blast radius, and repository policy.
4. For deep decisions, research prior art and present at least two viable
   alternatives with trade-offs. Ask user to choose when direction is genuinely
   ambiguous; do not hide choice inside implementation.
5. Record decision using repository's established mechanism. If none exists, use
   smallest persistent artifact justified by impact.
6. Update or cross-link architecture/topic docs without describing unimplemented
   behavior as already shipped.
7. Create implementation plan when work is multi-step, sequenced, coordinated, or
   likely to span sessions. Keep unsettled decisions out of active implementation.
8. Confirm handoff: accepted direction, scope, verification strategy, risks, and
   deferred work.

## Output

Decision proportional to impact, plus plan when needed. No production-code edits
unless user explicitly combines a small design decision with implementation and
repository policy allows it.
