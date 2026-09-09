from datetime import datetime, timezone
from app.extensions import db

class SupportQuery(db.Model):
    __tablename__ = "support_queries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    query_text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending") # pending, resolved, closed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "query_text": self.query_text,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
