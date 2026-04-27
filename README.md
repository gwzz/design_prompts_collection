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
- Edit mock featured ranking seeds in `content/featured_stats.json`
- Run `python build.py`

Each prompt is stored independently, which makes the content layer easier to review and maintain.
The build validates required fields, duplicate numbers, duplicate slugs, and allowed mode/font values before generating the site.

## Builder modules

- `builder/content_loader.py`: loads prompt files and site config
- `builder/featured_stats.py`: scores and ranks mock featured engagement data
- `builder/themes.py`: theme tokens and category mapping
- `builder/assets.py`: generated CSS, JS, favicon, and OG asset templates
- `builder/renderers.py`: page HTML, `robots.txt`, and `sitemap.xml`
- `builder/build_site.py`: build orchestration

The build also generates:

- modular client-side scripts in `site/assets/`
- localized static pages in `site/en/` and `site/zh/`
- mock featured ranking and local browser engagement state for click/like prototyping
- SEO metadata in each page
- `robots.txt`
- `sitemap.xml`
- SVG favicon and Open Graph cover assets

## Deployment

Deploy this project by connecting the GitHub repository directly to Vercel.

For analytics-backed featured ranking and likes, configure these Vercel environment variables:

- `KV_REST_API_URL`
- `KV_REST_API_TOKEN`

The runtime also accepts the alternate variable names exported by some Upstash dashboards:

- `prompt_collection_KV_REST_API_URL`
- `prompt_collection_KV_REST_API_TOKEN`

Use the repository root as the Vercel project Root Directory so both `api/` functions and the generated `site/` output are included. The root `vercel.json` runs `python build.py` and serves `site/` as the output directory.

As of April 27, 2026, this project targets the current Vercel-compatible replacement for the sunset Vercel KV product: Upstash Redis exposed through `KV_REST_API_URL` and `KV_REST_API_TOKEN`.

Recommended Vercel setup:

- Import the repository into Vercel
- Set Root Directory to the repository root
- Add `KV_REST_API_URL` and `KV_REST_API_TOKEN`
- Redeploy after updating environment variables

## Notes

- If the production domain changes, update `site_url` in `content/site.json`
- The root page prefers `localStorage.preferredLocale`, then falls back to `navigator.language`
- `content/featured_stats.json` provides seeded engagement values and local fallback data when the API is unavailable
- `.env.example` shows the expected Redis REST variables for local or hosted setup
- Generated files inside `site/` should be committed if you want Vercel to deploy the latest static output directly from the repo
