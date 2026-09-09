# Flask & BlockRush Full Stack Prompt Engineering Strategy & Specification

Welcome to the **Flask Prompt Engineering Specification** workspace for **BlockRush**. This documentation suite provides a production-grade strategy for building, auditing, and deploying modern full-stack web applications powered by a **Flask Python backend**, **Neon PostgreSQL database**, **Render cloud hosting**, and **HTML5/Tailwind/JS frontend**.

---

## 🚀 Tech Stack & Application Ecosystem

### Backend Engine & Frameworks
- [**Python 3.11+**](https://www.python.org/) - Server-side programming language.
- [**Flask 3.0+**](https://flask.palletsprojects.com/) - Lightweight WSGI web application framework using Application Factories and Blueprints.
- [**SQLAlchemy 2.0**](https://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper (ORM).
- [**Flask-SQLAlchemy**](https://flask-sqlalchemy.palletsprojects.com/) - Flask extension providing SQLAlchemy integration.
- [**Alembic / Flask-Migrate**](https://flask-migrate.readthedocs.io/) - Database migration management.
- [**Marshmallow / Pydantic**](https://marshmallow.readthedocs.io/) - Object serialization, deserialization, and request payload validation.
- [**Flask-JWT-Extended**](https://flask-jwt-extended.readthedocs.io/) - JWT token authentication management.
- [**Pytest**](https://docs.pytest.org/) - Automated testing framework for unit and API integration test suites.

### Database & Cloud Infrastructure
- [**PostgreSQL**](https://www.postgresql.org/) - Advanced open-source relational database.
- [**Neon DB**](https://neon.tech/) - Serverless PostgreSQL with instant branching, autoscaling, and connection pooling.
- [**Render**](https://render.com/) - Managed cloud hosting for Flask WSGI Web Services (Gunicorn).
- [**Vercel**](https://vercel.com/) - Cloud platform for frontend static site edge CDN hosting.

### Security, Audits & Tools
- [**OWASP Top 10**](https://owasp.org/www-project-top-ten/) - Web application security standard.
- [**Flask-CORS**](https://flask-cors.readthedocs.io/) - Cross-Origin Resource Sharing handling.
- [**Flask-Talisman**](https://github.com/GoogleCloudPlatform/flask-talisman) - HTTP security headers (CSP, HSTS, X-Content-Type-Options).
- [**Bandit**](https://bandit.readthedocs.io/) - Python security linter.

---

## 📚 Strategy Documentation Map

The Flask prompt engineering architecture is organized into 13 modular specification documents:

1. [**`PRD.md`**](PRD.md) - **Project Requirement Document**: Vision, target audience, feature specifications, and sequence diagrams.
2. [**`Architecture.md`**](Architecture.md) - **System Architecture**: Directory layout, Flask Application Factory pattern, Neon DB connection pooling, and Gunicorn WSGI config.
3. [**`Rules.md`**](Rules.md) - **Development Rules**: Flask best practices, anti-patterns (what to avoid), error handling, and AI prompt engineering standards.
4. [**`Phases.md`**](Phases.md) - **Project Roadmap**: 5-phase execution plan from scaffolding to auth, game engine integration, and production release.
5. [**`Designs.md`**](Designs.md) - **Frontend Design System**: Color tokens, Tailwind CSS rules, Figma MCP ingestion, and HTML templates.
6. [**`Memory.md`**](Memory.md) - **AI System Memory**: AGY implementation plan tracking, state preservation, and session memory context.
7. [**`Skill.md`**](Skill.md) - **Prompt Engineering Skills**: Stored AI logic, system prompt templates, task blueprints, and subagent delegation.
8. [**`Security_audits.md`**](Security_audits.md) - **System Security Audits**: OWASP Top 10 mitigation, CORS policies, XSS/CSP headers, and static analysis workflows.
9. [**`Security_db.md`**](Security_db.md) - **Database Security & DLP**: Neon DB TLS 1.3 encryption, database branching, point-in-time recovery (PITR), and SQL injection defenses.
10. [**`Authentication.md`**](Authentication.md) - **Authentication Strategy**: Flask-JWT-Extended, bcrypt hashing, refresh tokens, and Role-Based Access Control (RBAC).
11. [**`Color_theory.md`**](Color_theory.md) - **Color Theory & Palette Strategy**: Figma design node 594-2 palette, 60-30-10 rule, Tailwind palette mapping, and WCAG contrast rules.
12. [**`Typography_icons.md`**](Typography_icons.md) - **Typography & Icons Strategy**: Google Fonts (`Instrument Sans`, `Inria Sans`), font scaling, and Material Symbols.
13. [**`Deployment_vercel.md`**](Deployment_vercel.md) - **Frontend Vercel Deployment**: Vercel Edge CDN configuration, `vercel.json` rewrites, env variables, and Render CORS sync.

---

## ⚡ Quickstart & Local Setup

```bash
# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Flask dependencies
pip install -r backend/requirements.txt

# Run Flask development server
flask run --host=0.0.0.0 --port=5000
```
