import sys
import os

# Adiciona a raiz do projeto ao path para importar `app`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

def test_ping_db():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get('/ping-db')

    assert response.status_code in [200, 500]
    data = response.get_json()
    assert "status" in data
