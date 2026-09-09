from datetime import datetime, timezone
from app.extensions import db

class GameSession(db.Model):
    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    mode = db.Column(db.String(32), default="classic") # classic, challenge, playground
    tier = db.Column(db.String(32), default="Beginner") # Beginner, Pro, Master
    level = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer, default=0)
    max_tile = db.Column(db.Integer, default=2)
    duration_seconds = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mode": self.mode,
            "tier": self.tier,
            "level": self.level,
            "score": self.score,
            "max_tile": self.max_tile,
            "duration_seconds": self.duration_seconds,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class HighScore(db.Model):
    __tablename__ = "high_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    player_name = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Integer, default=0)
    max_tile = db.Column(db.Integer, default=2048)
    mode = db.Column(db.String(32), default="classic")
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "player_name": self.player_name,
            "score": self.score,
            "max_tile": self.max_tile,
            "mode": self.mode,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
