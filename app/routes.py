import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
)
from auth_middleware import token_required

from app.config import Config
from app.models import db, User, Feedback
api_bp = Blueprint("api", __name__)

@api_bp.route("/signup", methods=["POST"])
def register():
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    role = data.get("role", "Volunteer").capitalize()
    # print(role)
    # if role not in ["Volunteer", "Admin"]:
    #     return jsonify({"message": "Invalid role"}), 400

    user = User(email=data["email"], password=hashed_password, role=role, first_name=data["first_name"], last_name=data["last_name"])
    # print(user)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "User registered successfully",
                    "access_token": access_token}), 201

@api_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }), 400

        user = User.query.filter_by(email=data.get("email")).first()

        if not user or not check_password_hash(user.password, data.get("password")):
            return jsonify({
                "message": "Invalid credentials",
                "data": None,
                "error": "Unauthorized"
            }), 401

        try:
            token = jwt.encode(
                {"id": user.id},
                Config.SECRET_KEY,
                algorithm="HS256"
            )
            return jsonify({
                "message": "Successfully fetched auth token",
                "access_token": token
            })

        except Exception as e:
            return jsonify({
                "error": "Something went wrong",
                "message": str(e)
            }), 500

    except Exception as e:
        return jsonify({
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }), 500

@api_bp.route("/admin", methods=["GET"])
@token_required
def manage_team(current_user):
    # print(current_user.role)
    if current_user.role != "Admin":
        return jsonify({"message": "Access denied"}), 403

    output = []
    users = User.query.all() 
    for t in users:
        output.append({"id": t.id, "email": t.email, "role": t.role})

    return jsonify({'users': output})

@api_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if request.method == 'POST':
        feedback = Feedback(email=data['email'], feedback=data['feedback'], rating=data['rating'])
        db.session.add(feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    
@api_bp.route('/get_feedback', methods=['GET'])
def get_feedbacks():
    if request.method == 'GET':
        feedbacks = Feedback.query.all()
        feedback_list = [{'id': f.id, 'email': f.email,'feedback': f.feedback, 'rating': f.rating} for f in feedbacks]
        return jsonify(feedback_list), 200


@api_bp.route('/get_feedback/<int:id>', methods=['GET'])
def get_feedback(id):
    try:
        f = Feedback.query.get(id)
        return jsonify({'id': f.id, 'feedback_text': f.feedback, 'rating': f.rating}), 200
    except Exception as e:
            return jsonify({
                "error": "Error Getting Feedback ",
                "message": str(e)
            }), 500

