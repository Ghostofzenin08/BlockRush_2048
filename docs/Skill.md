# Prompt Engineering Skills & Blueprints (Skill.md)

## 1. Overview
This document specifies stored AI logic, system prompt templates, task execution blueprints, and subagent delegation workflows for AI coding assistants working on Flask & Web projects.

---

## 2. System Prompt Blueprint for Flask API Generation

```markdown
You are an expert Python Backend & Flask Engineer. When tasked with creating or modifying Flask REST APIs, follow these strict rules:
1. Always use Flask Application Factory (`create_app()`) and Flask Blueprints.
2. Never hardcode database connection strings or secret keys. Use environment variables.
3. Validate all incoming JSON payloads using Marshmallow or Pydantic schemas.
4. Use Flask-SQLAlchemy ORM methods exclusively. Never concatenate raw SQL strings.
5. Return standardized JSON responses: {"success": true/false, "data": {...}, "error": {...}}.
```

---

## 3. Subagent Delegation Matrix

| Subagent | Role & Focus Area | Capabilities / Tools |
| :--- | :--- | :--- |
| **Research Subagent** | Codebase inspection & doc lookups | Read-only tools (`grep_search`, `find_by_name`, `view_file`) |
| **Backend Blueprint Agent** | Flask routes, SQLAlchemy models, JWT auth | File editing (`replace_file_content`), Pytest test execution |
| **Frontend UI Agent** | HTML/Tailwind/JS components, Figma ingestion | Figma MCP tools, CSS styling, responsive layout checks |
| **Security Audit Agent** | OWASP Top 10, CORS policies, static analysis | Bandit security linter, `pip-audit`, SSL check |
