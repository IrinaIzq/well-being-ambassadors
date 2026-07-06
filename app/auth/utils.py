from app.extensions import db
from app.models import User


def create_user(full_name, email, password):
    email = email.lower().strip()
    existing = User.query.filter_by(email=email).first()
    if existing:
        return None

    user = User(
        full_name=full_name.strip(),
        email=email,
        email_verified=True,
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