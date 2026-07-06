from datetime import date

from app.seasons.data import SEASONS


def season_end_date(season_key, today=None):
    today = today or date.today()

    start_month, start_day = SEASONS[season_key]["start"]
    end_month, end_day = SEASONS[season_key]["end"]

    # Seasons that cross the year boundary (Winter)
    if start_month > end_month:
        if today.month >= start_month:
            end_date = date(today.year + 1, end_month, end_day)
        else:
            end_date = date(today.year, end_month, end_day)
    else:
        end_date = date(today.year, end_month, end_day)
        if end_date < today:
            end_date = date(today.year + 1, end_month, end_day)

    return end_date


def days_remaining_in_season(season_key, today=None):
    today = today or date.today()
    end_date = season_end_date(season_key, today)
    return max((end_date - today).days, 0)


def season_is_over(season_key, today=None):
    today = today or date.today()

    start_month, start_day = SEASONS[season_key]["start"]
    end_month, end_day = SEASONS[season_key]["end"]

    # Winter (crosses New Year)
    if start_month > end_month:
        if today.month >= start_month:
            start_date = date(today.year, start_month, start_day)
            end_date = date(today.year + 1, end_month, end_day)
        else:
            start_date = date(today.year - 1, start_month, start_day)
            end_date = date(today.year, end_month, end_day)
    else:
        start_date = date(today.year, start_month, start_day)
        end_date = date(today.year, end_month, end_day)

    return not (start_date <= today <= end_date)