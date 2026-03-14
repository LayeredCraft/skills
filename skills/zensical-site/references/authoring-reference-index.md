# Authoring Reference Index

Use this page to decide which reference file to load for a task.

## How to use this index

1. Identify the user task type.
2. Load the matching core or subject reference.
3. Load dependency references only when a feature requires setup/runtime context.
4. If the user asks for advanced behavior, link out to upstream docs.

## Task routing

| User need | Open this reference first | Also check |
| --- | --- | --- |
| Write or rewrite a standard docs page | `core/markdown-and-links.md` | `shared-patterns.md`, `core/front-matter.md` |
| Set page metadata | `core/front-matter.md` | `dependencies/navigation-runtime-caveats.md` |
| Use admonitions, tabs, buttons, or tooltips | `subjects/callouts-and-interactive-elements.md` | `dependencies/extension-prereqs.md` |
| Add code snippets, diagrams, or equations | `subjects/code-and-technical-content.md` | `dependencies/extension-prereqs.md`, `dependencies/navigation-runtime-caveats.md` |
| Build media-rich layouts | `subjects/layout-and-media.md` | `dependencies/customization-boundaries.md` |
| Create tables and structured data sections | `subjects/data-and-visualization.md` | `dependencies/extension-prereqs.md` |
| Improve text-level formatting and list structure | `subjects/inline-formatting-and-microcontent.md` | `shared-patterns.md` |
| Figure out whether custom CSS/JS/templates are needed | `dependencies/customization-boundaries.md` | upstream customization docs |

## When to escalate to upstream docs

Escalate (link out) when the task asks for:

- complex extension options not covered in these references
- deep theme customization or override internals
- unusual runtime behavior across multiple plugins
- edge-case compatibility behavior that affects production output

Use upstream links from `references/docs-reference-outline.md`.
