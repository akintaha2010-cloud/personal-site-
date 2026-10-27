import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
from main import app
from match import calculate_match_score


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()
    app.config["TESTING"] = True
    return app.test_client()


def register_and_login(client, email="a@example.com"):
    client.post("/register", data={"full_name": "A", "email": email, "password": "pw"})
    client.post("/login", data={"email": email, "password": "pw"})


def add(client, report_type="Lost"):
    return client.post("/add_user", data={
        "report_type": report_type,
        "item_name": "Keys",
        "location": "Library",
        "category": "Keys",
        "description": "red keychain",
    })


def test_match_score_identical_items():
    item = {"name": "Keys", "location": "Library", "category": "Keys", "description": "red keychain"}
    assert calculate_match_score(item, item) == 90


def test_add_requires_login(client):
    assert add(client).status_code == 302
    assert database.get_items() == []


def test_add_and_list(client):
    register_and_login(client)
    assert add(client).status_code == 302
    assert len(database.get_items()) == 1


def test_invalid_report_type_rejected(client):
    register_and_login(client)
    assert add(client, "Stolen").status_code == 400


def test_delete_only_by_owner(client):
    register_and_login(client)
    add(client)
    item_id = database.get_items()[0][0]
    client.get("/logout")
    register_and_login(client, "b@example.com")
    assert client.post(f"/delete_user/{item_id}").status_code == 403
    assert client.get(f"/delete_user/{item_id}").status_code == 405


def test_matches_shown_on_index(client):
    register_and_login(client)
    add(client, "Lost")
    add(client, "Found")
    assert b"90" in client.get("/").data
