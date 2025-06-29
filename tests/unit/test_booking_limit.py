import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server import app, clubs, competitions
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_more_than_available_places(client):
    # On remet la compétition et le club dans un état connu
    for comp in competitions:
        if comp['name'] == 'Spring Festival':
            comp['numberOfPlaces'] = '5' # Seulement 5 places dispo

    for club in clubs:
        if club['name'] == 'Simply Lift':
            club['points'] = '26' # Assez de points

    # Demande 6 places alors que seulement 5 sont dispo
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '6'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Cannot book more places than are available in the competition." in response.data
