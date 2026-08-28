import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2, Brain, Loader2, Tag, Clock } from 'lucide-react';
import api from '../lib/api';

const TYPES = ['fact', 'preference', 'summary', 'goal'];

export default function Memory() {
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: '', content: '', memory_type: 'fact' });

  const { data, isLoading } = useQuery({
    queryKey: ['memories'],
    queryFn: () => api.get('/memory', { params: { page: 1, size: 50 } }).then(r => r.data),
  });

  const create = useMutation({
    mutationFn: () => api.post('/memory', form),
    onSuccess: () => { qc.invalidateQueries(['memories']); setShowForm(false); setForm({ title: '', content: '', memory_type: 'fact' }); },
  });

  const remove = useMutation({
    mutationFn: (id) => api.delete(`/memory/${id}`),
    onSuccess: () => qc.invalidateQueries(['memories']),
  });

  const memories = data?.data ?? [];

  const typeColors = { fact: 'bg-blue-500/10 text-blue-400', preference: 'bg-purple-500/10 text-purple-400', summary: 'bg-orange-500/10 text-orange-400', goal: 'bg-green-500/10 text-green-400' };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Memory</h1>
          <p className="text-muted text-sm mt-1">Manage vector embeddings and semantic data.</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 transition-all">
          <Plus className="h-4 w-4" /> Add Memory
        </button>
      </div>

      {showForm && (
        <div className="border rounded-xl bg-card p-5 space-y-4">
          <h3 className="font-semibold text-sm">New Memory</h3>
          <input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} placeholder="Title (optional)" className="w-full px-3 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all" />
          <textarea value={form.content} onChange={e => setForm({ ...form, content: e.target.value })} placeholder="Memory content *" rows={3} className="w-full px-3 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all resize-none" />
          <div className="flex gap-2">
            {TYPES.map(t => (
              <button key={t} onClick={() => setForm({ ...form, memory_type: t })} className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all capitalize ${form.memory_type === t ? 'bg-primary text-primary-foreground border-primary' : 'border-border text-muted hover:border-primary/50'}`}>{t}</button>
            ))}
          </div>
          <div className="flex gap-2">
            <button onClick={() => create.mutate()} disabled={!form.content.trim() || create.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-60 flex items-center gap-2 transition-all">
              {create.isPending && <Loader2 className="h-3.5 w-3.5 animate-spin" />} Save
            </button>
            <button onClick={() => setShowForm(false)} className="px-4 py-2 border rounded-lg text-sm font-medium hover:bg-muted/10 transition-all">Cancel</button>
          </div>
        </div>
      )}

      {isLoading
        ? <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">{[1,2,3,4,5,6].map(i => <div key={i} className="h-36 rounded-xl bg-muted/10 animate-pulse border" />)}</div>
        : memories.length === 0
          ? <div className="border rounded-xl bg-card p-12 flex flex-col items-center justify-center gap-3 text-muted"><Brain className="h-10 w-10 opacity-30" /><p className="text-sm">No memories yet. Add one above.</p></div>
          : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {memories.map(m => (
                <div key={m.id} className="border rounded-xl bg-card p-4 flex flex-col gap-3 group hover:border-primary/30 transition-all">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      {m.title && <p className="font-semibold text-sm truncate">{m.title}</p>}
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium mt-1 ${typeColors[m.memory_type] ?? 'bg-muted/20 text-muted'}`}>
                        <Tag className="h-3 w-3" /> {m.memory_type}
                      </span>
                    </div>
                    <button onClick={() => remove.mutate(m.id)} className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-muted hover:text-red-400 hover:bg-red-400/10 transition-all">
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                  <p className="text-sm text-muted line-clamp-3">{m.content}</p>
                  <div className="flex items-center gap-1 text-xs text-muted mt-auto">
                    <Clock className="h-3 w-3" />
                    {new Date(m.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          )}
    </div>
  );
}
