import { useQuery } from '@tanstack/react-query';
import { ShieldAlert, ShieldCheck, AlertTriangle, Activity, Loader2 } from 'lucide-react';
import api from '../lib/api';

function Badge({ label, color }) {
  const colors = { low: 'bg-green-500/10 text-green-400 border-green-500/20', medium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20', high: 'bg-orange-500/10 text-orange-400 border-orange-500/20', critical: 'bg-red-500/10 text-red-400 border-red-500/20', open: 'bg-blue-500/10 text-blue-400 border-blue-500/20', resolved: 'bg-green-500/10 text-green-400 border-green-500/20' };
  return <span className={`px-2 py-0.5 rounded-full text-xs font-medium border capitalize ${colors[label] ?? 'bg-muted/20 text-muted border-muted/20'}`}>{label}</span>;
}

export default function Security() {
  const { data: eventsData, isLoading: eventsLoading } = useQuery({
    queryKey: ['audit-logs'],
    queryFn: () => api.get('/audit', { params: { page: 1, size: 20 } }).then(r => r.data),
    refetchInterval: 15000,
  });

  const events = eventsData?.data ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Security</h1>
        <p className="text-muted text-sm mt-1">Monitor threats, alerts, and audit logs.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {[
          { icon: ShieldCheck, label: 'Platform Status', value: 'Protected', color: 'text-green-400', bg: 'bg-green-500/10' },
          { icon: AlertTriangle, label: 'Open Threats', value: '—', color: 'text-orange-400', bg: 'bg-orange-500/10' },
          { icon: Activity, label: 'Audit Events', value: eventsData?.meta?.total ?? '—', color: 'text-blue-400', bg: 'bg-blue-500/10' },
        ].map(c => (
          <div key={c.label} className="border rounded-xl bg-card p-5 flex items-center gap-4">
            <div className={`h-10 w-10 rounded-xl ${c.bg} flex items-center justify-center shrink-0`}>
              <c.icon className={`h-5 w-5 ${c.color}`} />
            </div>
            <div>
              <p className="text-sm text-muted">{c.label}</p>
              <p className="text-xl font-bold">{c.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="border rounded-xl bg-card">
        <div className="p-4 border-b flex items-center justify-between">
          <h3 className="font-semibold">Recent Audit Logs</h3>
          {eventsLoading && <Loader2 className="h-4 w-4 animate-spin text-muted" />}
        </div>
        <div className="divide-y">
          {eventsLoading
            ? [1,2,3,4,5].map(i => <div key={i} className="h-14 mx-4 my-2 rounded-lg bg-muted/10 animate-pulse" />)
            : events.length === 0
              ? <div className="p-10 text-center text-muted text-sm"><ShieldCheck className="h-8 w-8 mx-auto mb-2 opacity-30" />No audit events found.</div>
              : events.map(e => (
                <div key={e.id} className="p-4 flex items-center justify-between gap-4 hover:bg-muted/5 transition-colors">
                  <div className="min-w-0">
                    <p className="text-sm font-medium truncate">{e.action} <span className="text-muted font-normal">on</span> {e.entity}</p>
                    <p className="text-xs text-muted">{new Date(e.created_at).toLocaleString()}</p>
                  </div>
                  <Badge label={e.action?.toLowerCase()} />
                </div>
              ))}
        </div>
      </div>
    </div>
  );
}
