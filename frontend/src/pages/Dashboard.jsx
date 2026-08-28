import { useQuery } from '@tanstack/react-query';
import { Activity, Brain, HardDrive, MessageSquare, Zap, Loader2, CheckCircle, XCircle } from 'lucide-react';
import api from '../lib/api';

function StatCard({ title, value, trend, icon: Icon, color }) {
  return (
    <div className="p-5 border rounded-xl bg-card flex flex-col gap-4">
      <div className="flex items-start justify-between">
        <span className="font-semibold text-foreground">{title}</span>
        <div className={`h-10 w-10 rounded-full flex items-center justify-center ${color}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div>
        <span className="text-2xl font-bold">{value ?? '—'}</span>
        {trend && <p className="text-xs text-muted mt-1">{trend}</p>}
      </div>
    </div>
  );
}

function HealthRow({ name, status, latency }) {
  const ok = status === 'Connected' || status === 'OK';
  return (
    <div className="flex items-center justify-between p-3 border-b last:border-0">
      <span className="font-medium text-sm text-muted">{name}</span>
      <div className="flex items-center gap-2 text-sm">
        {latency != null && <span className="text-muted font-mono text-xs">{latency}ms</span>}
        {ok
          ? <CheckCircle className="h-4 w-4 text-green-500" />
          : <XCircle className="h-4 w-4 text-red-400" />}
        <span className={ok ? 'text-green-500' : 'text-red-400'}>{status}</span>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => api.get('/health').then(r => r.data.data),
    refetchInterval: 30000,
  });

  const { data: memories } = useQuery({
    queryKey: ['memories-count'],
    queryFn: () => api.get('/memory', { params: { page: 1, size: 1 } }).then(r => r.data),
  });

  const { data: conversations } = useQuery({
    queryKey: ['conversations-count'],
    queryFn: () => api.get('/chat/conversations', { params: { page: 1, size: 1 } }).then(r => r.data),
  });

  const { data: reports } = useQuery({
    queryKey: ['reports-count'],
    queryFn: () => api.get('/reports', { params: { page: 1, size: 1 } }).then(r => r.data),
  });

  const systems = health ? [
    { name: 'Database', status: health.database?.status, latency: health.database?.latency_ms },
    { name: 'Supabase', status: health.supabase?.status, latency: health.supabase?.latency_ms },
    { name: 'Hugging Face', status: health.huggingface?.status, latency: health.huggingface?.latency_ms },
    { name: 'API', status: 'Connected', latency: null },
  ] : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-foreground/90">Dashboard</h1>
        <p className="text-muted text-sm mt-2">Overview of your enterprise AI security platform.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Conversations" value={conversations?.meta?.total ?? '—'} trend="Total sessions" icon={MessageSquare} color="bg-blue-500/10 text-blue-400" />
        <StatCard title="Memories" value={memories?.meta?.total ?? '—'} trend="Stored embeddings" icon={Brain} color="bg-purple-500/10 text-purple-400" />
        <StatCard title="Reports" value={reports?.meta?.total ?? '—'} trend="Generated reports" icon={Activity} color="bg-orange-500/10 text-orange-400" />
        <StatCard title="Platform" value="Active" trend="All systems running" icon={Zap} color="bg-green-500/10 text-green-400" />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="border rounded-xl bg-card p-6">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            System Health
            {healthLoading && <Loader2 className="h-4 w-4 animate-spin text-muted" />}
          </h3>
          <div className="space-y-3">
            {systems.length > 0
              ? systems.map(s => <HealthRow key={s.name} {...s} />)
              : [1, 2, 3, 4].map(i => (
                <div key={i} className="h-12 rounded-lg bg-muted/10 animate-pulse" />
              ))}
          </div>
        </div>

        <div className="border rounded-xl bg-card p-6">
          <h3 className="font-semibold mb-4">Platform Info</h3>
          <div className="space-y-3 text-sm">
            {health ? (
              <>
                <div className="flex justify-between p-3 border-b">
                  <span className="text-muted font-medium">Version</span>
                  <span className="font-semibold text-foreground">{health.version ?? '1.0.0'}</span>
                </div>
                <div className="flex justify-between p-3 border-b">
                  <span className="text-muted font-medium">Environment</span>
                  <span className="font-semibold text-foreground capitalize">{health.environment ?? 'development'}</span>
                </div>
                <div className="flex justify-between p-3">
                  <span className="text-muted font-medium">API Status</span>
                  <span className="font-semibold text-green-500">Online</span>
                </div>
              </>
            ) : (
              [1, 2, 3].map(i => <div key={i} className="h-12 rounded-lg bg-muted/10 animate-pulse" />)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
