# Perceptron

Maths practice for students aged 12–18 with ADHD and dyslexia: one fraction question at a time, read aloud with word-by-word highlighting, gentle three-step hints, and honey rewards that are never taken away.

## Stack

- **Frontend:** Vue 3 + Vite (`frontend/`)
- **Backend:** Flask + SQLite (`backend/`)
- No accounts, no external services, no API keys.

## Run it (development)

Two processes:

```bash
# terminal 1 — API on :5000
cd backend
pip install -r requirements.txt
python3 app.py

# terminal 2 — frontend on :5173
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api/*` to Flask, so no CORS is involved.

## Run it (demo, one process)

```bash
cd frontend && npm run build
cd ../backend && python3 app.py
```

Open http://localhost:5000 — Flask serves the built frontend and the API from one process.

`PERCEPTRON_DEMO=1` lowers the daily honey cap from 50 to 15 so the "Done for today" state is quick to show.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `PORT` | `5000` | Port Flask binds to (Render injects its own) |
| `PERCEPTRON_DEMO` | unset | `1` = demo cap of 15 honey/day |

No secrets exist in this project. The SQLite database (`backend/perceptron.db`) is created on first run.

## Deployment (optional, free tiers)

- Frontend: Vercel, serving `frontend/` — `frontend/vercel.json` rewrites `/api/*` to the Render API URL.
- API: Render web service from `backend/` — note the free tier's ephemeral filesystem resets the SQLite database on restart/spin-down.
- Push to the repository to trigger both deploys.

## Progress documents

`devpost/` holds the planning trail: scope, PRD, technical spec, and the build checklist.
