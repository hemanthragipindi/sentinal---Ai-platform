import { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2, MessageSquare, Send, Loader2, Bot, User, Menu, X } from 'lucide-react';
import api from '../lib/api';

export default function Conversations() {
  const qc = useQueryClient();
  const [selectedId, setSelectedId] = useState(null);
  const [newMsg, setNewMsg] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);

  const { data: convsData, isLoading } = useQuery({
    queryKey: ['conversations'],
    queryFn: () => api.get('/chat/conversations', { params: { page: 1, size: 50 } }).then(r => r.data),
  });

  const { data: msgsData } = useQuery({
    queryKey: ['messages', selectedId],
    queryFn: () => api.get(`/chat/messages/${selectedId}`, { params: { page: 1, size: 100 } }).then(r => r.data),
    enabled: !!selectedId,
  });

  const createConv = useMutation({
    mutationFn: () => api.post('/chat/conversations', { title: 'New Chat', model_name: 'default' }),
    onSuccess: (res) => {
      qc.invalidateQueries(['conversations']);
      setSelectedId(res.data.data.id);
      if (window.innerWidth < 768) setSidebarOpen(false);
    },
  });

  const deleteConv = useMutation({
    mutationFn: (id) => api.delete(`/chat/conversations/${id}`),
    onSuccess: (data, id) => { 
      qc.invalidateQueries(['conversations']); 
      if (selectedId === id) setSelectedId(null);
    },
  });

  const sendMsg = useMutation({
    mutationFn: () => api.post(`/chat/messages/${selectedId}`, { role: 'user', content: newMsg }),
    onSuccess: () => { 
      setNewMsg(''); 
      qc.invalidateQueries(['messages', selectedId]); 
    },
  });

  const convs = convsData?.data ?? [];
  const msgs = msgsData?.data ?? [];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [msgs]);

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-4 bg-background overflow-hidden relative">
      {/* Mobile Sidebar Overlay */}
      {!sidebarOpen && (
        <button 
          onClick={() => setSidebarOpen(true)}
          className="md:hidden absolute top-4 left-4 z-20 p-2 bg-background border rounded-md shadow-sm"
        >
          <Menu className="h-5 w-5" />
        </button>
      )}

      {/* Sidebar */}
      <div className={`
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} 
        md:translate-x-0 
        absolute md:relative z-10 
        w-72 h-full flex flex-col bg-[#f9f9f9] dark:bg-[#171717] border-r transition-transform duration-200 ease-in-out
      `}>
        <div className="p-3">
          <button
            onClick={() => createConv.mutate()}
            disabled={createConv.isPending}
            className="flex items-center justify-center gap-2 w-full px-3 py-2.5 bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm rounded-xl text-sm font-semibold transition-all"
          >
            {createConv.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
            New chat
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto px-3 pb-3 space-y-1">
          {isLoading ? (
            [1, 2, 3].map(i => <div key={i} className="h-10 rounded-lg bg-muted/10 animate-pulse" />)
          ) : (
            convs.map(c => (
              <div 
                key={c.id}
                onClick={() => { setSelectedId(c.id); if (window.innerWidth < 768) setSidebarOpen(false); }}
                className={`group flex items-center justify-between gap-2 px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-colors
                  ${selectedId === c.id ? 'bg-muted/40 font-medium' : 'hover:bg-muted/20'}
                `}
              >
                <div className="flex-1 min-w-0 flex items-center gap-2">
                  <MessageSquare className="h-4 w-4 shrink-0 opacity-50" />
                  <span className="truncate">{c.title}</span>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); deleteConv.mutate(c.id); }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500 transition-all shrink-0"
                  title="Delete chat"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            ))
          )}
        </div>
        
        {/* Mobile close button inside sidebar */}
        <button 
          onClick={() => setSidebarOpen(false)}
          className="md:hidden absolute top-4 -right-12 p-2 bg-background border rounded-md shadow-sm"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-background relative h-full min-w-0">
        {selectedId ? (
          <>
            <div className="flex-1 overflow-y-auto w-full">
              <div className="max-w-3xl mx-auto p-4 md:p-6 space-y-6">
                {msgs.map(m => (
                  <div key={m.id} className={`flex gap-4 w-full ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    {m.role !== 'user' && (
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0 border border-primary/20">
                        <Bot className="h-5 w-5 text-primary" />
                      </div>
                    )}
                    
                    <div className={`
                      max-w-[85%] md:max-w-[75%] px-4 py-3 text-[15px] leading-relaxed whitespace-pre-wrap
                      ${m.role === 'user' 
                        ? 'bg-[#f4f4f4] dark:bg-[#2f2f2f] rounded-3xl rounded-br-sm' 
                        : 'text-foreground'
                      }
                    `}>
                      {m.content}
                    </div>

                    {m.role === 'user' && (
                      <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center shrink-0">
                        <User className="h-5 w-5 opacity-70" />
                      </div>
                    )}
                  </div>
                ))}

                {sendMsg.isPending && (
                  <div className="flex gap-4 w-full justify-start">
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0 border border-primary/20">
                      <Bot className="h-5 w-5 text-primary" />
                    </div>
                    
                    <div className="px-4 py-4 text-[15px] text-foreground flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                      <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                      <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce"></span>
                    </div>
                  </div>
                )}
                
                {/* Standard spacer to ensure margin below the last message */}
                <div ref={messagesEndRef} className="h-4 w-full flex-shrink-0" />
              </div>
            </div>

            {/* Input Area */}
            <div className="w-full shrink-0 bg-background pt-2 pb-6 px-4">
              <div className="max-w-3xl mx-auto relative flex items-end gap-2 bg-card shadow-sm border rounded-[1.5rem] p-2 focus-within:ring-2 focus-within:ring-primary/20 focus-within:border-primary/30 transition-all">
                <textarea
                  value={newMsg}
                  onChange={e => setNewMsg(e.target.value)}
                  onKeyDown={e => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      if (newMsg.trim() && !sendMsg.isPending) sendMsg.mutate();
                    }
                  }}
                  placeholder="Message AI..."
                  className="flex-1 max-h-48 min-h-[44px] bg-transparent border-0 resize-none py-3 px-4 focus:outline-none focus:ring-0 text-[15px]"
                  rows={1}
                />
                <button
                  onClick={() => sendMsg.mutate()}
                  disabled={!newMsg.trim() || sendMsg.isPending}
                  className="mb-1 mr-1 p-2 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 disabled:opacity-30 disabled:bg-muted disabled:text-muted-foreground transition-all shrink-0"
                >
                  {sendMsg.isPending ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5 ml-[2px]" />}
                </button>
              </div>
              <p className="text-center text-xs text-muted-foreground mt-3">
                AI can make mistakes. Consider verifying important information.
              </p>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground gap-4 h-full">
            <div className="w-16 h-16 rounded-full bg-muted/30 flex items-center justify-center">
              <Bot className="h-8 w-8 opacity-50" />
            </div>
            <p className="text-lg font-medium text-foreground">How can I help you today?</p>
            <p className="text-sm">Select a chat from the sidebar or start a new one.</p>
          </div>
        )}
      </div>
    </div>
  );
}
