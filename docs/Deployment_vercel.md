# Frontend Vercel & Render Deployment Strategy (Deployment_vercel.md)

## 1. Cloud Architecture & Edge CDN Overview
The BlockRush deployment strategy decouples the static HTML5/Tailwind/JS frontend on **Vercel Edge CDN** from the Python WSGI backend hosted on **Render Web Services**.

```mermaid
graph TD
    Client[End User Browser] -->|HTTPS Edge CDN| Vercel[Vercel Global Edge Network]
    Vercel -->|REST API / JSON| Render[Render Web Service (Flask + Gunicorn)]
    Render -->|SSL Mode Require| NeonDB[(Neon PostgreSQL DB)]
```

---

## 2. Vercel Configuration (`vercel.json`)

Create `vercel.json` in the frontend root to handle routing and rewrites:

```json
{
  "version": 2,
  "name": "blockrush-frontend",
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/v1/(.*)",
      "dest": "https://blockrush-api.onrender.com/api/v1/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## 3. Render Infrastructure as Code (`render.yaml`)

Create `render.yaml` in the backend root:

```yaml
services:
  - type: web
    name: blockrush-backend-api
    env: python
    region: singapore
    plan: free
    buildCommand: "pip install -r requirements.txt && flask db upgrade"
    startCommand: "gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 4"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.4
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: CORS_ORIGINS
        value: "https://blockrush.vercel.app"
```
