import json
import os
from datetime import datetime, timezone

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")

os.makedirs(SESSIONS_DIR, exist_ok=True)


class JSONStorageService:
    @staticmethod
    def _path(name):
        clean = str(name).replace("/", "_").replace("\\", "_")
        return os.path.join(SESSIONS_DIR, clean)

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

        try:
            with open(cls.get_session_file_path(user_id, session_id), "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2)
        except OSError as e:
            print(f"Error saving session JSON: {e}")

        cls.update_player_history(user_id, session_data)
        return session_data

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

        unlocked = set(history.get("unlocked_tiers", ["Beginner"]))
        unlocked.add("Beginner")
        if history["highest_tile"] >= 64 or score >= 500: unlocked.add("Advanced")
        if history["highest_tile"] >= 128 or score >= 1500: unlocked.add("Pro")
        if history["highest_tile"] >= 256 or score >= 3000: unlocked.add("Master")
        history["unlocked_tiers"] = list(unlocked)

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
