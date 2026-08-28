import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useThemeStore = create()(
  persist(
    (set) => ({
      isDark: false,
      toggleTheme: () => set((state) => ({ isDark: !state.isDark })),
      setTheme: (isDark) => set({ isDark }),
    }),
    {
      name: 'sentinel-theme-v2',
    }
  )
);
