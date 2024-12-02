import enum
from app import db
class TeamStatus(enum.Enum):
    DONE = "done"
    ONGOING = "ongoing"
    UPCOMING = "upcoming"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)

class Team(db.Model):
    teamno = db.Column(db.Integer, primary_key=True) 
    team_name = db.Column(db.String(200), nullable=False)
    lab_assigned = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(TeamStatus), default=TeamStatus.UPCOMING, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=True)
    members = db.relationship('TeamMember', backref='team', lazy=True)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    team_id = db.Column(db.Integer, db.ForeignKey('team.teamno'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=True) 

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    domain = db.Column(db.String(200), nullable=True)
    teams = db.relationship('Team', backref='mentor', lazy=True)
