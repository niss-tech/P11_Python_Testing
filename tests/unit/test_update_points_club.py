import pytest
import copy
import sys
import os

# Ajoute le chemin vers la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

# Données isolées pour les tests
def get_test_data():
    return {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        ],
        "competitions": [
            {"name": "Spring Festival", "date": "2099-03-27 10:00:00", "numberOfPlaces": "25"},
        ]
    }

@pytest.fixture
def client():
    """Configure un client Flask de test avec des données isolées."""
    data = get_test_data()
    app.clubs = copy.deepcopy(data["clubs"])
    app.competitions = copy.deepcopy(data["competitions"])
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_club_points_are_updated(client):
    """
    Vérifie que les points du club sont bien mis à jour
    après une réservation valide.
    """
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '3'  # Réservation de 3 places
        },
        follow_redirects=True
    )

    # Vérifie que la réponse HTTP est correcte et que le message de succès s'affiche
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Vérifie que les points du club ont bien diminué (13 - 3 = 10)
    updated_points = next(c for c in app.clubs if c['name'] == 'Simply Lift')['points']
    assert updated_points == '10'
