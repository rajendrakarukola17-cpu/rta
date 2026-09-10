// Type definitions for Office Suite v7.2

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'user' | 'admin' | 'enterprise';
  storageUsed: number;
  storageLimit: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface FileMetadata {
  id: string;
  name: string;
  size: number;
  mimeType: string;
  path: string;
  storageProvider: StorageProvider;
  ownerId: string;
  isPublic: boolean;
  encrypted: boolean;
  checksum: string;
  version: number;
  parentId?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
  uploadedAt: Date;
}

export type StorageProvider = 
  | 'minio'
  | 'cloudinary'
  | 'box'
  | 'tigris'
  | 'sia'
  | 'neon'
  | 'vercel-blob'
  | 'local';

export interface StorageStats {
  provider: StorageProvider;
  used: number;
  limit: number;
  fileCount: number;
  lastSync?: Date;
}

export interface Folder {
  id: string;
  name: string;
  parentId?: string;
  ownerId: string;
  path: string;
  fileCount: number;
  folderCount: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface SearchResult {
  files: FileMetadata[];
  folders: Folder[];
  total: number;
  query: string;
}

export interface UploadProgress {
  fileId: string;
  fileName: string;
  progress: number;
  speed: number;
  eta: number;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error';
  error?: string;
}

export interface DownloadUrl {
  url: string;
  expiresAt: Date;
  directDownload?: boolean;
}

export interface ShareLink {
  id: string;
  fileId: string;
  token: string;
  password?: string;
  expiresAt?: Date;
  downloadLimit?: number;
  downloadCount: number;
  allowEdit: boolean;
  createdBy: string;
  createdAt: Date;
}

export interface ActivityLog {
  id: string;
  userId: string;
  action: ActivityAction;
  resourceId: string;
  resourceType: 'file' | 'folder' | 'share';
  details?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
  timestamp: Date;
}

export type ActivityAction =
  | 'upload'
  | 'download'
  | 'delete'
  | 'move'
  | 'rename'
  | 'share'
  | 'unshare'
  | 'login'
  | 'logout'
  | 'permission_change';

export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  read: boolean;
  actionUrl?: string;
  createdAt: Date;
}

export interface AppSettings {
  theme: 'dark' | 'light' | 'system';
  language: string;
  notifications: boolean;
  twoFactorEnabled: boolean;
  defaultStorageProvider: StorageProvider;
  autoBackup: boolean;
  compressImages: boolean;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}

export interface ApiError {
  code: string;
  message: string;
  details?: any;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
  twoFactorCode?: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
}
