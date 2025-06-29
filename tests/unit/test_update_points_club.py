import sys
import os
import pytest

# Ajout du chemin vers le dossier principal pour importer le serveur
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_club_points_are_updated(client):
    """Vérifie que les points du club sont correctement mis à jour après une réservation."""

    # Réinitialise les points du club Simply Lift à 13
    for club in clubs:
        if club['name'] == 'Simply Lift':
            club['points'] = '13'

    # Réinitialise les places disponibles pour Spring Festival
    for comp in competitions:
        if comp['name'] == 'Spring Festival':
            comp['numberOfPlaces'] = '25'

    # Effectue une réservation de 3 places
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '3'
        },
        follow_redirects=True
    )

    # Vérifie que la réponse est un succès et que le message de confirmation est présent
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Vérifie que les points du club ont bien été réduits (13 - 3 = 10)
    for club in clubs:
        if club['name'] == 'Simply Lift':
            assert club['points'] == '10'
