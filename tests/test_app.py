from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    updated = client.get("/activities")
    activity = updated.json()[activity_name]
    assert email not in activity["participants"]

    # Clean up so the test is idempotent
    client.post(f"/activities/{activity_name}/signup?email={email}")


def test_signup_participant_updates_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    updated = client.get("/activities")
    activity = updated.json()[activity_name]
    assert email in activity["participants"]

    # Clean up so the test is idempotent
    client.delete(f"/activities/{activity_name}/participants/{email}")
