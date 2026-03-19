# LayeredCraft Skills

This repo is a shared home for installable agent skills.

## What this repo is for

- Publish reusable skills from a single repo
- Make it easy to install a specific skill by name
- Keep related skills together as the collection grows

## Available skills

| Skill           | Description                                                                                                   | Install                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `git-workflow`  | Commit work, create branches, and open pull requests using conventional git workflow conventions               | `npx skills add https://github.com/LayeredCraft/skills --skill git-workflow`   |
| `zensical-site` | Tooling and guidance for Zensical-flavored documentation work                                                 | `npx skills add https://github.com/LayeredCraft/skills --skill zensical-site`  |

## Install a skill

Use the repo URL and pass the skill name you want to install:

```bash
npx skills add https://github.com/LayeredCraft/skills --skill zensical-site
```

## Repo layout

- `skills/` - installable skills in this collection
- `skills-lock.json` - tracked skill dependency metadata

## Skills

### `git-workflow`

Unified git workflow skill for committing, branching, and opening pull requests. Routes to the correct workflow based on your request.

- Commits using conventional commit format with automatic scope detection
- Creates branches using `<type>/<scope>-<short-description>` naming
- Runs the full PR workflow: branch, commit, push, and open PR from a template
- Shared rules for file inclusion, scope detection, and safety across all workflows
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill git-workflow`

### `zensical-site`

Zensical-flavored documentation skill for structured authoring, reference-driven content work, and site-oriented documentation workflows.

- Best for teams building polished docs with consistent voice and formatting
- Includes supporting references and templates inside `skills/zensical-site`
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill zensical-site`

## Licensing

Licensed under MIT. See `LICENSE`.
