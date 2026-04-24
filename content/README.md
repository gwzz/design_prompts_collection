# Content Structure

## Prompt files

Each prompt lives in its own directory:

```text
content/prompts/<slug>/prompt.json
```

Use `content/prompts/_template/prompt.json` as the starting point for a new style.

## Required prompt fields

- `number`: unique integer used for ordering
- `name`: display name
- `slug`: unique URL-safe identifier
- `mode`: `dark` or `light`
- `font`: `serif`, `sans-serif`, or `mono`
- `description`: short card summary
- `prompt`: full copy-ready prompt text

## Site config

`content/site.json` stores:

- site metadata
- category labels
- homepage UI copy
- detail page UI copy
