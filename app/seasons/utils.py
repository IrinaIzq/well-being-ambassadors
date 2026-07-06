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


def season_is_over(season_key, today=None):
    """True once today has passed this season's most recent window.

    Our seasons (Fall/Winter/Spring) never wrap across New Year's, so a
    season is currently "active" only if today falls within its start/end
    window for the current year. If today is before that window (e.g. it's
    January and the team is still set to "fall", whose Oct-Dec window
    already happened last year) or after it, the season is over.
    """
    today = today or date.today()
    start_month, start_day = SEASONS[season_key]["start"]
    end_month, end_day = SEASONS[season_key]["end"]

    start_date = date(today.year, start_month, start_day)
    end_date = date(today.year, end_month, end_day)

    return not (start_date <= today <= end_date)