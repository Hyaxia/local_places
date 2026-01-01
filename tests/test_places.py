import logging

from fastapi.testclient import TestClient

import my_api.google_places as google_places
from my_api.main import app


class DummyResponse:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict:
        return self._payload


def test_places_search_returns_results(monkeypatch) -> None:
    payload = {
        "places": [
            {
                "id": "place_123",
                "displayName": {"text": "Luigi's"},
                "formattedAddress": "123 Main St",
                "location": {"latitude": 1.1, "longitude": 2.2},
                "rating": 4.4,
                "priceLevel": "PRICE_LEVEL_EXPENSIVE",
                "types": ["restaurant"],
                "currentOpeningHours": {"openNow": True},
            }
        ],
        "nextPageToken": "next-token",
    }

    def fake_request(method: str, url: str, payload_body: dict, field_mask: str):
        assert method == "POST"
        assert "/places:searchText" in url
        assert payload_body["textQuery"] == "italian restaurant"
        return DummyResponse(200, payload)

    monkeypatch.setattr(google_places, "_request", fake_request)

    client = TestClient(app)
    response = client.post(
        "/places/search",
        json={
            "query": "italian restaurant",
            "filters": {"types": ["restaurant"]},
            "limit": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "place_id": "place_123",
                "name": "Luigi's",
                "address": "123 Main St",
                "location": {"lat": 1.1, "lng": 2.2},
                "rating": 4.4,
                "price_level": 3,
                "types": ["restaurant"],
                "open_now": True,
            }
        ],
        "next_page_token": "next-token",
    }


def test_places_details_returns_place(monkeypatch) -> None:
    payload = {
        "id": "place_456",
        "displayName": {"text": "Mario's"},
        "formattedAddress": "456 Elm St",
        "location": {"latitude": 3.3, "longitude": 4.4},
        "rating": 4.7,
        "priceLevel": "PRICE_LEVEL_MODERATE",
        "types": ["restaurant"],
        "nationalPhoneNumber": "+1 555-1212",
        "websiteUri": "https://example.com",
        "regularOpeningHours": {"weekdayDescriptions": ["Mon: 9AM-5PM"]},
        "currentOpeningHours": {"openNow": False},
    }

    def fake_request(method: str, url: str, payload_body, field_mask: str):
        assert method == "GET"
        assert "/places/place_456" in url
        assert payload_body is None
        return DummyResponse(200, payload)

    monkeypatch.setattr(google_places, "_request", fake_request)

    client = TestClient(app)
    response = client.get("/places/place_456")

    assert response.status_code == 200
    assert response.json() == {
        "place_id": "place_456",
        "name": "Mario's",
        "address": "456 Elm St",
        "location": {"lat": 3.3, "lng": 4.4},
        "rating": 4.7,
        "price_level": 2,
        "types": ["restaurant"],
        "phone": "+1 555-1212",
        "website": "https://example.com",
        "hours": ["Mon: 9AM-5PM"],
        "open_now": False,
    }


def test_places_search_rejects_invalid_min_rating(caplog) -> None:
    client = TestClient(app)
    with caplog.at_level(logging.ERROR, logger="my_api.validation"):
        response = client.post(
            "/places/search",
            json={"query": "pizza", "filters": {"min_rating": 4.3}},
        )

    assert response.status_code == 422
    assert any("Validation error on POST /places/search" in record.message for record in caplog.records)
