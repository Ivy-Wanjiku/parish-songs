import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from 'react';
import axios from 'axios';
import type { User } from '../types';

const BASE = (import.meta.env.VITE_API_URL as string | undefined) || 'http://localhost:8000';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  isSuperAdmin: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem('access_token'),
  );

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setToken(null);
  }, []);

  // Verify token on mount
  useEffect(() => {
    const stored = localStorage.getItem('access_token');
    if (!stored) return;
    axios
      .get<User>(`${BASE}/api/auth/me/`, {
        headers: { Authorization: `Bearer ${stored}` },
      })
      .then(({ data }) => {
        setUser(data);
        setToken(stored);
        axios.defaults.headers.common['Authorization'] = `Bearer ${stored}`;
      })
      .catch(() => logout());
  }, [logout]);

  const login = async (username: string, password: string) => {
    const { data } = await axios.post<{
      access: string;
      refresh: string;
    }>(`${BASE}/api/auth/login/`, { username, password });

    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;

    const meRes = await axios.get<User>(`${BASE}/api/auth/me/`, {
      headers: { Authorization: `Bearer ${data.access}` },
    });

    setToken(data.access);
    setUser(meRes.data);
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isAdmin: user?.role === 'admin' || user?.role === 'superadmin',
    isSuperAdmin: user?.role === 'superadmin',
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within <AuthProvider>');
  return ctx;
};
