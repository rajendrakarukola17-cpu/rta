// React Hooks for Office Suite

import { useState, useEffect, useCallback } from 'react';
import api from '../lib/api';
import type { 
  User, 
  FileMetadata, 
  Folder, 
  UploadProgress, 
  Notification,
  StorageStats,
  ActivityLog,
  AppSettings
} from '../types';

// Auth Hook
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const response = await api.getCurrentUser();
      if (response.success && response.data) {
        setUser(response.data);
      }
    } catch (err) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setError(null);
    try {
      const response = await api.login({ email, password });
      if (response.success) {
        await loadUser();
        return { success: true };
      }
      return { success: false, error: response.error?.message };
    } catch (err: any) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  const logout = async () => {
    await api.logout();
    setUser(null);
  };

  return { user, loading, error, login, logout, refreshUser: loadUser };
}

// Files Hook
export function useFiles(folderId?: string) {
  const [files, setFiles] = useState<FileMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadFiles = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getFiles(folderId);
      if (response.success && response.data) {
        setFiles(response.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [folderId]);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const uploadFile = async (file: File, onProgress?: (progress: UploadProgress) => void) => {
    try {
      const response = await api.uploadFile(file, folderId, onProgress);
      if (response.success && response.data) {
        setFiles(prev => [...prev, response.data!]);
        return response.data;
      }
      throw new Error(response.error?.message);
    } catch (err: any) {
      throw err;
    }
  };

  const deleteFile = async (fileId: string) => {
    const response = await api.deleteFile(fileId);
    if (response.success) {
      setFiles(prev => prev.filter(f => f.id !== fileId));
    }
  };

  const renameFile = async (fileId: string, newName: string) => {
    const response = await api.renameFile(fileId, newName);
    if (response.success && response.data) {
      setFiles(prev => prev.map(f => f.id === fileId ? response.data! : f));
    }
  };

  return { files, loading, error, refreshFiles: loadFiles, uploadFile, deleteFile, renameFile };
}

// Folders Hook
export function useFolders(parentId?: string) {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadFolders = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getFolders(parentId);
      if (response.success && response.data) {
        setFolders(response.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [parentId]);

  useEffect(() => {
    loadFolders();
  }, [loadFolders]);

  const createFolder = async (name: string) => {
    const response = await api.createFolder(name, parentId);
    if (response.success && response.data) {
      setFolders(prev => [...prev, response.data!]);
      return response.data;
    }
    throw new Error(response.error?.message);
  };

  const deleteFolder = async (folderId: string) => {
    const response = await api.deleteFolder(folderId);
    if (response.success) {
      setFolders(prev => prev.filter(f => f.id !== folderId));
    }
  };

  return { folders, loading, error, refreshFolders: loadFolders, createFolder, deleteFolder };
}

// Storage Stats Hook
export function useStorageStats() {
  const [stats, setStats] = useState<StorageStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await api.getStorageStats();
      if (response.success && response.data) {
        setStats(response.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const totalUsed = stats.reduce((sum, s) => sum + s.used, 0);
  const totalLimit = stats.reduce((sum, s) => sum + s.limit, 0);
  const percentUsed = totalLimit > 0 ? (totalUsed / totalLimit) * 100 : 0;

  return { stats, loading, error, totalUsed, totalLimit, percentUsed, refreshStats: loadStats };
}

// Notifications Hook
export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const response = await api.getNotifications();
      if (response.success && response.data) {
        setNotifications(response.data);
        setUnreadCount(response.data.filter(n => !n.read).length);
      }
    } catch (err) {
      console.error('Failed to load notifications:', err);
    }
  };

  const markAsRead = async (notificationId: string) => {
    await api.markNotificationRead(notificationId);
    setNotifications(prev => 
      prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  return { notifications, unreadCount, markAsRead, refreshNotifications: loadNotifications };
}

// Activity Log Hook
export function useActivityLog(limit: number = 20) {
  const [activities, setActivities] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadActivities();
  }, [limit]);

  const loadActivities = async () => {
    try {
      const response = await api.getActivityLog(limit);
      if (response.success && response.data) {
        setActivities(response.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { activities, loading, error, refreshActivities: loadActivities };
}

// Settings Hook
export function useSettings() {
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await api.getSettings();
      if (response.success && response.data) {
        setSettings(response.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateSettings = async (newSettings: Partial<AppSettings>) => {
    const response = await api.updateSettings(newSettings);
    if (response.success && response.data) {
      setSettings(response.data);
      return true;
    }
    return false;
  };

  return { settings, loading, error, updateSettings, refreshSettings: loadSettings };
}
