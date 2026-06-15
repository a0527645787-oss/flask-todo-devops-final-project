from datetime import datetime
from functools import wraps
from uuid import uuid4
from flask import abort, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', 'change-me'),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

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
        Stadium(name="Estadio Azteca / Mexico City Stadium", city="Mexico City", capacity=87523),
        Stadium(name="BMO Field / Toronto Stadium", city="Toronto", capacity=45000),
        Stadium(name="SoFi Stadium / Los Angeles Stadium", city="Inglewood", capacity=70240),
        Stadium(name="MetLife Stadium / New York New Jersey Stadium", city="East Rutherford", capacity=82500),
        Stadium(name="AT&T Stadium / Dallas Stadium", city="Arlington", capacity=80000),
        Stadium(name="Mercedes-Benz Stadium / Atlanta Stadium", city="Atlanta", capacity=71000),
        Stadium(name="Estadio Akron / Guadalajara Stadium", city="Zapopan", capacity=48071),
        Stadium(name="Estadio BBVA / Monterrey Stadium", city="Guadalupe", capacity=53500),
        Stadium(name="Gillette Stadium / Boston Stadium", city="Foxborough", capacity=65878),
        Stadium(name="Lincoln Financial Field / Philadelphia Stadium", city="Philadelphia", capacity=67594),
        Stadium(name="Hard Rock Stadium / Miami Stadium", city="Miami Gardens", capacity=65326),
    ]

    # Sample matches based on current public World Cup 2026 schedule information.
    # This is demo seed data, not the complete official schedule.
    matches_data = [
        ("Mexico", "South Africa", datetime(2026, 6, 11, 21, 0), stadiums[0]),
        ("Korea Republic", "Czechia", datetime(2026, 6, 11, 18, 0), stadiums[7]),
        ("Canada", "Bosnia and Herzegovina", datetime(2026, 6, 12, 20, 0), stadiums[1]),
        ("USA", "Paraguay", datetime(2026, 6, 12, 18, 0), stadiums[2]),
        ("Czechia", "Mexico", datetime(2026, 6, 18, 21, 0), stadiums[6]),
        ("South Africa", "Korea Republic", datetime(2026, 6, 19, 19, 0), stadiums[5]),
        ("France", "Norway", datetime(2026, 6, 20, 20, 0), stadiums[3]),
        ("England", "Panama", datetime(2026, 6, 21, 18, 0), stadiums[4]),
        ("Argentina", "Jordan", datetime(2026, 6, 22, 20, 30), stadiums[10]),
        ("Colombia", "Portugal", datetime(2026, 6, 23, 19, 30), stadiums[9]),
    ]

    matches = []
    for home_team, away_team, match_date, stadium in matches_data:
        match = Match(
            home_team=home_team,
            away_team=away_team,
            match_date=match_date,
            stadium=stadium,
        )
        regular_capacity = int(stadium.capacity * 0.55)
        premium_capacity = int(stadium.capacity * 0.18)
        vip_capacity = int(stadium.capacity * 0.03)
        match.seat_types = [
            SeatType(name="Regular", price=120.0, total_seats=regular_capacity),
            SeatType(name="Premium", price=280.0, total_seats=premium_capacity),
            SeatType(name="VIP", price=650.0, total_seats=vip_capacity),
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


def admin_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return view_function(*args, **kwargs)

    return wrapped_view

# create the DB on demand
@app.before_first_request
def create_tables():
    if app.config.get("TESTING"):
        return
    db.create_all()
    seed_sample_data()

@app.route('/', methods=["GET"])
def index():
    matches = Match.query.order_by(Match.match_date).all()
    return render_template("index.html", matches=matches)

@app.route('/health', methods=["GET"])
def health():
    return {"status": "ok"}, 200


@app.route('/matches/<int:match_id>', methods=["GET"])
def match_detail(match_id):
    match = Match.query.get_or_404(match_id)
    return render_template("match_detail.html", match=match)


@app.route('/matches/<int:match_id>/book', methods=["POST"])
def book_match(match_id):
    match = Match.query.get_or_404(match_id)
    customer_name = request.form.get("customer_name", "").strip()
    customer_email = request.form.get("customer_email", "").strip()
    seat_type_id = request.form.get("seat_type_id", type=int)
    seats_count = request.form.get("seats_count", type=int)

    selected_seat_type = SeatType.query.filter_by(
        id=seat_type_id,
        match_id=match.id,
    ).first()

    error = None
    if not customer_name or not customer_email:
        error = "Please enter your name and email."
    elif selected_seat_type is None:
        error = "Please choose a valid seat type for this match."
    elif seats_count is None or seats_count <= 0:
        error = "Please choose at least one seat."
    elif selected_seat_type.available_seats < seats_count:
        error = "Not enough seats are available for this seat type."

    if error:
        return render_template("match_detail.html", match=match, error=error), 400

    booking = Booking(
        customer_name=customer_name,
        customer_email=customer_email,
        seats_count=seats_count,
        match=match,
        seat_type=selected_seat_type,
    )
    db.session.add(booking)
    db.session.commit()

    return redirect(url_for("booking_success", booking_code=booking.booking_code))


@app.route('/bookings/<booking_code>', methods=["GET"])
def booking_success(booking_code):
    booking = Booking.query.filter_by(booking_code=booking_code).first()
    if booking is None:
        abort(404)

    total_price = booking.seats_count * booking.seat_type.price
    return render_template(
        "booking_success.html",
        booking=booking,
        total_price=total_price,
    )


@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_bookings"))
        error = "Invalid admin password"

    return render_template("admin_login.html", error=error)


@app.route('/admin/logout', methods=["GET"])
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index"))


@app.route('/admin/bookings', methods=["GET"])
@admin_required
def admin_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin_bookings.html", bookings=bookings)

if __name__ == "__main__":
    #db.create_all()
    app.run(host=os.getenv('IP', '0.0.0.0'), debug=True)
    # app.run(host=os.getenv('IP', '0.0.0.0'), debug=True,
    #         port=int(os.getenv('PORT', 4444)))
