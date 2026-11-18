def test_health_returns_ok(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"


def test_request_id_header_is_present(client):
    response = client.get("/api/v1/health")

    assert response.headers["X-Request-ID"]


def test_root_returns_service_info(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "CRM System"
