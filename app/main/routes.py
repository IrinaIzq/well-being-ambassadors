from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.main import main_bp
from app.models import Announcement, BonusChallenge, ChallengeCompletion, HallOfFameEntry, SeasonResult, Team
from app.seasons.data import DEFAULT_BONUS_CHALLENGES, SEASON_CHALLENGES, SEASONS
from app.seasons.utils import days_remaining_in_season, season_is_over


def get_active_bonus_challenges(season):
    """Bonus/surprise challenges currently active for a season, seeding the
    starter set the first time a season is touched."""
    ensure_default_bonus_challenges(season)
    return (
        BonusChallenge.query.filter_by(season=season, active=True)
        .order_by(BonusChallenge.created_at.asc())
        .all()
    )


def ensure_default_bonus_challenges(season):
    """Seed any bonus challenges from the shared default set that this
    season doesn't have yet (matched by key). Safe to call every time: it
    won't duplicate existing ones, and it will backfill new challenges added
    to the shared list for seasons that were already touched before."""
    existing_keys = {
        challenge.key for challenge in BonusChallenge.query.filter_by(season=season).all()
    }
    added = False
    for challenge in DEFAULT_BONUS_CHALLENGES.get(season, []):
        if challenge["key"] in existing_keys:
            continue
        db.session.add(BonusChallenge(season=season, key=challenge["key"], title=challenge["title"], description=challenge["description"]))
        added = True
    if added:
        db.session.commit()


def get_team_points(team, season):
    points = 0
    bonus_keys = {
        challenge.key
        for challenge in BonusChallenge.query.filter_by(season=season).all()
    }
    bonus_points_by_key = {
        challenge.key: challenge.points
        for challenge in BonusChallenge.query.filter_by(season=season).all()
    }

    for completion in team.completions:
        if completion.season != season:
            continue
        if completion.challenge_key in bonus_keys:
            if completion.completed:
                points += bonus_points_by_key[completion.challenge_key]
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
        return redirect(url_for("main.home"))
    return redirect(url_for("auth.login"))


@main_bp.route("/home")
@login_required
def home():
    if current_user.is_admin():
        return redirect(url_for("admin.admin_dashboard"))

    team = current_user.team
    if team is None:
        return redirect(url_for("teams.create_team"))

    season = team.current_season
    ensure_default_bonus_challenges(season)
    season_over = season_is_over(season)

    completion_map = {
        completion.challenge_key: completion
        for completion in team.completions
        if completion.season == season
    }
    pillars = {"Body": [], "Mind": [], "Soul": []}
    for challenge in SEASON_CHALLENGES[season]:
        pillars[challenge["pillar"]].append(challenge)

    return render_template(
        "home.html",
        team=team,
        season=season,
        seasons=SEASONS,
        days_left=0 if season_over else days_remaining_in_season(season),
        season_over=season_over,
        announcements=Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all(),
        pillars=pillars,
        bonus_challenges=get_active_bonus_challenges(season),
        completion_map=completion_map,
        points=get_team_points(team, season),
        ranking=ranked_teams(season),
    )


# Old bookmarks/links to /dashboard still work.
@main_bp.route("/dashboard")
@login_required
def dashboard():
    return redirect(url_for("main.home"))


@main_bp.route("/resources")
@login_required
def resources():
    return render_template("resources.html")


@main_bp.route("/hall-of-fame")
@login_required
def hall_of_fame():
    import json

    season_results = SeasonResult.query.order_by(
        SeasonResult.year.desc(), SeasonResult.closed_at.desc()
    ).all()
    for result in season_results:
        result.ranking = json.loads(result.ranking_json)

    entries = HallOfFameEntry.query.order_by(
        HallOfFameEntry.year.desc(), HallOfFameEntry.category.asc()
    ).all()
    entries_by_year = {}
    for entry in entries:
        entries_by_year.setdefault(entry.year, []).append(entry)

    return render_template(
        "hall_of_fame.html",
        season_results=season_results,
        entries_by_year=entries_by_year,
        seasons=SEASONS,
    )


@main_bp.route("/challenge/<challenge_key>", methods=["POST"])
@login_required
def update_challenge(challenge_key):
    team = current_user.team
    if team is None:
        return redirect(url_for("teams.create_team"))

    if season_is_over(team.current_season):
        flash("This season is over — go to Settings and start the next season to keep playing.", "warning")
        return redirect(url_for("main.home"))

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

    return redirect(url_for("main.home"))