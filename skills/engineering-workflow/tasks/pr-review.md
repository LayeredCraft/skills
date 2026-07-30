# Task: PR review

Use to review pull requests, merge requests, platform-specific change sets,
commits, patches, diffs, or local working trees. Review both correctness and
repository-process conformance.

## Load first

Always:

- [Collaboration](../references/code-of-conduct.md)
- [Review emoji legend](../references/review-emoji-legend.md)

As relevant:

- [Coding standards](../references/coding-standards.md) — code changes
- [Documentation](../references/documentation.md) — docs or public contracts
- [Design decisions](../references/design-decisions.md) — architecture or plans
- [Testing](../references/testing.md) — behavior or tests
- [Security](../references/security.md) — trust boundaries or sensitive data
- [Contributing](../references/contributing.md) — contribution process

## Procedure

1. Determine review target and base. Fetch complete diff and metadata without
   modifying work. If git, network, or platform APIs are unavailable, review
   user-provided or locally available material, state missing context, and request
   only information required for a reliable verdict.
2. Read repository instructions and changed files in full where context matters.
3. Identify intent, affected contracts, and associated issue/decision/plan.
4. Walk every changed file before reporting. Check:
   - correctness, edge cases, error handling, and concurrency
   - security and trust boundaries
   - compatibility, migrations, and rollout risk
   - tests: coverage quality, determinism, and realistic wiring
   - docs and decision/plan alignment
   - repository coding and contribution standards
5. Validate suspected defects with code paths, tests, docs, or reproducible
   reasoning. Do not report speculative style preferences as bugs.
6. Build complete findings list, ordered by severity. Each finding includes file,
   line/range, concrete failure mode, and smallest useful remediation.
7. If no findings, say so and list residual test/verification gaps.
8. Before posting comments, submitting verdict, or editing local work, get user
   approval unless request explicitly authorizes those actions.

## Severity

Use [review emoji legend](../references/review-emoji-legend.md) as single source
for finding severity and overall verdict. Follow repository-specific labels or
review vocabulary when present.

## Output

Findings first, concise and evidence-based. Include file/line references. Prefix
posted findings and verdicts using the review emoji legend; use same prefixes in
chat when useful for consistent disposition. Do not bury “no findings” behind
summary prose or claim approval when validation was incomplete.
