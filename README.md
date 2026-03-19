# LayeredCraft Skills

This repo is a shared home for installable agent skills.

## What this repo is for

- Publish reusable skills from a single repo
- Make it easy to install a specific skill by name
- Keep related skills together as the collection grows

## Available skills

| Skill           | Description                                                                                          | Install                                                                       |
| --------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `commit-work`   | Stage all user-modified files and create a conventional commit message                               | `npx skills add https://github.com/LayeredCraft/skills --skill commit-work`   |
| `create-branch` | Create and switch to a new branch using inferred conventional naming                                 | `npx skills add https://github.com/LayeredCraft/skills --skill create-branch` |
| `open-pr`       | Create a branch if needed, commit changes, push, and open a pull request using the local PR template | `npx skills add https://github.com/LayeredCraft/skills --skill open-pr`       |
| `zensical-site` | Tooling and guidance for Zensical-flavored documentation work                                        | `npx skills add https://github.com/LayeredCraft/skills --skill zensical-site` |

## Install a skill

Use the repo URL and pass the skill name you want to install:

```bash
npx skills add https://github.com/LayeredCraft/skills --skill zensical-site
```

## Repo layout

- `skills/` - installable skills in this collection
- `skills-lock.json` - tracked skill dependency metadata

## Skills

### `commit-work`

Stages all user-modified files and creates a conventional commit. Infers commit type and scope from the changed files and folder structure.

- Handles modified, staged, unstaged, untracked, and deleted files
- Excludes only obvious junk artifacts (build output, swap files, secrets)
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill commit-work`

### `create-branch`

Creates and switches to a properly named branch based on the inferred change intent.

- Uses `<type>/<scope>-<short-description>` naming convention
- Infers type and scope from the current working changes
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill create-branch`

### `open-pr`

Runs the full PR workflow: creates a branch if needed, commits all changes with a conventional message, pushes to origin, and opens a pull request using the local PR template.

- Infers branch name, commit message, and PR title from the changes
- Populates the PR body from `templates/pull-request-template.md`
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill open-pr`

### `zensical-site`

Zensical-flavored documentation skill for structured authoring, reference-driven content work, and site-oriented documentation workflows.

- Best for teams building polished docs with consistent voice and formatting
- Includes supporting references and templates inside `skills/zensical-site`
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill zensical-site`

## Licensing

Licensed under MIT. See `LICENSE`.
