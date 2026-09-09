# Project Roadmap & Execution Plan (Phases.md)

## Phase 1: Environment Scaffolding & Database Setup
- **Goal**: Initialize Flask backend app factory, Neon DB connection pooling, and Alembic migrations.
- **Tasks**:
  1. Create virtual environment and install requirements (`Flask`, `Flask-SQLAlchemy`, `Flask-Migrate`, `Flask-JWT-Extended`, `psycopg2-binary`, `gunicorn`).
  2. Implement `app/__init__.py` Application Factory and `app/config.py`.
  3. Configure Neon DB pooled PostgreSQL connection string (`sslmode=require`).
  4. Run `flask db init` and initial Alembic migration.

---

## Phase 2: Authentication & User Blueprints
- **Goal**: Build secure user registration, login, and JWT authorization middleware.
- **Tasks**:
  1. Define `User` SQLAlchemy model with `bcrypt` password hashing.
  2. Implement `/api/v1/auth/register` and `/api/v1/auth/login` Blueprints.
  3. Configure `Flask-JWT-Extended` with Access and Refresh tokens.
  4. Write unit tests in `tests/test_auth.py`.

---

## Phase 3: BlockRush Game Logic & Leaderboard APIs
- **Goal**: Implement server-side game score submission, session logging, and leaderboard rankings.
- **Tasks**:
  1. Define `GameSession` and `HighScore` SQLAlchemy models.
  2. Implement `/api/v1/game/submit` endpoint with game score validation.
  3. Implement `/api/v1/leaderboard` Blueprint supporting top weekly and all-time rankings.
  4. Implement `/api/v1/support/query` endpoint for handling BlockDocs player inquiries.

---

## Phase 4: Frontend UI Sync & Figma Design Compliance
- **Goal**: Integrate HTML5/Tailwind/JS frontend with Flask REST API.
- **Tasks**:
  1. Connect JavaScript `fetch()` client to Flask API endpoints.
  2. Enforce Figma design node `594-2` fonts (`Instrument Sans`, `Inria Sans`) and colors (`#1d1e2c`, `#ffbd00`, `#9e0059`, `#04c7fd`).
  3. Verify mobile responsiveness across 320px to 1280px viewports.

---

## Phase 5: Production Deployment & Security Audit
- **Goal**: Deploy Flask backend API to Render and static frontend to Vercel.
- **Tasks**:
  1. Deploy Flask Gunicorn service to Render Web Services.
  2. Deploy static frontend to Vercel with HTTPS edge CDN.
  3. Configure CORS origins and security headers using `Flask-Talisman`.
  4. Run static analysis tools (`bandit`, `pip-audit`).
