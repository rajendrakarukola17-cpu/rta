// API Client for Backend Communication
import type { 
  ApiResponse, 
  ApiError, 
  User, 
  FileMetadata, 
  Folder, 
  AuthTokens, 
  LoginCredentials, 
  RegisterData,
  UploadProgress,
  DownloadUrl,
  ShareLink,
  SearchResult,
  StorageStats,
  ActivityLog,
  Notification,
  AppSettings
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setAuthToken(token: string) {
  accessToken = token;
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
}

export function clearAuthToken() {
  accessToken = null;
  refreshToken = null;
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

class ApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw {
          code: data.error?.code || 'UNKNOWN_ERROR',
          message: data.error?.message || 'An error occurred',
          details: data.error?.details,
        } as ApiError;
      }

      return data as ApiResponse<T>;
    } catch (error) {
      if ((error as ApiError).code === 'TOKEN_EXPIRED') {
        await this.refreshAccessToken();
        // Retry the request
        return this.request<T>(endpoint, options);
      }
      throw error;
    }
  }

  private async refreshAccessToken() {
    if (!refreshToken) {
      clearAuthToken();
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refreshToken }),
      });

      const data = await response.json();

      if (response.ok && data.data) {
        const tokens = data.data as AuthTokens;
        accessToken = tokens.accessToken;
        refreshToken = tokens.refreshToken;
        if (typeof window !== 'undefined') {
          localStorage.setItem('access_token', tokens.accessToken);
          localStorage.setItem('refresh_token', tokens.refreshToken);
        }
      } else {
        clearAuthToken();
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
      }
    } catch (error) {
      clearAuthToken();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
  }

  // Authentication APIs
  async login(credentials: LoginCredentials): Promise<ApiResponse<AuthTokens>> {
    const response = await this.request<AuthTokens>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    if (response.success && response.data) {
      accessToken = response.data.accessToken;
      refreshToken = response.data.refreshToken;
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.data.accessToken);
        localStorage.setItem('refresh_token', response.data.refreshToken);
      }
    }
    
    return response;
  }

  async register(data: RegisterData): Promise<ApiResponse<AuthTokens>> {
    const response = await this.request<AuthTokens>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    
    if (response.success && response.data) {
      accessToken = response.data.accessToken;
      refreshToken = response.data.refreshToken;
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.data.accessToken);
        localStorage.setItem('refresh_token', response.data.refreshToken);
      }
    }
    
    return response;
  }

  async logout(): Promise<void> {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } finally {
      clearAuthToken();
    }
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    return this.request<User>('/auth/me');
  }

  async refreshAccessToken(refreshTokenValue: string): Promise<AuthTokens> {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshTokenValue }),
    });

    const data = await response.json();

    if (response.ok && data.data) {
      const tokens = data.data as AuthTokens;
      accessToken = tokens.accessToken;
      refreshToken = tokens.refreshToken;
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', tokens.accessToken);
        localStorage.setItem('refresh_token', tokens.refreshToken);
      }
      return tokens;
    } else {
      clearAuthToken();
      throw new Error('Failed to refresh token');
    }
  }

  // File APIs
  async uploadFile(
    file: File,
    parentId?: string,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<ApiResponse<FileMetadata>> {
    const formData = new FormData();
    formData.append('file', file);
    if (parentId) {
      formData.append('parentId', parentId);
    }

    const xhr = new XMLHttpRequest();
    
    return new Promise((resolve, reject) => {
      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable && onProgress) {
          const progress = (event.loaded / event.total) * 100;
          onProgress({
            fileId: '',
            fileName: file.name,
            progress,
            speed: 0,
            eta: 0,
            status: 'uploading',
          });
        }
      });

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject(new Error(xhr.statusText));
        }
      });

      xhr.addEventListener('error', () => reject(new Error('Upload failed')));

      xhr.open('POST', `${API_BASE_URL}/files/upload`);
      if (this.accessToken) {
        xhr.setRequestHeader('Authorization', `Bearer ${this.accessToken}`);
      }
      xhr.send(formData);
    });
  }

  async getFiles(folderId?: string): Promise<ApiResponse<FileMetadata[]>> {
    const query = folderId ? `?folderId=${folderId}` : '';
    return this.request<FileMetadata[]>(`/files${query}`);
  }

  async getFile(fileId: string): Promise<ApiResponse<FileMetadata>> {
    return this.request<FileMetadata>(`/files/${fileId}`);
  }

  async downloadFile(fileId: string): Promise<ApiResponse<DownloadUrl>> {
    return this.request<DownloadUrl>(`/files/${fileId}/download`);
  }

  async deleteFile(fileId: string): Promise<ApiResponse<void>> {
    return this.request(`/files/${fileId}`, { method: 'DELETE' });
  }

  async moveFile(fileId: string, newParentId: string): Promise<ApiResponse<FileMetadata>> {
    return this.request<FileMetadata>(`/files/${fileId}/move`, {
      method: 'POST',
      body: JSON.stringify({ newParentId }),
    });
  }

  async renameFile(fileId: string, newName: string): Promise<ApiResponse<FileMetadata>> {
    return this.request<FileMetadata>(`/files/${fileId}/rename`, {
      method: 'POST',
      body: JSON.stringify({ newName }),
    });
  }

  // Folder APIs
  async createFolder(name: string, parentId?: string): Promise<ApiResponse<Folder>> {
    return this.request<Folder>('/folders', {
      method: 'POST',
      body: JSON.stringify({ name, parentId }),
    });
  }

  async getFolders(parentId?: string): Promise<ApiResponse<Folder[]>> {
    const query = parentId ? `?parentId=${parentId}` : '';
    return this.request<Folder[]>(`/folders${query}`);
  }

  async deleteFolder(folderId: string): Promise<ApiResponse<void>> {
    return this.request(`/folders/${folderId}`, { method: 'DELETE' });
  }

  // Search APIs
  async search(query: string): Promise<ApiResponse<SearchResult>> {
    return this.request<SearchResult>(`/search?q=${encodeURIComponent(query)}`);
  }

  // Storage APIs
  async getStorageStats(): Promise<ApiResponse<StorageStats[]>> {
    return this.request<StorageStats[]>('/storage/stats');
  }

  // Share APIs
  async createShareLink(
    fileId: string,
    options?: { password?: string; expiresAt?: Date; allowEdit?: boolean }
  ): Promise<ApiResponse<ShareLink>> {
    return this.request<ShareLink>(`/files/${fileId}/share`, {
      method: 'POST',
      body: JSON.stringify(options),
    });
  }

  async revokeShareLink(shareId: string): Promise<ApiResponse<void>> {
    return this.request(`/shares/${shareId}`, { method: 'DELETE' });
  }

  // Activity APIs
  async getActivityLog(limit?: number): Promise<ApiResponse<ActivityLog[]>> {
    const query = limit ? `?limit=${limit}` : '';
    return this.request<ActivityLog[]>(`/activity${query}`);
  }

  // Notification APIs
  async getNotifications(): Promise<ApiResponse<Notification[]>> {
    return this.request<Notification[]>('/notifications');
  }

  async markNotificationRead(notificationId: string): Promise<ApiResponse<void>> {
    return this.request(`/notifications/${notificationId}/read`, { method: 'POST' });
  }

  // Settings APIs
  async getSettings(): Promise<ApiResponse<AppSettings>> {
    return this.request<AppSettings>('/settings');
  }

  async updateSettings(settings: Partial<AppSettings>): Promise<ApiResponse<AppSettings>> {
    return this.request<AppSettings>('/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  }
}

export const api = new ApiClient();
export default api;
