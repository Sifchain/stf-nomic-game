from fastapi.testclient import TestClient

from nomic.main import app

client = TestClient(app)


def test_list_rules():
    # Assuming you have a game with ID 'game123' and it has rule changes
    response = client.get("/game/game123/rule/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of rule changes


def test_list_rules_no_rules():
    # Assuming you have a game with ID 'game456' with no rule changes
    response = client.get("/game/game456/rule/list")
    assert response.status_code == 200
    assert response.json() == []  # Should return an empty list


def test_list_rules_no_game():
    # Assuming there is no game with ID 'game789'
    response = client.get("/game/game789/rule/list")
    assert response.status_code == 404
