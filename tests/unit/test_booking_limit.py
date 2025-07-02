import pytest
import copy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

# Fonction utilitaire pour fournir des données de test isolées
def get_test_data():
    """
    Renvoie un dictionnaire contenant des données de test fictives.
    Ces données remplacent temporairement les données réelles lues dans les fichiers JSON.
    Cela permet d’assurer l’indépendance des tests vis-à-vis du contenu réel de l’application.
    """
    return {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        ],
        "competitions": [
            {"name": "Spring Festival", "date": "2099-03-27 10:00:00", "numberOfPlaces": "5"},
        ]
    }


# Fixture Pytest : exécutée automatiquement avant chaque test qui utilise 'client'
@pytest.fixture
def client():
    """
    Crée un client de test Flask avec des données isolées.
    Cette fixture injecte les données simulées dans l’application,
    puis renvoie un client Flask qui permet d’envoyer des requêtes HTTP simulées.
    """
    data = get_test_data()

    # Injection des données fictives dans l’application Flask
    app.clubs = copy.deepcopy(data["clubs"])  # On copie profondément pour éviter les effets de bord entre tests
    app.competitions = copy.deepcopy(data["competitions"])

    app.config['TESTING'] = True  # Active le mode test (désactive certaines protections Flask)

    # Création d’un client de test qui simule un utilisateur Flask
    with app.test_client() as client:
        yield client  


# Test unitaire : s’assure qu’on ne peut pas réserver plus de places que disponibles
def test_booking_more_than_available_places(client):
    """
    Ce test vérifie que si un utilisateur essaie de réserver plus de places
    que ce qui est disponible dans une compétition, un message d'erreur est affiché.
    """
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '6'  # Demande volontairement plus de places que disponibles (5)
    }, follow_redirects=True)  # Suit la redirection si elle a lieu

    # Vérifie que le message d’erreur attendu est bien présent dans la réponse HTML
    assert b"Cannot book more places than are available in the competition." in response.data

