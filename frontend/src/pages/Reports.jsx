import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { FileBarChart, Plus, Eye, Download, Trash2, Loader2, Clock } from 'lucide-react';
import { useState } from 'react';
import api from '../lib/api';

export default function Reports() {
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: '', report_type: 'summary' });

  const { data, isLoading } = useQuery({
    queryKey: ['reports'],
    queryFn: () => api.get('/reports', { params: { page: 1, size: 50 } }).then(r => r.data),
  });

  const create = useMutation({
    mutationFn: () => api.post('/reports', form),
    onSuccess: () => { qc.invalidateQueries(['reports']); setShowForm(false); setForm({ title: '', report_type: 'summary' }); },
  });

  const remove = useMutation({
    mutationFn: (id) => api.delete(`/reports/${id}`),
    onSuccess: () => qc.invalidateQueries(['reports']),
  });

  const reports = data?.data ?? [];
  const TYPES = ['summary', 'threat', 'usage', 'audit'];
  const typeColors = { summary: 'bg-blue-500/10 text-blue-400', threat: 'bg-red-500/10 text-red-400', usage: 'bg-purple-500/10 text-purple-400', audit: 'bg-orange-500/10 text-orange-400' };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Reports</h1>
          <p className="text-muted text-sm mt-1">View and manage system analytics reports.</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 transition-all">
          <Plus className="h-4 w-4" /> New Report
        </button>
      </div>

      {showForm && (
        <div className="border rounded-xl bg-card p-5 space-y-4">
          <h3 className="font-semibold text-sm">Generate Report</h3>
          <input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} placeholder="Report title *" className="w-full px-3 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all" />
          <div className="flex gap-2">
            {TYPES.map(t => (
              <button key={t} onClick={() => setForm({ ...form, report_type: t })} className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all capitalize ${form.report_type === t ? 'bg-primary text-primary-foreground border-primary' : 'border-border text-muted hover:border-primary/50'}`}>{t}</button>
            ))}
          </div>
          <div className="flex gap-2">
            <button onClick={() => create.mutate()} disabled={!form.title.trim() || create.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-60 flex items-center gap-2 transition-all">
              {create.isPending && <Loader2 className="h-3.5 w-3.5 animate-spin" />} Generate
            </button>
            <button onClick={() => setShowForm(false)} className="px-4 py-2 border rounded-lg text-sm font-medium hover:bg-muted/10 transition-all">Cancel</button>
          </div>
        </div>
      )}

      {isLoading
        ? <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="h-20 rounded-xl border bg-muted/10 animate-pulse" />)}</div>
        : reports.length === 0
          ? <div className="border rounded-xl bg-card p-12 flex flex-col items-center gap-3 text-muted"><FileBarChart className="h-10 w-10 opacity-30" /><p className="text-sm">No reports yet.</p></div>
          : (
            <div className="border rounded-xl bg-card divide-y overflow-hidden">
              {reports.map(r => (
                <div key={r.id} className="p-4 flex items-center justify-between gap-4 hover:bg-muted/5 transition-colors">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="h-9 w-9 rounded-lg bg-primary/10 flex items-center justify-center shrink-0"><FileBarChart className="h-4 w-4 text-primary" /></div>
                    <div className="min-w-0">
                      <p className="font-medium text-sm truncate">{r.title}</p>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${typeColors[r.report_type] ?? 'bg-muted/20 text-muted'}`}>{r.report_type}</span>
                        <span className="text-xs text-muted flex items-center gap-1"><Clock className="h-3 w-3" />{new Date(r.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-1 shrink-0">
                    <button onClick={() => remove.mutate(r.id)} className="p-1.5 rounded-lg text-muted hover:text-red-400 hover:bg-red-400/10 transition-all"><Trash2 className="h-4 w-4" /></button>
                  </div>
                </div>
              ))}
            </div>
          )}
    </div>
  );
}
