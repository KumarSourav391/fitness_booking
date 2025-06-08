import pytest
from app import create_app, db
from app.models import FitnessClass, Booking
from flask import json
from datetime import datetime, timedelta
import pytz

@pytest.fixture(scope='module')
def test_client():
    app = create_app("local")
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()

        # Seed data
        ist = pytz.timezone("Asia/Kolkata")
        now = datetime.now(ist)

        fitness_class = FitnessClass(
            name="Yoga", datetime_ist=now + timedelta(days=1), instructor="Aniya Shetty", available_slots=5
        )
        db.session.add(fitness_class)
        db.session.commit()

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

        with app.app_context():
            db.drop_all()


def test_home_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Fitness Studio Booking API" in response.data


def test_get_classes(test_client):
    response = test_client.get("/classes")
    assert response.status_code == 200
    classes = json.loads(response.data)
    assert len(classes) >= 1
    assert "name" in classes[0]


def test_book_class_success(test_client):
    payload = {
        "class_id": 1,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    response = test_client.post("/book", json=payload)
    assert response.status_code == 201
    assert b"Booking successful" in response.data


def test_book_class_overbook(test_client):
    # Book 4 more times to exhaust slots (1 already booked above)
    for i in range(4):
        test_client.post("/book", json={
            "class_id": 1,
            "client_name": "User",
            "client_email": f"user{i}@mail.com"
        })

    # Now expect overbook error
    response = test_client.post("/book", json={
        "class_id": 1,
        "client_name": "Last User",
        "client_email": "last@mail.com"
    })
    assert response.status_code == 400
    assert b"Class is fully booked" in response.data


def test_get_bookings_by_email(test_client):
    response = test_client.get("/bookings", query_string={"email": "test@example.com"})
    assert response.status_code == 200
    bookings = json.loads(response.data)
    assert isinstance(bookings, list)
    assert len(bookings) > 0
    assert bookings[0]["client_email"] == "test@example.com"