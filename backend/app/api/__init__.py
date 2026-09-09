from app.api.auth import auth_bp
from app.api.game import game_bp
from app.api.leaderboard import leaderboard_bp
from app.api.support import support_bp

__all__ = ["auth_bp", "game_bp", "leaderboard_bp", "support_bp"]
