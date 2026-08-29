# FraudLens — Scam Message Risk Checker (Frontend)

React frontend for the scam-message risk checker. Built with Vite + React Router + Axios + Recharts.

## Setup

```bash
npm install
cp .env.example .env   # then edit VITE_API_URL if your Django backend isn't on localhost:8000
npm run dev
```

App runs at `http://localhost:5173`.

## Pages

- **Checker (`/`)** — paste a message/URL, calls `POST /api/analyze/`, shows a risk gauge + reasons.
- **Dashboard (`/dashboard`)** — calls `GET /api/trending/` on load, shows stat cards + a bar chart.
- **About (`/about`)** — static page explaining the rules → campaign match → score → LLM-explain pipeline.

## Backend API contract expected by this frontend

### `POST /api/analyze/`
Request:
```json
{ "content": "the pasted message or URL" }
```
Response:
```json
{
  "risk_level": "HIGH",
  "score": 82,
  "reasons": ["Suspicious URL detected", "Requests OTP/PIN", "Urgent/threatening language"],
  "matched_campaign": "Fake KYC update",
  "recommendation": "Do not click or pay until verified."
}
```

### `GET /api/trending/`
Response:
```json
{
  "total_submissions": 128,
  "total_scams_caught": 94,
  "categories": [
    { "name": "Fake KYC", "count": 41 },
    { "name": "Delivery fee", "count": 27 }
  ]
}
```

### `POST /api/report/`
Request:
```json
{ "content": "confirmed scam text", "category": "Fake KYC" }
```

## Django CORS setup (needed for local dev)

```bash
pip install django-cors-headers
```

In `settings.py`:
```python
INSTALLED_APPS = [..., "corsheaders"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", ...]  # keep near the top
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
```

## Deployment

- **Frontend**: Vercel or Netlify — connect the GitHub repo, set `VITE_API_URL` as an environment
  variable to your deployed backend URL, done.
- **Backend**: Render or Railway.

Remember to update `VITE_API_URL` for the production backend before the final demo.
