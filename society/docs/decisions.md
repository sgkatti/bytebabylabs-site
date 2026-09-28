# Architecture Decisions

## ADR-001: Isolate the society application

Decision: Keep the society platform under society/ during the free-tier phase.

Reason: Existing ByteBabyLabs tools remain stable while the new application can evolve independently. The structure also supports an eventual repository split.

## ADR-002: PostgreSQL instead of local SQLite

Decision: Use a managed PostgreSQL-compatible database for production persistence.

Reason: Free compute instances may restart or lose local filesystem state. Society tasks and audit history must survive deployments and restarts.

## ADR-003: Codespaces for development, Render for production API

Decision: Codespaces is the engineering workspace; the production API runs on a managed application host.

Reason: A development workspace is not a durable production runtime. Separating the two also gives us a conventional CI/CD deployment path.

## ADR-004: No public registration

Decision: Initial production user identities are provisioned administratively.

Reason: The initial system has a deliberately closed four-user population. Removing public registration reduces attack surface and simplifies governance.
