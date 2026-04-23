# Design Prompts Collection

A focused static website for browsing, filtering, previewing, and copying UI design prompts.

## Overview

This project keeps the stack intentionally simple:

- `content/` stores source data and site metadata
- `builder/` contains the static site generator
- `site/` is the generated output deployed to Vercel
- `build.py` is the root build entrypoint

The site is static by design. Content lives in JSON, the builder generates HTML files, and deployment publishes the generated `site/` directory.

## Local development

Build the site:

```bash
python build.py
```

After the build completes, open `site/index.html` locally or deploy the `site/` directory.

## Content workflow

- Edit prompt data in `content/prompts.json`
- Edit site metadata in `content/site.json`
- Run `python build.py`

The build also generates:

- modular client-side scripts in `site/assets/`
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
- Generated files inside `site/` should be committed if you want Vercel to deploy the latest static output directly from the repo
