import os
import sys
import glob
import json
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app
from app.extensions import db
from app.models.game_session import GameSession, PlayerHistory
from app.models.user import User

def parse_iso(val):
    if not val:
        return None
    try:
        if isinstance(val, str):
            return datetime.fromisoformat(val.replace("Z", "+00:00"))
    except Exception:
        pass
    return None

def migrate():
    app = create_app()
    with app.app_context():
        # Locate sessions directory
        base_dirs = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sessions")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend", "data", "sessions"))
        ]
        
        sessions_dir = None
        for bd in base_dirs:
            if os.path.exists(bd):
                sessions_dir = bd
                break
                
        if not sessions_dir:
            print("No sessions directory found.")
            return

        print(f"Reading JSON files from: {sessions_dir}")

        # 1. Migrate Player History files
        history_files = glob.glob(os.path.join(sessions_dir, "player_history_*.json"))
        histories_migrated = 0
        for hf in history_files:
            try:
                with open(hf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                user_id = data.get("user_id", "player0123")
                
                # Check or create User
                u = User.query.filter_by(username=user_id).first()
                if not u:
                    u = User(
                        username=user_id,
                        email=f"{user_id}@blockrush.local",
                        level=data.get("current_level", 1),
                        high_score=data.get("high_score", 0)
                    )
                    db.session.add(u)
                    db.session.flush()

                # Check or update PlayerHistory
                ph = PlayerHistory.query.filter_by(user_identifier=user_id).first()
                if not ph:
                    ph = PlayerHistory(user_identifier=user_id)
                    db.session.add(ph)

                ph.current_level = data.get("current_level", 1)
                ph.level_tier = data.get("level_tier", "Beginner")
                ph.current_score = data.get("current_score", 0)
                ph.high_score = data.get("high_score", data.get("best_score", 0))
                ph.best_score = data.get("best_score", data.get("high_score", 0))
                ph.highest_tile = data.get("highest_tile", 2)
                ph.total_moves = data.get("total_moves", 0)
                ph.total_playtime_seconds = data.get("total_playtime_seconds", 0)
                ph.sessions_completed = data.get("sessions_completed", 0)
                ph.unlocked_tiers = data.get("unlocked_tiers", ["Beginner"])
                ph.latest_grid_size = data.get("latest_grid_size", "4x4")
                ph.last_active = parse_iso(data.get("last_active")) or datetime.now(timezone.utc)
                ph.recent_sessions = data.get("recent_sessions", [])

                histories_migrated += 1
            except Exception as e:
                print(f"Error processing {hf}: {e}")

        db.session.commit()
        print(f"Successfully migrated {histories_migrated} player history records.")

        # 2. Migrate Session files
        session_files = glob.glob(os.path.join(sessions_dir, "session_*.json"))
        sessions_migrated = 0
        
        for sf in session_files:
            try:
                with open(sf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                sess_uid = data.get("session_id")
                if not sess_uid:
                    continue

                user_id_str = data.get("user_id", "player0123")
                existing = GameSession.query.filter_by(session_uid=sess_uid).first()
                if existing:
                    continue

                u = User.query.filter_by(username=user_id_str).first()
                u_id = u.id if u else None

                gs = GameSession(
                    session_uid=sess_uid,
                    user_id=u_id,
                    user_identifier=user_id_str,
                    mode=data.get("mode", "classic"),
                    tier=data.get("level_tier", data.get("tier", "Beginner")),
                    level=data.get("current_level", data.get("level", 1)),
                    grid_size=data.get("grid_size", "4x4"),
                    target_tile=data.get("target_tile", 2048),
                    score=data.get("score", data.get("current_score", 0)),
                    max_tile=data.get("highest_tile", data.get("max_tile", 2)),
                    number_of_moves=data.get("number_of_moves", 0),
                    duration_seconds=data.get("duration_seconds", 0),
                    game_status=data.get("game_status", "playing"),
                    completed=(data.get("game_status") == "won" or data.get("completed", False)),
                    session_start_time=parse_iso(data.get("session_start_time")),
                    created_at=parse_iso(data.get("session_start_time")) or datetime.now(timezone.utc),
                    updated_at=parse_iso(data.get("updated_at")) or datetime.now(timezone.utc)
                )
                db.session.add(gs)
                sessions_migrated += 1
            except Exception as e:
                print(f"Error processing {sf}: {e}")

        db.session.commit()
        print(f"Successfully migrated {sessions_migrated} game session records into Neon DB!")

        # Verify counts in Neon DB
        total_sessions = GameSession.query.count()
        total_histories = PlayerHistory.query.count()
        total_users = User.query.count()
        print(f"\n--- Neon DB Row Counts ---")
        print(f"blockrush_users: {total_users}")
        print(f"blockrush_game_sessions: {total_sessions}")
        print(f"blockrush_player_histories: {total_histories}")

if __name__ == "__main__":
    migrate()
