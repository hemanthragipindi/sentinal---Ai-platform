import { Search as SearchIcon, Bell as BellIcon, Menu as MenuIcon, Moon as MoonIcon, Sun as SunIcon, Activity } from 'lucide-react';
import { useSidebarStore } from '@/store/sidebar';
import { useThemeStore } from '@/store/theme';

export function TopNav() {
  const { toggle } = useSidebarStore();
  const { isDark, toggleTheme } = useThemeStore();

  return (
    <header className="h-16 border-b bg-card flex items-center justify-between px-4 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <button
          onClick={toggle}
          className="p-2 -ml-2 rounded-lg text-muted hover:bg-muted/10 transition-colors"
        >
          <MenuIcon className="h-5 w-5" />
        </button>

        <div className="hidden md:flex items-center gap-2">
          <div className="h-6 w-px bg-border mx-2" />
          <span className="font-semibold text-sm">Enterprise Workspace</span>
          <span className="px-2 py-0.5 rounded-full bg-success/10 text-success text-xs font-medium border border-success/20">Pro</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative hidden md:block">
          <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted" />
          <input
            type="text"
            placeholder="Search resources..."
            className="pl-9 pr-4 py-1.5 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary w-64 transition-all"
          />
          <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
            <kbd className="hidden sm:inline-flex h-5 items-center gap-1 rounded border bg-muted/20 px-1.5 font-mono text-[10px] font-medium text-muted">
              <span className="text-xs">⌘</span>K
            </kbd>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button className="p-2 rounded-lg text-muted hover:bg-muted/10 transition-colors hidden sm:block relative">
            <Activity className="h-5 w-5" />
          </button>
          <button className="p-2 rounded-lg text-muted hover:bg-muted/10 transition-colors relative">
            <BellIcon className="h-5 w-5" />
            <span className="absolute top-2 right-2.5 w-2 h-2 bg-danger rounded-full border-2 border-card"></span>
          </button>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-muted hover:bg-muted/10 transition-colors"
          >
            {isDark ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
          </button>

          <div className="h-6 w-px bg-border mx-1" />

          <button className="flex items-center gap-2 pl-2">
            <div className="h-8 w-8 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center text-primary font-semibold text-sm">
              JD
            </div>
          </button>
        </div>
      </div>
    </header>
  );
}
