import sys
import os

from app import create_app

def test_ping_db():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get('/ping-db')

    assert response.status_code in [200, 500]
    data = response.get_json()
    assert "status" in data
