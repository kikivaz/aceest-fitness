import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "ACEest" in res.get_json()["message"]


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_add_and_get_member(client):
    res = client.post("/members", json={"name": "Arun", "plan": "premium"})
    assert res.status_code == 201
    member = res.get_json()
    assert member["id"] == 1 and member["plan"] == "premium"

    res = client.get(f"/members/{member['id']}")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Arun"


def test_default_plan_is_basic(client):
    res = client.post("/members", json={"name": "Meena"})
    assert res.get_json()["plan"] == "basic"


def test_add_member_missing_name(client):
    assert client.post("/members", json={"plan": "basic"}).status_code == 400


def test_add_member_invalid_plan(client):
    res = client.post("/members", json={"name": "X", "plan": "gold"})
    assert res.status_code == 400


def test_list_members(client):
    client.post("/members", json={"name": "A"})
    client.post("/members", json={"name": "B"})
    res = client.get("/members")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_get_missing_member(client):
    assert client.get("/members/999").status_code == 404


def test_delete_member(client):
    client.post("/members", json={"name": "A"})
    assert client.delete("/members/1").status_code == 200
    assert client.delete("/members/1").status_code == 404


def test_bmi_valid(client):
    res = client.get("/bmi?weight=70&height=1.75")
    assert res.status_code == 200
    assert res.get_json()["bmi"] == 22.86


INVALID_BMI_QUERIES = ["", "?weight=70", "?weight=abc&height=1.7", "?weight=-1&height=1.7"]


@pytest.mark.parametrize("query", INVALID_BMI_QUERIES)
def test_bmi_invalid(client, query):
    assert client.get(f"/bmi{query}").status_code == 400
