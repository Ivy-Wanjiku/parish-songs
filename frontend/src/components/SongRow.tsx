import React from 'react';
import type { Song } from '../types';
import { CAT_COLORS, CATEGORY_LABELS } from '../constants';

interface SongRowProps {
  song: Song;
  index: number;
  onClick: () => void;
}

const MisaNames: Record<string, string> = {
  banana: 'Misa Banana',
  subukia: 'Misa Subukia',
  taita: 'Misa Taita',
  amecea: 'Misa AMECEA',
  other: 'Other Misa',
};

const SongRow: React.FC<SongRowProps> = ({ song, index, onClick }) => {
  const dotColor = CAT_COLORS[song.category] ?? 'var(--text-3)';

  const isOrdinary = song.category.startsWith('ord-');
  const categoryChipLabel = CATEGORY_LABELS[song.category] ?? song.category;

  const metaParts: string[] = [];
  if (song.language) metaParts.push(song.language);
  if (song.key_signature) metaParts.push(`Key: ${song.key_signature}`);
  if (song.uploaded_by_name) metaParts.push(song.uploaded_by_name);

  return (
    <div
      className="song-row"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      aria-label={`${song.title} — ${categoryChipLabel}`}
    >
      {/* Index */}
      <span className="song-row-index">{String(index).padStart(2, '0')}</span>

      {/* Colour dot */}
      <span
        className="song-row-dot"
        style={{ backgroundColor: dotColor }}
        aria-hidden="true"
      />

      {/* Body */}
      <div className="song-row-body">
        <div className="song-row-title">{song.title}</div>

        {metaParts.length > 0 && (
          <div className="song-row-meta">
            {metaParts.map((p, i) => (
              <React.Fragment key={p}>
                {i > 0 && <span style={{ opacity: 0.4 }}>·</span>}
                <span>{p}</span>
              </React.Fragment>
            ))}
          </div>
        )}

        <div className="song-row-tags">
          <span className="chip chip-muted">{categoryChipLabel}</span>
          {isOrdinary && song.misa_id && (
            <span className="chip chip-gold">
              {MisaNames[song.misa_id] ?? song.misa_id}
            </span>
          )}
          {song.has_score && <span className="score-badge">PDF</span>}
        </div>
      </div>

      {/* Right side */}
      <div className="song-row-right">
        <span className="song-row-chevron" aria-hidden="true">›</span>
      </div>
    </div>
  );
};

export default SongRow;
