from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Team, TeamMember
from app.seasons.data import SEASONS
from app.teams import teams_bp

import os
from uuid import uuid4

from werkzeug.utils import secure_filename
from flask import current_app


def member_rows_from_request():
    rows = []
    for name, email in zip(request.form.getlist("member_name"), request.form.getlist("member_email")):
        name = name.strip()
        email = email.strip().lower()
        if name and email:
            rows.append((name, email))
    return rows


@teams_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_team():
    if current_user.is_admin():
        return redirect(url_for("admin.admin_dashboard"))
    if current_user.team is not None:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        members = member_rows_from_request()
        if not members:
            flash("Add at least one team member with name and email.", "danger")
            return redirect(url_for("teams.create_team"))

        logo_url = None

        logo = request.files.get("logo")

        if logo and logo.filename:
            filename = secure_filename(logo.filename)
            extension = os.path.splitext(filename)[1]

            new_filename = f"{uuid4().hex}{extension}"

            upload_folder = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_folder, exist_ok=True)

            logo.save(os.path.join(upload_folder, new_filename))

            logo_url = url_for(
                "static",
                filename=f"uploads/{new_filename}"
            )

        team = Team(
            name=request.form["team_name"].strip(),
            departments=request.form["departments"].strip(),
            captain_user_id=current_user.id,
            logo_url=logo_url,
            current_season=request.form["season"],
        )

        db.session.add(team)
        db.session.flush()

        for name, email in members:
            db.session.add(TeamMember(team_id=team.id, full_name=name, email=email))

        current_user.full_name = request.form["captain_name"].strip()
        db.session.commit()
        flash("Team created and joined to the season.", "success")
        return redirect(url_for("main.home"))

    return render_template("team_create.html", seasons=SEASONS)


@teams_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    team = current_user.team
    if team is None:
        return redirect(url_for("teams.create_team"))

    if request.method == "POST":
        members = member_rows_from_request()
        if not members:
            flash("Keep at least one team member.", "danger")
            return redirect(url_for("teams.settings"))

        team.name = request.form["team_name"].strip()
        team.departments = request.form["departments"].strip()
        logo = request.files.get("logo")
        if logo and logo.filename:
            filename = secure_filename(logo.filename)
            extension = os.path.splitext(filename)[1]

            new_filename = f"{uuid4().hex}{extension}"

            upload_folder = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_folder, exist_ok=True)

            logo.save(os.path.join(upload_folder, new_filename))

            team.logo_url = url_for(
                "static",
                filename=f"uploads/{new_filename}"
            )
        team.current_season = request.form["season"]
        current_user.full_name = request.form["captain_name"].strip()

        team.members.clear()
        for name, email in members:
            team.members.append(TeamMember(full_name=name, email=email))

        db.session.commit()
        flash("Team settings updated.", "success")
        return redirect(url_for("teams.settings"))

    from app.main.routes import get_team_points

    return render_template(
        "settings.html",
        team=team,
        seasons=SEASONS,
        points=get_team_points(team, team.current_season),
    )
