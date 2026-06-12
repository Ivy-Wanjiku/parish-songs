import React, { useState, useEffect, useRef } from 'react';
import type { Song } from '../types';
import { MISAS, ORDINARY_PARTS, LANGUAGES } from '../constants';
import { createSong, updateSong } from '../api/client';

const PROPER_CATS = [
  'Entrance',
  'Bible Procession',
  'Offertory',
  'Communion',
  'Thanksgiving',
  'Recessional',
  'Responsorial Psalm',
];
const ORDINARY_CAT_IDS = ORDINARY_PARTS.map((p) => p.id);

interface SongFormProps {
  song: Song | null; // null = new song
  onClose: () => void;
  onSaved: (saved: Song, isNew: boolean) => void;
}

const SongForm: React.FC<SongFormProps> = ({ song, onClose, onSaved }) => {
  const isNew = song === null;
  const firstRef = useRef<HTMLInputElement>(null);

  const [title, setTitle] = useState(song?.title ?? '');
  const [category, setCategory] = useState(song?.category ?? 'Entrance');
  const [language, setLanguage] = useState(song?.language ?? 'Swahili');
  const [keySignature, setKeySignature] = useState(song?.key_signature ?? '');
  const [lyrics, setLyrics] = useState(song?.lyrics ?? '');
  const [misaId, setMisaId] = useState(song?.misa_id ?? '');
  const [ordPart, setOrdPart] = useState(song?.ord_part ?? '');
  const [scoreFile, setScoreFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const isOrdinary = ORDINARY_CAT_IDS.includes(category);

  // Sync ordPart with category for Ordinary songs
  useEffect(() => {
    if (isOrdinary) {
      const part = ORDINARY_PARTS.find((p) => p.id === category);
      setOrdPart(part?.name ?? '');
      if (!misaId) setMisaId('banana');
    } else {
      setOrdPart('');
      setMisaId('');
    }
  }, [category, isOrdinary, misaId]);

  useEffect(() => {
    firstRef.current?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  const validate = (): boolean => {
    const e: Record<string, string> = {};
    if (!title.trim()) e.title = 'Title is required.';
    if (!lyrics.trim()) e.lyrics = 'Lyrics are required.';
    if (isOrdinary && !misaId) e.misa_id = 'Misa is required for Ordinary songs.';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;
    setScoreFile(file);
    setFileName(file?.name ?? '');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setSubmitting(true);

    const fd = new FormData();
    fd.append('title', title.trim());
    fd.append('category', category);
    fd.append('language', language);
    fd.append('key_signature', keySignature.trim());
    fd.append('lyrics', lyrics.trim());
    fd.append('misa_id', isOrdinary ? misaId : '');
    fd.append('ord_part', isOrdinary ? ordPart : '');
    if (scoreFile) fd.append('score_file', scoreFile);

    try {
      let saved: Song;
      if (isNew) {
        const res = await createSong(fd);
        saved = res.data;
      } else {
        const res = await updateSong(song.id, fd);
        saved = res.data;
      }
      onSaved(saved, isNew);
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: Record<string, string[]> } };
      const data = axiosErr.response?.data;
      if (data && typeof data === 'object') {
        const mapped: Record<string, string> = {};
        for (const [k, v] of Object.entries(data)) {
          mapped[k] = Array.isArray(v) ? v[0] : String(v);
        }
        setErrors(mapped);
      } else {
        setErrors({ general: 'An error occurred. Please try again.' });
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="modal-backdrop"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="form-title"
    >
      <div className="modal">
        <div className="modal-header">
          <h2 className="modal-title" id="form-title">
            {isNew ? 'Upload New Song' : `Edit — ${song.title}`}
          </h2>
          <button className="btn btn-ghost btn-icon" onClick={onClose} aria-label="Close">✕</button>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <div className="modal-body">
            {errors.general && (
              <div className="login-error" style={{ marginBottom: 16 }}>{errors.general}</div>
            )}

            {/* Title */}
            <div className="form-group">
              <label className="form-label" htmlFor="f-title">Title *</label>
              <input
                ref={firstRef}
                id="f-title"
                className="form-input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Nalifurahi Waliponiambia"
              />
              {errors.title && <span className="form-error">{errors.title}</span>}
            </div>

            {/* Category + Language */}
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="f-category">Category *</label>
                <select
                  id="f-category"
                  className="form-select"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                >
                  <optgroup label="Proper of Mass">
                    {PROPER_CATS.map((c) => <option key={c} value={c}>{c}</option>)}
                  </optgroup>
                  <optgroup label="Ordinary of Mass">
                    {ORDINARY_PARTS.map((p) => (
                      <option key={p.id} value={p.id}>{p.name}</option>
                    ))}
                  </optgroup>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="f-language">Language *</label>
                <select
                  id="f-language"
                  className="form-select"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  {LANGUAGES.map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
              </div>
            </div>

            {/* Misa (only for Ordinary) */}
            {isOrdinary && (
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label" htmlFor="f-misa">Misa *</label>
                  <select
                    id="f-misa"
                    className="form-select"
                    value={misaId}
                    onChange={(e) => setMisaId(e.target.value)}
                  >
                    {MISAS.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
                  </select>
                  {errors.misa_id && <span className="form-error">{errors.misa_id}</span>}
                </div>
                <div className="form-group">
                  <label className="form-label" htmlFor="f-key">Key Signature</label>
                  <input
                    id="f-key"
                    className="form-input"
                    value={keySignature}
                    onChange={(e) => setKeySignature(e.target.value)}
                    placeholder="e.g. G, D, F#m"
                  />
                </div>
              </div>
            )}

            {/* Key (for non-Ordinary) */}
            {!isOrdinary && (
              <div className="form-group" style={{ maxWidth: 200 }}>
                <label className="form-label" htmlFor="f-key2">Key Signature</label>
                <input
                  id="f-key2"
                  className="form-input"
                  value={keySignature}
                  onChange={(e) => setKeySignature(e.target.value)}
                  placeholder="e.g. G, D, F#m"
                />
              </div>
            )}

            {/* Lyrics */}
            <div className="form-group">
              <label className="form-label" htmlFor="f-lyrics">Lyrics *</label>
              <textarea
                id="f-lyrics"
                className="form-textarea"
                value={lyrics}
                onChange={(e) => setLyrics(e.target.value)}
                placeholder="Paste the full lyrics here…"
                rows={12}
              />
              {errors.lyrics && <span className="form-error">{errors.lyrics}</span>}
            </div>

            {/* Score PDF upload */}
            <div className="form-group">
              <label className="form-label">Sheet Music Score (PDF)</label>
              <div className="file-input-wrap">
                <label className="file-label">
                  <span>📄</span>
                  <span>{fileName || (song?.has_score ? 'Replace existing score…' : 'Choose PDF file…')}</span>
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={handleFileChange}
                    aria-label="Upload score PDF"
                  />
                </label>
              </div>
              {song?.has_score && !scoreFile && (
                <span style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 4 }}>
                  A score is already attached. Upload a new file to replace it.
                </span>
              )}
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-ghost" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-gold" disabled={submitting}>
              {submitting ? 'Saving…' : isNew ? 'Upload Song' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SongForm;
