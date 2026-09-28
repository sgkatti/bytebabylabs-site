# Society Task Platform

Enterprise-oriented task management platform for a housing society committee and manager.

## Sprint 1

Sprint 1 establishes the application boundary and engineering foundation. Existing ByteBabyLabs tools remain untouched.

### Roles

- Chairman — create, assign, review and close tasks.
- Secretary — create, assign, review and close tasks.
- Treasurer — create, assign, review and close tasks.
- Manager — execute assigned tasks and report completion.

There is no public registration in production. User provisioning will be controlled, with credentials supplied through deployment secrets rather than committed to source control.

### Task lifecycle

ASSIGNED -> IN_PROGRESS -> COMPLETED -> REVIEWED

A task may be returned from review to IN_PROGRESS when follow-up is required.

### Target architecture

- Static frontend: Cloudflare Pages
- API: FastAPI on Render
- Persistent database: PostgreSQL-compatible managed service
- Source control and CI: GitHub
- Development: GitHub Codespaces
- Production secrets: deployment environment variables

Codespaces is the development/test environment; it is not the production runtime.

## Repository layout

society/
  backend/
    app/
      auth/
      audit/
      database/
      tasks/
      users/
    tests/
    requirements.txt
  frontend/
  docs/
  README.md

## Security principles

1. No passwords, tokens or production secrets in Git.
2. Authentication is enforced server-side.
3. Authorization is enforced server-side using roles.
4. No public registration endpoint.
5. State-changing requests use authenticated, protected sessions.
6. Task and role changes are auditable.
7. Production data does not depend on local filesystem persistence.

## Sprint roadmap

- Sprint 1: architecture, repository boundary, domain model, security baseline, CI skeleton.
- Sprint 2: backend authentication, users, database migrations and task APIs.
- Sprint 3: frontend dashboard and task workflow.
- Sprint 4: audit/review workflow, validation, hardening and UX polish.
- Sprint 5: deployment, DNS, production smoke tests and operational documentation.


## Local backend

From society/backend:

1. Set DATABASE_URL, SESSION_SECRET and FRONTEND_ORIGIN.
2. Run migrations with: alembic upgrade head
3. Provision the four controlled identities with: python -m app.bootstrap
4. Start the API with: uvicorn app.main:app --reload

The four provisioning identities map to Chairman, Secretary, Treasurer and Manager respectively. Password values are runtime secrets and must never be committed.
