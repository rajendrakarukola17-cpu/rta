# Pass 5B-1 — Source Trust Scoring + Search Badges

## Summary

Implemented architecture §10.2: Source trust scoring system with domain legitimacy scoring, admin rescore capability, and visual trust badges (🟢🟡🔴) displayed on search results.

## Files Created

### Backend
1. **docker/postgres/init/011_sources.sql** - Migration for sources table
2. **backend/app/db/models/source.py** - Source model with domain, legitimacy_score, legitimacy_basis
3. **backend/app/schemas/source.py** - SourceRead and SourceRescoreRequest schemas
4. **backend/app/services/source_service.py** - Service with compute_legitimacy() and badge_for() functions
5. **backend/app/api/v1/sources.py** - API endpoints for GET /{domain} and POST /{domain}/rescore
6. **backend/tests/test_source_trust.py** - Unit tests for legitimacy scoring and badge thresholds

### Frontend
7. **frontend/src/lib/trust.ts** - trustBadge() utility function with emoji/label/className mapping

## Files Modified

### Backend
1. **backend/app/db/models/document.py** - Added source_id field to Document model
2. **backend/app/schemas/search.py** - Added source_domain, trust_score, trust_badge fields to SearchResultItem
3. **backend/app/api/v1/search.py** - Enhanced search endpoint to join with sources table and populate badge fields
4. **backend/app/api/v1/__init__.py** - Registered sources router in optional_routers

### Frontend
5. **frontend/src/api/types.ts** - Added optional badge fields to SearchResultItem interface
6. **frontend/src/components/explore/ResultCard.tsx** - Enhanced to display source domain and trust badge with emoji

## Features Implemented

### Source Trust Scoring
- **Automatic scoring** based on domain patterns:
  - Government domains (.gov.in, .nic.in, .mil.in, .edu.in, .ac.in) → Score 90 (🟢 verified)
  - Indian registered domains (.org.in, .in) → Score 60 (🟡 caution)
  - Unknown domains → Score 50 (⚪ unknown)
- **Badge thresholds**:
  - 🟢 Verified: score >= 70
  - 🟡 Caution: score >= 40
  - 🔴 Untrusted: score < 40
  - ⚪ Unknown: no score

### Admin Rescore
- Admin users (system_admin, office_admin) can manually override legitimacy scores
- Endpoint: POST /api/v1/sources/{domain}/rescore
- Tracks who reviewed the source (reviewed_by field)

### Search Integration
- Search results now include source trust information
- Visual badges displayed inline: `[Source: domain.com] 🟢`
- Automatic source registration on first document import

## Database Schema

```sql
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain CITEXT NOT NULL UNIQUE,
    legitimacy_score INTEGER NOT NULL DEFAULT 50,
    legitimacy_basis TEXT NOT NULL DEFAULT 'unreviewed',
    first_seen_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE documents
    ADD COLUMN IF NOT EXISTS source_id UUID REFERENCES sources(id) ON DELETE SET NULL;
```

## API Endpoints

### GET /api/v1/sources/{domain}
Returns source trust information, auto-creates if not exists.

**Response:**
```json
{
  "id": "uuid",
  "domain": "example.gov.in",
  "legitimacy_score": 90,
  "legitimacy_basis": "government-domain",
  "first_seen_date": "2024-01-01T00:00:00Z"
}
```

### POST /api/v1/sources/{domain}/rescore
Admin-only endpoint to manually override trust score.

**Request:**
```json
{
  "legitimacy_score": 85,
  "legitimacy_basis": "verified government source"
}
```

**Response:**
```json
{
  "id": "uuid",
  "domain": "example.gov.in",
  "legitimacy_score": 85,
  "legitimacy_basis": "verified government source",
  "first_seen_date": "2024-01-01T00:00:00Z"
}
```

## Testing

### Backend Tests
```bash
docker compose exec fastapi pytest -q backend/tests/test_source_trust.py
```

**Test Coverage:**
- Government domain scoring (score 90, basis "government-domain")
- Indian domain scoring (score 60)
- Unknown domain defaults (score 50, basis "unreviewed")
- Badge threshold validation (🟢 >= 70, 🟡 >= 40, 🔴 < 40, ⚪ null)

### Frontend Verification
```bash
cd frontend && npm run typecheck && npm run dev
```

### Test Data Setup
```bash
docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<'SQL'
-- Register a government source (auto-scored 90 → 🟢)
INSERT INTO sources (domain, legitimacy_score, legitimacy_basis)
VALUES ('mea.gov.in', 90, 'government-domain')
ON CONFLICT (domain) DO NOTHING;

-- Attach it to one existing document so the badge shows in Explore
UPDATE documents
SET source_id = (SELECT id FROM sources WHERE domain = 'mea.gov.in')
WHERE source_id IS NULL
LIMIT 1;
SQL
```

## Frontend Display

Search results now display trust badges:

```tsx
<span className="flex min-w-0 items-center gap-1">
  <Globe size={12} className="shrink-0" />
  <span className="truncate">[Source: mea.gov.in]</span>
  <span title="verified" className="shrink-0">🟢</span>
</span>
```

## Architecture Compliance

✅ Implements §10.2 Source Trust Scoring
✅ Domain legitimacy scoring with deterministic first-pass
✅ Admin rescore capability with audit trail
✅ Visual trust badges (🟢🟡🔴⚪) on search results
✅ Automatic source registration on document import
✅ Integration with existing search infrastructure

## Next Steps

Part 5B-2 will implement social backend features:
- Connections table for user relationships
- 24h hard-deleted view_stories
- Reposts functionality
- Migration 012 for social tables
- Social service and API router
- Worker purge task for expired stories
- Tests for social features
