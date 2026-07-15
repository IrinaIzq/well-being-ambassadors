from datetime import date

from app.extensions import db
from app.models import Setting
from app.seasons.data import SEASONS
from app.seasons.services import archive_and_reset_season


def check_season_rollover():

    today = date.today()

    current = Setting.get("current_season", "fall")

    season = SEASONS[current]

    if today <= season["end"]:
        return

    last_reset = Setting.get("last_reset")

    key = today.isoformat()

    if last_reset == key:
        return

    archive_and_reset_season(
        current,
        today.year,
        reset=True,
    )

    seasons = list(SEASONS.keys())

    idx = seasons.index(current)

    next_idx = (idx + 1) % len(seasons)

    Setting.set("current_season", seasons[next_idx])
    Setting.set("last_reset", key)

    db.session.commit()