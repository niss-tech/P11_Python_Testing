import sys
import os
import pytest
import copy

# Ajout du chemin vers la racine du projet pour accéder au serveur
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

# Données de test indépendantes
def get_test_data():
    return {
        "clubs": [
            {"name": "Alpha Club", "email": "alpha@test.com", "points": "20"},
            {"name": "Beta Club", "email": "beta@test.com", "points": "35"},
            {"name": "Gamma Club", "email": "gamma@test.com", "points": "12"},
        ]
    }

@pytest.fixture
def client():
    # Initialise les données dynamiques dans le contexte Flask
    data = get_test_data()
    app.clubs = copy.deepcopy(data["clubs"])
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_points_display_board(client):
    """Vérifie que la page d’affichage des points affiche bien les noms des clubs et leurs points."""
    response = client.get("/points")

    assert response.status_code == 200
    assert b"Alpha Club" in response.data
    assert b"20" in response.data
    assert b"Beta Club" in response.data
    assert b"35" in response.data
    assert b"Gamma Club" in response.data
    assert b"12" in response.data
