# Documentation

Match repository voice, format, terminology, and documentation tooling.

- Update docs in same change as behavior or public-contract changes.
- Distinguish current behavior, intended future behavior, and unsupported cases.
- Link decision records for rationale instead of duplicating long histories.
- Prefer examples that compile or can be validated.
- Keep code self-explanatory through names and structure. Comments explain why,
  constraints, invariants, or non-obvious algorithms—not line-by-line narration.
- Document public APIs according to language and project conventions, including
  error behavior, nullability, ordering, side effects, and compatibility notes.
- Update changelogs, migration notes, examples, generated references, and release
  notes when project policy requires them.
- Write commit messages and PR descriptions around intent and impact; diff already
  shows mechanics.
- Avoid claims such as “tested,” “secure,” or “backward compatible” without
  evidence.

If docs intentionally lag implementation due to generated publishing flow, update
source artifacts and run or identify required generation step.
