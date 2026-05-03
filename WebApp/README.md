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

## Need to use two ternimals

### Terminal A — Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
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

### Point the backend at a different model folder

If you keep model files outside the repo:

```bash
export DS3010_DATA_DIR="/absolute/path/to/folder/containing/model_parameters.csv"
```



