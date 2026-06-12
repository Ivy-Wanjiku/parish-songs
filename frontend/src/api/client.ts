import axios, { AxiosInstance } from 'axios';
import type { Song, User } from '../types';

const BASE = (import.meta.env.VITE_API_URL as string | undefined) || 'http://localhost:8000';

const api: AxiosInstance = axios.create({ baseURL: BASE });

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config as typeof err.config & { _retry?: boolean };
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) throw new Error('No refresh token');
        const { data } = await axios.post(`${BASE}/api/auth/refresh/`, { refresh });
        localStorage.setItem('access_token', data.access as string);
        original.headers.Authorization = `Bearer ${data.access as string}`;
        return api(original);
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(err);
  },
);

// ── Songs ─────────────────────────────────────────────────────────────────
export const getSongs = (params?: Record<string, string>) =>
  api.get<Song[]>('/api/songs/', { params });

export const getSong = (id: number) =>
  api.get<Song>(`/api/songs/${id}/`);

export const createSong = (data: FormData) =>
  api.post<Song>('/api/songs/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const updateSong = (id: number, data: FormData) =>
  api.put<Song>(`/api/songs/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const deleteSong = (id: number) => api.delete(`/api/songs/${id}/`);

export const getScoreUrl = (id: number) => `${BASE}/api/songs/${id}/score/`;

// ── Users ─────────────────────────────────────────────────────────────────
export const getUsers = () => api.get<User[]>('/api/users/');

export const createUser = (data: Partial<User> & { password: string }) =>
  api.post<User>('/api/users/', data);

export const deleteUser = (id: number) => api.delete(`/api/users/${id}/`);

export const changePassword = (id: number, password: string) =>
  api.put(`/api/users/${id}/password/`, { password });

export default api;
