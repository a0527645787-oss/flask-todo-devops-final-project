from datetime import datetime
from uuid import uuid4
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', 'change-me'),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Stadium(db.Model):
    __tablename__ = "stadiums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    matches = db.relationship("Match", back_populates="stadium")


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey("stadiums.id"), nullable=False)

    stadium = db.relationship("Stadium", back_populates="matches")
    bookings = db.relationship("Booking", back_populates="match")
    seat_types = db.relationship("SeatType", back_populates="match")


class SeatType(db.Model):
    __tablename__ = "seat_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)

    match = db.relationship("Match", back_populates="seat_types")
    bookings = db.relationship("Booking", back_populates="seat_type")

    @property
    def available_seats(self):
        booked_seats = sum(
            booking.seats_count
            for booking in self.bookings
            if not booking.is_cancelled
        )
        return self.total_seats - booked_seats


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    seats_count = db.Column(db.Integer, nullable=False)
    is_cancelled = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)
    seat_type_id = db.Column(db.Integer, db.ForeignKey("seat_types.id"), nullable=False)

    match = db.relationship("Match", back_populates="bookings")
    seat_type = db.relationship("SeatType", back_populates="bookings")


def seed_sample_data():
    if Stadium.query.first():
        return

    stadiums = [
        Stadium(name="MetLife Stadium", city="East Rutherford", capacity=82500),
        Stadium(name="AT&T Stadium", city="Arlington", capacity=80000),
        Stadium(name="Estadio Azteca", city="Mexico City", capacity=87523),
        Stadium(name="Mercedes-Benz Stadium", city="Atlanta", capacity=71000),
    ]

    matches_data = [
        ("Argentina", "Brazil", datetime(2026, 6, 12, 20, 0), stadiums[0]),
        ("France", "Germany", datetime(2026, 6, 14, 18, 0), stadiums[1]),
        ("Mexico", "Canada", datetime(2026, 6, 16, 21, 0), stadiums[2]),
        ("USA", "England", datetime(2026, 6, 18, 19, 30), stadiums[3]),
        ("Spain", "Argentina", datetime(2026, 6, 21, 20, 30), stadiums[0]),
    ]

    matches = []
    for home_team, away_team, match_date, stadium in matches_data:
        match = Match(
            home_team=home_team,
            away_team=away_team,
            match_date=match_date,
            stadium=stadium,
        )
        match.seat_types = [
            SeatType(name="Regular", price=90.0, total_seats=30000),
            SeatType(name="Premium", price=180.0, total_seats=8000),
            SeatType(name="VIP", price=350.0, total_seats=1500),
        ]
        matches.append(match)

    sample_booking = Booking(
        booking_code=str(uuid4()),
        customer_name="Demo Fan",
        customer_email="demo@example.com",
        seats_count=2,
        match=matches[0],
        seat_type=matches[0].seat_types[0],
    )

    db.session.add_all(stadiums + matches + [sample_booking])
    db.session.commit()

# create the DB on demand
@app.before_first_request
def create_tables():
    if app.config.get("TESTING"):
        return
    db.create_all()
    seed_sample_data()

@app.route('/', methods=["GET"])
def index():
    matches = Match.query.all()
    return {
        "message": "Match seat booking app - basic API is ready",
        "matches": [
            {
                "id": match.id,
                "home_team": match.home_team,
                "away_team": match.away_team,
                "match_date": match.match_date.isoformat(),
                "stadium": match.stadium.name,
                "seat_types": [
                    {
                        "id": seat_type.id,
                        "name": seat_type.name,
                        "price": seat_type.price,
                        "total_seats": seat_type.total_seats,
                        "available_seats": seat_type.available_seats,
                    }
                    for seat_type in match.seat_types
                ],
            }
            for match in matches
        ],
    }

@app.route('/health', methods=["GET"])
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    #db.create_all()
    app.run(host=os.getenv('IP', '0.0.0.0'), debug=True)
    # app.run(host=os.getenv('IP', '0.0.0.0'), debug=True,
    #         port=int(os.getenv('PORT', 4444)))
