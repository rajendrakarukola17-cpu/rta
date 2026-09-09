# Office Suite v7.2 - CHANGELOG

## [7.2.1] - 2024 - Major Infrastructure Update

### 🚀 Added

#### New Docker Containers (3)
- **Ollama** - Self-hosted embedding model for local AI processing
  - Image: `ollama/ollama:latest`
  - Resource limits: 2GB RAM, 2 CPUs
  - Internal only (no exposed ports)
  - Auto-unloads model after 5min idle (`OLLAMA_KEEP_ALIVE=5m`)
  - Limited to 1 parallel request (`OLLAMA_NUM_PARALLEL=1`)
  
- **Karakeep** - AI-powered bookmark manager
  - Image: `ghcr.io/karakeep-app/karakeep:latest`
  - Uses internal Ollama for free AI tagging
  - Integrated with PostgreSQL for storage
  - Optional Traefik routing for external access
  
- **PostgreSQL with PGVector** - Vector search extension
  - Upgraded from `postgres:16-alpine` to `pgvector/pgvector:pg16`
  - Enables semantic search on document embeddings
  - Supports 768-dimensional vectors (nomic-embed-text)

#### New Storage Services (5)
- **Tigris** (5GB) - Edge CDN with zero egress fees
  - Perfect for PDF previews and thumbnails
  - S3-compatible API
  - Falls back to Cloudflare R2
  
- **Neon Object Storage** (5GB) - Branch-isolated scratch space
  - Each Git branch gets isolated storage
  - Perfect for testing OCR/PII pipelines
  - Free during beta period
  
- **Sia** (50GB) - Decentralized encrypted archive
  - Client-side encryption (keys stay with you)
  - Perfect for finalized government PDFs
  - No fallback - truly decentralized
  
- **Box Developer Edition** (10GB) - API-first document overflow
  - Separate from regular Box
  - 250MB file upload limit
  - 1,000 AI units/month included
  
- **Vercel Blob** (1GB) - Frontend thumbnail cache
  - Hobby plan
  - Perfect for PDF.js generated thumbnails
  - Temporary storage before archival

#### New AI Tools (3)
- **Karakeep** - Self-hosted bookmark manager
  - AI auto-tagging via Ollama
  - Full-text search
  - Page archiving
  - REST API integration
  
- **PGVector** - PostgreSQL vector extension
  - Semantic similarity search
  - 768-dimensional embeddings
  - IVFFlat indexing for fast queries
  
- **Ollama** - Local embedding model
  - nomic-embed-text model
  - No external API costs
  - Runs inside Docker

### 🔄 Changed

#### Storage Routing Logic
Updated `storage_manager.py` with new purpose-based routing:

```python
# New routing purposes:
"edge_cdn" → Tigris → R2 (fallback)
"branch_scratch" → Neon → MinIO temp (fallback)
"decentralized_archive" → Sia (no fallback)
"api_overflow" → Box Dev → Box (fallback)
"frontend_thumbnail" → Vercel Blob → MinIO (fallback)

# Updated existing routes:
"backup" → Mega → B2 → IBM COS (Storj removed)
"compliance" → IBM COS → Sia (Storj removed)
"disaster_recovery" → Sia → IBM COS (Storj removed)
```

#### Docker Compose Updates
- PostgreSQL image upgraded to `pgvector/pgvector:pg16`
- Added Ollama service with resource constraints
- Added Karakeep service with Ollama integration
- Added `ollama_data` and `karakeep_data` volumes

#### AI Pipeline
New URL knowledge base pipeline:
1. FastAPI calls Karakeep REST API to save URL
2. Celery worker scrapes page and chunks text
3. Ollama generates embeddings (768 dimensions)
4. PGVector stores embeddings in PostgreSQL
5. Semantic search returns relevant URLs in milliseconds

### 🗑️ Removed

#### Storj Integration
**Reason:** Free tier reduced to only 30 days (April 2026)

**Removed from:**
- `storage_manager.py` - All Storj routing logic
- `ARCHITECTURE.md` - Storage architecture diagrams
- `STORAGE_ROLES.md` - Role assignments
- `FINAL_WORKSPACE.md` - Service listings
- `UPDATE_SUMMARY.md` - Update documentation

**Impact:**
- Total free storage reduced from 206GB to 181GB
- Backup chain: Mega → B2 → IBM COS (removed Storj)
- DR chain: Sia → IBM COS (removed Storj)

### 📊 Updated Statistics

#### Before (v7.2.0)
- Storage Services: 18 (10 original + 5 new + 3 AI tools)
- Total Free Storage: 206GB
- Docker Containers: 21

#### After (v7.2.1)
- Storage Services: 17 (13 storage + 3 AI tools + 1 removed)
- Total Free Storage: 181GB (-25GB from Storj removal)
- Docker Containers: 23 (+2: Ollama, Karakeep)

### 🔧 Configuration Changes

#### New Environment Variables
```bash
# Ollama Configuration
OLLAMA_ENABLED=true
OLLAMA_ENDPOINT=http://ollama:11434
OLLAMA_MODEL=nomic-embed-text

# Karakeep Configuration
KARAKEEP_ENABLED=true
KARAKEEP_API_URL=http://karakeep:3000
KARAKEEP_API_KEY=CHANGE_ME

# PGVector Configuration
PGVECTOR_ENABLED=true

# New Storage Services
TIGRIS_ENABLED=false
TIGRIS_ACCESS_KEY=CHANGE_ME
TIGRIS_SECRET_KEY=CHANGE_ME
TIGRIS_ENDPOINT=CHANGE_ME

NEON_STORAGE_ENABLED=false
NEON_STORAGE_API_KEY=CHANGE_ME
NEON_STORAGE_ENDPOINT=CHANGE_ME

SIA_ENABLED=false
SIA_API_PASSWORD=CHANGE_ME
SIA_API_ENDPOINT=http://localhost:9980

BOX_DEV_ENABLED=false
BOX_DEV_CLIENT_ID=CHANGE_ME
BOX_DEV_CLIENT_SECRET=CHANGE_ME

VERCEL_BLOB_ENABLED=false
VERCEL_BLOB_TOKEN=CHANGE_ME
```

#### Docker Compose Changes
```yaml
# PostgreSQL upgraded
postgres:
  image: pgvector/pgvector:pg16  # was: postgres:16-alpine

# New services added
ollama:
  image: ollama/ollama:latest
  environment:
    - OLLAMA_NUM_PARALLEL=1
    - OLLAMA_KEEP_ALIVE=5m

karakeep:
  image: ghcr.io/karakeep-app/karakeep:latest
  environment:
    - OLLAMA_BASE_URL=http://ollama:11434
    - OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

### 🚀 Deployment Steps

#### 1. Pull New Images
```bash
docker compose pull
docker exec -it ollama ollama pull nomic-embed-text
```

#### 2. Create Karakeep Database
```bash
docker exec -it postgres psql -U office_user -d postgres \
  -c "CREATE DATABASE karakeep;"
```

#### 3. Initialize PGVector Extension
```bash
docker exec -it postgres psql -U office_user -d office_suite \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

#### 4. Start Services
```bash
docker compose up -d
```

#### 5. Verify Services
```bash
docker compose ps
curl http://localhost:11434/api/tags  # Ollama
curl http://localhost:3000           # Karakeep
```

### 📝 Migration Notes

#### For Existing Deployments
1. **Backup your database** before upgrading
2. PostgreSQL image change requires careful migration:
   ```bash
   # Export data
   docker exec postgres pg_dumpall -U office_user > backup.sql
   
   # Stop old container
   docker compose stop postgres
   
   # Remove old volume (WARNING: This deletes data!)
   docker volume rm office-suite-v7_postgres_data
   
   # Start new container
   docker compose up -d postgres
   
   # Import data
   cat backup.sql | docker exec -i postgres psql -U office_user
   ```

3. **Pull Ollama model** (one-time, ~1GB download):
   ```bash
   docker exec -it ollama ollama pull nomic-embed-text
   ```

4. **Configure Karakeep**:
   - Access via `http://localhost:3000` (or Traefik route)
   - Set up admin account
   - Configure Ollama integration (already done via env vars)

### 🔒 Security Updates

- Ollama and Karakeep are **internal-only** (no exposed ports)
- All new API keys stored in `.env` (not hardcoded)
- Sia uses client-side encryption (keys never leave your device)
- PGVector queries use parameterized statements

### 📈 Performance Optimizations

- Ollama limited to 1 parallel request to prevent CPU overload
- Ollama auto-unloads model after 5min idle to save RAM
- PGVector uses IVFFlat indexing for fast similarity search
- Karakeep uses existing PostgreSQL (no additional database)

### 🐛 Bug Fixes

- Removed broken Storj integration (30-day free tier expired)
- Fixed storage routing fallback chains
- Updated all documentation to reflect current architecture

### 📚 Documentation Updates

- `ARCHITECTURE.md` - Updated storage architecture diagrams
- `STORAGE_ROLES.md` - Updated role assignments
- `FINAL_WORKSPACE.md` - Updated service listings
- `UPDATE_SUMMARY.md` - Comprehensive update summary
- `CHANGELOG.md` - This file

### ⚠️ Breaking Changes

1. **PostgreSQL Image Change**: Requires database migration (see Deployment Steps)
2. **Storj Removal**: Backup/DR chains updated, no longer uses Storj
3. **New Environment Variables**: Must configure Ollama, Karakeep, PGVector, and new storage services

### 🔮 Future Plans

- Implement Cloudflare Workers AI for heavy AI processing
- Add more embedding models to Ollama
- Expand Karakeep integration with document processing
- Add vector search to existing document search
- Implement automatic thumbnail generation with Vercel Blob

---

## [7.2.0] - 2024 - Initial Release

### Added
- Complete Office Suite v7.2 implementation
- 22 parts of code generation
- 10 storage services (135GB free tier)
- 6 AI agents
- Full frontend with React + TypeScript
- Docker Compose orchestration
- Comprehensive documentation

---

**For questions or issues, refer to:**
- `ARCHITECTURE.md` - System architecture
- `STORAGE_ROLES.md` - Storage service roles
- `docs/deployment.md` - Deployment guide
- `docs/runbook.md` - Operations guide
