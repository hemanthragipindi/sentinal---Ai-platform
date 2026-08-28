import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '../store/auth';
import { User, Mail, AtSign, Save, Loader2, Camera } from 'lucide-react';
import { useState, useEffect } from 'react';
import api from '../lib/api';

export default function Profile() {
  const qc = useQueryClient();
  const { user: storeUser } = useAuthStore();
  const [form, setForm] = useState({ full_name: '', username: '' });
  const [saved, setSaved] = useState(false);

  const { data: user, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: () => api.get('/users/me').then(r => r.data.data),
    initialData: storeUser,
  });

  useEffect(() => {
    if (user) setForm({ full_name: user.full_name ?? '', username: user.username ?? '' });
  }, [user]);

  const update = useMutation({
    mutationFn: () => api.patch('/users/me', form),
    onSuccess: () => { qc.invalidateQueries(['me']); setSaved(true); setTimeout(() => setSaved(false), 2000); },
  });

  if (isLoading && !storeUser) return (
    <div className="flex items-center justify-center h-64"><Loader2 className="h-6 w-6 animate-spin text-muted" /></div>
  );

  const initials = (user?.full_name || user?.username || 'U').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Profile</h1>
        <p className="text-muted text-sm mt-1">Manage your personal account details.</p>
      </div>

      {/* Avatar section */}
      <div className="border rounded-xl bg-card p-6 flex items-center gap-5">
        <div className="relative">
          <div className="h-20 w-20 rounded-2xl bg-primary/20 border-2 border-primary/30 flex items-center justify-center text-primary font-bold text-2xl">
            {initials}
          </div>
          <button className="absolute -bottom-1 -right-1 h-7 w-7 rounded-lg bg-card border flex items-center justify-center hover:bg-muted/10 transition-colors">
            <Camera className="h-3.5 w-3.5 text-muted" />
          </button>
        </div>
        <div>
          <h2 className="font-semibold text-lg">{user?.full_name || user?.username}</h2>
          <p className="text-muted text-sm">{user?.email}</p>
          <span className={`inline-flex mt-1.5 px-2 py-0.5 rounded-full text-xs font-medium capitalize ${user?.status === 'active' ? 'bg-green-500/10 text-green-400' : 'bg-muted/20 text-muted'}`}>
            {user?.status ?? 'active'}
          </span>
        </div>
      </div>

      {/* Edit section */}
      <div className="border rounded-xl bg-card p-6 space-y-5">
        <h3 className="font-semibold border-b pb-4">Personal Information</h3>
        <div>
          <label className="block text-sm font-medium mb-1.5 flex items-center gap-1.5"><User className="h-3.5 w-3.5 text-muted" /> Full Name</label>
          <input
            value={form.full_name}
            onChange={e => setForm({ ...form, full_name: e.target.value })}
            placeholder="Your full name"
            className="w-full px-3 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1.5 flex items-center gap-1.5"><AtSign className="h-3.5 w-3.5 text-muted" /> Username</label>
          <input
            value={form.username}
            onChange={e => setForm({ ...form, username: e.target.value })}
            placeholder="Username"
            className="w-full px-3 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1.5 flex items-center gap-1.5"><Mail className="h-3.5 w-3.5 text-muted" /> Email</label>
          <input
            value={user?.email ?? ''}
            disabled
            className="w-full px-3 py-2 bg-muted/10 border rounded-lg text-sm text-muted cursor-not-allowed"
          />
          <p className="text-xs text-muted mt-1">Email cannot be changed.</p>
        </div>

        <div className="pt-2 flex items-center gap-3">
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

      <div className="border border-red-500/20 rounded-xl bg-red-500/5 p-5">
        <h3 className="font-semibold text-red-400 mb-2">Danger Zone</h3>
        <p className="text-sm text-muted mb-3">Permanently delete your account and all associated data.</p>
        <button className="px-4 py-2 border border-red-500/30 text-red-400 rounded-lg text-sm font-medium hover:bg-red-500/10 transition-all">
          Delete Account
        </button>
      </div>
    </div>
  );
}
