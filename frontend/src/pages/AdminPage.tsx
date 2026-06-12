import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import { getUsers, createUser, deleteUser } from '../api/client';
import { MISAS } from '../constants';
import type { User } from '../types';

void MISAS; // imported to avoid accidental removal

export default function AdminPage() {
  const { isAuthenticated, isSuperAdmin, user: currentUser } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  // New user form state
  const [newUsername, setNewUsername] = useState('');
  const [newFirstName, setNewFirstName] = useState('');
  const [newLastName, setNewLastName] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newRole, setNewRole] = useState<'admin' | 'superadmin'>('admin');
  const [formError, setFormError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login', { replace: true }); return; }
    if (!isSuperAdmin)    { navigate('/',      { replace: true }); return; }
    void fetchUsers();
  }, [isAuthenticated, isSuperAdmin, navigate]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await getUsers();
      setUsers(res.data);
    } catch {
      addToast('Failed to load users.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (u: User) => {
    if (u.id === currentUser?.id) {
      addToast('You cannot delete your own account.', 'error');
      return;
    }
    if (!window.confirm(`Remove admin "${u.username}"? They will lose all access.`)) return;
    try {
      await deleteUser(u.id);
      setUsers((prev) => prev.filter((x) => x.id !== u.id));
      addToast(`"${u.username}" removed.`, 'success');
    } catch {
      addToast('Failed to remove user.', 'error');
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');

    if (!newUsername.trim()) { setFormError('Username is required.'); return; }
    if (newPassword.length < 8) { setFormError('Password must be at least 8 characters.'); return; }

    setSubmitting(true);
    try {
      const res = await createUser({
        username: newUsername.trim(),
        first_name: newFirstName.trim(),
        last_name: newLastName.trim(),
        email: newEmail.trim(),
        password: newPassword,
        role: newRole,
      });
      setUsers((prev) => [...prev, res.data]);
      setNewUsername(''); setNewFirstName(''); setNewLastName('');
      setNewEmail(''); setNewPassword(''); setNewRole('admin');
      addToast(`Admin "${res.data.username}" created.`, 'success');
    } catch (err: unknown) {
      const axErr = err as { response?: { data?: Record<string, string[]> } };
      const data = axErr.response?.data;
      if (data) {
        const msg = Object.values(data).flat()[0];
        setFormError(typeof msg === 'string' ? msg : 'Creation failed.');
      } else {
        setFormError('An error occurred. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="admin-page">
      <h1 className="admin-heading">User Management</h1>

      {/* Current admins */}
      <section className="admin-section">
        <div className="admin-section-title">Admin Users</div>

        {loading ? (
          <div className="loading-state">Loading users…</div>
        ) : (
          <table className="user-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td style={{ color: 'var(--text)', fontWeight: 500 }}>{u.username}</td>
                  <td>{[u.first_name, u.last_name].filter(Boolean).join(' ') || '—'}</td>
                  <td>{u.email || '—'}</td>
                  <td>
                    <span className={`user-role-badge user-role-${u.role}`}>
                      {u.role === 'superadmin' ? 'Superadmin' : 'Admin'}
                    </span>
                  </td>
                  <td>
                    {u.id !== currentUser?.id && (
                      <button
                        className="btn btn-danger"
                        style={{ padding: '5px 12px', fontSize: 12 }}
                        onClick={() => void handleDelete(u)}
                      >
                        Remove
                      </button>
                    )}
                    {u.id === currentUser?.id && (
                      <span style={{ fontSize: 11, color: 'var(--text-3)' }}>You</span>
                    )}
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', color: 'var(--text-3)' }}>
                    No users found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </section>

      {/* Add new admin */}
      <section className="admin-section">
        <div className="admin-section-title">Add New Admin</div>

        <div style={{
          background: 'var(--navy-2)',
          border: '1px solid var(--border)',
          borderRadius: 10,
          padding: '24px 28px',
          maxWidth: 560,
        }}>
          {formError && (
            <div className="login-error" style={{ marginBottom: 16 }}>{formError}</div>
          )}

          <form onSubmit={(e) => void handleCreate(e)} noValidate>
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="a-username">Username *</label>
                <input
                  id="a-username"
                  className="form-input"
                  value={newUsername}
                  onChange={(e) => setNewUsername(e.target.value)}
                  placeholder="username"
                  autoComplete="off"
                />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="a-role">Role *</label>
                <select
                  id="a-role"
                  className="form-select"
                  value={newRole}
                  onChange={(e) => setNewRole(e.target.value as 'admin' | 'superadmin')}
                >
                  <option value="admin">Admin</option>
                  <option value="superadmin">Superadmin</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="a-first">First Name</label>
                <input
                  id="a-first"
                  className="form-input"
                  value={newFirstName}
                  onChange={(e) => setNewFirstName(e.target.value)}
                  placeholder="First"
                />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="a-last">Last Name</label>
                <input
                  id="a-last"
                  className="form-input"
                  value={newLastName}
                  onChange={(e) => setNewLastName(e.target.value)}
                  placeholder="Last"
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="a-email">Email</label>
              <input
                id="a-email"
                className="form-input"
                type="email"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                placeholder="email@parish.org"
                autoComplete="off"
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="a-password">Password * (min 8 chars)</label>
              <input
                id="a-password"
                className="form-input"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••"
                autoComplete="new-password"
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 8 }}>
              <button
                type="button"
                className="btn btn-ghost"
                disabled={submitting}
                onClick={() => {
                  setNewUsername('');
                  setNewFirstName('');
                  setNewLastName('');
                  setNewEmail('');
                  setNewPassword('');
                  setNewRole('admin');
                  setFormError('');
                }}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-gold" disabled={submitting}>
                {submitting ? 'Creating…' : 'Create Admin'}
              </button>
            </div>
          </form>
        </div>
      </section>
    </div>
  );
}
