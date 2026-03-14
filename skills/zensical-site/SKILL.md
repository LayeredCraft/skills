---
name: zensical-site
description: Use this skill whenever the user asks for anything related to https://zensical.org/ including researching pages, drafting or editing site copy, planning information architecture, writing Zensical-style markdown, extracting key points from docs, or preparing publish-ready content updates. Trigger even if the user does not explicitly mention "skill" or "zensical-style" but the work is clearly about zensical.org content.
---

# Zensical Site Assistant

Use this skill to create, revise, and organize content for `https://zensical.org/`.

This skill is intentionally lightweight: use compact reference pages for output-critical rules, and link out to upstream docs for deep detail.

## When to use this skill

Use this skill if the user asks to:

- Draft new pages/posts for zensical.org.
- Rewrite existing copy for clarity, tone, or SEO.
- Build content outlines, page briefs, or navigation structure.
- Summarize or compare pages from zensical.org.
- Convert rough notes into Zensical-style markdown.

## Core workflow

1. Clarify the content objective (page type, audience, and intent).
2. Collect source material from zensical.org and any user-provided notes.
3. Open `references/authoring-reference-index.md` and load only the subject references needed for this task.
4. Draft using the output template in this skill.
5. Run a quality pass for tone, structure, links, front matter, and factual consistency.
6. Return final markdown plus a short rationale and suggested next edits.

## Output format

Always provide:

1. `Draft` (markdown ready to paste into the site)
2. `Rationale` (2-5 bullets explaining important choices)
3. `Open Questions` (only when missing info blocks quality)

Use the page template in `templates/page-draft-template.md` unless the user requests another format.

## Writing guidance

- Prefer plain language and concrete examples.
- Keep paragraphs short and scannable.
- Use descriptive headings.
- Avoid hype and vague claims.
- Include links with meaningful anchor text.

## Reference routing

Start with:

- `references/authoring-reference-index.md`

Then load only what is needed:

- `references/core/markdown-and-links.md` for links, heading structure, and title behavior.
- `references/core/front-matter.md` for page metadata.
- `references/subjects/callouts-and-interactive-elements.md` for admonitions, buttons, tabs, and tooltips.
- `references/subjects/code-and-technical-content.md` for code blocks, diagrams, and math.
- `references/subjects/layout-and-media.md` for grids, images, and icons/emojis.
- `references/subjects/data-and-visualization.md` for tables and structured visual content patterns.
- `references/subjects/inline-formatting-and-microcontent.md` for lists, inline formatting, and footnotes.

If output depends on setup/runtime behavior, load:

- `references/dependencies/extension-prereqs.md`
- `references/dependencies/navigation-runtime-caveats.md`
- `references/dependencies/customization-boundaries.md`

Use `references/shared-patterns.md` for common rules and shared conventions.

## Sources and verification

- If browsing is available, reference exact pages used.
- Flag uncertainty instead of guessing.
- Do not invent product features, policies, or URLs.
- If deeper implementation detail is needed, cite the relevant upstream Zensical doc rather than expanding these references inline.
