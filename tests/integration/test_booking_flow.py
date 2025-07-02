import sys
import os
import pytest
import copy

# Accès au code source
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server import app

# Fonction de données isolées pour l’intégration
def get_test_data():
    return {
        "clubs": [
            {"name": "Test Club", "email": "test@club.com", "points": "20"},
        ],
        "competitions": [
            {"name": "Integration Cup", "date": "2099-01-01 10:00:00", "numberOfPlaces": "15"},
        ],
    }

# Fixture client avec données injectées
@pytest.fixture
def client():
    data = get_test_data()
    app.clubs = copy.deepcopy(data["clubs"])
    app.competitions = copy.deepcopy(data["competitions"])
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_complete_booking_flow(client):
    """
    Test d'intégration complet qui simule une réservation :
    1. Connexion au portail avec un email connu
    2. Accès à la page de réservation
    3. Réservation de 3 places
    4. Vérification du message de succès
    """
    test_club = app.clubs[0]
    test_comp = app.competitions[0]

    # Étape 1 : POST /showSummary
    response = client.post("/showSummary", data={"email": test_club["email"]})
    assert response.status_code == 200
    assert b"Welcome" in response.data

    # Étape 2 : GET /book
    response = client.get(f"/book/{test_comp['name']}/{test_club['name']}")
    assert response.status_code == 200
    assert bytes(test_comp["name"], 'utf-8') in response.data

    # Étape 3 : POST /purchasePlaces
    response = client.post("/purchasePlaces", data={
        "competition": test_comp["name"],
        "club": test_club["name"],
        "places": "3"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Vérifie que les points et places ont été mis à jour
    assert test_club["points"] == "17"
    assert test_comp["numberOfPlaces"] == "12"
