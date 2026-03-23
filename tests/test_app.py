import os
import time
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

def test_root_works():
    r = requests.get(f"{BASE_URL}/", timeout=10)
    assert r.status_code == 200
    assert "Entregable 5 OK" in r.text

def test_health_checks_db():
    for _ in range(20):
        r = requests.get(f"{BASE_URL}/health", timeout=10)
        if r.status_code == 200:
            data = r.json()
            assert data["status"] == "ok"
            assert data["db"] == "ok"
            return
        time.sleep(1)
    raise AssertionError("Health never returned 200")

def test_create_and_list_notes():
    r = requests.post(f"{BASE_URL}/notes", json={"title": "hola"}, timeout=10)
    assert r.status_code == 201
    rid = r.json()["id"]

    r = requests.get(f"{BASE_URL}/notes", timeout=10)
    assert r.status_code == 200
    ids = [x["id"] for x in r.json()]
    assert rid in ids
