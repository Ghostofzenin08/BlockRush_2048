from flask import Blueprint, jsonify
from app.models.game_session import HighScore

leaderboard_bp = Blueprint("leaderboard", __name__)

@leaderboard_bp.route("/weekly", methods=["GET"])
def weekly_leaderboard():
    scores = HighScore.query.order_by(HighScore.score.desc()).limit(10).all()
    return jsonify({
        "success": True,
        "mode": "weekly",
        "rankings": [s.to_dict() for s in scores]
    }), 200

@leaderboard_bp.route("/all-time", methods=["GET"])
def all_time_leaderboard():
    scores = HighScore.query.order_by(HighScore.score.desc()).limit(50).all()
    return jsonify({
        "success": True,
        "mode": "all-time",
        "rankings": [s.to_dict() for s in scores]
    }), 200
