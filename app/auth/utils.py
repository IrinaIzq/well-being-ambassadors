import secrets
from datetime import datetime, timedelta

from app.extensions import db
from app.models import User, VerificationToken


def create_user(full_name, email, password):
    email = email.lower().strip()
    existing = User.query.filter_by(email=email).first()
    if existing:
        return None

    user = User(
        full_name=full_name.strip(),
        email=email,
        email_verified=False,
        role="user",
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(email, password):
    user = User.query.filter_by(email=email.lower().strip()).first()
    if not user or not user.check_password(password):
        return None
    return user


def generate_verification_token(user):
    token = VerificationToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(hours=48),
    )
    db.session.add(token)
    db.session.commit()
    return token


def verify_email_token(token_value):
    token = VerificationToken.query.filter_by(token=token_value).first()
    if not token or token.used_at is not None or token.expires_at < datetime.utcnow():
        return False

    token.user.email_verified = True
    token.used_at = datetime.utcnow()
    db.session.commit()
    return True
