# Storage Services Integration Guide

## Overview
Office Suite v7.2 now integrates **9 storage services** with a total of **~135GB free storage** across multiple tiers and use cases.

---

## 📊 Storage Services Summary

| Service | Free Tier | Purpose | Status |
|---------|-----------|---------|--------|
| **Mega Cloud** | 25GB | Primary backup | ✅ Integrated |
| **IBM COS** | Free tier | Cold/archive storage | ✅ Integrated |
| **Box** | 10GB | Document overflow | ✅ Integrated |
| **pCloud** | 10GB | File sync/backup | ✅ Integrated |
| **Cloudinary** | 25GB | Media optimization | ✅ Integrated |
| **ImageKit** | 20GB | Image processing | ✅ Integrated |
| **Backblaze B2** | 10GB | Secondary backup | ✅ Original |
| **Cloudflare R2** | 10GB | CDN/warm storage | ✅ Original |
| **Storj** | 25GB | Decentralized archive | ✅ Original |

**Total Free Storage: ~135GB**

---

## 🎯 Storage Strategy by File Type

### 1. Documents & Files
```
Primary: MinIO (local)
Overflow: Box → pCloud → IBM COS
```

**Use Case:** General document storage, office files, PDFs
**Services Used:** MinIO, Box, pCloud, IBM COS

### 2. Images
```
Primary: Cloudinary (optimized)
Alternative: ImageKit (processing)
Fallback: MinIO → R2
```

**Use Case:** User uploads, avatars, product images
**Services Used:** Cloudinary, ImageKit, MinIO, R2

### 3. Media (Video/Audio)
```
Primary: Cloudinary (streaming)
Fallback: MinIO → R2
```

**Use Case:** Video uploads, audio files, streaming content
**Services Used:** Cloudinary, MinIO, R2

### 4. Backups
```
Priority: Mega Cloud → B2 → IBM COS → Storj → Local
```

**Use Case:** Database backups, system backups, disaster recovery
**Services Used:** Mega, B2, IBM COS, Storj

---

## 🔧 Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Mega Cloud (25GB)
MEGA_ENABLED=true
MEGA_EMAIL=your-email@example.com
MEGA_PASSWORD=your-password
MEGA_BACKUP_PATH=/OfficeSuite/backups

# IBM Cloud Object Storage
IBM_COS_ENABLED=true
IBM_COS_API_KEY=your-api-key
IBM_COS_SERVICE_INSTANCE_ID=your-instance-id
IBM_COS_BUCKET=office-suite-archive
IBM_COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
IBM_COS_REGION=us-south

# Box (10GB)
BOX_ENABLED=true
BOX_CLIENT_ID=your-client-id
BOX_CLIENT_SECRET=your-client-secret
BOX_FOLDER_ID=0

# pCloud (10GB)
PCLOUD_ENABLED=true
PCLOUD_USERNAME=your-username
PCLOUD_PASSWORD=your-password
PCLOUD_FOLDER_ID=0

# Cloudinary (25GB)
CLOUDINARY_ENABLED=true
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# ImageKit (20GB)
IMAGEKIT_ENABLED=true
IMAGEKIT_PUBLIC_KEY=your-public-key
IMAGEKIT_PRIVATE_KEY=your-private-key
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your-endpoint

# Backblaze B2 (10GB)
B2_ENABLED=true
B2_APPLICATION_KEY_ID=your-key-id
B2_APPLICATION_KEY=your-key
B2_BUCKET=office-suite-b2

# Cloudflare R2 (10GB)
R2_ENABLED=true
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET=office-suite-r2
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com

# Storj (25GB)
STORJ_ENABLED=true
STORJ_ACCESS_KEY=your-access-key
STORJ_BUCKET=office-suite-storj
STORJ_ENDPOINT=https://gateway.storjshare.io
```

---

## 📁 Service Files

### New Service Files Created

1. **`backend/app/services/box_storage_service.py`**
   - Box API integration
   - Upload, download, list, delete operations
   - OAuth2 authentication

2. **`backend/app/services/pcloud_storage_service.py`**
   - pCloud API integration
   - Upload, download, list, delete operations
   - Username/password authentication

3. **`backend/app/services/cloudinary_service.py`**
   - Cloudinary API integration
   - Image/video upload and optimization
   - Transformation URL generation
   - CDN delivery

4. **`backend/app/services/imagekit_service.py`**
   - ImageKit API integration
   - Image upload and processing
   - Real-time transformations
   - URL-based operations

5. **`backend/app/services/storage_manager.py`**
   - Unified storage manager
   - Intelligent file routing
   - Automatic fallback
   - Storage statistics

### Modified Files

1. **`backend/app/core/config.py`**
   - Added configuration for all 4 new services
   - Box, pCloud, Cloudinary, ImageKit settings

2. **`.env.example`**
   - Added environment variables for new services
   - Documentation for each service

3. **`IMPROVEMENTS.md`**
   - Updated with new storage services
   - Configuration examples
   - Use cases and impact

---

## 🚀 Usage Examples

### Upload a Document

```python
from app.services.storage_manager import upload_file

# Upload document (will use MinIO → Box → pCloud strategy)
result = await upload_file(
    local_path="/path/to/document.pdf",
    filename="report.pdf",
    purpose="general"
)

print(f"Uploaded to: {result['primary_service']}")
```

### Upload an Image (with optimization)

```python
from app.services.storage_manager import upload_file

# Upload image (will use Cloudinary → ImageKit → MinIO strategy)
result = await upload_file(
    local_path="/path/to/image.jpg",
    filename="avatar.jpg",
    purpose="general",
    optimize=True
)

# Get optimized URL
if result['primary_service'] == 'cloudinary':
    from app.services.cloudinary_service import optimize_image
    optimized_url = optimize_image(
        result['public_id'],
        width=800,
        quality=80,
        format='webp'
    )
```

### Upload a Backup

```python
from app.services.storage_manager import upload_file

# Upload backup (will use Mega → B2 → IBM COS → Storj strategy)
result = await upload_file(
    local_path="/backups/db-backup.sql.gz",
    filename="backup-2024-01-15.sql.gz",
    purpose="backup"
)

print(f"Backup stored in: {result['primary_service']}")
```

### Get Storage Statistics

```python
from app.services.storage_manager import get_storage_stats

stats = await get_storage_stats()

print(f"Total free storage: {stats['total_free_storage_gb']}GB")

for service, info in stats['services'].items():
    print(f"{service}: {info.get('free_gb', 'N/A')}GB free")
```

---

## 🔄 Automatic Fallback

The storage manager automatically handles failures:

1. **Primary service fails** → Try next service in chain
2. **All services fail** → Raise `StorageManagerError`
3. **Logging** → All failures are logged for debugging

Example fallback chain for images:
```
Cloudinary (25GB) → ImageKit (20GB) → MinIO (local) → R2 (10GB)
```

---

## 📈 Benefits

### Cost Savings
- **135GB free storage** across 9 services
- No upfront costs for small to medium deployments
- Pay-as-you-go only when exceeding free tiers

### Reliability
- **Multi-tier redundancy** - data stored in multiple locations
- **Automatic failover** - if one service fails, try next
- **Geographic distribution** - data stored across multiple regions

### Performance
- **CDN delivery** - Cloudinary and ImageKit provide global CDN
- **Image optimization** - automatic format conversion and compression
- **Fast uploads** - parallel uploads to multiple services

### Scalability
- **Start free** - use free tiers initially
- **Scale gradually** - upgrade to paid plans as needed
- **No vendor lock-in** - switch between services easily

---

## 🔒 Security

### Authentication
- **OAuth2** - Box uses OAuth2 for secure authentication
- **API Keys** - All services use API keys/secrets
- **Environment Variables** - Credentials stored securely in `.env`

### Data Protection
- **Encryption at rest** - All services encrypt stored data
- **HTTPS only** - All API calls use HTTPS
- **Access control** - Configurable folder/file permissions

### Compliance
- **GDPR ready** - Services provide data deletion APIs
- **DPDP compliant** - Indian data protection ready
- **Audit trails** - All operations logged

---

## 🧪 Testing

### Test Individual Services

```python
# Test Box
from app.services.box_storage_service import upload_to_box, is_box_enabled

if is_box_enabled():
    result = await upload_to_box("/path/to/test.txt")
    print(f"Box upload successful: {result['id']}")

# Test pCloud
from app.services.pcloud_storage_service import upload_to_pcloud, is_pcloud_enabled

if is_pcloud_enabled():
    result = await upload_to_pcloud("/path/to/test.txt")
    print(f"pCloud upload successful: {result['fileid']}")

# Test Cloudinary
from app.services.cloudinary_service import upload_to_cloudinary, is_cloudinary_enabled

if is_cloudinary_enabled():
    result = await upload_to_cloudinary("/path/to/test.jpg")
    print(f"Cloudinary upload successful: {result['public_id']}")

# Test ImageKit
from app.services.imagekit_service import upload_to_imagekit, is_imagekit_enabled

if is_imagekit_enabled():
    result = await upload_to_imagekit("/path/to/test.jpg")
    print(f"ImageKit upload successful: {result['fileId']}")
```

---

## 📚 Documentation

### Service Documentation

- **Box:** https://developer.box.com/
- **pCloud:** https://docs.pcloud.com/
- **Cloudinary:** https://cloudinary.com/documentation
- **ImageKit:** https://docs.imagekit.io/
- **Mega:** https://mega.io/developers
- **IBM COS:** https://cloud.ibm.com/docs/cloud-object-storage
- **B2:** https://www.backblaze.com/b2/docs/
- **R2:** https://developers.cloudflare.com/r2/
- **Storj:** https://docs.storj.io/

### Internal Documentation

- **IMPROVEMENTS.md** - Complete list of all improvements
- **STORAGE_SERVICES.md** - This file
- **API Documentation** - Auto-generated from code

---

## 🎓 Best Practices

### 1. Enable Services Gradually
Start with 2-3 services, then add more as needed:
```bash
# Phase 1: Core storage
MEGA_ENABLED=true
B2_ENABLED=true

# Phase 2: Add media optimization
CLOUDINARY_ENABLED=true
IMAGEKIT_ENABLED=true

# Phase 3: Add overflow storage
BOX_ENABLED=true
PCLOUD_ENABLED=true
```

### 2. Monitor Storage Usage
```python
stats = await get_storage_stats()
for service, info in stats['services'].items():
    used = info.get('used_gb', 0)
    total = info.get('total_gb', 0)
    if isinstance(total, (int, float)) and used / total > 0.8:
        print(f"Warning: {service} is 80% full!")
```

### 3. Use Appropriate Services
- **Documents:** MinIO → Box → pCloud
- **Images:** Cloudinary → ImageKit
- **Videos:** Cloudinary
- **Backups:** Mega → B2 → IBM COS

### 4. Implement Cleanup
```python
# Delete old files
from app.services.cloudinary_service import delete_from_cloudinary
await delete_from_cloudinary("old-image-id")

# Clean up backups
import os
os.remove("/backups/old-backup.sql.gz")
```

---

## 🆘 Troubleshooting

### Common Issues

**Issue:** "Service not enabled"
```bash
# Solution: Check .env file
grep "SERVICE_ENABLED" .env
# Make sure it's set to true
```

**Issue:** "Authentication failed"
```bash
# Solution: Verify credentials
# Check API keys in .env file
# Regenerate keys if expired
```

**Issue:** "Upload failed"
```bash
# Solution: Check logs
docker compose logs backend | grep "storage"
# Verify file exists and is accessible
ls -la /path/to/file
```

**Issue:** "All services failed"
```bash
# Solution: Check network connectivity
curl -I https://api.box.com
curl -I https://api.pcloud.com
# Verify firewall rules
```

---

## 📞 Support

### Service Support
- **Box:** https://support.box.com/
- **pCloud:** https://www.pcloud.com/policy/contact
- **Cloudinary:** https://support.cloudinary.com/
- **ImageKit:** https://imagekit.io/contact

### Project Support
- Check `IMPROVEMENTS.md` for implementation details
- Review service-specific documentation
- Check logs for error messages

---

## ✅ Checklist

Before going to production:

- [ ] Configure all storage services in `.env`
- [ ] Test each service individually
- [ ] Verify automatic fallback works
- [ ] Set up monitoring for storage usage
- [ ] Implement cleanup procedures
- [ ] Document service credentials securely
- [ ] Test backup and restore procedures
- [ ] Verify CDN delivery for images
- [ ] Check authentication for all services
- [ ] Review security settings

---

**Total Free Storage: ~135GB across 9 services** 🎉

All services are integrated and ready to use!
