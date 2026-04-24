# Design Prompts Collection

A focused static website for browsing, filtering, previewing, and copying UI design prompts in English and Chinese.

## Overview

This project keeps the stack intentionally simple:

- `content/` stores source data and site metadata
- `builder/` contains the modular static site generator
- `site/` is the generated bilingual output deployed to Vercel
- `build.py` is the root build entrypoint

The site is static by design. Prompt content lives in per-style JSON files, the builder generates HTML files, and deployment publishes the generated `site/` directory.

## Local development

Build the site:

```bash
python build.py
```

After the build completes:

- `site/index.html` auto-routes visitors based on browser locale or saved language preference
- `site/en/` contains the English site
- `site/zh/` contains the Simplified Chinese site

## Content workflow

- Add or edit a prompt in `content/prompts/<slug>/prompt.json`
- Start from `content/prompts/_template/prompt.json` when creating a new style
- Edit site metadata, localized UI copy, and language labels in `content/site.json`
- Run `python build.py`

Each prompt is stored independently, which makes the content layer easier to review and maintain.
The build validates required fields, duplicate numbers, duplicate slugs, and allowed mode/font values before generating the site.

## Builder modules

- `builder/content_loader.py`: loads prompt files and site config
- `builder/themes.py`: theme tokens and category mapping
- `builder/assets.py`: generated CSS, JS, favicon, and OG asset templates
- `builder/renderers.py`: page HTML, `robots.txt`, and `sitemap.xml`
- `builder/build_site.py`: build orchestration

The build also generates:

- modular client-side scripts in `site/assets/`
- localized static pages in `site/en/` and `site/zh/`
- SEO metadata in each page
- `robots.txt`
- `sitemap.xml`
- SVG favicon and Open Graph cover assets

## Deployment

This repository includes GitHub Actions deployment to Vercel via `.github/workflows/vercel-deploy.yml`.

Required GitHub repository secrets:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

In Vercel, set the project Root Directory to `site`.

## Notes

- If the production domain changes, update `site_url` in `content/site.json`
- The root page prefers `localStorage.preferredLocale`, then falls back to `navigator.language`
- Generated files inside `site/` should be committed if you want Vercel to deploy the latest static output directly from the repo
