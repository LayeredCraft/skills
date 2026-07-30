# Task: Respond to review feedback

Use for existing comments on pull requests, merge requests, patches, or other
review systems. Distinct from generating new review: fetch, classify, resolve,
verify, reply, then close threads where platform supports them.

## Load first

Always:

- [Coding standards](../references/coding-standards.md)
- [Documentation](../references/documentation.md)
- [Collaboration](../references/code-of-conduct.md)

As relevant:

- [Design decisions](../references/design-decisions.md)
- [Testing](../references/testing.md)
- [Security](../references/security.md)
- [Contributing](../references/contributing.md)

## Procedure

### 1. Fetch and triage

1. Fetch all feedback using platform's available APIs or tools, including
   pagination, replies, and resolution state where supported.
2. Skip resolved threads and comments already handled. Preserve stable record so
   reruns converge instead of replying repeatedly.
3. Classify each remaining item:
   - **Fix**: valid issue within scope.
   - **Defer**: valid but out of scope; needs explicit follow-up.
   - **No action**: already addressed, based on misunderstanding, praise, or
     non-actionable automation output.
4. Show classification, reasoning, and proposed response. Get user approval before
   each class of external mutation: creating follow-up records, pushing changes,
   posting replies, changing verdicts, or resolving threads—unless request already
   authorizes it explicitly.

### 2. Implement

5. Apply approved fixes as coherent batch. Preserve unrelated user work. Add
   regression tests and docs where needed. Record deferred work in repository's
   issue/plan mechanism only with approved external-write scope.
6. Run required validation and inspect final diff.
7. Commit and push only when requested or explicitly part of task.

### 3. Reply and resolve

8. Reply to each handled item with outcome and evidence. Link fixing commit or
   follow-up when available; explain no-action decisions respectfully.
9. Resolve threads after fix is pushed or decision is recorded when platform
   supports resolution. Otherwise leave clear reply trail.
10. Re-fetch status and report remaining unresolved feedback.

## Output

Approved fixes, validation evidence, replies on handled feedback, resolved threads,
and explicit list of anything remaining. Never claim feedback handled when change
exists only locally but reply implies it was pushed.
