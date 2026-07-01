from flask import redirect, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.seasons import seasons_bp
from app.seasons.data import SEASONS


@seasons_bp.route("/change", methods=["POST"])
@login_required
def change_season():
    if current_user.team is None:
        return redirect(url_for("teams.create_team"))

    season = request.form.get("season")
    if season in SEASONS:
        current_user.team.current_season = season
        db.session.commit()

    return redirect(url_for("teams.settings"))
