---
name: engineering-workflow
description: >
  Project-agnostic engineering workflow for non-trivial software work.
  Use whenever designing or implementing features, fixing meaningful bugs,
  reviewing code or pull requests, responding to review feedback, writing
  tests or technical documentation, introducing architecture or coding
  patterns, or deciding how work should be structured. Consult this skill
  even when user does not explicitly request an engineering workflow. It
  adapts to repository-local instructions, architecture records, language
  conventions, test tooling, and contribution rules instead of imposing a
  specific stack.
---

# Engineering Workflow

Use this skill as process guidance for non-trivial work in any software
repository. Apply guidance in this order: system and user instructions; explicit
current project policy; accepted architecture decisions; then established code
as evidence of precedent. Existing code may be legacy, defective, or insecure,
so never let precedent override safety requirements. Note meaningful conflicts
rather than silently inventing a third convention.

## Start with repository discovery

Before changing anything:

1. Read repository-level agent instructions and contributor guidance.
2. Inspect relevant code, tests, docs, build files, and recent nearby changes.
3. Identify established architecture, naming, testing, and documentation patterns.
4. Check working-tree and branch state before edits.
5. Load only task and reference files relevant to current request.
6. Record pre-existing modified and staged files. Preserve unrelated user work;
   never overwrite, revert, clean, reset, or restage it without approval.

Avoid treating absence of evidence as permission to impose personal preferences.
For new repositories with no precedent, propose lightweight defaults and explain
trade-offs.

## Tasks

| Request                                                  | Run                                                    |
| -------------------------------------------------------- | ------------------------------------------------------ |
| Design feature or architecture decision                  | [Design](tasks/design.md)                              |
| Implement accepted design, scoped change, tests, or docs | [Implement](tasks/implement.md)                        |
| Review PR/MR, commit, diff, or working tree              | [PR review](tasks/pr-review.md)                        |
| Address existing review feedback                         | [Respond to feedback](tasks/respond-to-pr-feedback.md) |
| Explain code or completed work in depth                  | [Explain](tasks/explain.md)                            |

Design → implement → review → feedback response forms full lifecycle. Small,
low-risk changes may combine design and implementation when repository policy
does not require a formal decision record.

## References

| Work                                                           | Read                                               |
| -------------------------------------------------------------- | -------------------------------------------------- |
| Architecture decisions, ADRs, plans, or roadmap changes        | [Design decisions](references/design-decisions.md) |
| Writing or reviewing code                                      | [Coding standards](references/coding-standards.md) |
| Adding or changing tests                                       | [Testing](references/testing.md)                   |
| Trust boundaries, dependencies, credentials, or sensitive data | [Security](references/security.md)                 |
| Docs, comments, changelogs, or commit messages                 | [Documentation](references/documentation.md)       |
| Giving feedback or resolving disagreements                     | [Collaboration](references/code-of-conduct.md)     |
| Preparing a change for contribution                            | [Contributing](references/contributing.md)         |

Most non-trivial work needs several references. Read matched files before
producing code, design, docs, or review findings.
