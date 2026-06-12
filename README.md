# Parish Song Library

A full-stack digital hymnal for a Catholic parish choir in Kenya.  
Choir members browse and read lyrics on their phones during Mass rehearsals and services.  
Choir directors log in to manage the song catalogue.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite |
| Backend | Python + Django 4.2 + Django REST Framework |
| Database | PostgreSQL (SQLite for local dev) |
| Auth | JWT via djangorestframework-simplejwt |
| Frontend hosting | Vercel |
| Backend hosting | Render.com |

---

## Project Structure

```
parish-songs/
├── backend/         ← Django API
└── frontend/        ← React TypeScript app
```

---

## Backend Setup

### 1. Create and activate a virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY, DATABASE_URL, etc.
```

For local development with SQLite you can leave `DATABASE_URL` unset —
it defaults to `db.sqlite3` in the project root.

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Seed the database (songs + default superadmin)

```bash
python manage.py seed_songs
```

Default superadmin credentials: `director` / `ChangeMe123!`  
**Change this password immediately after first login.**

### 6. Start the development server

```bash
python manage.py runserver
```

API is now available at `http://localhost:8000`.

---

## Frontend Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure environment

```bash
cp .env.example .env.local
# Edit .env.local — set VITE_API_URL=http://localhost:8000
```

### 3. Start the development server

```bash
npm run dev
```

App is now available at `http://localhost:5173`.

---

## API Reference

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/login/` | — | JWT login → access + refresh tokens |
| `POST` | `/api/auth/refresh/` | — | Refresh access token |
| `GET`  | `/api/auth/me/` | Bearer | Current user info |

### Songs

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET`    | `/api/songs/`       | — | List songs. Query: `?category=`, `?misa_id=`, `?language=`, `?search=` |
| `POST`   | `/api/songs/`       | Admin | Upload song (`multipart/form-data`) |
| `GET`    | `/api/songs/{id}/`  | — | Get single song |
| `PUT`    | `/api/songs/{id}/`  | Admin | Update song |
| `DELETE` | `/api/songs/{id}/`  | Admin | Delete song |
| `GET`    | `/api/songs/{id}/score/` | — | Download score PDF |

### Users (Superadmin only)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET`    | `/api/users/`              | Superadmin | List all admins |
| `POST`   | `/api/users/`              | Superadmin | Create admin user |
| `DELETE` | `/api/users/{id}/`         | Superadmin | Remove admin |
| `PUT`    | `/api/users/{id}/password/`| Self or Superadmin | Change password |

---

## User Roles

| Role | Permissions |
|------|-------------|
| **Public** | Browse all songs, search, filter, view lyrics, print |
| **Admin** | All public + upload, edit, delete songs |
| **Superadmin** | All admin + manage admin user list |

At launch there are 4 users: 1 Superadmin + 3 Admins.

---

## Song Categories

### Proper of Mass
Entrance · Bible Procession · Offertory · Communion · Thanksgiving · Recessional · Responsorial Psalm

### Ordinary of Mass (belong to a Misa)
ord-Kyrie · ord-Gloria · ord-Sanctus · ord-Agnus Dei · ord-Other

### Misa Settings
Misa Banana · Misa Subukia · Misa Taita · Misa AMECEA · Other Misa

---

## Deployment

### Backend — Render.com

- **Service type:** Web Service
- **Build command:**
  ```
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
  ```
- **Start command:**
  ```
  gunicorn parish_songs.wsgi:application
  ```
- **Environment variables:**
  - `DATABASE_URL` — from Render PostgreSQL add-on
  - `SECRET_KEY` — long random string
  - `DEBUG` — `False`
  - `ALLOWED_HOSTS` — your `.onrender.com` domain
  - `CORS_ALLOWED_ORIGINS` — your Vercel frontend URL

After first deploy, run the seed command via Render's shell:
```bash
python manage.py seed_songs
```

### Frontend — Vercel

- **Framework preset:** Vite
- **Build command:** `npm run build`
- **Output directory:** `dist`
- **Environment variable:**
  - `VITE_API_URL` — your Render backend URL (e.g. `https://parish-songs.onrender.com`)

---

## Languages Supported

Swahili · Kikuyu · English · Latin · Other

---

## Design System

**Fonts:** Cinzel (headings/labels) · EB Garamond (lyrics/titles) · Inter (UI)  
**Theme:** Deep Navy & Gold — cathedral aesthetic

```
--navy:   #0D1B2E   page background
--gold:   #C9A84C   primary accent
--text:   #FAF8F3   primary text
```
