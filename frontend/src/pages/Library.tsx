import React, { useState, useEffect, useMemo, useCallback } from 'react';
import type { Song, FilterType } from '../types';
import { getSongs, deleteSong } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import Sidebar from '../components/Sidebar';
import SongRow from '../components/SongRow';
import SongDetail from '../components/SongDetail';
import SongForm from '../components/SongForm';
import { PROPER_CATEGORIES, ORDINARY_PARTS, LANGUAGES, ALL_CATEGORY_ORDER, CATEGORY_LABELS } from '../constants';

export default function Library() {
  const { isAdmin } = useAuth();
  const { addToast } = useToast();

  const [songs, setSongs] = useState<Song[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [language, setLanguage] = useState('');
  const [filter, setFilter] = useState<FilterType>({ type: 'all' });
  const [selectedSong, setSelectedSong] = useState<Song | null>(null);
  const [editingSong, setEditingSong] = useState<Song | 'new' | null>(null);

  const fetchSongs = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getSongs();
      setSongs(res.data);
    } catch {
      addToast('Failed to load songs. Is the backend running?', 'error');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => { void fetchSongs(); }, [fetchSongs]);

  // Base set: search + language only
  const baseSongs = useMemo(() => {
    let s = songs;
    if (language) s = s.filter((song) => song.language === language);
    const q = search.trim().toLowerCase();
    if (q) {
      s = s.filter(
        (song) =>
          song.title.toLowerCase().includes(q) ||
          song.lyrics.toLowerCase().includes(q),
      );
    }
    return s;
  }, [songs, search, language]);

  // Apply sidebar filter on top
  const displayedSongs = useMemo(() => {
    switch (filter.type) {
      case 'all':
        return baseSongs;
      case 'proper':
        return baseSongs.filter((s) => s.category === filter.category);
      case 'misa':
        return baseSongs.filter((s) => s.misa_id === filter.misa_id);
      case 'misa_part':
        return baseSongs.filter(
          (s) => s.misa_id === filter.misa_id && s.category === filter.category,
        );
    }
  }, [baseSongs, filter]);

  // Group by category in canonical order
  const groupedSongs = useMemo(() => {
    const groups: Record<string, Song[]> = {};
    for (const s of displayedSongs) {
      if (!groups[s.category]) groups[s.category] = [];
      groups[s.category].push(s);
    }
    return groups;
  }, [displayedSongs]);

  const orderedGroups = useMemo(() => {
    return Object.keys(groupedSongs).sort(
      (a, b) => ALL_CATEGORY_ORDER.indexOf(a) - ALL_CATEGORY_ORDER.indexOf(b),
    );
  }, [groupedSongs]);

  const handleDelete = async (song: Song) => {
    if (!window.confirm(`Delete "${song.title}"? This cannot be undone.`)) return;
    try {
      await deleteSong(song.id);
      setSongs((prev) => prev.filter((s) => s.id !== song.id));
      setSelectedSong(null);
      addToast(`"${song.title}" deleted.`, 'success');
    } catch {
      addToast('Failed to delete song.', 'error');
    }
  };

  const handleSaved = (saved: Song, isNew: boolean) => {
    setSongs((prev) =>
      isNew ? [saved, ...prev] : prev.map((s) => (s.id === saved.id ? saved : s)),
    );
    setEditingSong(null);
    // If we just edited the open song, update the detail view
    if (!isNew && selectedSong?.id === saved.id) setSelectedSong(saved);
    addToast(isNew ? 'Song uploaded!' : 'Song updated!', 'success');
  };

  const pageTitle = useMemo(() => {
    switch (filter.type) {
      case 'all': return 'All Songs';
      case 'proper': return filter.category;
      case 'misa': return filter.misa_id;
      case 'misa_part': return `${filter.misa_id} — ${CATEGORY_LABELS[filter.category] ?? filter.category}`;
    }
  }, [filter]);

  // Determine which categories exist in displayed songs for section headers
  const properCats = [...PROPER_CATEGORIES];
  const ordinaryCats = ORDINARY_PARTS.map((p) => p.id);
  const allCatIds = [...properCats, ...ordinaryCats];
  void allCatIds; // suppress unused warning

  return (
    <div className="library-layout">
      <Sidebar
        songs={baseSongs}
        allSongs={songs}
        filter={filter}
        onFilter={(f) => {
          setFilter(f);
          setSelectedSong(null);
        }}
      />

      <main className="library-main">
        {/* Toolbar */}
        <div className="library-toolbar">
          <div className="search-wrap">
            <input
              className="form-input search-input"
              placeholder="Search songs or lyrics…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              aria-label="Search songs"
            />
          </div>

          <select
            className="form-select lang-select"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            aria-label="Filter by language"
          >
            <option value="">All Languages</option>
            {LANGUAGES.map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>

          {isAdmin && (
            <button
              className="btn btn-gold"
              onClick={() => setEditingSong('new')}
            >
              + Add Song
            </button>
          )}
        </div>

        {/* Meta bar */}
        <div className="library-meta">
          <strong style={{ color: 'var(--text-2)' }}>{pageTitle}</strong>
          {' '}
          <span>— {displayedSongs.length} {displayedSongs.length === 1 ? 'song' : 'songs'}</span>
        </div>

        {/* Song list */}
        <div className="songs-list">
          {loading ? (
            <div className="loading-state">Loading songs…</div>
          ) : orderedGroups.length === 0 ? (
            <div className="empty-state">
              <span style={{ fontSize: 32 }}>🎵</span>
              <span>No songs found.</span>
              {(search || language) && (
                <button
                  className="btn btn-ghost"
                  onClick={() => { setSearch(''); setLanguage(''); }}
                >
                  Clear filters
                </button>
              )}
            </div>
          ) : (
            orderedGroups.map((cat) => {
              const group = groupedSongs[cat];
              // Only show group heading when multiple groups are visible
              const showHeading = orderedGroups.length > 1;
              return (
                <div key={cat}>
                  {showHeading && (
                    <h2 className="group-heading">
                      {CATEGORY_LABELS[cat] ?? cat}
                    </h2>
                  )}
                  {group.map((song, idx) => (
                    <SongRow
                      key={song.id}
                      song={song}
                      index={idx + 1}
                      onClick={() => setSelectedSong(song)}
                    />
                  ))}
                </div>
              );
            })
          )}
        </div>
      </main>

      {/* Song detail modal */}
      {selectedSong && (
        <SongDetail
          song={selectedSong}
          onClose={() => setSelectedSong(null)}
          onEdit={isAdmin ? () => setEditingSong(selectedSong) : undefined}
          onDelete={isAdmin ? () => void handleDelete(selectedSong) : undefined}
        />
      )}

      {/* Song form modal */}
      {editingSong !== null && (
        <SongForm
          song={editingSong === 'new' ? null : editingSong}
          onClose={() => setEditingSong(null)}
          onSaved={handleSaved}
        />
      )}
    </div>
  );
}
