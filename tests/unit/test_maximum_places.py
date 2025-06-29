import sys
import os
import pytest

# Ajout du chemin vers le dossier racine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cannot_book_more_than_12_places(client):
    # Simule un club et une compétition existants
    test_club = {"name": "Test Club", "email": "test@club.com", "points": "100"}
    test_competition = {"name": "Mega Event", "date": "2099-01-01 10:00:00", "numberOfPlaces": "50"}

    # On modifie les variables globales utilisées par le serveur
    clubs.clear()
    clubs.append(test_club)

    competitions.clear()
    competitions.append(test_competition)

    # Envoie une réservation de 13 places
    response = client.post(
        "/purchasePlaces",
        data={
            "club": test_club["name"],
            "competition": test_competition["name"],
            "places": "13"  # dépasse la limite
        },
        follow_redirects=True
    )

    # Vérifie qu'un message d'erreur est affiché
    assert b"cannot book more than 12 places" in response.data.lower()
