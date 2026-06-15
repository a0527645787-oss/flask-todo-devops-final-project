from datetime import datetime
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
    seat_types = db.relationship("SeatType", back_populates="stadium")


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey("stadiums.id"), nullable=False)

    stadium = db.relationship("Stadium", back_populates="matches")
    bookings = db.relationship("Booking", back_populates="match")


class SeatType(db.Model):
    __tablename__ = "seat_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey("stadiums.id"), nullable=False)

    stadium = db.relationship("Stadium", back_populates="seat_types")
    bookings = db.relationship("Booking", back_populates="seat_type")


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    seats_count = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)
    seat_type_id = db.Column(db.Integer, db.ForeignKey("seat_types.id"), nullable=False)

    match = db.relationship("Match", back_populates="bookings")
    seat_type = db.relationship("SeatType", back_populates="bookings")


def seed_sample_data():
    if Stadium.query.first():
        return

    stadium = Stadium(name="Bloomfield Stadium", city="Tel Aviv", capacity=29400)
    regular_seat = SeatType(name="Regular", price=80.0, total_seats=20000, stadium=stadium)
    vip_seat = SeatType(name="VIP", price=250.0, total_seats=1000, stadium=stadium)
    match = Match(
        home_team="Maccabi Tel Aviv",
        away_team="Hapoel Beer Sheva",
        match_date=datetime(2026, 7, 1, 20, 30),
        stadium=stadium,
    )

    db.session.add_all([stadium, regular_seat, vip_seat, match])
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
