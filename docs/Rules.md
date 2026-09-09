# Development Rules & Prompt Standards (Rules.md)

## 1. Core Development Rules

### 1.1 Python & Flask Coding Standards
- **Application Factory**: Always use `create_app()` factory function to instantiate Flask applications. Never create global `app = Flask(__name__)` at module level.
- **Blueprints**: Group related routes inside dedicated Flask Blueprints (`auth_bp`, `game_bp`, `support_bp`).
- **ORM Transactions**: Always handle SQLAlchemy database sessions cleanly:
  ```python
  try:
      db.session.add(entity)
      db.session.commit()
  except Exception as e:
      db.session.rollback()
      raise e
  ```
- **Explicit Error Handlers**: Return standard JSON error responses using `@app.errorhandler(400)`, `@app.errorhandler(404)`, `@app.errorhandler(500)`.

### 1.2 Anti-Patterns (What NOT To Do)
- ❌ **NO Raw SQL Concatenation**: Never build SQL queries using string formatting (`f"SELECT * FROM users WHERE name='{user_input}'"`). Always use SQLAlchemy ORM or parameterized queries.
- ❌ **NO Hardcoded Credentials**: Never hardcode database passwords, JWT secret keys, or API tokens in source files. Use `os.environ.get()` with `pydantic-settings` or `python-dotenv`.
- ❌ **NO Silent Failure**: Never use empty `except:` blocks that swallow exceptions without logging.
- ❌ **NO Direct DOM Mutation in Global Scope**: Keep JavaScript UI state inside component functions or event handlers.

---

## 2. Standard JSON Error Response Format

All API errors must return a consistent JSON payload:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PAYLOAD",
    "message": "Validation failed for field 'email': Invalid email format.",
    "status_code": 400
  }
}
```

---

## 3. AI Prompt Engineering Rules for Coding Agents
1. **Never Invent Symbols**: View existing source files before writing imports, functions, or variable names.
2. **Obey Design Tokens**: Strictly follow color tokens (`#ffbd00`, `#ff0054`, `#390099`, `#9e0059`, `#04c7fd`, `#1d1e2c`) and font rules (`Instrument Sans`, `Inria Sans`).
3. **Verify Code Execution**: Always test endpoints or run build scripts after modifying files.
