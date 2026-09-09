from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.game_session import GameSession, HighScore
from app.models.user import User

game_bp = Blueprint("game", __name__)

@game_bp.route("/session/start", methods=["POST"])
@jwt_required(optional=True)
def start_session():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    mode = data.get("mode", "classic")
    tier = data.get("tier", "Beginner")
    level = data.get("level", 1)

    session = GameSession(
        user_id=int(current_user_id) if current_user_id else None,
        mode=mode,
        tier=tier,
        level=level
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Game session initialized.",
        "session": session.to_dict(),
        "placeholder_note": "Awaiting game logic engine integration from colleague."
    }), 201

@game_bp.route("/session/submit", methods=["POST"])
@jwt_required(optional=True)
def submit_session():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    session_id = data.get("session_id")
    score = data.get("score", 0)
    max_tile = data.get("max_tile", 2)
    duration = data.get("duration_seconds", 0)
    completed = data.get("completed", False)

    session = GameSession.query.get(session_id) if session_id else None
    if session:
        session.score = score
        session.max_tile = max_tile
        session.duration_seconds = duration
        session.completed = completed
        db.session.commit()

    # Update user high score if authenticated
    new_high_score = False
    if current_user_id:
        user = User.query.get(int(current_user_id))
        if user and score > user.high_score:
            user.high_score = score
            new_high_score = True
            db.session.commit()

            # Record or update high score ranking
            hs = HighScore.query.filter_by(user_id=user.id, mode=session.mode if session else "classic").first()
            if not hs:
                hs = HighScore(user_id=user.id, player_name=user.username, score=score, max_tile=max_tile, mode=session.mode if session else "classic")
                db.session.add(hs)
            else:
                hs.score = score
                hs.max_tile = max_tile
            db.session.commit()

    return jsonify({
        "success": True,
        "new_high_score": new_high_score,
        "session": session.to_dict() if session else None,
        "score_recorded": score
    }), 200

@game_bp.route("/session/state", methods=["GET"])
def game_state_hook():
    """Placeholder state hook for colleague's custom game logic engine."""
    return jsonify({
        "success": True,
        "status": "ready",
        "supported_modes": ["classic", "challenge", "playground"],
        "placeholder_engine": "Colleague game logic pending integration."
    }), 200
