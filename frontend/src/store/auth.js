import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '@/lib/api';

export const useAuthStore = create()(
  persist(
    (set, get) => ({
      user: null,
      access_token: null,
      refresh_token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          const { data } = await api.post('/auth/login', { email, password });
          const { access_token, refresh_token } = data.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          // Fetch user profile
          const userRes = await api.get('/users/me');
          set({
            access_token,
            refresh_token,
            user: userRes.data.data,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (err) {
          set({ error: err.response?.data?.message || 'Login failed', isLoading: false });
          throw err;
        }
      },

      googleLogin: async (credential) => {
        set({ isLoading: true, error: null });
        try {
          const { data } = await api.post('/auth/google', { credential });
          const { access_token, refresh_token } = data.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          const userRes = await api.get('/users/me');
          set({
            access_token,
            refresh_token,
            user: userRes.data.data,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (err) {
          set({ error: err.response?.data?.message || 'Google Login failed', isLoading: false });
          throw err;
        }
      },

      register: async (email, username, password, full_name) => {
        set({ isLoading: true, error: null });
        try {
          await api.post('/auth/register', { email, username, password, full_name });
          set({ isLoading: false });
        } catch (err) {
          set({ error: err.response?.data?.message || 'Registration failed', isLoading: false });
          throw err;
        }
      },

      logout: async () => {
        try {
          const refresh_token = localStorage.getItem('refresh_token');
          if (refresh_token) await api.post('/auth/logout', { refresh_token });
        } catch {}
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        set({ user: null, access_token: null, refresh_token: null, isAuthenticated: false });
      },

      fetchMe: async () => {
        try {
          const { data } = await api.get('/users/me');
          set({ user: data.data, isAuthenticated: true });
        } catch {
          set({ user: null, isAuthenticated: false });
        }
      },
    }),
    { name: 'sentinel-auth', partialize: (s) => ({ access_token: s.access_token, refresh_token: s.refresh_token }) }
  )
);
