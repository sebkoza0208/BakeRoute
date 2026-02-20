"""Basic tests to ensure the Flask test client can start the app."""
from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "ok"}