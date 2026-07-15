from datetime import date


SEASONS = {
    "fall": {
        "name": "Fall",
        "period": "October - December",
        "start": date(2026,7,15),
        "end": date(2026,12,18),
    },
    "winter": {
        "name": "Winter",
        "period": "December - March",
        "start": date(2027,1,7),
        "end": date(2027,3,19),
    },
    "spring": {
        "name": "Spring",
        "period": "March - June",
        "start": date(2027,3,20),
        "end": date(2027,6,18),
    },
}


FALL_CHALLENGES = [
    {
        "key": "fall-mindfulness-together",
        "pillar": "Mind",
        "title": "Mindfulness Together",
        "description": "Attend a guided meditation session organised by the Center for Health & Well-being.",
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
        "description": "Each team member writes a positive message for another colleague. (In honor of World Kindness Day, November 13th)",
    },
    {
        "key": "fall-gratitude-wall",
        "pillar": "Soul",
        "title": "Gratitude Wall",
        "description": "Create a gratitude wall and collect at least 10 messages.",
    },
]

WINTER_CHALLENGES = [
    {
        "key": "winter-mindfulness-together",
        "pillar": "Mind",
        "title": "Mindfulness Together",
        "description": "Attend a guided meditation session organised by the Center for Health & Well-being.",
    },
    {
        "key": "winter-focus-hour",
        "pillar": "Mind",
        "title": "Focus Hour",
        "description": "Dedicate one uninterrupted hour to focused work by silencing notifications and avoiding multitasking.",
    },
    {
        "key": "winter-exercise-snacks",
        "pillar": "Body",
        "title": "Exercise Snacks",
        "description": "Take a 2-3 minute movement break every hour during the working day.",
    },
    {
        "key": "winter-stairs",
        "pillar": "Body",
        "title": "Stairs Challenge",
        "description": "Take the stairs instead of the elevator for a few times this week.",
    },
    {
        "key": "winter-strength-spotting",
        "pillar": "Soul",
        "title": "Strength Spotting",
        "description": "Identify and acknowledge the strengths of your colleagues.",
    },
    {
        "key": "winter-happiness-week",
        "pillar": "Soul",
        "title": "Happiness Week",
        "description": "Participate in any of the activities organized during the Happiness Week (March 15-19).",
    },
]

SPRING_CHALLENGES = [
    {
        "key": "spring-mindfulness-together",
        "pillar": "Mind",
        "title": "Mindfulness Together",
        "description": "Attend a guided meditation session organised by the Center for Health & Well-being.",
    },
    {
        "key": "spring-outside-lunch",
        "pillar": "Mind",
        "title": "Outside Lunch",
        "description": "Take your lunch break outside to enjoy fresh air and sunlight.",
    },
    {
        "key": "spring-afterlunch-walk",
        "pillar": "Body",
        "title": "After-Lunch Walk",
        "description": "Take a 10-15 minute walk after your lunch break.",
    },
    {
        "key": "fall-active-break",
        "pillar": "Body",
        "title": "Active Break",
        "description": "Organise one five-minute active break during the working week.",
    },
    {
        "key": "spring-coffee-break-conversations",
        "pillar": "Soul",
        "title": "Coffee Break Conversations",
        "description": "Take a few minutes each day to have a conversation with a colleague over coffee.",
    },
        {
        "key": "spring-journaling-practice",
        "pillar": "Soul",
        "title": "Journaling Practice",
        "description": "Spend a moment minutes each day writing in a journal. If needed, you can ask us for a journal and we will provide it.",
    },
]


SEASON_CHALLENGES = {
    "fall": FALL_CHALLENGES,
    "winter": WINTER_CHALLENGES,
    "spring": SPRING_CHALLENGES,
}


# Starting set of bonus/surprise challenges. Unlike season challenges, the
# same 6 bonus challenges are offered every season (only Season Challenges
# vary by season) - each season simply tracks its own completions for them.
# These are seeded into the BonusChallenge table the first time each season
# is used, but from then on admins manage bonus challenges from the Admin
# panel (add new "surprise" ones, deactivate old ones) without needing a
# code change.
BONUS_CHALLENGES = [
    {
        "key": "bonus-digital-detox-lunch",
        "title": "Digital Detox Lunch",
        "description": "Enjoy lunch together without phones or laptops and focus on meaningful conversation.",
    },
    {
        "key": "bonus-step-challenge",
        "title": "Step Challenge",
        "description": "Complete a step challenge as a team during the day.",
    },
    {
        "key": "bonus-kindness",
        "title": "Random Acts of Kindness",
        "description": "Carry out an unexpected act of kindness for someone else.",
    },
]

DEFAULT_BONUS_CHALLENGES = {season: BONUS_CHALLENGES for season in SEASONS}