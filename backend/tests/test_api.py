import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "BlockRush" in data["service"]

def test_support_query_submission(client):
    payload = {"email": "testplayer@example.com", "query_text": "How do I clear Level 5?"}
    res = client.post("/api/v1/support/submit-query", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["query"]["email"] == "testplayer@example.com"

def test_auth_registration_and_login(client):
    reg_payload = {"username": "playerone", "email": "playerone@example.com", "password": "securepassword123"}
    res_reg = client.post("/api/v1/auth/register", json=reg_payload)
    assert res_reg.status_code == 201
    assert "access_token" in res_reg.get_json()

    login_payload = {"email": "playerone@example.com", "password": "securepassword123"}
    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    assert "access_token" in res_login.get_json()

def test_game_session_placeholder_endpoint(client):
    res = client.get("/api/v1/game/session/state")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "classic" in data["supported_modes"]
