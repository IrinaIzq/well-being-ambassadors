from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.admin import admin_bp
from app.main.routes import get_team_points
from app.models import Team
from app.seasons.data import SEASONS


@admin_bp.route("/")
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        return redirect(url_for("main.dashboard"))

    season = request.args.get("season", "fall")
    rows = [
        {"team": team, "points": get_team_points(team, season)}
        for team in Team.query.order_by(Team.name.asc()).all()
        if team.current_season == season
    ]
    rows.sort(key=lambda item: (-item["points"], item["team"].name.lower()))

    return render_template("admin.html", rows=rows, season=season, seasons=SEASONS)
