# Changelog

All notable changes to this project are documented here.

---

## [Unreleased] — develop branch

---

## 2026-06-12 — Initial Build + CI Fixes

### Added — Full project scaffold

#### Backend (Django)
- `backend/requirements.txt` — Django 4.2, DRF, simplejwt, cors-headers, psycopg2, whitenoise, gunicorn, python-decouple, dj-database-url
- `backend/manage.py`
- `backend/parish_songs/settings.py` — JWT auth, CORS, WhiteNoise, dj-database-url, SQLite fallback for local dev
- `backend/parish_songs/urls.py` — all API routes wired up
- `backend/parish_songs/wsgi.py`
- `backend/users/models.py` — custom `User` model extending `AbstractUser` with `role` field (admin / superadmin)
- `backend/users/serializers.py` — `UserSerializer`, `CreateUserSerializer`
- `backend/users/views.py` — JWT login with role in token payload, `/me` endpoint, user CRUD, password change
- `backend/users/urls.py`
- `backend/users/admin.py`
- `backend/songs/models.py` — `Song` model with all fields (title, category, language, key_signature, lyrics, misa_id, ord_part, has_score, score_file, uploaded_by, uploaded_by_name, timestamps)
- `backend/songs/serializers.py` — auto-sets `uploaded_by`, `has_score`, and `score_url`
- `backend/songs/views.py` — public list/detail, admin create/update/delete, secure PDF download
- `backend/songs/urls.py`
- `backend/songs/admin.py`
- `backend/songs/management/commands/seed_songs.py` — loads 36 real parish songs across all categories + creates default superadmin (`director` / `ChangeMe123!`)

#### Backend tests
- `backend/songs/tests.py` — 11 tests covering public access, search, category filter, CRUD, auth guards
- `backend/users/tests.py` — 9 tests covering JWT login, `/me`, user management, superadmin-only permissions, self-delete prevention

#### Frontend (React + TypeScript + Vite)
- `frontend/package.json`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`, `index.html`
- `frontend/src/vite-env.d.ts` — Vite `ImportMeta.env` type reference
- `frontend/src/types.ts` — `Song`, `User`, `FilterType` interfaces
- `frontend/src/constants.ts` — `MISAS`, `PROPER_CATEGORIES`, `ORDINARY_PARTS`, `LANGUAGES`, `CAT_COLORS`, `CATEGORY_LABELS`, `ALL_CATEGORY_ORDER`
- `frontend/src/index.css` — full Deep Navy & Gold design system (CSS variables, buttons, forms, modals, song rows, sidebar, toasts, print styles, responsive)
- `frontend/src/main.tsx`
- `frontend/src/App.tsx` — BrowserRouter, `ProtectedRoute`, provider composition
- `frontend/src/api/client.ts` — Axios instance with JWT Bearer attach + silent token refresh on 401
- `frontend/src/context/AuthContext.tsx` — JWT login/logout, token persistence in localStorage, auto-verify on page load
- `frontend/src/components/Toast.tsx` — toast notification context + container (success / error / info)
- `frontend/src/components/Header.tsx` — logo, nav, role badge, login/logout
- `frontend/src/components/Sidebar.tsx` — Proper categories + collapsible Misa groups with part drill-down, live song counts
- `frontend/src/components/SongRow.tsx` — index number, colour dot, title (EB Garamond), meta line, category/misa chips, chevron
- `frontend/src/components/SongDetail.tsx` — full-screen modal: lyrics, chips, score download, print, edit/delete for admins
- `frontend/src/components/SongForm.tsx` — upload/edit modal: all fields, Misa conditional fields, PDF file upload
- `frontend/src/pages/Library.tsx` — main page: search + language filter, sidebar filter, grouped song rows, all modals wired
- `frontend/src/pages/Login.tsx` — JWT login form
- `frontend/src/pages/AdminPage.tsx` — superadmin-only: user table + create user form

#### CI/CD (GitHub Actions — free tier)
- `.github/workflows/backend.yml` — runs Django tests on SQLite (no external DB needed), triggers Render deploy hook on push to master
- `.github/workflows/frontend.yml` — TypeScript check + Vite build, triggers Vercel deploy on push to master

#### Config / project files
- `backend/.env.example`
- `frontend/.env.example`
- `backend/.gitignore`, `frontend/.gitignore`, root `.gitignore`
- `README.md` — full setup guide, API reference, deployment steps

---

### Fixed — 2026-06-12 (CI run 1)

**Problem:** Frontend CI failed at `actions/setup-node` with:
> `Error: Some specified paths were not resolved, unable to cache dependencies.`

**Cause:** `cache-dependency-path: frontend/package-lock.json` was set but no `package-lock.json` existed yet (npm install had not been run locally).

**Fix:** Removed `cache: 'npm'` and `cache-dependency-path` from both `setup-node` steps in `frontend.yml`. Changed `npm ci` → `npm install` (ci requires a lock file; install generates one).

---

### Fixed — 2026-06-12 (CI run 1)

**Problem:** `frontend.yml` YAML lint errors:
1. Line 2: `Expected a scalar value, a sequence, or a mapping` (invisible BOM character)
2. Line 90: `Unrecognized named-value: 'secrets'` / `Unexpected symbol: '${{' in if expression`

**Cause:**
1. File encoding issue introduced a BOM.
2. GitHub Actions does not allow the `secrets` context inside a step-level `if:` expression.

**Fix:**
1. Rewrote the file cleanly.
2. Removed `if: ${{ secrets.VERCEL_TOKEN != '' }}` from the step. Moved the check into the shell script using `[ -n "$VERCEL_TOKEN" ]`, which is safe and equivalent.

---

### Fixed — 2026-06-12 (CI run 1)

**Problem:** Workflow branches were targeting `main` but the GitHub default branch is `master`.

**Fix:** Updated both `backend.yml` and `frontend.yml` — replaced all occurrences of `main` with `master` in `branches:` triggers and `if: github.ref ==` conditions.

---

### Fixed — 2026-06-12 (CI run 2)

**Problem:** TypeScript check failed with 5 errors:

| File | Error |
|------|-------|
| `src/api/client.ts:4` | `TS2339: Property 'env' does not exist on type 'ImportMeta'` |
| `src/context/AuthContext.tsx:11` | `TS2339: Property 'env' does not exist on type 'ImportMeta'` |
| `src/pages/Library.tsx:1` | `TS6133: 'React' is declared but its value is never read` |
| `src/pages/Library.tsx:81` | `TS2345: string not assignable to ALL_CATEGORY_ORDER union` |
| `src/components/SongForm.tsx:39` | `TS2345: string not assignable to ORDINARY_CAT_IDS union` |

**Fixes:**
1. Created `frontend/src/vite-env.d.ts` with `/// <reference types="vite/client" />` — this gives TypeScript the `ImportMeta.env` type from Vite.
2. Removed unused `React` import from `Library.tsx` (not needed with the modern JSX transform configured in `tsconfig.json`).
3. Cast `a` and `b` to `typeof ALL_CATEGORY_ORDER[number]` in the `indexOf` calls in `Library.tsx`.
4. Cast `category` to `typeof ORDINARY_CAT_IDS[number]` in the `includes()` call in `SongForm.tsx`.
