from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import bcrypt
from app.extensions import db
from app.models.user import User
from app.schemas.auth_schema import AuthValidation

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    errors = AuthValidation.validate_register(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    username = data.get("username").strip()
    email = data.get("email").strip().lower()
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "error": "Email is already registered."}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "error": "Username is already taken."}), 409

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "message": "User registered successfully.",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    errors = AuthValidation.validate_login(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    email = data.get("email").strip().lower()
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"success": False, "error": "Invalid email or password."}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"success": True, "access_token": new_access_token}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({"success": False, "error": "User not found."}), 404
    return jsonify({"success": True, "user": user.to_dict()}), 200
