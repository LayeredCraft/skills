# Agent instructions

## Skills

- Use `git-workflow` for every branch, commit, push, or pull-request task.
- Use `skill-creator` when creating or modifying a skill.
- A skill intended for later deployment with Skills Lock belongs in `skills/<skill-name>/`, never `.agents/`.
- To make that skill available locally through `.agents`, create `.agents/skills/<skill-name>` as a symbolic link to `../../skills/<skill-name>`.

## Repository conventions

- Follow existing skill layout: each skill has `SKILL.md` with required YAML frontmatter; keep optional resources inside that skill directory.
- Keep changes scoped. Match existing Markdown style and skill conventions.
- Run Markdown formatting for changed `.md` files when available. Inspect final diff for unintended changes.
- Do not commit generated caches, local configuration, credentials, or secrets.
