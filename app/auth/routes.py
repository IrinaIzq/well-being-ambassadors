from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth_bp
from app.auth.forms import LoginForm, RegisterForm
from app.auth.utils import authenticate_user, create_user
from app.models import User


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
        else:
            login_user(user)
            if user.is_admin():
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("main.dashboard"))

    return render_template("login.html", login_form=login_form, register_form=register_form)


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

    create_user(form.full_name.data, form.email.data, form.password.data)
    flash("Your account has been created. You can now sign in.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))