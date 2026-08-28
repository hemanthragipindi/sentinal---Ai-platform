import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, MessageSquare, Database, Search,
  ShieldAlert, HardDrive, FileBarChart, Settings, User, LogOut,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useSidebarStore } from '@/store/sidebar';
import { useAuthStore } from '@/store/auth';

const navItems = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Conversations', href: '/conversations', icon: MessageSquare },
  { name: 'Memory', href: '/memory', icon: Database },
  { name: 'Retrieval', href: '/retrieval', icon: Search },
  { name: 'Security', href: '/security', icon: ShieldAlert },
  { name: 'Storage', href: '/storage', icon: HardDrive },
  { name: 'Reports', href: '/reports', icon: FileBarChart },
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Profile', href: '/profile', icon: User },
];

export function Sidebar() {
  const { isOpen } = useSidebarStore();
  const { logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <aside className={cn(
      'flex flex-col border-r bg-card h-screen transition-all duration-300 ease-in-out shrink-0 sticky top-0',
      isOpen ? 'w-[260px]' : 'w-[68px]'
    )}>
      <div className="h-16 flex items-center justify-center border-b shrink-0 px-4">
        {isOpen
          ? <span className="font-extrabold text-2xl tracking-tighter bg-gradient-to-br from-primary to-blue-500 bg-clip-text text-transparent w-full drop-shadow-sm">Sentinel</span>
          : <span className="font-extrabold text-2xl tracking-tighter bg-gradient-to-br from-primary to-blue-500 bg-clip-text text-transparent drop-shadow-sm">S</span>}
      </div>

      <nav className="flex-1 py-4 flex flex-col gap-1 overflow-y-auto px-2">
        {navItems.map((item) => (
          <NavLink
            key={item.href}
            to={item.href}
            end={item.href === '/'}
            className={({ isActive }) => cn(
              'flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 text-sm font-medium',
              isActive ? 'bg-primary/10 text-primary shadow-sm' : 'text-muted hover:bg-muted/15 hover:text-foreground'
            )}
            title={!isOpen ? item.name : undefined}
          >
            <item.icon className="h-5 w-5 shrink-0" />
            {isOpen && <span>{item.name}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t shrink-0 flex flex-col gap-2">
        <button
          onClick={handleLogout}
          className={cn(
            'flex items-center gap-3 px-3 py-2.5 rounded-xl w-full text-muted hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-500/10 dark:hover:text-red-400 transition-all duration-200 text-sm font-medium border border-transparent hover:border-red-100 dark:hover:border-red-500/20',
            isOpen ? 'justify-start' : 'justify-center'
          )}
          title={!isOpen ? 'Logout' : undefined}
        >
          <LogOut className="h-5 w-5 shrink-0" />
          {isOpen && <span>Logout</span>}
        </button>
        {isOpen && (
          <div className="text-[10px] text-muted/40 font-mono text-center truncate">
            {window.location.host || 'localhost:5173'}
          </div>
        )}
      </div>
    </aside>
  );
}
