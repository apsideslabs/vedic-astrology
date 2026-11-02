"""API tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_index_serves_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "Jyotish" in r.text
    assert "/api/chart" in r.text


def test_chart_endpoint():
    payload = {
        "date": "1935-11-02", "time": "05:20:00", "latitude": 13.0,
        "longitude": 77.5833333, "tz_offset": 5.1722222,
        "ayanamsa": "raman_397", "house_system": "whole_sign",
    }
    r = client.post("/api/chart", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["lagna"]["sign"] == "Libra"
    assert len(data["planets"]) == 9
    assert len(data["south_indian"]) == 16
    assert len(data["navamsa_grid"]) == 16
    assert data["interpretation"]["sections"]
    assert data["transits"]["gochara"]


def test_bad_date_is_rejected():
    r = client.post("/api/chart", json={
        "date": "02-11-1935", "time": "05:20", "latitude": 13.0, "longitude": 77.5,
    })
    assert r.status_code == 422


def test_latitude_out_of_range():
    r = client.post("/api/chart", json={
        "date": "1935-11-02", "time": "05:20", "latitude": 100.0, "longitude": 77.5,
    })
    assert r.status_code == 422


def test_alternative_settings():
    r = client.post("/api/chart", json={
        "date": "2000-01-01", "time": "00:00", "latitude": 28.6139, "longitude": 77.209,
        "tz_offset": 5.5, "ayanamsa": "lahiri", "house_system": "sripati",
    })
    assert r.status_code == 200, r.text
    assert r.json()["ayanamsa"]["model"] == "lahiri"
