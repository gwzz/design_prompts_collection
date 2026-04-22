# design_prompts_collection

Static site source lives in `site/`.

## GitHub -> Vercel auto deploy

This repo is configured to deploy to Vercel with GitHub Actions.

1. Create a Vercel project and set its Root Directory to `site`.
2. In Vercel, open the project and get:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
3. In GitHub, go to `Settings -> Secrets and variables -> Actions` and add those three repository secrets.
4. Push to the `main` branch.

The workflow file is `.github/workflows/vercel-deploy.yml`.
