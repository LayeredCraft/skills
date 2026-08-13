# LayeredCraft Skills

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

This repo is a shared home for installable agent skills.

## What this repo is for

- Publish reusable skills from a single repo
- Make it easy to install a specific skill by name
- Keep related skills together as the collection grows

## Available skills

| Skill                  | Description                                                                                                            | Install                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `git-workflow`         | Commit work, create branches, and open pull requests using conventional git workflow conventions                       | `npx skills add https://github.com/LayeredCraft/skills --skill git-workflow`         |
| `engineering-workflow` | Project-agnostic process for design, implementation, testing, review, feedback, security, and documentation            | `npx skills add https://github.com/LayeredCraft/skills --skill engineering-workflow` |
| `simple-dotnet-architecture` | Pragmatic .NET 8+ Minimal API, worker, and consumer architecture guidance | `npx skills add https://github.com/LayeredCraft/skills --skill simple-dotnet-architecture` |
| `zensical-site`        | Tooling and guidance for Zensical-flavored documentation work                                                          | `npx skills add https://github.com/LayeredCraft/skills --skill zensical-site`        |
| `partiql-dynamodb`     | DynamoDB-specific PartiQL guidance with focused references for statements, functions, operators, transactions, and IAM | `npx skills add https://github.com/LayeredCraft/skills --skill partiql-dynamodb`     |

## Install a skill

Use the repo URL and pass the skill name you want to install:

```bash
npx skills add https://github.com/LayeredCraft/skills --skill zensical-site
```

## Repo layout

- `skills/` - installable skills in this collection

## Skills

### `git-workflow`

Unified git workflow skill for committing, branching, and opening pull requests. Routes to the correct workflow based on your request.

- Commits using conventional commit format with automatic scope detection
- Creates branches using `<type>/<scope>-<short-description>` naming
- Runs the full PR workflow: branch, commit, push, and open PR from a template
- Shared rules for file inclusion, scope detection, and safety across all workflows
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill git-workflow`

### `engineering-workflow`

Project-agnostic workflow for non-trivial engineering work. Adapts to local repository policies and technology choices instead of imposing one stack.

- Routes design, implementation, review, feedback response, and explanation tasks
- Includes reusable guidance for coding, testing, security, documentation, decisions, and collaboration
- Preserves repository-local conventions while keeping safety requirements explicit
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill engineering-workflow`

### `simple-dotnet-architecture`

Pragmatic architecture guidance for .NET 8+ Minimal APIs, background workers, and message consumers.

- Starts with feature slices and clear delivery-edge boundaries
- Covers direct EF Core use, services and shared models, idempotency, outbox boundaries, and gradual complexity
- Includes focused references and code examples for APIs, workers, and consumers
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill simple-dotnet-architecture`

### `zensical-site`

Zensical-flavored documentation skill for structured authoring, reference-driven content work, and site-oriented documentation workflows.

- Best for teams building polished docs with consistent voice and formatting
- Includes supporting references and templates inside `skills/zensical-site`
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill zensical-site`

### `partiql-dynamodb`

DynamoDB PartiQL skill for statement syntax, practical usage guidance, caveats, and IAM-aware operational safety.

- Covers `SELECT`, `INSERT`, `UPDATE`, `DELETE`, built-in functions, operators, transactions, and batch operations
- Includes local references sourced from AWS DynamoDB PartiQL docs
- Adds source links in each reference page for traceability
- Install with `npx skills add https://github.com/LayeredCraft/skills --skill partiql-dynamodb`

## Licensing

Licensed under MIT. See `LICENSE`.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->

<!-- prettier-ignore-start -->

<!-- markdownlint-disable -->

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/j-d-ha"><img src="https://avatars.githubusercontent.com/u/61319894?v=4?s=100" width="100px;" alt="Jonas Ha"/><br /><sub><b>Jonas Ha</b></sub></a><br /><a href="https://github.com/LayeredCraft/skills/commits?author=j-d-ha" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ncipollina"><img src="https://avatars.githubusercontent.com/u/1405469?v=4?s=100" width="100px;" alt="Nick Cipollina"/><br /><sub><b>Nick Cipollina</b></sub></a><br /><a href="https://github.com/LayeredCraft/skills/commits?author=ncipollina" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->

<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
