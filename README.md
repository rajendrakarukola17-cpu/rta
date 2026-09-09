# Office Suite v7.2

Production-ready internal office platform based on Architecture v7.2-final.

## Core stack

- Backend: FastAPI + SQLAlchemy + Pydantic v2
- Worker: Celery
- Database: PostgreSQL
- Cache: Redis
- Object storage: MinIO
- Search: Typesense + PostgreSQL FTS + Qdrant
- Chat: Dendrite / Matrix
- Collaboration: CryptPad
- SSO: Authentik
- Reverse proxy: Traefik
- OCR: PaddleOCR
- Monitoring: Grafana + Loki
- Frontend: React + TypeScript + Vite + Tailwind + shadcn/ui
- Frontend hosting: Cloudflare Pages
- VM target: Oracle ARM Always Free VM

## Architecture constraints

- MongoDB is removed.
- Rocket.Chat is removed.
- PostgreSQL is the single durable source of truth.
- Redis is ephemeral only.
- Typesense and Qdrant are derived search indexes.
- MinIO is hot object storage.
- Cloudflare R2, Backblaze B2, and Storj are colder storage tiers.
- Human approval is required for AI-generated public content.
- Tapal routing proposals require human confirmation.
- PII redaction fails closed.
- Backups must be encrypted and restore-tested.

## Repository layout

```text
office-suite-v7/
├── README.md
├── Makefile
├── .env.example
├── docker-compose.yml
├── docker/
├── scripts/
├── ansible/
├── backend/
├── worker/
├── crawler/
├── frontend/
├── docs/
└── .qwen/
```

## Local development

```bash
cp .env.example .env
# Edit .env and fill in placeholder values
docker compose config
docker compose up -d traefik postgres redis minio typesense qdrant
```

## Production deployment

Primary server path:

```text
/opt/office-suite-v7
```

Typical production commands:

```bash
make health
make up
make logs
make backup-postgres
make restore-drill
```

## Frontend deployment

The frontend is deployed to Cloudflare Pages.

Build output directory:

```text
frontend/dist
```

Environment variables for the frontend build should point to the public API domain.

## Important operational rules

1. PostgreSQL backups must succeed nightly.
2. Restore drill must run weekly and fail loudly.
3. OCR workers must be memory-limited and isolated.
4. Search indexes must be rebuildable from PostgreSQL.
5. Admin dashboards must not be publicly exposed.
6. Secrets must never be committed.
7. AI output must be treated as draft until approved.

## Documentation

See:

```text
docs/deployment.md
docs/runbook.md
docs/backup-restore.md
docs/pilot-plan.md
docs/api.md
```
