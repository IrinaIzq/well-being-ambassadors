from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, mail, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app import models
    from app.admin.routes import admin_bp
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.seasons.routes import seasons_bp
    from app.teams.routes import teams_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(seasons_bp, url_prefix="/seasons")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
        ensure_admin_user(app)

    return app


def ensure_admin_user(app):
    from app.models import User

    admin = User.query.filter_by(email=app.config["ADMIN_EMAIL"].lower()).first()
    if admin:
        return

    admin = User(
        full_name="Wellbeing Quest Admin",
        email=app.config["ADMIN_EMAIL"].lower(),
        role="admin",
        email_verified=True,
    )
    admin.set_password(app.config["ADMIN_PASSWORD"])
    db.session.add(admin)
    db.session.commit()
