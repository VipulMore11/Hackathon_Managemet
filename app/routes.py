import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
)
from auth_middleware import token_required

from app.config import Config
from app.models import db, User, Feedback, Team, TeamStatus, Mentor, TeamMember

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

@api_bp.route('/update_team_status/<int:teamno>', methods=['PUT'])
def update_team_status(teamno):
    data = request.json
    team = Team.query.get_or_404(teamno)
    try:
        team.status = TeamStatus(data['status'])
        db.session.commit()
        return jsonify({"message": "Status updated successfully!"})
    except ValueError:
        return jsonify({"error": "Invalid status value"}), 400

@api_bp.route('/get_team/', defaults={'teamno': None}, methods=['GET'])
@api_bp.route('/get_team/<int:teamno>', methods=['GET'])
def get_team(teamno):
    if teamno:
        team = Team.query.get_or_404(teamno)
        result = {
            "teamno": team.teamno,
            "team_name": team.team_name,
            "lab_assigned": team.lab_assigned,
            "status": team.status.value,
            "members": [
                {
                    "name": member.name,
                    "role": member.role,
                    "email": member.email
                }
                for member in team.members
            ]
        }
    else:
        teams = Team.query.all()
        result = [
            {
                "teamno": team.teamno,
                "team_name": team.team_name,
                "lab_assigned": team.lab_assigned,
                "status": team.status.value,
                "members": [
                    {
                        "name": member.name,
                        "role": member.role,
                        "email": member.email
                    }
                    for member in team.members
                ]
            }
            for team in teams
        ]
    return jsonify(result)

@api_bp.route('/get_mentor/', defaults={'mentorid': None}, methods=['GET'])
@api_bp.route('/get_mentor/<int:mentorid>', methods=['GET'])
def get_mentors(mentorid):
    if mentorid:
        mentors = Mentor.query.get_or_404(mentorid)
        mentor_list = [
            {
                'id': mentors.id,
                'name': mentors.name,
                'email': mentors.email,
                'expertise': mentors.domain,
                'teams': [
                    {
                        'teamno': team.teamno,
                        'team_name': team.team_name,
                        'lab_assigned': team.lab_assigned,
                        'status': team.status.value,
                        'members': [
                                    {
                                        "name": member.name,
                                        "role": member.role,
                                        "email": member.email
                                    }
                                    for member in team.members
                        ]
                    }
                    for team in mentors.teams
                ]
            }
        ]
    else:
        mentors = Mentor.query.all()
        mentor_list = [
            {
                'id': mentor.id,
                'name': mentor.name,
                'email': mentor.email,
                'expertise': mentor.domain,
                'teams': [
                    {
                        'teamno': team.teamno,
                        'team_name': team.team_name,
                        'lab_assigned': team.lab_assigned,
                        'status': team.status.value,
                        'members': [
                                    {
                                        "name": member.name,
                                        "role": member.role,
                                        "email": member.email
                                    }
                                    for member in team.members
                        ]
                    }
                    for team in mentor.teams
                ]
            }
            for mentor in mentors
        ]
    return jsonify(mentor_list), 200

@api_bp.route('/mentors', methods=['POST'])
def create_mentor():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and Email are required fields'}), 400

    existing_mentor = Mentor.query.filter_by(email=data['email']).first()
    if existing_mentor:
        return jsonify({'error': 'Mentor with this email already exists'}), 400

    mentor = Mentor(name=data['name'], email=data['email'], domain=data.get('domain', ''))
    db.session.add(mentor)
    db.session.commit()

    return jsonify({'message': 'Mentor created successfully', 'mentor_id': mentor.id}), 201

@api_bp.route('/update_mentors/<int:mentor_id>', methods=['PUT'])
def assignee_mentors(mentor_id):
    data = request.get_json()
    if not data.get("team_id"):
        return jsonify({'error': 'team_id is required'}), 400
    mentor = Mentor.query.get(mentor_id)
    if not mentor:
        return jsonify({'error': 'Mentor not found'}), 404
    team_ids = []
    team_id = data.get("team_id")
    for ids in team_id:
        team = Team.query.get(ids)
        team_ids.append(team)
    mentor.teams = team_ids
    db.session.add(mentor)
    db.session.commit()

    return jsonify({'success': f'Team assigneed to mentor {mentor.name}'}), 200

@api_bp.route('/create_team', methods=['POST'])
def create_team():
    data = request.get_json()

    if not data.get("team_name") or not data.get("lab_assigned"):
        return jsonify({'error': 'team_name and lab_assigned are required'}), 400

    members = data.get("members", [])
    if not isinstance(members, list) or not members:
        return jsonify({'error': 'At least one member must be provided'}), 400

    new_team = Team(
        team_name=data["team_name"],
        lab_assigned=data["lab_assigned"],
        status=data.get("status", TeamStatus.UPCOMING)
    )
    db.session.add(new_team)
    db.session.commit()

    for member in members:
        if not member.get("name") or not member.get("role"):
            return jsonify({'error': 'Each member must have a name and role'}), 400

        new_member = TeamMember(
            team_id=new_team.teamno,
            name=member["name"],
            role=member["role"],
            email=member.get("email")
        )
        db.session.add(new_member)

    db.session.commit()

    return jsonify({'success': 'Team and members created successfully', 'team_id': new_team.teamno}), 201