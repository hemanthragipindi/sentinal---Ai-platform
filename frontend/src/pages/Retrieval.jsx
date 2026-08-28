import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Search, Loader2, Brain, Zap, Clock } from 'lucide-react';
import api from '../lib/api';

export default function Retrieval() {
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState(5);

  const search = useMutation({
    mutationFn: () => api.post('/retrieval/search', { query, top_k: topK }).then(r => r.data.data),
  });

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) search.mutate();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Retrieval Pipeline</h1>
        <p className="text-muted text-sm mt-1">Semantic vector search across your memory store.</p>
      </div>

      <form onSubmit={handleSearch} className="border rounded-xl bg-card p-5 space-y-4">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted" />
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Enter your semantic search query..."
              className="w-full pl-9 pr-4 py-2.5 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
            />
          </div>
          <select
            value={topK}
            onChange={e => setTopK(Number(e.target.value))}
            className="px-3 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
          >
            {[3, 5, 10, 20].map(k => <option key={k} value={k}>Top {k}</option>)}
          </select>
          <button
            type="submit"
            disabled={!query.trim() || search.isPending}
            className="px-5 py-2.5 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-60 flex items-center gap-2 transition-all"
          >
            {search.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Zap className="h-4 w-4" />}
            Search
          </button>
        </div>
      </form>

      {search.data && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm text-muted">
            <span>{search.data.results?.length ?? 0} results for "<span className="text-foreground font-medium">{search.data.query}</span>"</span>
            <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" />{search.data.response_time?.toFixed(0)}ms</span>
          </div>

          {search.data.results?.length === 0
            ? <div className="border rounded-xl bg-card p-10 flex flex-col items-center gap-3 text-muted"><Brain className="h-10 w-10 opacity-30" /><p className="text-sm">No results found. The embedding model may not be configured yet.</p></div>
            : search.data.results?.map((r, i) => (
              <div key={r.memory_id ?? i} className="border rounded-xl bg-card p-5 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-muted">Rank #{r.rank}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium">{(r.similarity_score * 100).toFixed(1)}% match</span>
                </div>
                <p className="text-sm">{r.memory?.content}</p>
              </div>
            ))}
        </div>
      )}

      {!search.data && !search.isPending && (
        <div className="border rounded-xl bg-card p-12 flex flex-col items-center gap-3 text-muted">
          <Search className="h-10 w-10 opacity-30" />
          <p className="text-sm">Enter a query above to search your memory store.</p>
        </div>
      )}
    </div>
  );
}
