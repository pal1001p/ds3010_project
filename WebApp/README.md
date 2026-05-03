# DS3010 Web App — Clone & Run Guide

React (Vite + TypeScript) frontend and a FastAPI backend for Connecticut property exploration and sale-price prediction.


### What must be in the repo for a fresh clone to work

- `package.json`, `package-lock.json`, `src/`, `vite.config.ts`, etc. (frontend)
- `backend/app.py`, `backend/requirements.txt` (API)
- **`backend/data/`**:
  - `model_parameters.csv`
  - `prediction_interval.txt`
  - `coefficient_ranking_all_columns.csv`

If those CSV/txt files are missing, prediction will not load until someone copies them in or sets `DS3010_DATA_DIR`.

## Prerequisites

- **Node.js 20+**
- **Python 3.11+** (3.12/3.13 usually work too)
- Two terminals (one for backend, one for frontend)

## Quick start (two terminals)

### Terminal A — Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

You should see startup lines like:

- `[ds3010] model data dir: …/backend/data`
- `[ds3010] predictor loaded OK`

Sanity check:

```bash
curl -s http://127.0.0.1:8000/api/health
```

You want `"predictor_ready": true`. If it is `false`, read `"predictor_error"` in that JSON.

### Terminal B — Frontend (Vite)

From the **repository root** (same folder as `package.json`):

```bash
npm install
npm run dev
```

Open `http://localhost:5173`.

The frontend calls the API at **`http://127.0.0.1:8000` by default** (see `src/services/api.ts`).

## Optional configuration

### Point the backend at a different model folder

If you keep model files outside the repo:

```bash
export DS3010_DATA_DIR="/absolute/path/to/folder/containing/model_parameters.csv"
```

Then restart the backend. The folder must contain (at least) `model_parameters.csv`. The other two files are used for intervals and feature importance.

### Point the frontend at a different API URL

Create a root env file (not committed) named `.env.local`:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Restart `npm run dev` after changing env vars.

**Note:** `backend/app.py` currently allows CORS from `http://localhost:5173` and `http://127.0.0.1:5173`. If you host the frontend on another origin, update `allow_origins` in `backend/app.py`.

## Common issues

### “Could not find …/backend/data/model_parameters.csv”

- Confirm the three files exist under `backend/data/`.
- Confirm you started Uvicorn from the `backend/` folder (or that `DS3010_DATA_DIR` is set correctly).
- Hit `/api/health` and verify `model_parameters_exists` is `true`.

### Prediction UI errors / network failures

- Ensure the backend is running on port **8000**.
- Check the browser devtools Network tab for `/api/predict` status codes.
- If you changed API host/port, set `VITE_API_BASE_URL`.

## Production-ish build (optional)

```bash
npm run build
npm run preview
```

This serves the built static site; you still need the backend running separately (or behind a reverse proxy).

## Repo hygiene (what not to commit)

These are ignored on purpose (or should be):

- `node_modules/`
- `dist/`
- `backend/.venv/`

## First-time git push (if you created the repo locally)

```bash
git init
git add .
git commit -m "Add DS3010 web app"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
