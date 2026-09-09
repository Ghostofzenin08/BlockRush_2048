# System Architecture & Tech Stack (Architecture.md)

## 1. Technology Stack Overview

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend Engine** | Python 3.11+ / Flask 3.0+ | Lightweight WSGI web framework using Application Factory pattern |
| **Database** | PostgreSQL on Neon DB | Serverless, autoscaling PostgreSQL with SSL connection pooling |
| **Database ORM** | Flask-SQLAlchemy / SQLAlchemy 2.0 | Python Object Relational Mapper |
| **Migrations** | Flask-Migrate / Alembic | Managed schema migration scripts |
| **Data Validation** | Marshmallow / Pydantic | Request payload validation & serialization |
| **Auth Engine** | Flask-JWT-Extended & Bcrypt | JWT authentication with custom claims & password hashing |
| **WSGI Server** | Gunicorn | Production WSGI HTTP server for UNIX |
| **Hosting & Infra** | Render & Vercel | Render for Flask API backend; Vercel for static frontend Edge CDN |

---

## 2. Recommended Directory Structure

```
blockrush-root/
├── docs/
│   ├── README.md
│   ├── PRD.md
│   ├── Architecture.md
│   ├── Rules.md
│   ├── Phases.md
│   ├── Designs.md
│   ├── Memory.md
│   ├── Skill.md
│   ├── Security_audits.md
│   ├── Security_db.md
│   ├── Authentication.md
│   ├── Color_theory.md
│   ├── Typography_icons.md
│   └── Deployment_vercel.md
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask Application Factory (create_app)
│   │   ├── extensions.py        # db, jwt, cors, migrate initializations
│   │   ├── config.py            # Development, Testing, Production Configs
│   │   ├── api/                 # Flask Blueprints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # /api/v1/auth Blueprint
│   │   │   ├── game.py          # /api/v1/game Blueprint
│   │   │   ├── leaderboard.py   # /api/v1/leaderboard Blueprint
│   │   │   └── support.py       # /api/v1/support Blueprint
│   │   ├── models/              # SQLAlchemy Database Models
│   │   │   ├── user.py
│   │   │   ├── game_session.py
│   │   │   └── support_query.py
│   │   ├── schemas/             # Marshmallow Validation Schemas
│   │   │   ├── auth_schema.py
│   │   │   └── game_schema.py
│   │   └── services/            # Core business & game logic algorithms
│   │       ├── auth_service.py
│   │       └── game_service.py
│   ├── migrations/              # Flask-Migrate Alembic scripts
│   ├── tests/                   # Pytest test suite
│   ├── wsgi.py                  # Entry point for Gunicorn (app = create_app())
│   ├── requirements.txt
│   └── render.yaml              # Render Infra-as-Code spec
├── frontend/
│   ├── index.html               # Multi-screen SPA HTML
│   ├── styles.css               # Responsive Tailwind & Figma design CSS
│   ├── script.js                # Client SPA router & REST API client
│   ├── goz_logo_dark.png
│   ├── goz_logo_light.png
│   └── assets/
└── README.md
```

---

## 3. Flask Application Factory Pattern (`app/__init__.py`)

```python
from flask import Flask
from app.config import get_config
from app.extensions import db, jwt, cors, migrate

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    migrate.init_app(app, db)

    # Register Blueprints
    from app.api.auth import auth_bp
    from app.api.game import game_bp
    from app.api.leaderboard import leaderboard_bp
    from app.api.support import support_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(game_bp, url_prefix="/api/v1/game")
    app.register_blueprint(leaderboard_bp, url_prefix="/api/v1/leaderboard")
    app.register_blueprint(support_bp, url_prefix="/api/v1/support")

    return app
```

---

## 4. Neon DB Connection Architecture
- Connection Mode: Mandatory SSL mode (`sslmode=require`).
- Connection String format:
  `postgresql://user:password@ep-xxx-pooler.neon.tech/neondb?sslmode=require`
- Database Engine: `pool_size=10`, `max_overflow=20`, `pool_recycle=300` for connection stability.
