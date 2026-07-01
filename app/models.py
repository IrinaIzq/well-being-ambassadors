from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    team = db.relationship("Team", back_populates="captain", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class VerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User")


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    departments = db.Column(db.String(255), nullable=False)
    captain_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    logo_url = db.Column(db.String(500))
    current_season = db.Column(db.String(20), nullable=False, default="fall")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    captain = db.relationship("User", back_populates="team")
    members = db.relationship(
        "TeamMember",
        back_populates="team",
        cascade="all, delete-orphan",
        order_by="TeamMember.id",
    )
    completions = db.relationship(
        "ChallengeCompletion",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    @property
    def member_count(self):
        return len(self.members)


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    team = db.relationship("Team", back_populates="members")


class ChallengeCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    season = db.Column(db.String(20), nullable=False)
    challenge_key = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    proof_sent = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    team = db.relationship("Team", back_populates="completions")

    __table_args__ = (
        db.UniqueConstraint("team_id", "season", "challenge_key", name="uq_team_season_challenge"),
    )
