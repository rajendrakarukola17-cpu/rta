# Office Suite v7.2 — Final Storage Roles & Maximum Utilization

## 🎯 Storage Service Role Assignment

Each storage service has a **specific, dedicated role** to maximize free tier usage and avoid overlap.

---

## 📊 Role Assignment Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    STORAGE SERVICE ROLE ASSIGNMENT (18 SERVICES)                 │
│                                                                                  │
│  STORAGE SERVICES (10):                                                          │
│  Service          │ Role                    │ Free Tier │ Primary Use Case        │
│  ─────────────────┼─────────────────────────┼───────────┼──────────────────────── │
│  MinIO (local)    │ 🔥 HOT STORAGE          │ Unlimited │ Active working files    │
│  Cloudinary       │ 🎬 MEDIA ENGINE         │ 25 GB     │ Images + Videos         │
│  ImageKit         │ 🖼️ IMAGE PROCESSOR      │ 20 GB     │ Image transforms        │
│  Box              │ 📁 ENTERPRISE COLLAB    │ 10 GB     │ Team documents          │
│  pCloud           │ 👤 USER PERSONAL        │ 10 GB     │ User file sync          │
│  Mega Cloud       │ 🔒 PRIMARY BACKUP       │ 25 GB     │ Encrypted backups       │
│  Backblaze B2     │ 💰 SECONDARY BACKUP     │ 10 GB     │ Cost-effective          │
│  Cloudflare R2    │ 🌐 CDN DELIVERY         │ 10 GB     │ Public assets           │
│  Storj            │ 🛡️ DISASTER RECOVERY    │ 25 GB     │ Decentralized DR        │
│  IBM COS          │ 🗄️ COMPLIANCE ARCHIVE   │ Free tier │ Long-term retention     │
│                                                                                  │
│  NEW STORAGE SERVICES (5):                                                       │
│  Service          │ Role                    │ Free Tier │ Primary Use Case        │
│  ─────────────────┼─────────────────────────┼───────────┼──────────────────────── │
│  Tigris           │ ⚡ EDGE CDN             │ 5 GB      │ PDF previews, zero egress│
│  Neon             │ 🌿 BRANCH SCRATCH       │ 5 GB      │ Testing OCR/PII         │
│  Sia              │ 🔐 DECENTRALIZED        │ 50 GB     │ Gov PDFs, E2E encrypted │
│  Box Dev          │ 📦 API OVERFLOW         │ 10 GB     │ App integrations        │
│  Vercel Blob      │ 🎨 FRONTEND THUMBNAILS  │ 1 GB      │ PDF.js cache            │
│                                                                                  │
│  AI TOOLS (3):                                                                   │
│  Tool             │ Role                    │ Type      │ Primary Use Case        │
│  ─────────────────┼─────────────────────────┼───────────┼──────────────────────── │
│  Karakeep         │ 🔖 BOOKMARK MANAGER     │ AI Tool   │ AI tagging, search      │
│  PGVector         │ 🧮 VECTOR SEARCH        │ Extension │ Semantic search         │
│  Ollama           │ 🤖 EMBEDDINGS           │ AI Model  │ Self-hosted vectors     │
│                                                                                  │
│  TOTAL FREE STORAGE: ~206 GB (135GB + 71GB new)                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔥 1. MinIO — HOT STORAGE (Primary Working Files)

### Role
**Active working files** — All files currently being used, edited, or processed.

### What Goes Here
- ✅ Documents being actively edited
- ✅ Recently uploaded files (last 30 days)
- ✅ Temporary processing files
- ✅ Thumbnails and previews
- ✅ Chat media (recent)
- ✅ User avatars and profile images

### Why MinIO
- Unlimited local storage (200GB VM disk)
- Fastest access (no network latency)
- S3-compatible API
- Full control over data

### Retention Policy
```
Active files: Keep indefinitely
Temp files: Delete after 24 hours
Processed files: Move to cold storage after 30 days
```

### Configuration
```env
MINIO_ROOT_USER=office_suite
MINIO_ROOT_PASSWORD=CHANGE_ME
MINIO_BUCKET_DOCUMENTS=documents
MINIO_BUCKET_TEMP=temp-uploads
MINIO_BUCKET_IMAGES=images
MINIO_BUCKET_CHAT_MEDIA=chat-media
```

---

## 🎬 2. Cloudinary — MEDIA ENGINE (Images + Videos)

### Role
**Primary media processing and delivery** — All images and videos go through Cloudinary first.

### What Goes Here
- ✅ User-uploaded images (auto-optimize)
- ✅ Profile pictures and avatars
- ✅ Document thumbnails
- ✅ Video uploads (auto-transcode)
- ✅ Media for feed posts
- ✅ Product images

### Why Cloudinary
- 25GB free tier (largest media storage)
- Automatic format conversion (WebP, AVIF)
- On-the-fly transformations
- Global CDN delivery
- Video transcoding

### Key Features Used
```python
# Auto-optimize images
optimized_url = cloudinary.optimize_image(
    public_id="avatar_123",
    width=400,
    quality="auto",
    format="webp"
)

# Generate thumbnails
thumbnail_url = cloudinary.create_thumbnail(
    public_id="document_456",
    width=200,
    height=200,
    crop="fill"
)

# Video upload with auto-transcode
video_result = cloudinary.upload_to_cloudinary(
    local_path="video.mp4",
    resource_type="video"
)
```

### Retention Policy
```
Active media: Keep indefinitely
Unused media: Delete after 90 days
Video files: Keep original + optimized versions
```

### Configuration
```env
CLOUDINARY_ENABLED=true
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

---

## 🖼️ 3. ImageKit — IMAGE PROCESSOR (Backup + Advanced Transforms)

### Role
**Secondary image processing** — Backup to Cloudinary + advanced transformations.

### What Goes Here
- ✅ Fallback when Cloudinary is down
- ✅ Advanced image transformations (watermarking, filters)
- ✅ Batch image processing
- ✅ Image format conversion
- ✅ Backup of critical images

### Why ImageKit
- 20GB free tier (second largest)
- Real-time transformations
- URL-based operations
- Good alternative to Cloudinary

### When to Use ImageKit
```python
# Use ImageKit when:
# 1. Cloudinary is unavailable (fallback)
# 2. Need advanced transformations not in Cloudinary
# 3. Batch processing images
# 4. Need URL-based transformations

if not cloudinary_available:
    result = imagekit.upload_to_imagekit(
        local_path="image.jpg",
        transformations={
            "width": 800,
            "quality": 85,
            "format": "webp",
            "effect": "sharpen"
        }
    )
```

### Retention Policy
```
Backup images: Keep 180 days
Processed images: Keep 90 days
Original uploads: Keep 30 days
```

### Configuration
```env
IMAGEKIT_ENABLED=true
IMAGEKIT_PUBLIC_KEY=your-public-key
IMAGEKIT_PRIVATE_KEY=your-private-key
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your-endpoint
```

---

## 📁 4. Box — ENTERPRISE COLLABORATION (Team Documents)

### Role
**Team document collaboration** — Shared documents for team workflows.

### What Goes Here
- ✅ Shared team documents
- ✅ Collaborative editing files
- ✅ Project documentation
- ✅ Meeting notes and agendas
- ✅ Policy documents
- ✅ HR documents

### Why Box
- 10GB free tier
- Enterprise-grade collaboration
- Version history
- Access controls
- Integration with office suites

### Use Cases
```python
# Upload shared team document
box.upload_to_box(
    local_path="policy.pdf",
    folder_id="team_policies",
    filename="Office Policy 2024.pdf"
)

# Share with team
box_file = box.get_file_info(file_id)
# Box handles sharing permissions automatically
```

### Retention Policy
```
Active documents: Keep indefinitely
Archived documents: Move to IBM COS after 1 year
Deleted documents: Keep 30 days (recoverable)
```

### Configuration
```env
BOX_ENABLED=true
BOX_CLIENT_ID=your-client-id
BOX_CLIENT_SECRET=your-client-secret
BOX_FOLDER_ID=0
```

---

## 👤 5. pCloud — USER PERSONAL STORAGE (File Sync)

### Role
**Personal user file sync** — Each user's personal file storage.

### What Goes Here
- ✅ User's personal documents
- ✅ User's downloaded files
- ✅ User's exported data
- ✅ User's backup files
- ✅ User's shared files (personal)

### Why pCloud
- 10GB free tier
- Simple sync client
- Cross-platform
- Easy file sharing
- Version history

### Use Cases
```python
# Upload user's personal file
pcloud.upload_to_pcloud(
    local_path="user_document.pdf",
    folder_id=user.pcloud_folder_id,
    filename="My Document.pdf"
)

# Sync user's files
user_files = pcloud.list_pcloud_files(folder_id=user.pcloud_folder_id)
```

### Retention Policy
```
User files: Keep while user is active
Deleted user files: Keep 90 days after account deletion
Inactive users: Archive after 1 year
```

### Configuration
```env
PCLOUD_ENABLED=true
PCLOUD_USERNAME=your-username
PCLOUD_PASSWORD=your-password
PCLOUD_FOLDER_ID=0
```

---

## 🔒 6. Mega Cloud — PRIMARY BACKUP (Encrypted)

### Role
**Primary encrypted backup** — All critical data backups go here first.

### What Goes Here
- ✅ Daily PostgreSQL backups (encrypted)
- ✅ Weekly MinIO backups
- ✅ Configuration backups
- ✅ User data exports
- ✅ Critical system backups

### Why Mega Cloud
- 25GB free tier (largest backup storage)
- End-to-end encryption
- Reliable and fast
- Good for large files

### Backup Schedule
```
Daily:   PostgreSQL database backup → Mega Cloud
Weekly:  MinIO object backup → Mega Cloud
Monthly: Full system backup → Mega Cloud
```

### Backup Flow
```python
# Daily database backup
backup_file = "/backups/postgres/db-2024-01-15.sql.gz"
mega.upload_to_mega(
    local_path=backup_file,
    remote_path="/OfficeSuite/backups/postgres"
)

# Weekly object backup
rclone sync minio:documents mega:OfficeSuite/backups/minio/documents
```

### Retention Policy
```
Daily backups: Keep 30 days
Weekly backups: Keep 12 weeks
Monthly backups: Keep 12 months
```

### Configuration
```env
MEGA_ENABLED=true
MEGA_EMAIL=your-email@example.com
MEGA_PASSWORD=your-password
MEGA_BACKUP_PATH=/OfficeSuite/backups
```

---

## 💰 7. Backblaze B2 — SECONDARY BACKUP (Cost-Effective)

### Role
**Secondary backup** — Backup of backups, cost-effective long-term storage.

### What Goes Here
- ✅ Backup of Mega Cloud backups
- ✅ Older backups (> 30 days)
- ✅ Compliance-required backups
- ✅ Disaster recovery copies

### Why B2
- 10GB free tier
- Very cost-effective ($0.005/GB/month after free tier)
- S3-compatible API
- Reliable and durable

### Backup Strategy
```python
# If Mega upload fails, try B2
try:
    mega.upload_to_mega(backup_file)
except:
    b2.upload_to_b2(backup_file, f"backups/{filename}")

# Move old backups from Mega to B2
if backup_age > 30 days:
    b2.upload_to_b2(backup_file, f"archive/{filename}")
    mega.delete_from_mega(remote_path)
```

### Retention Policy
```
Recent backups: Keep 90 days
Archive backups: Keep 1 year
Compliance backups: Keep 7 years
```

### Configuration
```env
B2_ENABLED=true
B2_APPLICATION_KEY_ID=your-key-id
B2_APPLICATION_KEY=your-key
B2_BUCKET=office-suite-b2
```

---

## 🌐 8. Cloudflare R2 — CDN DELIVERY (Public Assets)

### Role
**Public asset delivery** — Files that need to be served to end users globally.

### What Goes Here
- ✅ Public documents (shared links)
- ✅ Downloadable resources
- ✅ Public media files
- ✅ Static assets
- ✅ Exported reports

### Why R2
- 10GB free tier
- No egress fees (huge savings!)
- Global CDN (fast worldwide)
- S3-compatible API
- Integrated with Cloudflare

### Use Cases
```python
# Upload public document
r2.upload_to_r2(
    local_path="public-report.pdf",
    object_key="public/reports/2024/q1-report.pdf"
)

# Generate public URL (no auth required)
public_url = f"https://cdn.office.example.com/public/reports/2024/q1-report.pdf"
```

### Retention Policy
```
Public assets: Keep indefinitely
Expired links: Delete after link expires
Unused assets: Delete after 1 year
```

### Configuration
```env
R2_ENABLED=true
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET=office-suite-r2
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com
```

---

## 🛡️ 9. Storj — DISASTER RECOVERY (Decentralized)

### Role
**Disaster recovery** — Decentralized backup for catastrophic failures.

### What Goes Here
- ✅ Complete system backups
- ✅ Encrypted database dumps
- ✅ Critical configuration files
- ✅ User data archives
- ✅ Long-term archives

### Why Storj
- 25GB free tier (large DR storage)
- Decentralized (no single point of failure)
- End-to-end encryption
- Geographically distributed
- Cost-effective for archives

### Disaster Recovery Strategy
```python
# Monthly full system backup to Storj
system_backup = create_full_system_backup()
storj.upload_to_storj(
    local_path=system_backup,
    object_key=f"dr/system-backup-{date}.tar.gz"
)

# Quarterly user data archive
user_archive = export_all_user_data()
storj.upload_to_storj(
    local_path=user_archive,
    object_key=f"dr/user-archive-{quarter}.tar.gz"
)
```

### Retention Policy
```
System backups: Keep 1 year
User archives: Keep 3 years
Compliance data: Keep 7 years
```

### Configuration
```env
STORJ_ENABLED=true
STORJ_ACCESS_KEY=your-access-key
STORJ_BUCKET=office-suite-storj
STORJ_ENDPOINT=https://gateway.storjshare.io
```

---

## 🗄️ 10. IBM COS — COMPLIANCE ARCHIVE (Long-Term)

### Role
**Compliance and legal archive** — Long-term retention for regulatory requirements.

### What Goes Here
- ✅ Audit logs (7+ years)
- ✅ Financial records
- ✅ Legal documents
- ✅ Compliance reports
- ✅ Deleted user data (legal hold)

### Why IBM COS
- Free tier available
- Enterprise-grade compliance
- Glacier storage class (very cheap)
- S3-compatible API
- Good for regulatory requirements

### Compliance Strategy
```python
# Archive audit logs (keep 7 years)
audit_log_export = export_audit_logs(year=2024)
ibm_cos.upload_to_ibm_cos(
    local_path=audit_log_export,
    object_key="compliance/audit-logs/2024.json.gz",
    storage_class="GLACIER"  # Move to cold storage
)

# Legal hold for deleted users
deleted_user_data = export_deleted_user_data(user_id)
ibm_cos.upload_to_ibm_cos(
    local_path=deleted_user_data,
    object_key=f"compliance/legal-hold/user-{user_id}.tar.gz",
    storage_class="GLACIER"
)
```

### Retention Policy
```
Audit logs: Keep 7 years (GLACIER)
Financial records: Keep 10 years (GLACIER)
Legal holds: Keep indefinitely (GLACIER)
Compliance reports: Keep 5 years
```

### Configuration
```env
IBM_COS_ENABLED=true
IBM_COS_API_KEY=your-api-key
IBM_COS_SERVICE_INSTANCE_ID=your-instance-id
IBM_COS_BUCKET=office-suite-compliance
IBM_COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
IBM_COS_REGION=us-south
```

---

## 🔄 Storage Routing Logic

### File Type → Service Chain

```python
def route_file(filename: str, purpose: str) -> str:
    """Route file to appropriate storage service."""
    
    # BACKUPS → Mega → B2 → IBM COS
    if purpose == "backup":
        return ["mega", "b2", "ibm_cos"]
    
    # IMAGES → Cloudinary → ImageKit → MinIO → R2
    if is_image(filename):
        return ["cloudinary", "imagekit", "minio", "r2"]
    
    # VIDEOS → Cloudinary → MinIO → R2
    if is_video(filename):
        return ["cloudinary", "minio", "r2"]
    
    # TEAM DOCUMENTS → MinIO → Box → pCloud
    if purpose == "team_collab":
        return ["minio", "box", "pcloud"]
    
    # USER PERSONAL → MinIO → pCloud → Box
    if purpose == "user_personal":
        return ["minio", "pcloud", "box"]
    
    # PUBLIC ASSETS → MinIO → R2
    if purpose == "public":
        return ["minio", "r2"]
    
    # COMPLIANCE → IBM COS → Storj
    if purpose == "compliance":
        return ["ibm_cos", "storj"]
    
    # DISASTER RECOVERY → Storj → IBM COS
    if purpose == "disaster_recovery":
        return ["storj", "ibm_cos"]
    
    # DEFAULT → MinIO
    return ["minio"]
```

### Automatic Fallback Chain

```
Upload Request
     │
     ▼
┌──────────────┐
│ Primary      │──► Success? ──YES──► Return result
│ Service      │
└──────┬───────┘
       │ NO (error/timeout)
       ▼
┌──────────────┐
│ Secondary    │──► Success? ──YES──► Return result
│ Service      │
└──────┬───────┘
       │ NO
       ▼
┌──────────────┐
│ Tertiary     │──► Success? ──YES──► Return result
│ Service      │
└──────┬───────┘
       │ NO
       ▼
┌──────────────┐
│ Raise Error  │
└──────────────┘
```

---

## 📈 Maximum Utilization Strategy

### Monthly Storage Plan

```
Week 1:  Upload active files to MinIO
         ↓
Week 2:  Process images → Cloudinary + ImageKit
         ↓
Week 3:  Backup to Mega Cloud
         ↓
Week 4:  Archive old files → B2 + Storj
         ↓
Monthly: Compliance archive → IBM COS
```

### Storage Optimization

```python
# Move files based on age
def optimize_storage():
    # Files older than 30 days → Move from MinIO to cold storage
    old_files = get_files_older_than(days=30)
    for file in old_files:
        if file.type == "image":
            # Already in Cloudinary, remove from MinIO
            minio.delete(file.path)
        elif file.type == "document":
            # Move to Box for collaboration
            box.upload(file.path)
            minio.delete(file.path)
    
    # Files older than 90 days → Move to archive
    very_old_files = get_files_older_than(days=90)
    for file in very_old_files:
        b2.upload(file.path)
        minio.delete(file.path)
    
    # Files older than 1 year → Move to cold storage
    ancient_files = get_files_older_than(days=365)
    for file in ancient_files:
        ibm_cos.upload(file.path, storage_class="GLACIER")
        b2.delete(file.path)
```

### Cost Optimization

```
Hot Storage (MinIO):    Free (local disk)
Media (Cloudinary):     25GB free, then $0.0085/GB
Images (ImageKit):      20GB free, then $0.01/GB
Collab (Box):           10GB free, then $15/user/month
Personal (pCloud):      10GB free, then $4.99/month
Backup (Mega):          25GB free, then €9.99/month
Secondary (B2):         10GB free, then $0.005/GB
CDN (R2):               10GB free, $0.015/GB after
DR (Storj):             25GB free, then $0.004/GB
Compliance (IBM COS):   Free tier, then $0.018/GB

TOTAL COST WITH FREE TIERS: $0/month for ~135GB
```

---

## 🎯 Service Assignment Summary

| Service | Role | Free Tier | Best For |
|---------|------|-----------|----------|
| **MinIO** | 🔥 Hot Storage | Unlimited | Active files, fast access |
| **Cloudinary** | 🎬 Media Engine | 25GB | Images, videos, optimization |
| **ImageKit** | 🖼️ Image Processor | 20GB | Image transforms, fallback |
| **Box** | 📁 Enterprise Collab | 10GB | Team documents, sharing |
| **pCloud** | 👤 User Personal | 10GB | User files, sync |
| **Mega** | 🔒 Primary Backup | 25GB | Encrypted backups |
| **B2** | 💰 Secondary Backup | 10GB | Cost-effective backup |
| **R2** | 🌐 CDN Delivery | 10GB | Public assets, no egress fees |
| **Storj** | 🛡️ Disaster Recovery | 25GB | Decentralized DR |
| **IBM COS** | 🗄️ Compliance Archive | Free tier | Long-term retention |

---

## ✅ Implementation Checklist

- [ ] Configure all 10 storage services in `.env`
- [ ] Test each service individually
- [ ] Verify automatic fallback works
- [ ] Set up storage optimization cron job
- [ ] Monitor storage usage per service
- [ ] Implement lifecycle policies
- [ ] Test disaster recovery procedure
- [ ] Verify compliance archive retention
- [ ] Set up alerts for storage limits
- [ ] Document recovery procedures

---

## 🚀 Quick Start

```bash
# 1. Enable all services
cp .env.example .env
nano .env  # Fill in all credentials

# 2. Test storage manager
python -c "
from app.services.storage_manager import get_storage_stats
import asyncio
stats = asyncio.run(get_storage_stats())
print(f'Total free storage: {stats[\"total_free_storage_gb\"]}GB')
"

# 3. Upload test file
python -c "
from app.services.storage_manager import upload_file
import asyncio
result = asyncio.run(upload_file('/path/to/test.jpg', purpose='general'))
print(f'Uploaded to: {result[\"primary_service\"]}')
"
```

---

**All 10 storage services are now assigned specific roles for maximum utilization of free tiers!** 🎉

Total free storage: **~135GB** across all services.
