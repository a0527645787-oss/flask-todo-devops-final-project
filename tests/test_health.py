from datetime import datetime

import pytest

from app import Match, SeatType, Stadium, app, db


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()
        stadium = Stadium(
            name="Test Stadium",
            city="Test City",
            capacity=50000,
        )
        match = Match(
            home_team="Team A",
            away_team="Team B",
            match_date=datetime(2026, 6, 11, 20, 0),
            stadium=stadium,
        )
        match.seat_types = [
            SeatType(name="Regular", price=100.0, total_seats=100),
            SeatType(name="VIP", price=500.0, total_seats=10),
        ]
        db.session.add(match)
        db.session.commit()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_health_route(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_home_page_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Team A vs Team B" in response.data


def test_match_detail_page_returns_200(client):
    with app.app_context():
        match = Match.query.first()

    response = client.get(f"/matches/{match.id}")

    assert response.status_code == 200
    assert b"Book seats" in response.data
