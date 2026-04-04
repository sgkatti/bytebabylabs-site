# NETOPS: Packet Catcher — FastAPI + Render.com Setup Guide

## Architecture

```
GitHub Pages  (netops-game-v3.html)
      │
      │  fetch() to your Render URL
      ▼
Render.com  (FastAPI + SQLite on persistent disk)
      │
      │  SQLite WAL mode, auto-persisted
      ▼
  netops.db  (leaderboard data)
```

Zero Supabase. Zero extra accounts. Just Python + Render.

---

## Part 1 — Deploy the FastAPI Backend to Render.com

### Step 1 — Create a new GitHub repo for the API

```bash
# Unzip the provided netops-api.zip, then:
cd netops-api
git init
git add .
git commit -m "feat: NETOPS leaderboard API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/netops-api.git
git push -u origin main
```

The repo structure should look like this:
```
netops-api/
├── app/
│   └── main.py          ← FastAPI application
├── requirements.txt     ← fastapi, uvicorn, pydantic
├── render.yaml          ← Render deployment config
├── Procfile             ← fallback start command
└── README.md
```

### Step 2 — Create the Web Service on Render

1. Go to https://render.com → **New** → **Web Service**
2. Connect your GitHub account and select the `netops-api` repo
3. Render will auto-detect the `render.yaml` — confirm these settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `netops-api` (or any name) |
   | **Runtime** | Python |
   | **Build command** | `pip install -r requirements.txt` |
   | **Start command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Instance type** | Free |

### Step 3 — Add a Persistent Disk (IMPORTANT)

SQLite needs a persistent disk so data survives service restarts.

In Render dashboard → your service → **Disks** → **Add Disk**:

| Field | Value |
|-------|-------|
| **Name** | `netops-db` |
| **Mount path** | `/opt/render/project/src` |
| **Size** | 1 GB (free tier max) |

### Step 4 — Set Environment Variables

In Render → your service → **Environment** → add:

| Key | Value |
|-----|-------|
| `DB_PATH` | `/opt/render/project/src/netops.db` |
| `ALLOWED_ORIGIN` | `https://YOUR_USERNAME.github.io` |
| `MAX_SCORE` | `999999` |
| `RATE_LIMIT_REQ` | `15` |
| `RATE_LIMIT_WIN` | `60` |

> **ALLOWED_ORIGIN** is your GitHub Pages URL. This locks CORS so only
> your game can call the API. Set it to `*` during testing if needed.

### Step 5 — Deploy

Click **Create Web Service**. Render will build and deploy in ~2 minutes.

Your API will be live at:
```
https://netops-api.onrender.com
```
(or whatever name you chose)

Test it by visiting:
```
https://netops-api.onrender.com/docs
```
This opens the auto-generated Swagger UI — you can test all endpoints live.

---

## Part 2 — Configure the Game HTML

Open `netops-game-v3.html` and find this line near the top of the `<script>`:

```javascript
const API_URL = 'https://YOUR-SERVICE.onrender.com';
```

Replace with your actual Render URL:

```javascript
const API_URL = 'https://netops-api.onrender.com';
```

---

## Part 3 — Deploy Game to GitHub Pages

```bash
# In your game repo:
cp netops-game-v3.html index.html
git add index.html
git commit -m "feat: add leaderboard with FastAPI backend"
git push
```

GitHub → repo **Settings** → **Pages** → Source: `main` / `/ (root)` → Save.

---

## API Reference

All endpoints return JSON. Base URL: `https://YOUR-SERVICE.onrender.com`

### `GET /`
Health check. Returns `{"status": "online"}`.

### `GET /health`
DB connectivity check. Returns `{"status": "ok", "db": "connected"}`.

### `POST /scores`
Submit a score after a game.

**Request body:**
```json
{
  "player_name": "xXNetOpsXx",
  "score": 4200,
  "difficulty": "hard",
  "caught": 28,
  "wrong": 3,
  "dropped": 1,
  "level": 4
}
```

**Response:**
```json
{
  "id": 42,
  "rank": 3,
  "message": "Score saved! You are ranked 🥉 on HARD"
}
```

### `GET /scores`
Get leaderboard (up to 100 entries, sorted by score descending).

Optional query params:
- `?difficulty=easy|normal|hard` — filter by mode
- `?limit=50` — max entries (default 100, max 200)
- `?offset=0` — for pagination

**Response:**
```json
{
  "scores": [
    {
      "id": 42,
      "player_name": "xXNetOpsXx",
      "score": 4200,
      "difficulty": "hard",
      "caught": 28,
      "wrong": 3,
      "dropped": 1,
      "level": 4,
      "created_at": "2025-04-04T10:22:00"
    }
  ],
  "total": 87,
  "filter_diff": "hard",
  "generated": "2025-04-04T10:30:00Z"
}
```

### `GET /scores/player/{player_name}`
Get all scores for a specific player.

### `GET /scores/rank/{player_name}?difficulty=hard`
Get a player's best rank on a given difficulty.

### `GET /stats`
Global statistics.

```json
{
  "total_games": 214,
  "unique_players": 38,
  "top_score": 18400,
  "avg_score": 1240,
  "by_difficulty": [
    {"difficulty": "easy",   "games": 80,  "top": 4200},
    {"difficulty": "normal", "games": 90,  "top": 12000},
    {"difficulty": "hard",   "games": 44,  "top": 18400}
  ]
}
```

---

## ⚠️ Render Free Tier — Cold Start Note

Render free tier **spins down** after 15 minutes of inactivity.
The first request after sleep takes ~30 seconds to wake up.

**Solutions:**

**Option A — Just display a loading message (already built in)**
The game shows `// submitting score...` and `// FETCHING RECORDS FROM DB...`
while waiting, so players see feedback.

**Option B — Keep-alive ping (free)**
Use https://cron-job.org (free) to ping your `/health` endpoint every 10 minutes:
```
URL: https://netops-api.onrender.com/health
Schedule: */10 * * * *
```

**Option C — Upgrade to Render Starter ($7/month)**
No sleep, instant responses.

---

## Local Development & Testing

```bash
cd netops-api
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload --port 8000

# API docs:  http://localhost:8000/docs
# Test POST: http://localhost:8000/scores
```

For local testing, change `API_URL` in the HTML to `http://localhost:8000`.

---

## Upgrading to Postgres (optional, when you outgrow SQLite)

If you move to Render's managed Postgres later, replace the SQLite logic
in `main.py` with `psycopg2` or `asyncpg`. The API endpoints and HTML
game code stay identical — only the DB driver changes.

```python
# In render.yaml, add:
databases:
  - name: netops-postgres
    plan: free
```

Then set `DATABASE_URL` env var in Render and swap `sqlite3` for
`psycopg2` in `main.py`.

---

## Security Notes

| Concern | Mitigation |
|---------|------------|
| Score spoofing | `MAX_SCORE` env var rejects absurd values. God mode skips submit. |
| Name injection | Regex `^[\w]{2,16}$` enforced in Pydantic + DB CHECK constraint |
| Flooding | Per-IP rate limiter (15 req/60s default, configurable via env) |
| CORS | Locked to your GitHub Pages origin via `ALLOWED_ORIGIN` |
| SQL injection | SQLite parameterised queries throughout (`?` placeholders) |
| Data loss | WAL journal mode + persistent disk on Render |
