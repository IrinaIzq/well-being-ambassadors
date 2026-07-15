from datetime import date

from app.seasons.data import SEASONS


def season_is_over(season_key):
    """Returns True if today's date is after the season end."""
    return date.today() > SEASONS[season_key]["end"]


def days_remaining_in_season(season_key):
    """Returns the remaining days in the season."""
    remaining = (SEASONS[season_key]["end"] - date.today()).days
    return max(remaining, 0)