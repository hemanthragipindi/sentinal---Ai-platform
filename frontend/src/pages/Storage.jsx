import { useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Upload, Download, Trash2, File, Loader2, HardDrive } from 'lucide-react';
import api from '../lib/api';

function formatBytes(bytes) {
  if (!bytes) return '0 B';
  const k = 1024, sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

export default function Storage() {
  const qc = useQueryClient();
  const inputRef = useRef();

  const { data, isLoading } = useQuery({
    queryKey: ['files'],
    queryFn: () => api.get('/storage', { params: { page: 1, size: 50 } }).then(r => r.data),
  });

  const upload = useMutation({
    mutationFn: async (file) => {
      const res = await api.post('/storage/upload', {
        bucket: 'sentinel-uploads',
        file_name: file.name,
        storage_path: `uploads/${Date.now()}_${file.name}`,
        mime_type: file.type,
        file_size: file.size,
      });
      return res.data.data;
    },
    onSuccess: () => qc.invalidateQueries(['files']),
  });

  const remove = useMutation({
    mutationFn: (id) => api.delete(`/storage/${id}`),
    onSuccess: () => qc.invalidateQueries(['files']),
  });

  const getDownload = useMutation({
    mutationFn: (id) => api.get(`/storage/${id}/download`).then(r => {
      const url = r.data.data?.download_url;
      if (url) window.open(url, '_blank');
    }),
  });

  const files = data?.data ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Storage</h1>
          <p className="text-muted text-sm mt-1">Manage documents, files, and uploads.</p>
        </div>
        <button
          onClick={() => inputRef.current?.click()}
          disabled={upload.isPending}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-60 transition-all"
        >
          {upload.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
          Upload
        </button>
        <input ref={inputRef} type="file" className="hidden" onChange={e => e.target.files[0] && upload.mutate(e.target.files[0])} />
      </div>

      {isLoading
        ? <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">{[1,2,3].map(i => <div key={i} className="h-24 rounded-xl border bg-muted/10 animate-pulse" />)}</div>
        : files.length === 0
          ? <div className="border rounded-xl bg-card p-12 flex flex-col items-center gap-3 text-muted"><HardDrive className="h-10 w-10 opacity-30" /><p className="text-sm">No files yet. Click upload to get started.</p></div>
          : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {files.map(f => (
                <div key={f.id} className="border rounded-xl bg-card p-4 flex flex-col gap-3 group hover:border-primary/30 transition-all">
                  <div className="flex items-start gap-3">
                    <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                      <File className="h-5 w-5 text-primary" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-sm truncate">{f.file_name}</p>
                      <p className="text-xs text-muted">{formatBytes(f.file_size)} · {f.mime_type}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => getDownload.mutate(f.id)} className="flex-1 flex items-center justify-center gap-1.5 py-1.5 border rounded-lg text-xs font-medium hover:bg-muted/10 transition-all">
                      <Download className="h-3.5 w-3.5" /> Download
                    </button>
                    <button onClick={() => remove.mutate(f.id)} className="p-1.5 rounded-lg border text-muted hover:text-red-400 hover:border-red-400/30 hover:bg-red-400/5 transition-all">
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
    </div>
  );
}
