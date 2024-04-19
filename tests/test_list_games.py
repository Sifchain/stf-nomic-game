from unittest.mock import patch

from fastapi.testclient import TestClient

from nomic.main import app

client = TestClient(app)


def test_list_games():
    response = client.get("/game/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Response should be a list of games


def test_no_games():
    # You would mock the database response here to simulate no games existing
    # Using patch or another library to simulate the database response
    with patch("nomic.routes.game_info.crud.get_db") as mock_db:
        mock_db.return_value.query.return_value.all.return_value = []
        response = client.get("/game/list")
        assert response.status_code == 200
        assert response.json() == []  # Should return an empty list
