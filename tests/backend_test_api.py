from fastapi.testclient import TestClient
from backend.app.main import app


def test_health_endpoint_shape():
    client = TestClient(app)
    res = client.get('/health')
    assert res.status_code == 200
    body = res.json()
    assert body['ok'] is True
    assert body['version'] == '2.6.0-rc1'
