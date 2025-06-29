import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_unknown_email_redirects(client):
    response = client.post('/showSummary', data={'email': 'email-inexistant@test.com'}, follow_redirects=True)

    # Vérifie que l'utilisateur est redirigé vers la page d'accueil
    assert b"Welcome to the GUDLFT Registration Portal" in response.data

    # Vérifie que le message d'erreur est affiché
    assert b"sorry" in response.data.lower()
