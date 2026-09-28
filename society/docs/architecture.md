# Architecture

## Context

The platform manages operational tasks for a four-person housing society committee and manager role. The system is intentionally small in user count but follows production-oriented separation of concerns.

## Components

| Component | Responsibility |
|---|---|
| Cloudflare Pages | Static web frontend and custom subdomain |
| FastAPI | Authentication, authorization and REST API |
| PostgreSQL | Durable application state and audit records |
| GitHub | Source control, pull requests and CI |
| Codespaces | Development and test environment |
| Render | Production API runtime |

## Trust boundary

Browser -> HTTPS -> API -> Database

The browser is an untrusted client. Role checks must never rely on hidden buttons or frontend state. Every protected API operation validates the authenticated identity and role.

## Application boundary

The society application lives entirely under society/. It must not modify or depend on existing ByteBabyLabs tools unless an explicit integration is introduced later.

## Future migration

The application should be deployable from its own repository without changing domain logic. Configuration is environment-driven, so a future move to a paid database/API tier should primarily change infrastructure configuration rather than application code.
