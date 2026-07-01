from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.main import main_bp
from app.models import ChallengeCompletion, Team
from app.seasons.data import BONUS_CHALLENGES, SEASON_CHALLENGES, SEASONS


def get_team_points(team, season):
    points = 0
    bonus_keys = {challenge["key"] for challenge in BONUS_CHALLENGES[season]}

    for completion in team.completions:
        if completion.season != season:
            continue
        if completion.challenge_key in bonus_keys:
            if completion.completed:
                points += 2
            continue
        if completion.completed:
            points += 1
        if completion.proof_sent:
            points += 1

    return points


def ranked_teams(season):
    ranking = [
        {"team": team, "points": get_team_points(team, season)}
        for team in Team.query.order_by(Team.name.asc()).all()
        if team.current_season == season
    ]
    return sorted(ranking, key=lambda item: (-item["points"], item["team"].name.lower()))


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for("admin.admin_dashboard"))

    team = current_user.team
    if team is None:
        return redirect(url_for("teams.create_team"))

    season = team.current_season
    completion_map = {
        completion.challenge_key: completion
        for completion in team.completions
        if completion.season == season
    }
    pillars = {"Body": [], "Mind": [], "Soul": []}
    for challenge in SEASON_CHALLENGES[season]:
        pillars[challenge["pillar"]].append(challenge)

    return render_template(
        "dashboard.html",
        team=team,
        season=season,
        seasons=SEASONS,
        pillars=pillars,
        bonus_challenges=BONUS_CHALLENGES[season],
        completion_map=completion_map,
        points=get_team_points(team, season),
        ranking=ranked_teams(season),
    )


@main_bp.route("/challenge/<challenge_key>", methods=["POST"])
@login_required
def update_challenge(challenge_key):
    team = current_user.team
    if team is None:
        return redirect(url_for("teams.create_team"))

    completion = ChallengeCompletion.query.filter_by(
        team_id=team.id,
        season=team.current_season,
        challenge_key=challenge_key,
    ).first()

    if completion is None:
        completion = ChallengeCompletion(
            team_id=team.id,
            season=team.current_season,
            challenge_key=challenge_key,
        )
        db.session.add(completion)

    completion.completed = request.form.get("completed") == "on"
    completion.proof_sent = request.form.get("proof_sent") == "on"
    db.session.commit()

    return redirect(url_for("main.dashboard"))
