CUSTOMER = {
    "full_name": "Іван Петренко",
    "email": "ivan@example.com",
    "phone": "+380501112233",
    "company": "ТОВ Ромашка",
}


def test_create_and_list_customers(client):
    created = client.post("/api/v1/customers", json=CUSTOMER)

    assert created.status_code == 201
    body = created.json()
    assert body["id"] == 1
    assert body["status"] == "active"

    listed = client.get("/api/v1/customers")

    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["email"] == "ivan@example.com"


def test_get_customer_by_id(client):
    created = client.post("/api/v1/customers", json=CUSTOMER)

    response = client.get(f"/api/v1/customers/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json()["full_name"] == "Іван Петренко"


def test_duplicate_email_returns_conflict(client):
    client.post("/api/v1/customers", json=CUSTOMER)

    response = client.post("/api/v1/customers", json=CUSTOMER)

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "conflict"


def test_missing_customer_returns_not_found(client):
    response = client.get("/api/v1/customers/999")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_invalid_payload_returns_validation_error(client):
    response = client.post(
        "/api/v1/customers",
        json={"full_name": "І", "email": "not-an-email"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
