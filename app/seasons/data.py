SEASONS = {
    "fall": {"name": "Fall", "period": "October - December", "start": (10, 1), "end": (12, 31)},
    "winter": {"name": "Winter", "period": "January - March", "start": (1, 1), "end": (3, 31)},
    "spring": {"name": "Spring", "period": "April - June", "start": (4, 1), "end": (6, 30)},
}


FALL_CHALLENGES = [
    {
        "key": "fall-mindfulness-together",
        "pillar": "Mind",
        "title": "Mindfulness Together",
        "description": "Attend a mindfulness session organised by the Center for Health & Well-being.",
    },
    {
        "key": "fall-one-minute-pause",
        "pillar": "Mind",
        "title": "One-Minute Pause",
        "description": "Dedicate one minute during a team meeting to a guided breathing exercise.",
    },
    {
        "key": "fall-move-together",
        "pillar": "Body",
        "title": "Move Together",
        "description": "Participate in an activity organised by the Athletic Center.",
    },
    {
        "key": "fall-active-break",
        "pillar": "Body",
        "title": "Active Break",
        "description": "Organise one five-minute active break during the working week.",
    },
    {
        "key": "fall-kindness-challenge",
        "pillar": "Soul",
        "title": "Kindness Challenge",
        "description": "Each team member writes a positive message for another colleague.",
    },
    {
        "key": "fall-gratitude-wall",
        "pillar": "Soul",
        "title": "Gratitude Wall",
        "description": "Create a gratitude wall and collect at least 10 messages.",
    },
]


SEASON_CHALLENGES = {
    "fall": FALL_CHALLENGES,
    "winter": [{**challenge, "key": challenge["key"].replace("fall", "winter", 1)} for challenge in FALL_CHALLENGES],
    "spring": [{**challenge, "key": challenge["key"].replace("fall", "spring", 1)} for challenge in FALL_CHALLENGES],
}


# Starting set of bonus/surprise challenges. Unlike season challenges, the
# same 6 bonus challenges are offered every season (only Season Challenges
# vary by season) - each season simply tracks its own completions for them.
# These are seeded into the BonusChallenge table the first time each season
# is used, but from then on admins manage bonus challenges from the Admin
# panel (add new "surprise" ones, deactivate old ones) without needing a
# code change.
BONUS_CHALLENGES = [
    {"key": "bonus-healthy-snack", "title": "Bring a Healthy Snack to Share"},
    {"key": "bonus-digital-detox-lunch", "title": "Digital Detox Lunch"},
    {"key": "bonus-step-challenge", "title": "Step Challenge"},
    {"key": "bonus-hydration-week", "title": "Hydration Week"},
    {"key": "bonus-kindness-week", "title": "Random Acts of Kindness Week"},
    {"key": "bonus-walk-bike", "title": "Walk or Bike to Campus Day"},
]

DEFAULT_BONUS_CHALLENGES = {season: BONUS_CHALLENGES for season in SEASONS}