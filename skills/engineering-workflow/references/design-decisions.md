# Design decisions

Check existing code, architecture docs, ADRs, plans, issues, and recent changes
before proposing a new design. Many requests are extensions of decisions already
made rather than blank-slate problems.

## Where information belongs

Adapt paths and names to repository conventions:

- **README or product docs**: user-facing purpose and current capabilities.
- **Architecture/topic docs**: current system shape and constraints.
- **Decision records**: what was decided, why, alternatives, and consequences.
- **Implementation plans**: ordered execution work, scope, files, tests, and live
  progress.
- **Issues/roadmaps**: prioritization and deferred work.

Do not mix decision rationale with mutable execution checklists. If repository
uses no ADRs or plans, do not create bureaucracy automatically; use smallest
persistent artifact proportional to decision impact.

## Decision depth

Choose process based on reversibility, ambiguity, blast radius, and cost.

- **Inline**: local, low-risk, easy-to-reverse choice following precedent.
  Capture reasoning in code/review only when non-obvious.
- **Light**: clear change with modest cross-cutting impact. Record context,
  decision, key alternative, and consequences in repository's preferred place.
- **Deep**: ambiguous, expensive, security-sensitive, externally visible, or
  cross-system change. Restate problem and constraints, research precedent,
  compare at least two viable alternatives, and confirm direction before coding.

## Decision record contents

When formal record is warranted, include:

1. Title, date/status, and owners or decision authority if project uses them.
2. Context and problem.
3. Constraints and decision drivers.
4. Viable alternatives with honest trade-offs.
5. Decision and rationale.
6. Positive and negative consequences.
7. Links to related docs, issues, plans, or superseded decisions.

Treat accepted records as history. Supersede with new record rather than
rewriting old rationale unless repository policy says otherwise.

## Plans

Create persistent plan when work is multi-step, spans sessions, has meaningful
sequencing, or needs coordination. Re-read plan from disk before resuming and
update it as work proceeds.

Useful plan sections:

- Goal and measurable completion criteria
- In scope and explicitly deferred work
- Ordered phases or tasks
- Critical files and interfaces
- Test and verification strategy
- Risks, rollout, migration, and rollback where relevant
- Status and checked completion evidence

Do not begin implementation against an unsettled decision when wrong direction
would create meaningful rework. Small reversible changes need no ceremonial ADR
or plan unless repository requires one.
