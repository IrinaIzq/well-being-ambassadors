import json

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.admin import admin_bp
from app.extensions import db
from app.main.routes import ensure_default_bonus_challenges, get_team_points, ranked_teams
from app.models import Announcement, BonusChallenge, ChallengeCompletion, HallOfFameEntry, SeasonResult, Team, TeamMember, User
from app.seasons.data import SEASONS


def admin_only():
    return current_user.is_authenticated and current_user.is_admin()


@admin_bp.route("/")
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        return redirect(url_for("main.home"))

    from datetime import date

    season = request.args.get("season", "fall")
    ensure_default_bonus_challenges(season)

    rows = [
        {"team": team, "points": get_team_points(team, season)}
        for team in Team.query.order_by(Team.name.asc()).all()
        if team.current_season == season
    ]
    rows.sort(key=lambda item: (-item["points"], item["team"].name.lower()))

    return render_template(
        "admin.html",
        rows=rows,
        season=season,
        seasons=SEASONS,
        current_year=date.today().year,
        bonus_challenges=BonusChallenge.query.filter_by(season=season).order_by(BonusChallenge.created_at.asc()).all(),
        announcements=Announcement.query.order_by(Announcement.created_at.desc()).all(),
        hall_of_fame_entries=HallOfFameEntry.query.order_by(
            HallOfFameEntry.year.desc(), HallOfFameEntry.category.asc()
        ).all(),
        season_results=SeasonResult.query.order_by(
            SeasonResult.year.desc(), SeasonResult.closed_at.desc()
        ).all(),
    )

# ---- Teams -------------------------------------------------------------------------

@admin_bp.route("/teams/<int:team_id>/delete", methods=["POST"])
@login_required
def delete_team(team_id):
    if not admin_only():
        return redirect(url_for("main.home"))

    team = Team.query.get_or_404(team_id)
    team_name = team.name
    captain = team.captain

    # Clean up everything that points at this team so nothing is left orphaned.
    ChallengeCompletion.query.filter_by(team_id=team.id).delete()
    TeamMember.query.filter_by(team_id=team.id).delete()
    if hasattr(BonusChallenge, "created_by_team_id"):
        BonusChallenge.query.filter_by(created_by_team_id=team.id).delete()

    db.session.delete(team)
    if captain:
        db.session.delete(captain)

    db.session.commit()
    flash(f'Team "{team_name}" and its login were deleted.', "success")
    return redirect(url_for("admin.admin_dashboard", season=request.form.get("season", "fall")))

# ---- Bonus / surprise challenges -------------------------------------------------

@admin_bp.route("/bonus-challenges/create", methods=["POST"])
@login_required
def create_bonus_challenge():
    if not admin_only():
        return redirect(url_for("main.home"))

    season = request.form["season"]
    title = request.form["title"].strip()
    description = request.form["description"].strip()
    points = request.form.get("points", "2").strip() or "2"
    key = request.form.get("key", "").strip() or title.lower().replace(" ", "-")[:70]

    if not title or not description:
        flash("Give the bonus challenge a title and description.", "danger")
        return redirect(url_for("admin.admin_dashboard", season=season))

    existing = BonusChallenge.query.filter_by(season=season, key=key).first()
    if existing:
        flash("A bonus challenge with that key already exists for this season.", "danger")
        return redirect(url_for("admin.admin_dashboard", season=season))

    db.session.add(BonusChallenge(season=season, key=key, title=title, description=description,points=int(points)))
    db.session.commit()
    flash("Surprise challenge launched!", "success")
    return redirect(url_for("admin.admin_dashboard", season=season))


@admin_bp.route("/bonus-challenges/<int:challenge_id>/toggle", methods=["POST"])
@login_required
def toggle_bonus_challenge(challenge_id):
    if not admin_only():
        return redirect(url_for("main.home"))

    challenge = BonusChallenge.query.get_or_404(challenge_id)
    challenge.active = not challenge.active
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard", season=challenge.season))


@admin_bp.route("/bonus-challenges/<int:challenge_id>/delete", methods=["POST"])
@login_required
def delete_bonus_challenge(challenge_id):
    if not admin_only():
        return redirect(url_for("main.home"))

    challenge = BonusChallenge.query.get_or_404(challenge_id)
    season = challenge.season
    db.session.delete(challenge)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard", season=season))


# ---- Announcements ----------------------------------------------------------------

@admin_bp.route("/announcements/create", methods=["POST"])
@login_required
def create_announcement():
    if not admin_only():
        return redirect(url_for("main.home"))

    title = request.form["title"].strip()
    body = request.form["body"].strip()
    if not title or not body:
        flash("Announcements need a title and a message.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    db.session.add(Announcement(title=title, body=body))
    db.session.commit()
    flash("Announcement posted to the Home screen.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/announcements/<int:announcement_id>/delete", methods=["POST"])
@login_required
def delete_announcement(announcement_id):
    if not admin_only():
        return redirect(url_for("main.home"))

    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard"))


# ---- Hall of Fame -------------------------------------------------------------------

@admin_bp.route("/hall-of-fame/create", methods=["POST"])
@login_required
def create_hall_of_fame_entry():
    if not admin_only():
        return redirect(url_for("main.home"))

    year = request.form.get("year", "").strip()
    category = request.form.get("category", "").strip()
    team_name = request.form.get("team_name", "").strip()
    note = request.form.get("note", "").strip() or None

    if not (year.isdigit() and category and team_name):
        flash("Year, category and team name are required for a Hall of Fame entry.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    db.session.add(HallOfFameEntry(year=int(year), category=category, team_name=team_name, note=note))
    db.session.commit()
    flash("Added to the Hall of Fame.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/hall-of-fame/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_hall_of_fame_entry(entry_id):
    if not admin_only():
        return redirect(url_for("main.home"))

    entry = HallOfFameEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard"))


# ---- Season results archive (feeds the Hall of Fame podium history) --------------

@admin_bp.route("/season-results/close", methods=["POST"])
@login_required
def close_season():
    if not admin_only():
        return redirect(url_for("main.home"))

    season = request.form["season"]
    year = request.form.get("year", "").strip()
    if not year.isdigit():
        flash("Give the season edition a year.", "danger")
        return redirect(url_for("admin.admin_dashboard", season=season))

    ranking = ranked_teams(season)
    snapshot = [
        {
            "team_name": item["team"].name,
            "logo_url": item["team"].logo_url,
            "points": item["points"],
        }
        for item in ranking
    ]

    db.session.add(SeasonResult(season=season, year=int(year), ranking_json=json.dumps(snapshot)))
    db.session.commit()
    flash(f"{SEASONS[season]['name']} {year} archived to the Hall of Fame.", "success")
    return redirect(url_for("admin.admin_dashboard", season=season))


@admin_bp.route("/season-results/<int:result_id>/delete", methods=["POST"])
@login_required
def delete_season_result(result_id):
    if not admin_only():
        return redirect(url_for("main.home"))

    result = SeasonResult.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard"))
