from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.game_session import GameSession, HighScore
from app.models.user import User
from app.services.json_storage import JSONStorageService

game_bp = Blueprint("game", __name__)

GRID_PROGRESSION = [
    {"level": 1, "size": "2x2", "rows": 2, "cols": 2, "target": 16, "time_limit": 15},
    {"level": 2, "size": "4x4", "rows": 4, "cols": 4, "target": 64, "time_limit": 30},
    {"level": 3, "size": "6x6", "rows": 6, "cols": 6, "target": 128, "time_limit": 45},
    {"level": 4, "size": "8x8", "rows": 8, "cols": 8, "target": 256, "time_limit": 60},
    {"level": 5, "size": "10x10", "rows": 10, "cols": 10, "target": 512, "time_limit": 90},
    {"level": 6, "size": "12x12", "rows": 12, "cols": 12, "target": 1024, "time_limit": 120},
]


@game_bp.route("/session/start", methods=["POST"])
@jwt_required(optional=True)
def start_session():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    user_id = data.get("user_id") or (str(current_user_id) if current_user_id else "player0123")
    mode = data.get("mode", "classic")
    tier = data.get("tier", "Beginner")
    level = data.get("level", 1)
    grid_size = data.get("grid_size", "4x4")
    target_tile = data.get("target_tile", 2048)

    session = GameSession(
        user_id=int(current_user_id) if current_user_id and str(current_user_id).isdigit() else None,
        mode=mode,
        tier=tier,
        level=level
    )
    db.session.add(session)
    db.session.commit()

    sess_id = f"sess_{session.id}"
    json_record = {
        "user_id": user_id,
        "session_id": sess_id,
        "mode": mode,
        "current_level": level,
        "level_tier": tier,
        "grid_size": grid_size,
        "target_tile": target_tile,
        "current_score": 0,
        "score": 0,
        "highest_tile": 2,
        "number_of_moves": 0,
        "session_start_time": datetime.now(timezone.utc).isoformat(),
        "game_status": "playing"
    }

    JSONStorageService.save_session(json_record)

    return jsonify({
        "success": True,
        "message": "Game session initialized and logged to JSON storage.",
        "session_id": sess_id,
        "session": session.to_dict(),
        "json_record": json_record
    }), 201


@game_bp.route("/session/submit", methods=["POST"])
@jwt_required(optional=True)
def submit_session():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    user_id = data.get("user_id") or (str(current_user_id) if current_user_id else "player0123")
    raw_session_id = data.get("session_id", "sess_0")
    db_id = int(str(raw_session_id).replace("sess_", "")) if str(raw_session_id).replace("sess_", "").isdigit() else None

    score = data.get("score", 0)
    max_tile = data.get("highest_tile", data.get("max_tile", 2))
    duration = data.get("duration_seconds", 0)
    completed = data.get("completed", False)
    moves = data.get("number_of_moves", 0)
    game_status = data.get("game_status", "won" if completed else "lost")
    tier = data.get("level_tier", "Beginner")
    level = data.get("current_level", 1)

    if db_id:
        session = GameSession.query.get(db_id)
        if session:
            session.score = score
            session.max_tile = max_tile
            session.duration_seconds = duration
            session.completed = completed
            db.session.commit()

    # Save complete JSON session record
    json_record = {
        "user_id": user_id,
        "session_id": raw_session_id,
        "mode": data.get("mode", "classic"),
        "current_level": level,
        "level_tier": tier,
        "grid_size": data.get("grid_size", "4x4"),
        "target_tile": data.get("target_tile", 2048),
        "score": score,
        "current_score": score,
        "highest_tile": max_tile,
        "number_of_moves": moves,
        "duration_seconds": duration,
        "time_limit_seconds": data.get("time_limit_seconds", 0),
        "actual_completion_time_seconds": duration,
        "session_start_time": data.get("session_start_time", datetime.now(timezone.utc).isoformat()),
        "session_end_time": datetime.now(timezone.utc).isoformat(),
        "game_status": game_status
    }

    updated_summary = JSONStorageService.save_session(json_record)

    return jsonify({
        "success": True,
        "score_recorded": score,
        "summary": updated_summary,
        "json_record": json_record
    }), 200


@game_bp.route("/player/summary/<user_id>", methods=["GET"])
def get_player_summary(user_id):
    """Fetch complete player summary for Playground UI rendering."""
    summary = JSONStorageService.get_player_summary(user_id)
    return jsonify({
        "success": True,
        "player_data": summary
    }), 200


@game_bp.route("/challenge/next-level", methods=["GET"])
def get_challenge_level():
    """Get progressive grid ladder spec (2x2 up to 12x12)."""
    level_num = int(request.args.get("level", 1))
    index = min(max(0, level_num - 1), len(GRID_PROGRESSION) - 1)
    spec = GRID_PROGRESSION[index].copy()

    # Beyond 12x12 (level > 6), keep grid at 12x12 and scale difficulty
    if level_num > len(GRID_PROGRESSION):
        extra = level_num - len(GRID_PROGRESSION)
        spec["target"] = 1024 * (2 ** extra)
        spec["time_limit"] = max(30, 120 - extra * 10)
        spec["max_grid_reached"] = True
        spec["randomization_level"] = "high"

    return jsonify({
        "success": True,
        "challenge_spec": spec
    }), 200
