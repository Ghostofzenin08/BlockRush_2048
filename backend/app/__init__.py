from flask import Flask, jsonify
from app.config import get_config
from app.extensions import db, jwt, cors, migrate

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    migrate.init_app(app, db)

    # Register API Blueprints under /api/v1/
    from app.api.auth import auth_bp
    from app.api.game import game_bp
    from app.api.leaderboard import leaderboard_bp
    from app.api.support import support_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(game_bp, url_prefix="/api/v1/game")
    app.register_blueprint(leaderboard_bp, url_prefix="/api/v1/leaderboard")
    app.register_blueprint(support_bp, url_prefix="/api/v1/support")

    # Global Health Check & Standard Error Handlers
    @app.route("/health", methods=["GET"])
    @app.route("/api/v1/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "service": "BlockRush Flask API Backend",
            "game_logic_engine": "ready_for_colleague_integration"
        }), 200

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"success": False, "error": {"code": "BAD_REQUEST", "message": str(e)}}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": {"code": "NOT_FOUND", "message": "Resource not found."}}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "error": {"code": "INTERNAL_SERVER_ERROR", "message": "An internal error occurred."}}), 500

    return app
