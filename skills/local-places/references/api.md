# Local Places API (localhost)

Base URL
- Default: `http://127.0.0.1:8000`
- Health: `GET /ping` -> `{ "message": "pong" }`

## 1) Resolve user location

Endpoint
- `POST /locations/resolve`

Request
```json
{
  "location_text": "Riverside Park, New York",
  "limit": 5
}
```

Response
```json
{
  "results": [
    {
      "place_id": "...",
      "name": "Riverside Park",
      "address": "...",
      "location": { "lat": 40.8004, "lng": -73.9702 },
      "types": ["park", "point_of_interest"]
    }
  ]
}
```

Notes
- If multiple results are returned, the user must choose one.
- If none, ask the user to clarify the location text.

## 2) Search for places

Endpoint
- `POST /places/search`

Request
```json
{
  "query": "italian restaurant",
  "location_bias": {
    "lat": 40.8065,
    "lng": -73.9719,
    "radius_m": 3000
  },
  "filters": {
    "types": ["restaurant"],
    "open_now": true,
    "min_rating": 4.0,
    "price_levels": [1, 2, 3],
    "keyword": "outdoor seating"
  },
  "limit": 10,
  "page_token": null
}
```

Response
```json
{
  "results": [
    {
      "place_id": "...",
      "name": "...",
      "address": "...",
      "location": { "lat": 40.7, "lng": -73.9 },
      "rating": 4.6,
      "price_level": 2,
      "types": ["restaurant", "food"],
      "open_now": true
    }
  ],
  "next_page_token": "..."
}
```

Notes
- `filters.types` accepts exactly one type. If user provides multiple, choose one and put the rest into `query` or `filters.keyword`.
- `filters.price_levels`: integers 0–4.
- `filters.min_rating`: 0–5 in 0.5 increments.
- `filters.keyword` is appended to the query by the backend.
- Use `next_page_token` as `page_token` for more results.

## 3) Get place details

Endpoint
- `GET /places/{place_id}`

Response (example fields)
```json
{
  "place_id": "...",
  "name": "...",
  "address": "...",
  "location": { "lat": 40.7, "lng": -73.9 },
  "rating": 4.6,
  "price_level": 2,
  "types": ["restaurant", "food"],
  "phone": "+1 212-555-0100",
  "website": "https://example.com",
  "hours": ["Mon: 9:00 AM – 10:00 PM", "Tue: 9:00 AM – 10:00 PM"],
  "open_now": true
}
```

## Common errors
- 422 validation errors -> fix input ranges or required fields.
- 500/502 from server -> Google Places key missing or upstream failure.
