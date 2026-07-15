import json

from app.extensions import db
from app.models import (
    BonusChallenge,
    ChallengeCompletion,
    SeasonResult,
    Team,
    TeamMember,
    User,
)


def get_team_points(team, season):
    points = 0

    bonus_keys = {
        c.key
        for c in BonusChallenge.query.filter(
            BonusChallenge.season == season,
            (BonusChallenge.created_by_team_id == None)
            | (BonusChallenge.created_by_team_id == team.id)
        )
    }

    bonus_points = {
        c.key: c.points
        for c in BonusChallenge.query.filter_by(season=season).all()
    }

    for completion in team.completions:
        if completion.season != season:
            continue

        if completion.challenge_key in bonus_keys:
            if completion.completed:
                points += bonus_points[completion.challenge_key]
            continue

        if completion.completed:
            points += 1

        if completion.proof_sent:
            points += 1

    return points


def ranked_teams(season):
    ranking = [
        {
            "team": team,
            "points": get_team_points(team, season),
        }
        for team in Team.query.order_by(Team.name.asc()).all()
        if team.current_season == season
    ]

    return sorted(
        ranking,
        key=lambda item: (-item["points"], item["team"].name.lower())
    )


def archive_and_reset_season(season, year, reset=True):
    ranking = ranked_teams(season)

    snapshot = [
        {
            "team_name": item["team"].name,
            "logo_url": item["team"].logo_url,
            "points": item["points"],
        }
        for item in ranking
    ]

    db.session.add(
        SeasonResult(
            season=season,
            year=year,
            ranking_json=json.dumps(snapshot),
        )
    )

    if reset:
        BonusChallenge.query.filter(
            BonusChallenge.created_by_team_id.isnot(None)
        ).delete()

        ChallengeCompletion.query.delete()
        TeamMember.query.delete()
        Team.query.delete()

        User.query.filter(User.role != "admin").delete()

    db.session.commit()