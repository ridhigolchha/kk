from app import app


def test_dashboard_page_loads():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Lead Generation Dashboard" in response.data


def test_generate_endpoint_returns_leads():
    client = app.test_client()
    response = client.post("/generate", json={"count": 3})

    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload["leads"]) == 3
    assert all("score" in lead for lead in payload["leads"])
