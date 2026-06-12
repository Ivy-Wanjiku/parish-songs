import React, { useState, useMemo } from 'react';
import type { Song, FilterType } from '../types';
import { PROPER_CATEGORIES, MISAS, ORDINARY_PARTS } from '../constants';

interface SidebarProps {
  songs: Song[];     // base-filtered songs (search+language) — used for counts
  allSongs: Song[];  // all songs — used for "All Songs" total
  filter: FilterType;
  onFilter: (f: FilterType) => void;
}

const ChevronIcon: React.FC<{ open: boolean }> = ({ open }) => (
  <span className={`sidebar-misa-chevron ${open ? 'open' : ''}`}>▶</span>
);

const Sidebar: React.FC<SidebarProps> = ({ songs, allSongs, filter, onFilter }) => {
  const [expandedMisas, setExpandedMisas] = useState<Set<string>>(new Set(['banana', 'amecea']));
  const [ordinaryOpen, setOrdinaryOpen] = useState(true);

  const toggleMisa = (id: string) => {
    setExpandedMisas((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const isActive = (f: FilterType): boolean => {
    if (filter.type !== f.type) return false;
    if (f.type === 'proper' && filter.type === 'proper') return filter.category === f.category;
    if (f.type === 'misa' && filter.type === 'misa') return filter.misa_id === f.misa_id;
    if (f.type === 'misa_part' && filter.type === 'misa_part') {
      return filter.misa_id === f.misa_id && filter.category === f.category;
    }
    return f.type === 'all' && filter.type === 'all';
  };

  // Count helpers
  const countCategory = (cat: string) => songs.filter((s) => s.category === cat).length;
  const countMisa = (id: string) => songs.filter((s) => s.misa_id === id).length;
  const countMisaPart = (misa_id: string, cat: string) =>
    songs.filter((s) => s.misa_id === misa_id && s.category === cat).length;

  // Which Misas have songs in base set
  const activeMisas = useMemo(
    () => MISAS.filter((m) => allSongs.some((s) => s.misa_id === m.id)),
    [allSongs],
  );

  return (
    <aside className="sidebar">
      {/* All Songs */}
      <div
        className={`sidebar-item ${isActive({ type: 'all' }) ? 'active' : ''}`}
        onClick={() => onFilter({ type: 'all' })}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && onFilter({ type: 'all' })}
      >
        <span>All Songs</span>
        <span className="sidebar-item-count">{songs.length}</span>
      </div>

      <div className="sidebar-divider" />

      {/* Proper of Mass */}
      <div className="sidebar-section-label">Proper of Mass</div>
      {PROPER_CATEGORIES.map((cat) => (
        <div
          key={cat}
          className={`sidebar-item ${isActive({ type: 'proper', category: cat }) ? 'active' : ''}`}
          onClick={() => onFilter({ type: 'proper', category: cat })}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && onFilter({ type: 'proper', category: cat })}
        >
          <span>{cat}</span>
          <span className="sidebar-item-count">{countCategory(cat)}</span>
        </div>
      ))}

      <div className="sidebar-divider" />

      {/* Ordinary of Mass */}
      <button
        className="sidebar-misa-toggle"
        onClick={() => setOrdinaryOpen((p) => !p)}
        aria-expanded={ordinaryOpen}
      >
        <span className="sidebar-misa-toggle-left">
          <span className="sidebar-section-label" style={{ padding: 0 }}>Ordinary of Mass</span>
        </span>
        <ChevronIcon open={ordinaryOpen} />
      </button>

      {ordinaryOpen && (
        <div className="sidebar-misa-parts">
          {activeMisas.map((misa) => {
            const isExpanded = expandedMisas.has(misa.id);
            const misaActive = filter.type === 'misa' && filter.misa_id === misa.id;

            return (
              <div key={misa.id} className="sidebar-misa-group">
                <button
                  className={`sidebar-misa-toggle ${misaActive ? 'active' : ''}`}
                  onClick={() => {
                    onFilter({ type: 'misa', misa_id: misa.id });
                    toggleMisa(misa.id);
                  }}
                  aria-expanded={isExpanded}
                >
                  <span className="sidebar-misa-toggle-left" style={{ fontSize: '12px' }}>
                    {misa.name}
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span className="sidebar-item-count">{countMisa(misa.id)}</span>
                    <ChevronIcon open={isExpanded} />
                  </span>
                </button>

                {isExpanded && (
                  <div>
                    {ORDINARY_PARTS.filter(
                      (p) => countMisaPart(misa.id, p.id) > 0,
                    ).map((part) => (
                      <div
                        key={part.id}
                        className={`sidebar-part-item ${
                          filter.type === 'misa_part' &&
                          filter.misa_id === misa.id &&
                          filter.category === part.id
                            ? 'active'
                            : ''
                        }`}
                        onClick={(e) => {
                          e.stopPropagation();
                          onFilter({ type: 'misa_part', misa_id: misa.id, category: part.id });
                        }}
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            onFilter({ type: 'misa_part', misa_id: misa.id, category: part.id });
                          }
                        }}
                      >
                        <span>{part.name}</span>
                        <span className="sidebar-item-count">
                          {countMisaPart(misa.id, part.id)}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
