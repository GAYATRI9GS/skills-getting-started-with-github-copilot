import os
import sys

# Ensure the app module can be imported from the src directory
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    # Known activity should exist
    assert "Soccer" in data


def test_signup_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Make sure email isn't registered (ignore errors)
    client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert f"Signed up {email}" in r.json()["message"]

    # Duplicate sign-up should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400

    # Unregister
    r3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r3.status_code == 200
    assert f"Removed {email}" in r3.json()["message"]

    # Unregistering again should fail
    r4 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r4.status_code == 400


def test_activity_not_found():
    r = client.post("/activities/NoSuchActivity/signup?email=someone@nowhere.com")
    assert r.status_code == 404

    r2 = client.post("/activities/NoSuchActivity/unregister?email=someone@nowhere.com")
    assert r2.status_code == 404
