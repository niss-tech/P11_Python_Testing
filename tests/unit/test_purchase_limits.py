import pytest
import copy
import sys
import os

# Ajoute le chemin vers la racine du projet pour pouvoir importer server.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

# Fonction utilitaire pour fournir des données isolées pour ce test uniquement
def get_test_data():
    return {
        "clubs": [
            # Club avec seulement 5 points disponibles
            {"name": "Test Club", "email": "test@club.com", "points": "5"},
        ],
        "competitions": [
            {"name": "Test Competition", "date": "2099-01-01 10:00:00", "numberOfPlaces": "20"},
        ]
    }


@pytest.fixture
def client():
    # On isole les données pour ne pas altérer celles du programme
    data = get_test_data()
    app.clubs = copy.deepcopy(data["clubs"])
    app.competitions = copy.deepcopy(data["competitions"])
    app.config["TESTING"] = True  # Active le mode test
    with app.test_client() as client:
        yield client

def test_cannot_purchase_more_than_club_points(client):
    """
    Ce test vérifie qu’on ne peut pas réserver plus de places que le nombre de points du club.
    """
    # Le club essaie de réserver 6 places alors qu’il n’a que 5 points
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": "6"
        },
        follow_redirects=True
    )

    #  # Vérifie que le message d’erreur attendu est bien présent dans la réponse HTML
    assert b"not enough points" in response.data.lower()
