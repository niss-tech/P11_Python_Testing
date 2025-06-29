import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from server import app, clubs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_points_display_board(client):
    # Simuler quelques clubs avec points
    clubs.clear()
    clubs.extend([
        {"name": "Alpha Club", "email": "alpha@test.com", "points": "20"},
        {"name": "Beta Club", "email": "beta@test.com", "points": "35"},
        {"name": "Gamma Club", "email": "gamma@test.com", "points": "12"}
    ])

    response = client.get("/points")
    
    assert response.status_code == 200
    assert b"Alpha Club" in response.data
    assert b"20" in response.data

    assert b"Beta Club" in response.data
    assert b"35" in response.data

    assert b"Gamma Club" in response.data
    assert b"12" in response.data
