# Office Suite v7.2

A self-hosted office suite with multi-cloud storage orchestration, designed for Oracle ARM Always Free VM.

## Status: Phase 1 Complete ✅

**Core Backend Foundation** - FastAPI backend with basic storage service integrations is now implemented.

## What's Implemented

### Backend Services (Phase 1)
- ✅ **FastAPI Application** (`backend/app/main.py`)
- ✅ **Configuration Management** (`backend/app/core/config.py`)
- ✅ **Database Layer** (`backend/app/core/database.py`)
- ✅ **Data Models** (`backend/app/models/__init__.py`)
- ✅ **MinIO Service** - Primary local storage (S3-compatible)
- ✅ **Cloudinary Service** - Media processing (25GB free tier)
- ✅ **Box Service** - Enterprise document storage (10GB free tier)
- ✅ **Celery Worker** - Background task processing

### Infrastructure
- ✅ PostgreSQL with pgvector
- ✅ Redis (for Celery broker/cache)
- ✅ MinIO (local S3-compatible storage)
- ✅ Docker Compose configuration
- ✅ Health checks and monitoring endpoints

## Quick Start

### 1. Clone and Configure
```bash
git clone <repository>
cd office-suite
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start services
```bash
docker-compose up -d postgres redis minio
docker-compose up -d fastapi worker
```

### 3. Verify
```bash
curl http://localhost:8000/health
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/api/v1/storage/services` | GET | List configured storage services |
| `/api/v1/storage/stats` | GET | Storage usage statistics |

## Storage Services

### Currently Implemented
1. **MinIO** - Primary hot storage (unlimited local)
2. **Cloudinary** - Media optimization (25GB free)
3. **Box** - Enterprise documents (10GB free)

### Planned (Future Phases)
- pCloud, Mega Cloud, ImageKit
- Backblaze B2, Cloudflare R2, Storj
- IBM COS, Tigris, Neon, Sia
- Box Dev Edition, Vercel Blob

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│  FastAPI     │────▶│  PostgreSQL │
│   (Vite)    │     │  Backend     │     │  + pgvector │
└─────────────┘     └──────────────┘     └─────────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
             ┌──────────┐  ┌──────────┐
             │  MinIO   │  │  Redis   │
             │ (Local)  │  │ (Cache)  │
             └──────────┘  └──────────┘
                    │
             ┌──────┴──────┐
             ▼             ▼
       ┌──────────┐  ┌──────────┐
       │Cloudinary│  │   Box    │
       │ (Media)  │  │ (Docs)   │
       └──────────┘  └──────────┘
```

## Development

### Backend Structure
```
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Config, database
│   ├── models/       # SQLAlchemy models
│   ├── services/     # Storage service integrations
│   └── utils/        # Utilities
├── requirements.txt
└── Dockerfile
```

### Running Tests
```bash
cd backend
pip install -r requirements.txt
pytest
```

## Configuration

See `.env.example` for all available environment variables. Key settings:

```bash
# Required
SECRET_KEY=your-secret-key
POSTGRES_PASSWORD=secure-password
REDIS_PASSWORD=secure-redis-password
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=secure-minio-password

# Optional - Cloud Services
CLOUDINARY_ENABLED=true
CLOUDINARY_CLOUD_NAME=your-cloud
BOX_ENABLED=true
BOX_CLIENT_ID=your-client-id
```

## Next Steps (Phase 2)

1. Implement file upload/download endpoints
2. Add authentication and user management
3. Implement remaining storage services
4. Add automatic fallback logic
5. Build frontend application

## Documentation

- `IMPLEMENTATION_STATUS.md` - Detailed status of implemented vs planned features
- `ARCHITECTURE.md` - System architecture documentation
- `docker-compose.yml` - Service definitions

## License

MIT License
