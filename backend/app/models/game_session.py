from datetime import datetime, timezone
from app.extensions import db

class GameSession(db.Model):
    __tablename__ = "blockrush_game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    session_uid = db.Column(db.String(64), unique=True, nullable=True, index=True) # e.g. sess_50
    user_id = db.Column(db.Integer, db.ForeignKey("blockrush_users.id"), nullable=True)
    user_identifier = db.Column(db.String(128), index=True, default="player0123")
    mode = db.Column(db.String(32), default="classic") # classic, challenge, playground
    tier = db.Column(db.String(32), default="Beginner") # Beginner, Pro, Master
    level = db.Column(db.Integer, default=1)
    grid_size = db.Column(db.String(16), default="4x4")
    target_tile = db.Column(db.Integer, default=2048)
    score = db.Column(db.Integer, default=0)
    max_tile = db.Column(db.Integer, default=2)
    number_of_moves = db.Column(db.Integer, default=0)
    duration_seconds = db.Column(db.Integer, default=0)
    game_status = db.Column(db.String(32), default="playing") # playing, won, lost, completed
    completed = db.Column(db.Boolean, default=False)
    session_start_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_uid or f"sess_{self.id}",
            "user_id": self.user_id,
            "user_identifier": self.user_identifier,
            "mode": self.mode,
            "tier": self.tier,
            "level": self.level,
            "grid_size": self.grid_size,
            "target_tile": self.target_tile,
            "score": self.score,
            "highest_tile": self.max_tile,
            "max_tile": self.max_tile,
            "number_of_moves": self.number_of_moves,
            "duration_seconds": self.duration_seconds,
            "game_status": self.game_status,
            "completed": self.completed,
            "session_start_time": self.session_start_time.isoformat() if self.session_start_time else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class PlayerHistory(db.Model):
    __tablename__ = "blockrush_player_histories"

    id = db.Column(db.Integer, primary_key=True)
    user_identifier = db.Column(db.String(128), unique=True, nullable=False, index=True) # player0123 or Firebase UID
    current_level = db.Column(db.Integer, default=1)
    level_tier = db.Column(db.String(32), default="Beginner")
    current_score = db.Column(db.Integer, default=0)
    high_score = db.Column(db.Integer, default=0)
    best_score = db.Column(db.Integer, default=0)
    highest_tile = db.Column(db.Integer, default=2)
    total_moves = db.Column(db.Integer, default=0)
    total_playtime_seconds = db.Column(db.Integer, default=0)
    sessions_completed = db.Column(db.Integer, default=0)
    unlocked_tiers = db.Column(db.JSON, default=lambda: ["Beginner"])
    latest_grid_size = db.Column(db.String(16), default="4x4")
    last_active = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    recent_sessions = db.Column(db.JSON, default=list)

    def to_dict(self):
        return {
            "user_id": self.user_identifier,
            "current_level": self.current_level,
            "level_tier": self.level_tier,
            "current_score": self.current_score,
            "high_score": self.high_score,
            "best_score": self.best_score,
            "highest_tile": self.highest_tile,
            "total_moves": self.total_moves,
            "total_playtime_seconds": self.total_playtime_seconds,
            "sessions_completed": self.sessions_completed,
            "unlocked_tiers": self.unlocked_tiers or ["Beginner"],
            "latest_grid_size": self.latest_grid_size,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "recent_sessions": self.recent_sessions or []
        }

class HighScore(db.Model):
    __tablename__ = "blockrush_high_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("blockrush_users.id"), nullable=True)
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
