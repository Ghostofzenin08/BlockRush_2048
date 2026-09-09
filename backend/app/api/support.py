from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.support_query import SupportQuery

support_bp = Blueprint("support", __name__)

@support_bp.route("/submit-query", methods=["POST"])
@jwt_required(optional=True)
def submit_query():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    query_text = data.get("query_text") or data.get("query")
    email = data.get("email")

    if not query_text or len(query_text.strip()) < 5:
        return jsonify({"success": False, "error": "Query text must be at least 5 characters long."}), 400

    query_obj = SupportQuery(
        user_id=int(current_user_id) if current_user_id else None,
        email=email,
        query_text=query_text.strip()
    )
    db.session.add(query_obj)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Support query submitted successfully.",
        "query": query_obj.to_dict()
    }), 201

@support_bp.route("/faqs", methods=["GET"])
def get_faqs():
    faqs = [
        {
            "category": "How to Play",
            "question": "How do I slide and merge number blocks?",
            "answer": "Swipe on touch devices or use WASD / Arrow Keys on desktop. Same numbers merge together."
        },
        {
            "category": "Game Progress",
            "question": "How is score calculated?",
            "answer": "Every merge adds double the block value directly to your score."
        },
        {
            "category": "Contact Support",
            "question": "Where can I contact technical support?",
            "answer": "Email support@blockrush.game or use the BlockDocs Support form."
        }
    ]
    return jsonify({"success": True, "faqs": faqs}), 200
