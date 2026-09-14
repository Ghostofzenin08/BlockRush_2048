import json
import os
from datetime import datetime, timezone
from app.extensions import db
from app.models.game_session import GameSession, PlayerHistory
from app.models.user import User

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")

os.makedirs(SESSIONS_DIR, exist_ok=True)


class JSONStorageService:
    @staticmethod
    def _path(name):
        return os.path.join(SESSIONS_DIR, os.path.basename(str(name)))

    @staticmethod
    def _calculate_unlocked_tiers(existing_unlocked, highest_tile, score):
        unlocked = set(existing_unlocked or ["Beginner"])
        unlocked.add("Beginner")
        if (highest_tile or 2) >= 64 or (score or 0) >= 500: unlocked.add("Advanced")
        if (highest_tile or 2) >= 128 or (score or 0) >= 1500: unlocked.add("Pro")
        if (highest_tile or 2) >= 256 or (score or 0) >= 3000: unlocked.add("Master")
        return list(unlocked)

    @classmethod
    def get_session_file_path(cls, user_id, session_id):
        return cls._path(f"session_{user_id}_{session_id}.json")

    @classmethod
    def get_player_history_file(cls, user_id):
        return cls._path(f"player_history_{user_id}.json")

    @classmethod
    def save_session(cls, session_data):
        user_id = session_data.setdefault("user_id", "anonymous")
        session_id = session_data.setdefault("session_id", f"sess_{int(datetime.now(timezone.utc).timestamp())}")
        session_data["updated_at"] = datetime.now(timezone.utc).isoformat()

        # 1. Persist to local JSON file
        try:
            with open(cls.get_session_file_path(user_id, session_id), "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2)
        except OSError as e:
            print(f"Notice: local JSON save skipped: {e}")

        # 2. Persist to Neon PostgreSQL Database
        try:
            score = session_data.get("score", session_data.get("current_score", 0))
            max_tile = session_data.get("highest_tile", session_data.get("max_tile", 2))
            moves = session_data.get("number_of_moves", 0)
            duration = session_data.get("duration_seconds", 0)
            status = session_data.get("game_status", "playing")
            completed = session_data.get("completed", status == "won")

            # Check or create user in Neon DB
            u = User.query.filter((User.username == user_id) | (User.firebase_uid == user_id)).first()
            if not u and user_id != "anonymous":
                u = User(username=user_id, email=f"{user_id}@blockrush.local")
                db.session.add(u)
                db.session.flush()

            # Find or create GameSession row in Neon DB
            gs = GameSession.query.filter_by(session_uid=session_id).first()
            if not gs:
                gs = GameSession(
                    session_uid=session_id,
                    user_id=u.id if u else None,
                    user_identifier=user_id,
                    mode=session_data.get("mode", "classic"),
                    tier=session_data.get("level_tier", "Beginner"),
                    level=session_data.get("current_level", 1),
                    grid_size=session_data.get("grid_size", "4x4"),
                    target_tile=session_data.get("target_tile", 2048),
                    score=score,
                    max_tile=max_tile,
                    number_of_moves=moves,
                    duration_seconds=duration,
                    game_status=status,
                    completed=completed
                )
                db.session.add(gs)
            else:
                gs.score = max(gs.score or 0, score or 0)
                gs.max_tile = max(gs.max_tile or 2, max_tile or 2)
                gs.number_of_moves = moves or 0
                gs.duration_seconds = duration or 0
                gs.game_status = status
                gs.completed = completed

            # Update PlayerHistory row in Neon DB
            ph = PlayerHistory.query.filter_by(user_identifier=user_id).first()
            if not ph:
                ph = PlayerHistory(user_identifier=user_id)
                db.session.add(ph)

            ph.current_score = score or 0
            ph.best_score = max(ph.best_score or 0, score or 0)
            ph.high_score = ph.best_score
            ph.highest_tile = max(ph.highest_tile or 2, max_tile or 2)
            ph.total_moves = (ph.total_moves or 0) + (moves or 0)
            ph.total_playtime_seconds = (ph.total_playtime_seconds or 0) + (duration or 0)
            ph.sessions_completed = (ph.sessions_completed or 0) + 1
            ph.current_level = max(ph.current_level or 1, session_data.get("current_level", 1) or 1)
            ph.level_tier = session_data.get("level_tier", "Beginner")
            ph.last_active = datetime.now(timezone.utc)
            ph.unlocked_tiers = cls._calculate_unlocked_tiers(ph.unlocked_tiers, ph.highest_tile, score)

            recent = list(ph.recent_sessions or [])
            recent.insert(0, {
                "session_id": session_id,
                "mode": session_data.get("mode"),
                "score": score,
                "highest_tile": max_tile,
                "status": status,
                "date": datetime.now(timezone.utc).isoformat()
            })
            ph.recent_sessions = recent[:10]

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Notice: Neon DB sync error: {e}")

        cls.update_player_history(user_id, session_data)
        return cls.get_player_summary(user_id)

    @classmethod
    def update_player_history(cls, user_id, latest_session):
        history_path = cls.get_player_history_file(user_id)
        history = {
            "user_id": user_id, "current_level": 1, "level_tier": "Beginner",
            "current_score": 0, "high_score": 0, "best_score": 0, "highest_tile": 2,
            "total_moves": 0, "total_playtime_seconds": 0, "sessions_completed": 0,
            "unlocked_tiers": ["Beginner"], "latest_grid_size": "4x4",
            "last_active": datetime.now(timezone.utc).isoformat(), "recent_sessions": []
        }

        if os.path.isfile(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history.update(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass

        score = latest_session.get("score", 0)
        max_tile = latest_session.get("highest_tile", latest_session.get("max_tile", 2))

        history["current_score"] = score
        history["best_score"] = max(history["best_score"], score)
        history["high_score"] = history["best_score"]
        history["highest_tile"] = max(history["highest_tile"], max_tile)
        history["total_moves"] += latest_session.get("number_of_moves", 0)
        history["total_playtime_seconds"] += latest_session.get("duration_seconds", 0)
        history["sessions_completed"] += 1
        history["current_level"] = max(history["current_level"], latest_session.get("current_level", 1))
        history["level_tier"] = latest_session.get("level_tier", "Beginner")
        history["last_active"] = datetime.now(timezone.utc).isoformat()
        history["unlocked_tiers"] = cls._calculate_unlocked_tiers(history.get("unlocked_tiers"), history["highest_tile"], score)

        recent = history.get("recent_sessions", [])
        recent.insert(0, {
            "session_id": latest_session.get("session_id"),
            "mode": latest_session.get("mode"),
            "score": score,
            "highest_tile": max_tile,
            "status": latest_session.get("game_status", "completed"),
            "date": datetime.now(timezone.utc).isoformat()
        })
        history["recent_sessions"] = recent[:10]

        try:
            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except OSError:
            pass

    @classmethod
    def get_player_summary(cls, user_id):
        # 1. Try Neon DB first
        try:
            ph = PlayerHistory.query.filter_by(user_identifier=user_id).first()
            if ph:
                return ph.to_dict()
        except Exception as e:
            print(f"Notice: Neon DB read error: {e}")

        # 2. Fallback to local JSON file
        history_path = cls.get_player_history_file(user_id)
        if os.path.isfile(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        return {
            "user_id": user_id, "current_level": 1, "level_tier": "Beginner",
            "current_score": 0, "high_score": 0, "best_score": 0, "highest_tile": 2,
            "total_moves": 0, "total_playtime_seconds": 0, "sessions_completed": 0,
            "unlocked_tiers": ["Beginner"], "latest_grid_size": "4x4", "recent_sessions": []
        }
