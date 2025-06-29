import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cannot_purchase_more_than_club_points(client):
    test_club = {"name": "Test Club", "email": "test@club.com", "points": 5}
    test_competition = {
        "name": "Test Competition",
        "date": "2099-01-01 10:00:00",
        "numberOfPlaces": "20"
    }

    app.clubs = [test_club]
    app.competitions = [test_competition]

    response = client.post(
        "/purchasePlaces",
        data={
            "club": test_club["name"],
            "competition": test_competition["name"],
            "places": "6"  # Plus que 5 points
        },
        follow_redirects=True
    )

    assert b"not enough points" in response.data.lower()
