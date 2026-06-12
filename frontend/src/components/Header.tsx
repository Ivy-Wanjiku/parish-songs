import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const CrossIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <line x1="12" y1="2" x2="12" y2="22" />
    <line x1="4"  y1="8" x2="20" y2="8" />
  </svg>
);

const Header: React.FC = () => {
  const { isAuthenticated, isAdmin, isSuperAdmin, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <Link to="/" className="header-logo">
        <span className="header-logo-icon" style={{ color: 'var(--gold)' }}>
          <CrossIcon />
        </span>
        Parish Song Library
      </Link>

      <nav className="header-nav">
        {isAuthenticated && isSuperAdmin && (
          <Link to="/admin">
            <button className="btn btn-ghost" style={{ fontSize: '12px' }}>
              Manage Users
            </button>
          </Link>
        )}

        {isAuthenticated && isAdmin && (
          <span className="header-badge">
            {isSuperAdmin ? 'Superadmin' : 'Admin'}
          </span>
        )}

        {isAuthenticated ? (
          <>
            <span style={{ fontSize: '12px', color: 'var(--text-3)', padding: '0 4px' }}>
              {user?.first_name || user?.username}
            </span>
            <button className="btn btn-outline" onClick={handleLogout} style={{ fontSize: '12px', padding: '6px 14px' }}>
              Sign out
            </button>
          </>
        ) : (
          <Link to="/login">
            <button className="btn btn-outline" style={{ fontSize: '12px', padding: '6px 14px' }}>
              Admin Login
            </button>
          </Link>
        )}
      </nav>
    </header>
  );
};

export default Header;
