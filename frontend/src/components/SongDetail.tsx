import React, { useEffect, useRef } from 'react';
import type { Song } from '../types';
import { CAT_COLORS, CATEGORY_LABELS } from '../constants';
import { getScoreUrl } from '../api/client';

interface SongDetailProps {
  song: Song;
  onClose: () => void;
  onEdit?: () => void;
  onDelete?: () => void;
}

const MisaNames: Record<string, string> = {
  banana: 'Misa Banana',
  subukia: 'Misa Subukia',
  taita: 'Misa Taita',
  amecea: 'Misa AMECEA',
  other: 'Other Misa',
};

const SongDetail: React.FC<SongDetailProps> = ({ song, onClose, onEdit, onDelete }) => {
  const closeRef = useRef<HTMLButtonElement>(null);

  // Trap focus & close on Escape
  useEffect(() => {
    closeRef.current?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  const handlePrint = () => window.print();

  const isOrdinary = song.category.startsWith('ord-');
  const dotColor = CAT_COLORS[song.category] ?? 'var(--text-3)';

  return (
    <>
      {/* Hidden div used as print target — only this becomes visible on print */}
      <div className="print-target" aria-hidden="true">
        <div className="detail-title">{song.title}</div>
        {song.key_signature && (
          <p style={{ fontSize: 13, color: '#555', marginBottom: 16 }}>
            Key: {song.key_signature}
          </p>
        )}
        <pre className="detail-lyrics">{song.lyrics}</pre>
      </div>

      <div
        className="modal-backdrop"
        onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
        role="dialog"
        aria-modal="true"
        aria-labelledby="detail-title"
      >
        <div className="modal modal-wide">
          {/* Header */}
          <div className="modal-header">
            <div style={{ minWidth: 0 }}>
              <h1 className="detail-title" id="detail-title">{song.title}</h1>
              {song.key_signature && (
                <div className="detail-key">Key of {song.key_signature}</div>
              )}
              <div className="detail-header-meta" style={{ marginTop: 10 }}>
                <span
                  className="chip chip-muted"
                  style={{ borderColor: dotColor, color: dotColor }}
                >
                  {CATEGORY_LABELS[song.category] ?? song.category}
                </span>
                <span className="chip chip-muted">{song.language}</span>
                {isOrdinary && song.misa_id && (
                  <span className="chip chip-gold">
                    {MisaNames[song.misa_id] ?? song.misa_id}
                  </span>
                )}
                {song.has_score && <span className="score-badge">Score PDF</span>}
              </div>
            </div>
            <button
              ref={closeRef}
              className="btn btn-ghost btn-icon"
              onClick={onClose}
              aria-label="Close"
              style={{ marginLeft: 12, flexShrink: 0 }}
            >
              ✕
            </button>
          </div>

          {/* Lyrics */}
          <div className="modal-body">
            <div className="detail-section-label">Lyrics</div>
            <pre className="detail-lyrics">{song.lyrics}</pre>

            {song.uploaded_by_name && (
              <p className="detail-uploaded-by" style={{ marginTop: 20 }}>
                Uploaded by {song.uploaded_by_name}
              </p>
            )}
          </div>

          {/* Footer */}
          <div className="modal-footer">
            <div className="detail-footer-actions" style={{ width: '100%' }}>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {song.has_score && (
                  <a
                    href={getScoreUrl(song.id)}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <button className="btn btn-outline">⬇ Download Score</button>
                  </a>
                )}
                <button className="btn btn-outline" onClick={handlePrint}>
                  🖨 Print Lyrics
                </button>
              </div>

              <div style={{ display: 'flex', gap: 8 }}>
                {onEdit && (
                  <button className="btn btn-outline" onClick={onEdit}>
                    Edit
                  </button>
                )}
                {onDelete && (
                  <button className="btn btn-danger" onClick={onDelete}>
                    Delete
                  </button>
                )}
                <button className="btn btn-ghost" onClick={onClose}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SongDetail;
