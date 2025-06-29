import pytest
import sys
import os
import pytest

# Ajout du chemin vers le dossier racine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime, timedelta
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_cannot_book_past_competition(client):
    test_club = {"name": "Time Travelers", "email": "time@travel.com", "points": "20"}
    past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    test_competition = {"name": "Old Cup", "date": past_date, "numberOfPlaces": "10"}

    clubs.clear()
    competitions.clear()
    clubs.append(test_club)
    competitions.append(test_competition)

    response = client.get(f"/book/{test_competition['name']}/{test_club['name']}", follow_redirects=True)
    
    assert b"cannot book a competition that has already taken place" in response.data.lower()
