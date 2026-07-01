from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth_bp
from app.auth.forms import LoginForm, RegisterForm
from app.auth.utils import (
    authenticate_user,
    create_user,
    generate_verification_token,
    verify_email_token,
)
from app.models import User
from app.services.email_service import send_verification_email


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    login_form = LoginForm(prefix="login")
    register_form = RegisterForm(prefix="register")

    if login_form.validate_on_submit():
        user = authenticate_user(login_form.email.data, login_form.password.data)
        if user is None:
            flash("Incorrect email or password.", "danger")
        elif not user.email_verified:
            token = generate_verification_token(user)
            send_verification_email(user, token.token)
            flash("Please verify your email first. We have sent you a new verification email.", "warning")
        else:
            login_user(user)
            if user.is_admin():
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("main.dashboard"))

    return render_template(
        "login.html",
        login_form=login_form,
        register_form=register_form,
    )


@auth_bp.route("/register", methods=["POST"])
def register():
    form = RegisterForm(prefix="register")
    login_form = LoginForm(prefix="login")

    if not form.validate_on_submit():
        return render_template("login.html", login_form=login_form, register_form=form)

    existing = User.query.filter_by(email=form.email.data.lower()).first()
    if existing:
        flash("This email is already registered.", "danger")
        return redirect(url_for("auth.login"))

    user = create_user(form.full_name.data, form.email.data, form.password.data)
    token = generate_verification_token(user)
    sent = send_verification_email(user, token.token)

    if sent:
        flash("Your account has been created. Please verify your email.", "success")
    else:
        flash("Your account has been created. Email is not configured, so the verification link was printed in the terminal.", "warning")

    return redirect(url_for("auth.login"))


@auth_bp.route("/verify/<token>")
def verify_email(token):
    if verify_email_token(token):
        flash("Email verified successfully. You can now sign in.", "success")
    else:
        flash("Invalid or expired verification link.", "danger")
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
