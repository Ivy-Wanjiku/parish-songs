import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './components/Toast';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import Library from './pages/Library';
import Login from './pages/Login';
import AdminPage from './pages/AdminPage';

interface ProtectedRouteProps {
  element: React.ReactElement;
  superAdminOnly?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ element, superAdminOnly = false }) => {
  const { isAuthenticated, isSuperAdmin } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (superAdminOnly && !isSuperAdmin) return <Navigate to="/" replace />;
  return element;
};

const AppRoutes: React.FC = () => (
  <div className="app-shell">
    <Header />
    <Routes>
      <Route path="/" element={<Library />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/admin"
        element={<ProtectedRoute element={<AdminPage />} superAdminOnly />}
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  </div>
);

export default function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <ToastProvider>
            <AppRoutes />
          </ToastProvider>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}
