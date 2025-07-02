import pytest
import copy
import sys
import os

# Chemin vers la racine du projet pour importer server.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

# Données spécifiques au test
def get_test_data():
    return {
        "clubs": [
            {"name": "Test Club", "email": "test@club.com", "points": "100"},
        ],
        "competitions": [
            {"name": "Mega Event", "date": "2099-01-01 10:00:00", "numberOfPlaces": "50"},
        ]
    }

@pytest.fixture
def client():
    """
    Crée un client de test Flask avec des données isolées.
    Cette fixture injecte les données simulées dans l’application,
    puis renvoie un client Flask qui permet d’envoyer des requêtes HTTP simulées.
    """
    data = get_test_data()

    # Injection des données fictives dans l’application Flask
    app.clubs = copy.deepcopy(data["clubs"])
    app.competitions = copy.deepcopy(data["competitions"])
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cannot_book_more_than_12_places(client):
    """
    Ce test vérifie que si un utilisateur essaie de réserver plus de 12 places, un message d'erreur est affiché.
    """
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Test Club",
            "competition": "Mega Event",
            "places": "13"  # ➜ dépasse la limite autorisée
        },
        follow_redirects=True
    )

    #Vérifie que le message d’erreur attendu est bien présent dans la réponse HTML
    assert b"Cannot book more than 12 places" in response.data
