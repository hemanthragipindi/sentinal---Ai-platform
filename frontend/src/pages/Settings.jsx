import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Loader2, Save, Settings as SettingsIcon } from 'lucide-react';
import { useState, useEffect } from 'react';
import api from '../lib/api';

export default function Settings() {
  const qc = useQueryClient();
  const [form, setForm] = useState({});
  const [saved, setSaved] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ['settings'],
    queryFn: () => api.get('/settings').then(r => r.data.data),
  });

  useEffect(() => {
    if (data) setForm(data);
  }, [data]);

  const update = useMutation({
    mutationFn: () => api.patch('/settings', form),
    onSuccess: () => { qc.invalidateQueries(['settings']); setSaved(true); setTimeout(() => setSaved(false), 2000); },
  });

  if (isLoading) return (
    <div className="flex items-center justify-center h-64"><Loader2 className="h-6 w-6 animate-spin text-muted" /></div>
  );

  const fields = [
    { key: 'theme', label: 'Theme', type: 'select', options: ['dark', 'light', 'system'] },
    { key: 'language', label: 'Language', type: 'select', options: ['en', 'fr', 'de', 'es'] },
    { key: 'max_memory_items', label: 'Max Memory Items', type: 'number' },
    { key: 'default_top_k', label: 'Default Search Top-K', type: 'number' },
    { key: 'email_notifications', label: 'Email Notifications', type: 'toggle' },
    { key: 'security_alerts', label: 'Security Alerts', type: 'toggle' },
  ];

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted text-sm mt-1">Manage platform preferences and integrations.</p>
      </div>

      <div className="border rounded-xl bg-card p-6 space-y-6">
        <div className="flex items-center gap-2 pb-4 border-b">
          <SettingsIcon className="h-4 w-4 text-primary" />
          <h2 className="font-semibold">Platform Settings</h2>
        </div>

        {fields.map(field => (
          <div key={field.key} className="flex items-center justify-between gap-8">
            <div>
              <label className="text-sm font-medium">{field.label}</label>
            </div>
            <div className="shrink-0">
              {field.type === 'select' && (
                <select
                  value={form[field.key] ?? ''}
                  onChange={e => setForm({ ...form, [field.key]: e.target.value })}
                  className="px-3 py-1.5 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                >
                  {field.options.map(o => <option key={o} value={o}>{o}</option>)}
                </select>
              )}
              {field.type === 'number' && (
                <input
                  type="number"
                  value={form[field.key] ?? ''}
                  onChange={e => setForm({ ...form, [field.key]: Number(e.target.value) })}
                  className="w-24 px-3 py-1.5 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                />
              )}
              {field.type === 'toggle' && (
                <button
                  onClick={() => setForm({ ...form, [field.key]: !form[field.key] })}
                  className={`relative h-6 w-11 rounded-full transition-colors duration-200 ${form[field.key] ? 'bg-primary' : 'bg-muted/30'}`}
                >
                  <span className={`absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform duration-200 ${form[field.key] ? 'translate-x-5' : 'translate-x-0.5'}`} />
                </button>
              )}
            </div>
          </div>
        ))}

        <div className="pt-4 border-t flex items-center gap-3">
          <button
            onClick={() => update.mutate()}
            disabled={update.isPending}
            className="px-5 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-60 flex items-center gap-2 transition-all"
          >
            {update.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
            Save Changes
          </button>
          {saved && <span className="text-sm text-green-400">✓ Saved!</span>}
        </div>
      </div>
    </div>
  );
}
