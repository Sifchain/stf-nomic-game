from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from nomic.main import app

client = TestClient(app)


def test_full_game_flow():
    # 1) Register first user
    response = client.post(
        "/register", data={"username": "user1", "password": "password123"}
    )
    assert response.status_code == 200

    assert "user_id" in response.json()
    user1_id = response.json()["user_id"]

    # 2) Login to first user
    response = client.post(
        "/login", data={"username": "user1", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    token_user1 = response.json()["access_token"]

    # 3) First user creates a new game
    response = client.post(
        "/game/create",
        headers={"Authorization": f"Bearer {token_user1}"},
        data={"game_name": "Nomic Fun", "initial_rules": ["Rule 1", "Rule 2"]},
    )
    assert response.status_code == 200, response.text
    assert "game_id" in response.json()
    game_id = response.json()["game_id"]

    # 3.1) Check if the game was created successfully
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    assert response.json()["game_name"] == "Nomic Fun"

    # 3.2) Check if the list of games is correct
    response = client.get("/games")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["game_name"] == "Nomic Fun"

    # 4) First user joins the new game
    response = client.post(
        f"/game/{game_id}/join", headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Joined the game successfully"

    # 5) Register second user
    response = client.post(
        "/register", data={"username": "user2", "password": "password123"}
    )
    assert response.status_code == 200
    assert "user_id" in response.json()
    user2_id = response.json()["user_id"]

    # 6) Login to second user
    response = client.post(
        "/login", data={"username": "user2", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    token_user2 = response.json()["access_token"]

    # 7) Second user joins the new game
    response = client.post(
        f"/game/{game_id}/join", headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Joined the game successfully"

    # 8) Login to first user again to refresh token (if necessary)
    response = client.post(
        "/login", data={"username": "user1", "password": "password123"}
    )
    assert response.status_code == 200
    token_user1 = response.json()["access_token"]

    # 9) First user starts the game
    response = client.post(
        f"/game/{game_id}/start", headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Started the game successfully"

    # 10) First user proposes a new rule
    response = client.post(
        f"/game/{game_id}/propose-rule",
        headers={"Authorization": f"Bearer {token_user1}"},
        data={"rule_name": "Rule 1", "rule_description": "This is a new rule"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Rule proposed successfully"
    rule_proposal_id = response.json()["rule_proposal_id"]

    # 10.1) Check if the rule proposal was created successfully
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    assert len(response.json()["rule_proposals"]) == 1
    assert response.json()["rule_proposals"][0]["name"] == "Rule 1"
    assert response.json()["rule_proposals"][0]["status"] == "CREATED"

    # 10.2) Check if the list of rule proposals is correct
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Rule 1"
    assert response.json()[0]["status"] == "CREATED"
    assert len(response.json()[0]["votes"]) == 0

    # 10.3) Cast a vote on the rule proposal prior to the voting stage (should fail)
    response = client.post(
        f"/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/yes",
        headers={"Authorization": f"Bearer {token_user2}"},
    )
    assert response.status_code == 400

    # 10.4) Second user ends turn (should fail because it's not their turn)
    response = client.post(
        f"/game/{game_id}/end-turn", headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 400

    # 11) First user ends turn
    response = client.post(
        f"/game/{game_id}/end-turn", headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Turn ended and votes processed"
    assert response.json()["old_turn"] == str(user1_id)
    assert response.json()["new_turn"] == str(user2_id)

    # 11.1) Check if the rule proposal was updated to VOTING stage
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "VOTING"

    # 11.2) Check if the rule proposal was updated to VOTING stage within the game object
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    assert len(response.json()["rule_proposals"]) == 1
    assert response.json()["rule_proposals"][0]["status"] == "VOTING"
    assert response.json()["turn"] == str(user2_id)

    # 12) Second user casts a vote on the rule proposal
    response = client.post(
        f"/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/yes",
        headers={"Authorization": f"Bearer {token_user2}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Vote recorded successfully"

    # 12.1) Same user tries to vote again (should fail)
    response = client.post(
        f"/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/yes",
        headers={"Authorization": f"Bearer {token_user2}"},
    )
    assert response.status_code == 400

    # 12.2) Check if the vote was recorded successfully
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]["votes"]) == 1
    assert response.json()[0]["votes"][0]["vote_type"] == "yes"
    assert response.json()[0]["votes"][0]["user_id"] == str(user2_id)

    # 12.3) Check if the vote was recorded successfully within the game object
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    assert len(response.json()["rule_proposals"]) == 1
    assert len(response.json()["rule_proposals"][0]["votes"]) == 1
    assert response.json()["rule_proposals"][0]["votes"][0]["vote_type"] == "yes"
    assert response.json()["rule_proposals"][0]["votes"][0]["user_id"] == str(user2_id)

    # 12.4) Check if the vote was recorded successfully within the game object when calling /games
    response = client.get("/games")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]["rule_proposals"]) == 1
    assert len(response.json()[0]["rule_proposals"][0]["votes"]) == 1
    assert response.json()[0]["rule_proposals"][0]["votes"][0]["vote_type"] == "yes"
    assert response.json()[0]["rule_proposals"][0]["votes"][0]["user_id"] == str(
        user2_id
    )

    # 13) First user casts a vote on the rule proposal
    response = client.post(
        f"/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/no",
        headers={"Authorization": f"Bearer {token_user1}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Vote recorded successfully"

    # 13.1) Check if the vote was recorded successfully
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]["votes"]) == 2
    assert response.json()[0]["votes"][1]["vote_type"] == "no"
    assert response.json()[0]["votes"][1]["user_id"] == str(user1_id)

    # 14) Second user proposes a new rule
    response = client.post(
        f"/game/{game_id}/propose-rule",
        headers={"Authorization": f"Bearer {token_user2}"},
        data={"rule_name": "Rule 2", "rule_description": "This is a new rule"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Rule proposed successfully"
    rule_proposal_id = response.json()["rule_proposal_id"]

    # 14.1) Check if the rule proposal was created successfully
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    assert len(response.json()["rule_proposals"]) == 2
    assert response.json()["rule_proposals"][1]["name"] == "Rule 2"
    assert response.json()["rule_proposals"][1]["status"] == "CREATED"

    # 14.2) Check if the list of rule proposals is correct
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["name"] == "Rule 2"
    assert response.json()[1]["status"] == "CREATED"
    assert len(response.json()[1]["votes"]) == 0

    # 15) Second user ends turn
    response = client.post(
        f"/game/{game_id}/end-turn", headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Turn ended and votes processed"
    assert response.json()["old_turn"] == str(user2_id)
    assert response.json()["new_turn"] == str(user1_id)

    # 15.1) Check if the rule proposal was updated to REJECTED stage
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 2
    responseJson = response.json()
    responseJson.sort(key=lambda x: x["name"])
    assert responseJson[0]["name"] == "Rule 1"
    assert responseJson[0]["status"] == "REJECTED"
    assert responseJson[1]["name"] == "Rule 2"
    assert responseJson[1]["status"] == "VOTING"
    rule_proposal_id = responseJson[1]["rule_proposal_id"]

    # 16) First user casts a vote on the rule proposal
    response = client.post(
        f"/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/yes",
        headers={"Authorization": f"Bearer {token_user1}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Vote recorded successfully"

    # 17) Second user casts a vote on the rule proposal
    response = client.post(
        f"/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/yes",
        headers={"Authorization": f"Bearer {token_user2}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Vote recorded successfully"

    # 17.1) Check if the rule proposal was updated
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 2
    responseJson = response.json()
    responseJson.sort(key=lambda x: x["name"])
    assert responseJson[0]["status"] == "REJECTED"
    assert responseJson[1]["status"] == "VOTING"
    assert len(responseJson[1]["votes"]) == 2
    assert responseJson[1]["votes"][0]["vote_type"] == "yes"
    assert responseJson[1]["votes"][1]["vote_type"] == "yes"

    # 18) First user ends turn
    response = client.post(
        f"/game/{game_id}/end-turn", headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Turn ended and votes processed"
    assert response.json()["old_turn"] == str(user1_id)
    assert response.json()["new_turn"] == str(user2_id)

    # 18.1) Check if the rule proposal was updated to PASSED stage
    response = client.get(f"/game/{game_id}/rule-proposals")
    assert response.status_code == 200
    assert len(response.json()) == 2
    responseJson = response.json()
    responseJson.sort(key=lambda x: x["name"])
    assert responseJson[0]["status"] == "REJECTED"
    assert responseJson[1]["status"] == "PASSED"

    # 18.2) Check if the new rule is added to the game
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    assert len(response.json()["rules"]) == 1
    assert response.json()["rules"][0]["name"] == "Rule 2"
    assert response.json()["rules"][0]["description"] == "This is a new rule"


@pytest.mark.asyncio
async def main():
    test_full_game_flow()


if __name__ == "__main__":
    pytest.main()
