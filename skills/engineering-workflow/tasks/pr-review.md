# Task: PR review

Use to review pull requests, merge requests, platform-specific change sets,
commits, patches, diffs, or local working trees. Review both correctness and
repository-process conformance.

## Load first

Always:

- [Coding standards](../references/coding-standards.md)
- [Collaboration](../references/code-of-conduct.md)
- [Documentation](../references/documentation.md)

As relevant:

- [Design decisions](../references/design-decisions.md)
- [Testing](../references/testing.md)
- [Security](../references/security.md)
- [Contributing](../references/contributing.md)

## Procedure

1. Determine review target and base. Fetch complete diff and metadata without
   modifying work.
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

- **Blocking**: correctness, security, data loss, broken contract, or required
  validation gap that must be fixed before merge.
- **Important**: real maintainability, reliability, or coverage issue worth fixing
  now or tracking explicitly.
- **Suggestion**: optional improvement or preference.
- **Question**: clarification needed before judging issue.

Follow repository-specific labels or review vocabulary when present.

## Output

Findings first, concise and evidence-based. Include file/line references. Do not
bury “no findings” behind summary prose or claim approval when validation was
incomplete.
