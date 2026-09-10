import React from 'react';
import { motion } from 'framer-motion';
import { useFiles, useFolders, useStorageStats } from '../hooks';
import { Card, Button, Badge, Skeleton, ProgressBar } from './ui';
import { MainLayout } from './layout';

const DashboardPage: React.FC = () => {
  const { files, loading: filesLoading } = useFiles();
  const { folders, loading: foldersLoading } = useFolders();
  const { stats, totalUsed, totalLimit, percentUsed, loading: statsLoading } = useStorageStats();

  const recentFiles = files.slice(0, 5);
  const storageProviders = [
    { name: 'MinIO', used: 25, limit: 50, color: 'from-blue-500 to-cyan-500' },
    { name: 'Cloudinary', used: 15, limit: 25, color: 'from-purple-500 to-pink-500' },
    { name: 'Box', used: 8, limit: 10, color: 'from-orange-500 to-red-500' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1 },
  };

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto">
        {/* Page Header */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gradient mb-2">Dashboard</h1>
          <p className="text-white/40">Welcome back! Here's an overview of your storage.</p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
        >
          {/* Total Storage */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
                </svg>
              </div>
              <Badge variant="info">{percentUsed.toFixed(0)}%</Badge>
            </div>
            {statsLoading ? (
              <Skeleton className="h-8 w-32 mb-2" />
            ) : (
              <>
                <p className="text-2xl font-bold text-white">{(totalUsed / 1024 / 1024 / 1024).toFixed(2)} GB</p>
                <p className="text-sm text-white/40">of {(totalLimit / 1024 / 1024 / 1024).toFixed(2)} GB used</p>
              </>
            )}
            <div className="mt-4">
              <ProgressBar value={percentUsed} variant={percentUsed > 90 ? 'error' : percentUsed > 75 ? 'warning' : 'success'} />
            </div>
          </Card>

          {/* Files Count */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <Badge variant="success">+12%</Badge>
            </div>
            {filesLoading ? (
              <Skeleton className="h-8 w-24 mb-2" />
            ) : (
              <>
                <p className="text-2xl font-bold text-white">{files.length}</p>
                <p className="text-sm text-white/40">Total files</p>
              </>
            )}
          </Card>

          {/* Folders Count */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
              </div>
            </div>
            {foldersLoading ? (
              <Skeleton className="h-8 w-24 mb-2" />
            ) : (
              <>
                <p className="text-2xl font-bold text-white">{folders.length}</p>
                <p className="text-sm text-white/40">Total folders</p>
              </>
            )}
          </Card>

          {/* Shared Files */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
              </div>
              <Badge variant="warning">3 new</Badge>
            </div>
            <p className="text-2xl font-bold text-white">24</p>
            <p className="text-sm text-white/40">Shared with you</p>
          </Card>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Files */}
          <div className="lg:col-span-2">
            <Card>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-white">Recent Files</h2>
                <Button variant="ghost" size="sm">View All</Button>
              </div>
              
              {filesLoading ? (
                <div className="space-y-3">
                  {[...Array(5)].map((_, i) => (
                    <Skeleton key={i} className="h-16 w-full" />
                  ))}
                </div>
              ) : recentFiles.length > 0 ? (
                <motion.div variants={containerVariants} initial="hidden" animate="show" className="space-y-2">
                  {recentFiles.map((file) => (
                    <motion.div
                      key={file.id}
                      variants={itemVariants}
                      className="flex items-center gap-4 p-3 rounded-xl hover:bg-white/5 transition-colors cursor-pointer group"
                    >
                      <div className="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center">
                        {file.mimeType.startsWith('image/') ? (
                          <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                        ) : file.mimeType.includes('pdf') ? (
                          <svg className="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                          </svg>
                        ) : (
                          <svg className="w-5 h-5 text-white/60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-white truncate">{file.name}</p>
                        <p className="text-xs text-white/40">{new Date(file.createdAt).toLocaleDateString()}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-white/60">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                        <Badge variant="default" size="sm" className="mt-1">{file.storageProvider}</Badge>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              ) : (
                <div className="text-center py-12">
                  <svg className="w-16 h-16 mx-auto text-white/20 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p className="text-white/40 mb-4">No files yet</p>
                  <Button variant="primary">Upload Your First File</Button>
                </div>
              )}
            </Card>
          </div>

          {/* Storage by Provider */}
          <div>
            <Card>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-white">Storage Providers</h2>
                <Button variant="ghost" size="sm">Manage</Button>
              </div>
              
              <div className="space-y-4">
                {storageProviders.map((provider) => (
                  <div key={provider.name} className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-white">{provider.name}</span>
                      <span className="text-sm text-white/40">{provider.used}GB / {provider.limit}GB</span>
                    </div>
                    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full bg-gradient-to-r ${provider.color} rounded-full`}
                        initial={{ width: 0 }}
                        animate={{ width: `${(provider.used / provider.limit) * 100}%` }}
                        transition={{ duration: 1, delay: 0.5 }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <Button variant="secondary" className="w-full mt-6">
                Add Storage Provider
              </Button>
            </Card>

            {/* Quick Actions */}
            <Card className="mt-6">
              <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
              <div className="space-y-2">
                <Button variant="secondary" className="w-full justify-start" leftIcon={
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                }>
                  Upload Files
                </Button>
                <Button variant="secondary" className="w-full justify-start" leftIcon={
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                  </svg>
                }>
                  Create Folder
                </Button>
                <Button variant="secondary" className="w-full justify-start" leftIcon={
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                }>
                  Share File
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;
