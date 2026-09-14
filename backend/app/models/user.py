from datetime import datetime, timezone
from app.extensions import db

class User(db.Model):
    __tablename__ = "blockrush_users"

    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True, index=True)
    username = db.Column(db.String(64), unique=True, nullable=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    display_name = db.Column(db.String(128), nullable=True)
    photo_url = db.Column(db.String(512), nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    role = db.Column(db.String(20), default="player")
    level = db.Column(db.Integer, default=1)
    high_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    game_sessions = db.relationship("GameSession", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "firebase_uid": self.firebase_uid,
            "username": self.username or self.display_name or (self.email.split("@")[0] if self.email else "Player"),
            "email": self.email,
            "display_name": self.display_name,
            "photo_url": self.photo_url,
            "role": self.role,
            "level": self.level,
            "high_score": self.high_score,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
