from datetime import datetime


SOURCE_URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup"
SOURCE_NOTE = "FIFA World Cup 2026 schedule data summarized from the public schedule table, which cites FIFA match schedule data."

STAGE_ORDER = {
    "Group Stage": 1,
    "Round of 32": 2,
    "Round of 16": 3,
    "Quarter-finals": 4,
    "Semi-finals": 5,
    "Third-place match": 6,
    "Final": 7,
}

STAGE_PRICES = {
    "Group Stage": {"Regular": 80, "Premium": 150, "VIP": 300},
    "Round of 32": {"Regular": 120, "Premium": 220, "VIP": 450},
    "Round of 16": {"Regular": 160, "Premium": 300, "VIP": 600},
    "Quarter-finals": {"Regular": 220, "Premium": 450, "VIP": 900},
    "Semi-finals": {"Regular": 300, "Premium": 700, "VIP": 1400},
    "Third-place match": {"Regular": 220, "Premium": 450, "VIP": 900},
    "Final": {"Regular": 400, "Premium": 900, "VIP": 1800},
}

STADIUMS = {
    "Mexico City Stadium": ("Estadio Azteca / Mexico City Stadium", "Mexico City", 83000),
    "Guadalajara Stadium": ("Estadio Akron / Guadalajara Stadium", "Zapopan", 48071),
    "Monterrey Stadium": ("Estadio BBVA / Monterrey Stadium", "Guadalupe", 53500),
    "Toronto Stadium": ("BMO Field / Toronto Stadium", "Toronto", 45000),
    "Vancouver Stadium": ("BC Place / Vancouver Stadium", "Vancouver", 54500),
    "Los Angeles Stadium": ("SoFi Stadium / Los Angeles Stadium", "Inglewood", 70240),
    "San Francisco Bay Area Stadium": ("Levi's Stadium / San Francisco Bay Area Stadium", "Santa Clara", 68500),
    "Seattle Stadium": ("Lumen Field / Seattle Stadium", "Seattle", 69000),
    "Dallas Stadium": ("AT&T Stadium / Dallas Stadium", "Arlington", 94000),
    "Houston Stadium": ("NRG Stadium / Houston Stadium", "Houston", 72000),
    "Kansas City Stadium": ("Arrowhead Stadium / Kansas City Stadium", "Kansas City", 73000),
    "Atlanta Stadium": ("Mercedes-Benz Stadium / Atlanta Stadium", "Atlanta", 75000),
    "Miami Stadium": ("Hard Rock Stadium / Miami Stadium", "Miami Gardens", 65326),
    "Boston Stadium": ("Gillette Stadium / Boston Stadium", "Foxborough", 65878),
    "Philadelphia Stadium": ("Lincoln Financial Field / Philadelphia Stadium", "Philadelphia", 67594),
    "New York New Jersey Stadium": ("MetLife Stadium / New York New Jersey Stadium", "East Rutherford", 82500),
}

GROUPS = {
    "Group A": ["Mexico", "South Africa", "Korea Republic", "Czechia"],
    "Group B": ["Canada", "Qatar", "Switzerland", "Bosnia and Herzegovina"],
    "Group C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "Group D": ["United States", "Paraguay", "Australia", "Turkiye"],
    "Group E": ["Germany", "Curacao", "Cote d'Ivoire", "Ecuador"],
    "Group F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "Group G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "Group H": ["Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"],
    "Group I": ["France", "Iraq", "Norway", "Senegal"],
    "Group J": ["Argentina", "Austria", "Jordan", "Algeria"],
    "Group K": ["Portugal", "Uzbekistan", "Colombia", "Congo DR"],
    "Group L": ["England", "Ghana", "Panama", "Croatia"],
}

GROUP_DATES = {
    "Group A": ["2026-06-11", "2026-06-18", "2026-06-24"],
    "Group B": ["2026-06-12", "2026-06-18", "2026-06-24"],
    "Group C": ["2026-06-13", "2026-06-19", "2026-06-24"],
    "Group D": ["2026-06-12", "2026-06-19", "2026-06-25"],
    "Group E": ["2026-06-14", "2026-06-20", "2026-06-25"],
    "Group F": ["2026-06-14", "2026-06-20", "2026-06-25"],
    "Group G": ["2026-06-15", "2026-06-21", "2026-06-26"],
    "Group H": ["2026-06-15", "2026-06-21", "2026-06-26"],
    "Group I": ["2026-06-16", "2026-06-22", "2026-06-26"],
    "Group J": ["2026-06-16", "2026-06-22", "2026-06-27"],
    "Group K": ["2026-06-17", "2026-06-23", "2026-06-27"],
    "Group L": ["2026-06-17", "2026-06-23", "2026-06-27"],
}

GROUP_STADIUMS = {
    "Group A": ["Mexico City Stadium", "Guadalajara Stadium", "Mexico City Stadium", "Monterrey Stadium", "Guadalajara Stadium", "Mexico City Stadium"],
    "Group B": ["Toronto Stadium", "San Francisco Bay Area Stadium", "Vancouver Stadium", "Toronto Stadium", "Vancouver Stadium", "Toronto Stadium"],
    "Group C": ["New York New Jersey Stadium", "Boston Stadium", "Philadelphia Stadium", "Boston Stadium", "Miami Stadium", "Atlanta Stadium"],
    "Group D": ["Los Angeles Stadium", "Vancouver Stadium", "Seattle Stadium", "San Francisco Bay Area Stadium", "Kansas City Stadium", "Dallas Stadium"],
    "Group E": ["Philadelphia Stadium", "Houston Stadium", "Toronto Stadium", "Kansas City Stadium", "New York New Jersey Stadium", "Philadelphia Stadium"],
    "Group F": ["Dallas Stadium", "Monterrey Stadium", "Houston Stadium", "Monterrey Stadium", "Boston Stadium", "Dallas Stadium"],
    "Group G": ["Seattle Stadium", "Los Angeles Stadium", "Los Angeles Stadium", "Vancouver Stadium", "Seattle Stadium", "Vancouver Stadium"],
    "Group H": ["Miami Stadium", "Atlanta Stadium", "Miami Stadium", "Atlanta Stadium", "Houston Stadium", "Kansas City Stadium"],
    "Group I": ["New York New Jersey Stadium", "Philadelphia Stadium", "New York New Jersey Stadium", "Philadelphia Stadium", "Boston Stadium", "Miami Stadium"],
    "Group J": ["Dallas Stadium", "San Francisco Bay Area Stadium", "Dallas Stadium", "San Francisco Bay Area Stadium", "Seattle Stadium", "Kansas City Stadium"],
    "Group K": ["Houston Stadium", "Guadalajara Stadium", "Houston Stadium", "Guadalajara Stadium", "Monterrey Stadium", "Dallas Stadium"],
    "Group L": ["Boston Stadium", "Toronto Stadium", "Boston Stadium", "Toronto Stadium", "New York New Jersey Stadium", "Philadelphia Stadium"],
}

GROUP_TIMES = ["12:00", "18:00", "12:00", "18:00", "18:00", "18:00"]


def parse_datetime(date_text, time_text):
    hour, minute = [int(part) for part in time_text.split(":")]
    year, month, day = [int(part) for part in date_text.split("-")]
    return datetime(year, month, day, hour, minute)


def group_stage_matches():
    pairings = [(0, 1), (2, 3), (0, 2), (3, 1), (3, 0), (1, 2)]
    matches = []
    match_number = 1
    for group_name, teams in GROUPS.items():
        dates = GROUP_DATES[group_name]
        stadiums = GROUP_STADIUMS[group_name]
        for index, (home_index, away_index) in enumerate(pairings):
            date_text = dates[index // 2]
            time_text = GROUP_TIMES[index]
            matches.append({
                "match_number": match_number,
                "stage": "Group Stage",
                "stage_order": STAGE_ORDER["Group Stage"],
                "group_name": group_name,
                "home_team": teams[home_index],
                "away_team": teams[away_index],
                "home_placeholder": False,
                "away_placeholder": False,
                "match_date": parse_datetime(date_text, time_text),
                "kickoff_time": time_text,
                "stadium_key": stadiums[index],
            })
            match_number += 1
    return matches


KNOCKOUT_MATCHES = [
    (73, "Round of 32", "2026-06-28", "12:00", "Runner-up Group A", "Runner-up Group B", "Los Angeles Stadium"),
    (74, "Round of 32", "2026-06-29", "16:30", "Winner Group E", "3rd Group A/B/C/D/F", "Boston Stadium"),
    (75, "Round of 32", "2026-06-29", "12:00", "Winner Group C", "Runner-up Group F", "Houston Stadium"),
    (76, "Round of 32", "2026-06-29", "19:00", "Winner Group F", "Runner-up Group C", "Monterrey Stadium"),
    (77, "Round of 32", "2026-06-30", "12:00", "Runner-up Group E", "Runner-up Group I", "Dallas Stadium"),
    (78, "Round of 32", "2026-06-30", "17:00", "Winner Group I", "3rd Group C/D/F/G/H", "New York New Jersey Stadium"),
    (79, "Round of 32", "2026-06-30", "19:00", "Winner Group A", "3rd Group C/E/F/H/I", "Mexico City Stadium"),
    (80, "Round of 32", "2026-07-01", "12:00", "Winner Group L", "3rd Group E/H/I/J/K", "Atlanta Stadium"),
    (81, "Round of 32", "2026-07-01", "17:00", "Winner Group D", "3rd Group B/E/F/I/J", "San Francisco Bay Area Stadium"),
    (82, "Round of 32", "2026-07-01", "13:00", "Winner Group G", "3rd Group A/E/H/I/J", "Seattle Stadium"),
    (83, "Round of 32", "2026-07-02", "12:00", "Winner Group H", "Runner-up Group J", "Los Angeles Stadium"),
    (84, "Round of 32", "2026-07-02", "19:00", "Runner-up Group K", "Runner-up Group L", "Toronto Stadium"),
    (85, "Round of 32", "2026-07-02", "20:00", "Winner Group B", "3rd Group E/F/G/I/J", "Vancouver Stadium"),
    (86, "Round of 32", "2026-07-03", "18:00", "Winner Group J", "Runner-up Group H", "Miami Stadium"),
    (87, "Round of 32", "2026-07-03", "13:00", "Runner-up Group D", "Runner-up Group G", "Dallas Stadium"),
    (88, "Round of 32", "2026-07-03", "20:30", "Winner Group K", "3rd Group D/E/I/J/L", "Kansas City Stadium"),
    (89, "Round of 16", "2026-07-04", "17:00", "Winner Match 74", "Winner Match 77", "Philadelphia Stadium"),
    (90, "Round of 16", "2026-07-04", "12:00", "Winner Match 73", "Winner Match 75", "Houston Stadium"),
    (91, "Round of 16", "2026-07-05", "16:00", "Winner Match 76", "Winner Match 78", "New York New Jersey Stadium"),
    (92, "Round of 16", "2026-07-05", "18:00", "Winner Match 79", "Winner Match 80", "Mexico City Stadium"),
    (93, "Round of 16", "2026-07-06", "14:00", "Winner Match 83", "Winner Match 84", "Dallas Stadium"),
    (94, "Round of 16", "2026-07-06", "17:00", "Winner Match 81", "Winner Match 82", "Seattle Stadium"),
    (95, "Round of 16", "2026-07-07", "12:00", "Winner Match 86", "Winner Match 88", "Atlanta Stadium"),
    (96, "Round of 16", "2026-07-07", "13:00", "Winner Match 85", "Winner Match 87", "Vancouver Stadium"),
    (97, "Quarter-finals", "2026-07-09", "16:00", "Winner Match 89", "Winner Match 90", "Boston Stadium"),
    (98, "Quarter-finals", "2026-07-10", "12:00", "Winner Match 93", "Winner Match 94", "Los Angeles Stadium"),
    (99, "Quarter-finals", "2026-07-11", "17:00", "Winner Match 91", "Winner Match 92", "Miami Stadium"),
    (100, "Quarter-finals", "2026-07-11", "20:00", "Winner Match 95", "Winner Match 96", "Kansas City Stadium"),
    (101, "Semi-finals", "2026-07-14", "14:00", "Winner Match 97", "Winner Match 98", "Dallas Stadium"),
    (102, "Semi-finals", "2026-07-15", "15:00", "Winner Match 99", "Winner Match 100", "Atlanta Stadium"),
    (103, "Third-place match", "2026-07-18", "17:00", "Loser Match 101", "Loser Match 102", "Miami Stadium"),
    (104, "Final", "2026-07-19", "15:00", "Winner Match 101", "Winner Match 102", "New York New Jersey Stadium"),
]


def knockout_matches():
    return [
        {
            "match_number": number,
            "stage": stage,
            "stage_order": STAGE_ORDER[stage],
            "group_name": None,
            "home_team": home,
            "away_team": away,
            "home_placeholder": True,
            "away_placeholder": True,
            "match_date": parse_datetime(date_text, time_text),
            "kickoff_time": time_text,
            "stadium_key": stadium_key,
        }
        for number, stage, date_text, time_text, home, away, stadium_key in KNOCKOUT_MATCHES
    ]


def all_matches():
    return group_stage_matches() + knockout_matches()


def seat_capacity_for(stadium, seat_name):
    ratios = {"Regular": 0.55, "Premium": 0.18, "VIP": 0.03}
    return max(1, int(stadium.capacity * ratios[seat_name]))


def upsert_stage_prices(match, SeatType):
    prices = STAGE_PRICES[match.stage]
    existing = {seat_type.name: seat_type for seat_type in match.seat_types}
    for seat_name, price in prices.items():
        if seat_name in existing:
            existing[seat_name].price = float(price)
            existing[seat_name].total_seats = seat_capacity_for(match.stadium, seat_name)
        else:
            match.seat_types.append(SeatType(
                name=seat_name,
                price=float(price),
                total_seats=seat_capacity_for(match.stadium, seat_name),
            ))


def seed_world_cup_2026_data(db, Stadium, Match, SeatType):
    stadiums = {}
    for key, (name, city, capacity) in STADIUMS.items():
        stadium = Stadium.query.filter_by(name=name).first()
        if stadium is None:
            stadium = Stadium(name=name, city=city, capacity=capacity)
            db.session.add(stadium)
        else:
            stadium.city = city
            stadium.capacity = capacity
        stadiums[key] = stadium

    db.session.flush()

    for match_data in all_matches():
        stadium = stadiums[match_data.pop("stadium_key")]
        match = Match.query.filter_by(match_number=match_data["match_number"]).first()
        if match is None:
            match = Match(stadium=stadium, **match_data)
            db.session.add(match)
        else:
            for key, value in match_data.items():
                setattr(match, key, value)
            match.stadium = stadium

        match.source_note = SOURCE_NOTE
        match.source_url = SOURCE_URL
        upsert_stage_prices(match, SeatType)

    db.session.commit()


if __name__ == "__main__":
    from app import Match, SeatType, Stadium, app, db

    with app.app_context():
        db.create_all()
        seed_world_cup_2026_data(db, Stadium, Match, SeatType)
        print(f"Seeded {Match.query.filter(Match.match_number.isnot(None)).count()} World Cup 2026 matches.")
