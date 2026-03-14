# Zensical Docs Reference Outline

Goal: define which docs to reference later when expanding the `zensical-site` skill, and what to extract from each.

## 1) Authoring docs to reference

- `https://zensical.org/docs/authoring/markdown/`
  - Pull later: baseline markdown rules, internal linking guidance, page-title precedence.
- `https://zensical.org/docs/authoring/frontmatter/`
  - Pull later: supported front matter keys, precedence/override behavior, layout/search-related keys.
- `https://zensical.org/docs/authoring/admonitions/`
  - Pull later: syntax variants, supported admonition types, required extension/config.
- `https://zensical.org/docs/authoring/buttons/`
  - Pull later: button syntax/classes, icon usage in buttons, extension requirements.
- `https://zensical.org/docs/authoring/code-blocks/`
  - Pull later: fenced code options (titles/line numbers/highlights/annotations/snippets), toggles, feature flags.
- `https://zensical.org/docs/authoring/content-tabs/`
  - Pull later: tab syntax, linked-tab behavior, nesting/anchor constraints.
- `https://zensical.org/docs/authoring/data-tables/`
  - Pull later: table syntax conventions, sorting integration, compatibility constraints.
- `https://zensical.org/docs/authoring/diagrams/`
  - Pull later: Mermaid setup, supported diagram families, customization hooks.
- `https://zensical.org/docs/authoring/footnotes/`
  - Pull later: reference/definition syntax, tooltip integration behavior.
- `https://zensical.org/docs/authoring/formatting/`
  - Pull later: inline formatting patterns, required extensions.
- `https://zensical.org/docs/authoring/grids/`
  - Pull later: card/grid container syntax, nesting rules, extension dependencies.
- `https://zensical.org/docs/authoring/icons-emojis/`
  - Pull later: shortcode conventions, icon naming rules, template usage.
- `https://zensical.org/docs/authoring/images/`
  - Pull later: alignment/captions/lazy-load patterns, light/dark asset behavior.
- `https://zensical.org/docs/authoring/lists/`
  - Pull later: list-type syntax (unordered/ordered/definition/task), extension requirements.
- `https://zensical.org/docs/authoring/math/`
  - Pull later: MathJax vs KaTeX options, delimiter conventions, navigation integration caveats.
- `https://zensical.org/docs/authoring/tooltips/`
  - Pull later: tooltip and abbreviation syntax, glossary automation behavior.

## 2) Cross-reference docs required for authoring correctness

- `https://zensical.org/docs/setup/basics/#use_directory_urls`
  - Pull later: how URL mode changes link generation/resolution.
- `https://zensical.org/docs/setup/navigation/#instant-navigation`
  - Pull later: runtime navigation behavior impacting JS-backed features (math/diagrams/tables).
- `https://zensical.org/docs/setup/navigation/#hide-the-sidebars`
  - Pull later: sidebar/layout controls that affect page composition and front matter.
- `https://zensical.org/docs/setup/search/`
  - Pull later: metadata/indexing behavior tied to front matter and discoverability.
- `https://zensical.org/docs/setup/colors/`
  - Pull later: theme/palette behavior affecting rendering choices.
- `https://zensical.org/docs/setup/logo-and-icons/#additional-icons`
  - Pull later: custom icon registration and usage flow.
- `https://zensical.org/docs/setup/extensions/python-markdown/`
  - Pull later: base Python Markdown extension setup required by authoring features.
- `https://zensical.org/docs/setup/extensions/python-markdown-extensions/`
  - Pull later: pymdown extension setup/options used across many authoring features.
- `https://zensical.org/docs/customization/`
  - Pull later: CSS/JS/template override mechanisms for behavior and styling adjustments.
- `https://zensical.org/docs/customization/#additional-css`
  - Pull later: custom stylesheet integration points.
- `https://zensical.org/docs/customization/#additional-javascript`
  - Pull later: custom JS integration points.
- `https://zensical.org/docs/customization/#custom-templates`
  - Pull later: template customization entry points.
- `https://zensical.org/docs/customization/#configuring-overrides`
  - Pull later: override config structure and placement.
- `https://zensical.org/docs/customization/#template-overrides`
  - Pull later: template override behavior and scope.
- `https://zensical.org/docs/customization/#overriding-blocks`
  - Pull later: block-level extension points.
- `https://zensical.org/docs/customization/#extending-the-theme`
  - Pull later: theme extension strategy and boundaries.

## 3) Extraction template for the next pass

Use these fields when we return to pull details:

- `doc_url`
- `doc_title`
- `feature_area`
- `authoring_purpose`
- `required_config`
- `syntax_patterns`
- `options_modifiers`
- `dependencies`
- `behavioral_rules`
- `limitations_edge_cases`
- `cross_reference_urls`
- `minimal_examples_to_capture`
