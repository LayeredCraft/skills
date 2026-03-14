# TODO: Zensical Docs Capture Plan

Purpose: track the information we need to extract from each doc page before updating the `zensical-site` skill content.

## Capture fields to collect for every page

- [ ] `doc_title`
- [ ] `doc_url`
- [ ] `feature_area`
- [ ] `authoring_purpose`
- [ ] `required_config` (e.g. `zensical.toml`, `mkdocs.yml`, `theme.features`, extension flags)
- [ ] `syntax_patterns` (author-facing syntax we must generate correctly)
- [ ] `options_modifiers` (classes, attributes, fence options, toggles)
- [ ] `dependencies` (extensions/features/other docs)
- [ ] `behavioral_rules` (precedence, fallback, runtime behavior)
- [ ] `limitations_edge_cases`
- [ ] `cross_reference_urls`
- [ ] `minimal_examples_to_capture`

## Authoring pages

### Markdown
- [ ] Page: `https://zensical.org/docs/authoring/markdown/`
- [ ] Capture types needed: linking rules, markdown baseline, page-title precedence.

### Front matter
- [ ] Page: `https://zensical.org/docs/authoring/frontmatter/`
- [ ] Capture types needed: keys/schema, precedence/override behavior, layout/search metadata controls.

### Admonitions
- [ ] Page: `https://zensical.org/docs/authoring/admonitions/`
- [ ] Capture types needed: admonition syntax variants, type taxonomy, extension/config requirements.

### Buttons
- [ ] Page: `https://zensical.org/docs/authoring/buttons/`
- [ ] Capture types needed: button class syntax, icon-in-button patterns, prerequisites.

### Code blocks
- [ ] Page: `https://zensical.org/docs/authoring/code-blocks/`
- [ ] Capture types needed: fenced code options, highlighting/annotations/snippets, feature toggles.

### Content tabs
- [ ] Page: `https://zensical.org/docs/authoring/content-tabs/`
- [ ] Capture types needed: tab syntax, linked tabs behavior, nesting/anchor rules.

### Data tables
- [ ] Page: `https://zensical.org/docs/authoring/data-tables/`
- [ ] Capture types needed: table syntax conventions, sorting behavior, compatibility notes.

### Diagrams
- [ ] Page: `https://zensical.org/docs/authoring/diagrams/`
- [ ] Capture types needed: Mermaid setup, supported families, customization hooks.

### Footnotes
- [ ] Page: `https://zensical.org/docs/authoring/footnotes/`
- [ ] Capture types needed: reference/definition syntax, tooltip behavior.

### Formatting
- [ ] Page: `https://zensical.org/docs/authoring/formatting/`
- [ ] Capture types needed: inline formatting patterns, required extension mappings.

### Grids
- [ ] Page: `https://zensical.org/docs/authoring/grids/`
- [ ] Capture types needed: grid/card syntax, nesting rules, extension requirements.

### Icons and emojis
- [ ] Page: `https://zensical.org/docs/authoring/icons-emojis/`
- [ ] Capture types needed: shortcode conventions, icon naming, template usage patterns.

### Images
- [ ] Page: `https://zensical.org/docs/authoring/images/`
- [ ] Capture types needed: alignment/caption syntax, lazy-load rules, light/dark image behavior.

### Lists
- [ ] Page: `https://zensical.org/docs/authoring/lists/`
- [ ] Capture types needed: unordered/ordered/definition/task list syntax, extension dependencies.

### Math
- [ ] Page: `https://zensical.org/docs/authoring/math/`
- [ ] Capture types needed: MathJax vs KaTeX setup, delimiter rules, instant-navigation caveats.

### Tooltips
- [ ] Page: `https://zensical.org/docs/authoring/tooltips/`
- [ ] Capture types needed: tooltip syntax, abbreviation/glossary behavior.

## Cross-reference pages (authoring dependencies)

### Link and URL behavior
- [ ] Page: `https://zensical.org/docs/setup/basics/#use_directory_urls`
- [ ] Capture types needed: URL mode impacts on internal links and generated output paths.

### Navigation/runtime behavior
- [ ] Page: `https://zensical.org/docs/setup/navigation/#instant-navigation`
- [ ] Capture types needed: client-side navigation effects on JS-based authoring features.
- [ ] Page: `https://zensical.org/docs/setup/navigation/#hide-the-sidebars`
- [ ] Capture types needed: sidebar/layout controls that interact with page metadata.

### Search and discoverability
- [ ] Page: `https://zensical.org/docs/setup/search/`
- [ ] Capture types needed: indexing and metadata controls tied to front matter.

### Styling and icon dependencies
- [ ] Page: `https://zensical.org/docs/setup/colors/`
- [ ] Capture types needed: palette/scheme behavior affecting rendered authoring components.
- [ ] Page: `https://zensical.org/docs/setup/logo-and-icons/#additional-icons`
- [ ] Capture types needed: custom icon registration workflow and naming constraints.

### Extension configuration
- [ ] Page: `https://zensical.org/docs/setup/extensions/python-markdown/`
- [ ] Capture types needed: base Python Markdown extension setup and options.
- [ ] Page: `https://zensical.org/docs/setup/extensions/python-markdown-extensions/`
- [ ] Capture types needed: pymdown extension setup/options used across authoring pages.

### Customization and overrides
- [ ] Page: `https://zensical.org/docs/customization/`
- [ ] Capture types needed: overview of CSS/JS/template override mechanics.
- [ ] Page: `https://zensical.org/docs/customization/#additional-css`
- [ ] Capture types needed: stylesheet injection points and file placement.
- [ ] Page: `https://zensical.org/docs/customization/#additional-javascript`
- [ ] Capture types needed: script injection points and initialization expectations.
- [ ] Page: `https://zensical.org/docs/customization/#custom-templates`
- [ ] Capture types needed: custom template structure and usage boundaries.
- [ ] Page: `https://zensical.org/docs/customization/#configuring-overrides`
- [ ] Capture types needed: override config structure and path conventions.
- [ ] Page: `https://zensical.org/docs/customization/#template-overrides`
- [ ] Capture types needed: override scope and precedence.
- [ ] Page: `https://zensical.org/docs/customization/#overriding-blocks`
- [ ] Capture types needed: block-level extension points and constraints.
- [ ] Page: `https://zensical.org/docs/customization/#extending-the-theme`
- [ ] Capture types needed: theme-extension strategy and compatibility boundaries.
