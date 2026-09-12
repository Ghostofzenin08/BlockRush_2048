import json
import os
from datetime import datetime, timezone

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")

os.makedirs(SESSIONS_DIR, exist_ok=True)


class JSONStorageService:
    @staticmethod
    def get_session_file_path(user_id, session_id):
        clean_user = str(user_id).replace("/", "_").replace("\\", "_")
        clean_sess = str(session_id).replace("/", "_").replace("\\", "_")
        return os.path.join(SESSIONS_DIR, f"session_{clean_user}_{clean_sess}.json")

    @staticmethod
    def get_player_history_file(user_id):
        clean_user = str(user_id).replace("/", "_").replace("\\", "_")
        return os.path.join(SESSIONS_DIR, f"player_history_{clean_user}.json")

    @classmethod
    def save_session(cls, session_data):
        """Save an individual session object to its own JSON file and update player history ledger."""
        user_id = session_data.get("user_id", "anonymous")
        session_id = session_data.get("session_id", f"sess_{int(datetime.now(timezone.utc).timestamp())}")

        session_data["user_id"] = user_id
        session_data["session_id"] = session_id
        session_data["updated_at"] = datetime.now(timezone.utc).isoformat()

        session_path = cls.get_session_file_path(user_id, session_id)
        try:
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2)
        except OSError as e:
            print(f"Error saving session JSON: {e}")

        # Update player summary ledger
        cls.update_player_history(user_id, session_data)
        return session_data

    @classmethod
    def update_player_history(cls, user_id, latest_session):
        history_path = cls.get_player_history_file(user_id)
        history = {
            "user_id": user_id,
            "current_level": 1,
            "level_tier": "Beginner",
            "current_score": 0,
            "high_score": 0,
            "best_score": 0,
            "highest_tile": 2,
            "total_moves": 0,
            "total_playtime_seconds": 0,
            "sessions_completed": 0,
            "unlocked_tiers": ["Beginner"],
            "latest_grid_size": "4x4",
            "last_active": datetime.now(timezone.utc).isoformat(),
            "recent_sessions": []
        }

        if os.path.isfile(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        history.update(loaded)
            except (json.JSONDecodeError, OSError):
                pass

        score = latest_session.get("score", 0)
        max_tile = latest_session.get("highest_tile", latest_session.get("max_tile", 2))
        moves = latest_session.get("number_of_moves", 0)
        duration = latest_session.get("duration_seconds", 0)
        tier = latest_session.get("level_tier", "Beginner")
        level = latest_session.get("current_level", 1)

        history["current_score"] = score
        if score > history.get("best_score", 0):
            history["best_score"] = score
            history["high_score"] = score

        if max_tile > history.get("highest_tile", 2):
            history["highest_tile"] = max_tile

        history["total_moves"] = history.get("total_moves", 0) + moves
        history["total_playtime_seconds"] = history.get("total_playtime_seconds", 0) + duration
        history["sessions_completed"] = history.get("sessions_completed", 0) + 1
        history["current_level"] = max(history.get("current_level", 1), level)
        history["level_tier"] = tier
        history["last_active"] = datetime.now(timezone.utc).isoformat()

        # Update unlocked tiers ladder
        unlocked = set(history.get("unlocked_tiers", ["Beginner"]))
        unlocked.add("Beginner")
        if history["highest_tile"] >= 64 or history["current_score"] >= 500:
            unlocked.add("Advanced")
        if history["highest_tile"] >= 128 or history["current_score"] >= 1500:
            unlocked.add("Pro")
        if history["highest_tile"] >= 256 or history["current_score"] >= 3000:
            unlocked.add("Master")
        history["unlocked_tiers"] = list(unlocked)

        # Retain last 10 session IDs
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
            "user_id": user_id,
            "current_level": 1,
            "level_tier": "Beginner",
            "current_score": 0,
            "high_score": 0,
            "best_score": 0,
            "highest_tile": 2,
            "total_moves": 0,
            "total_playtime_seconds": 0,
            "sessions_completed": 0,
            "unlocked_tiers": ["Beginner"],
            "latest_grid_size": "4x4",
            "recent_sessions": []
        }
