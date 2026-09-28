# Deployment

## Backend — Render

Deploy the society/render.yaml file as a Render Blueprint. The service is stateless; PostgreSQL is external and persistent.

Required secrets/configuration:
- DATABASE_URL
- SESSION_SECRET
- FRONTEND_ORIGIN=https://tasks.bytebabylabs.com
- SOCIETY_USER_1_USERNAME / DISPLAY_NAME / PASSWORD
- SOCIETY_USER_2_USERNAME / DISPLAY_NAME / PASSWORD
- SOCIETY_USER_3_USERNAME / DISPLAY_NAME / PASSWORD
- SOCIETY_USER_4_USERNAME / DISPLAY_NAME / PASSWORD

The startup command runs migrations, bootstraps the four society accounts, and starts FastAPI.

## Frontend — Cloudflare Pages

Publish society/frontend/ as a static site. Configure the API origin in app.js before production deployment, or provide an environment-specific wrapper that defines window.SOCIETY_API_URL.

## API domain

Use a Render custom domain such as api-tasks.bytebabylabs.com for the FastAPI service. This keeps the frontend and API under the same registrable site while retaining separate origins for CORS and security policy.

## DNS

Create the custom domain tasks.bytebabylabs.com in the Cloudflare Pages project. Do not rely on an unassociated CNAME alone.

## Operational notes

- Render Free filesystem is ephemeral; the application stores no uploads locally.
- PostgreSQL must be a persistent external service.
- Never commit passwords, database URLs, or session secrets.
