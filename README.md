# Data-Hub (MVP)

Full-stack MVP with Flask API and Vite + React frontend.

## Tech
- **Backend**: Flask, SQLAlchemy, Marshmallow, CORS, Gunicorn
- **Frontend**: Vite + React, React Router, Formik, Yup

## Project Structure
```
Data-Hub/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── requirements.txt
│   └── instance/
│       └── (app.db auto-created)
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api.js
        ├── components/
        │   ├── NavBar.jsx
        │   └── UploadForm.jsx
        ├── pages/
        │   ├── Dashboard.jsx
        │   ├── Upload.jsx
        │   └── Collections.jsx
        └── styles/
            └── global.css
```

## Backend: Run Locally
```
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows (WSL) ok; on Windows cmd: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --port 5000
```
- API base URL (local): `http://localhost:5000/api`
- Tables are created automatically on startup (`db.create_all()`).

### Database migrations (Alembic via Flask-Migrate)
We set up Flask-Migrate so you can manage schema changes.

Initial setup (first time only):
```
cd backend
source venv/bin/activate
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial"
flask db upgrade
```
Later, when models change:
```
flask db migrate -m "<describe change>"
flask db upgrade
```

Note: There's a lightweight SQLite safety in `app.py` that adds `file_tags.created_at` if missing, but Alembic is the preferred path.

## Frontend: Run Locally
```
cd frontend
npm install
npm run dev
```
- Open the printed local URL (default: `http://localhost:5173`).
- The frontend talks to the backend via `VITE_API_URL` (defaults to `http://localhost:5000/api`).

## Routes (MVP)
- `POST /api/register` { username, password }
- `POST /api/login` { username, password }
- `GET /api/files`
- `POST /api/files` (multipart or JSON)
- `GET /api/files/:id`
- `PATCH /api/files/:id`
- `DELETE /api/files/:id`
- `GET /api/collections`
- `POST /api/collections` { name, user_id, file_ids? }

## Models and Relationships
- `User` 1—* `File`
- `User` 1—* `Collection`
- `File` *—* `Tag` (via `file_tags` with `added_by` column)
- `Collection` *—* `File` (via `collection_files`)

## Deployment

### Backend (Render)
1. Push `backend/` to GitHub (or whole repo).
2. Create Render Web Service.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables: `DATABASE_URL`, `SECRET_KEY`
3. Deploy and copy the Base URL, e.g. `https://your-backend.onrender.com`

### Frontend (Vercel)
1. Push `frontend/` to GitHub (or the whole repo and set project root to `frontend/`).
2. Import in Vercel.
3. Add Environment Variable:
   - `VITE_API_URL=https://your-backend.onrender.com/api`
4. Deploy.

## Notes
- This MVP auth is not secure; do not use for production authentication.
- File uploads are stored in `backend/instance/uploads/` for development.
- For local testing, create a user first via `POST /api/register` before uploading files (default `UploadForm` uses `user_id = 1`).


## Seeding the Database
We provide `backend/seed.py` to populate development data (users, files, tags with `added_by`, collections with files).

Steps:
```
cd backend
source venv/bin/activate
export FLASK_APP=app.py
flask db upgrade       # ensure schema is current
python seed.py         # populate seed data
```

Seed contents include examples like users `alice`, `bob`, `carol`, files with tags (e.g., `finance`, `health`, `personal`), and collections that reference multiple files.

Team Members
M
