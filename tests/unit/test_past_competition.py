import pytest
import copy
import sys
import os
from datetime import datetime

# Ajout du chemin vers la racine du projet pour pouvoir importer le fichier server.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

# Fonction utilitaire pour fournir des données isolées pour le test
def get_test_data():
    return {
        "clubs": [
            # Un club fictif avec 20 points
            {"name": "Time Travelers", "email": "time@travel.com", "points": "20"},
        ],
        "competitions": [
            {
                "name": "Old Cup",
                "date": "2023-01-01 10:00:00",  # date passée volontairement
                "numberOfPlaces": "10"
            },
        ]
    }


@pytest.fixture
def client():
    data = get_test_data()

    # On remplace les données globales utilisées par l’application
    app.clubs = copy.deepcopy(data["clubs"])
    app.competitions = copy.deepcopy(data["competitions"])
    app.config["TESTING"] = True  # Mode test activé (désactive le catch des erreurs)

    # Création du client Flask pour simuler des requêtes HTTP
    with app.test_client() as client:
        yield client


def test_cannot_book_past_competition(client):
    """
    Ce test empêche la réservation d’une compétition déjà passée
    """
    # Appelle la route `/book/...` pour simuler une tentative de réservation
    response = client.get('/book/Old%20Cup/Time%20Travelers', follow_redirects=True)

    # Vérifie que le message d’erreur apparaît bien dans la réponse HTML
    assert b"you cannot book a competition that has already taken place" in response.data.lower()
