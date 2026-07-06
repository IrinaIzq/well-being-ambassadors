from datetime import date

from app.seasons.data import SEASONS


def season_end_date(season_key, today=None):
    """Return the next end-of-season date for the given season key.

    Seasons repeat every year, so if "today" is already past this year's
    end date we roll forward to next year's occurrence.
    """
    today = today or date.today()
    end_month, end_day = SEASONS[season_key]["end"]

    end_date = date(today.year, end_month, end_day)
    if end_date < today:
        end_date = date(today.year + 1, end_month, end_day)
    return end_date


def days_remaining_in_season(season_key, today=None):
    today = today or date.today()
    end_date = season_end_date(season_key, today)
    return max((end_date - today).days, 0)
