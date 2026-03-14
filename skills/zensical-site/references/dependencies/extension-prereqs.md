# Dependencies: Extension Prerequisites

Use this page to check feature prerequisites before generating advanced syntax.

## Use this when

- a subject feature might depend on markdown extensions
- output behavior differs by installed extension stack
- you need to decide between advanced syntax and safe fallback syntax

## Feature-to-prerequisite map

- Admonitions -> markdown extension support for admonition blocks
- Buttons -> style/extension support for button classes
- Content tabs -> extension support for tabbed content syntax
- Advanced code block options -> code extension support
- Diagrams -> Mermaid support
- Math -> math renderer setup (MathJax or KaTeX path)
- Tooltips/abbreviations -> extension support
- Grids/cards/icons extras -> extension and/or theme support

## Safe default policy

- If prerequisite status is unknown, use a simpler markdown pattern.
- Add an `Open Questions` note when setup is required for the requested output.
- Do not invent extension names or settings.

## Verification checklist

- Is this feature in a dependency-heavy subject area?
- Is there a known extension requirement?
- Can a simpler equivalent communicate the same content?

## Deeper docs

- `https://zensical.org/docs/setup/extensions/python-markdown/`
- `https://zensical.org/docs/setup/extensions/python-markdown-extensions/`
