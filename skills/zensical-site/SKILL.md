---
name: zensical-site
description: Use this skill whenever the user asks for anything related to https://zensical.org/ including researching pages, drafting or editing site copy, planning information architecture, writing Zensical-style markdown, extracting key points from docs, or preparing publish-ready content updates. Trigger even if the user does not explicitly mention "skill" or "zensical-style" but the work is clearly about zensical.org content.
---

# Zensical Site Assistant

Use this skill to create, revise, and organize content for `https://zensical.org/`.

This is a scaffold meant to be expanded over time.

## Goals

- Keep outputs aligned with Zensical voice and structure.
- Produce publish-ready markdown with clear headings and links.
- Ground every recommendation in source material from zensical.org when available.

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
3. Draft using the output template in this skill.
4. Run a quality pass for tone, structure, links, and factual consistency.
5. Return final markdown plus a short rationale and suggested next edits.

## Output format

Always provide:

1. `Draft` (markdown ready to paste into the site)
2. `Rationale` (2-5 bullets explaining important choices)
3. `Open Questions` (only when missing info blocks quality)

Use the page template in `templates/page-draft-template.md` unless the user requests another format.

## Writing guidance (initial)

- Prefer plain language and concrete examples.
- Keep paragraphs short and scannable.
- Use descriptive headings.
- Avoid hype and vague claims.
- Include links with meaningful anchor text.

## Sources and verification

- If browsing is available, reference exact pages used.
- Flag uncertainty instead of guessing.
- Do not invent product features, policies, or URLs.

## Customization checklist

When extending this scaffold later, prioritize:

1. Fill `references/voice-and-tone.md` with real examples from zensical.org.
2. Fill `references/content-types.md` with page-specific conventions.
3. Add reusable snippets for recurring page sections.
4. Add concrete do/don't examples based on accepted published pages.
