import os
from app import create_app
from app.extensions import db

env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)

# Create database tables automatically for SQLite/Dev mode
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
