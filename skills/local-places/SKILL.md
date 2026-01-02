---
name: local-places
description: Use the local Places API (Google Maps search proxy on localhost) to resolve a user's location, have them choose the correct match, then search for nearby places with preferences (type, open now, min rating, price levels, limit). Trigger for requests like “find restaurants near me”, “coffee in SoHo”, “best gyms in Brooklyn”, or when you need place details by place_id.
---

# Local Places

Use this skill to run a two-step flow: resolve location first, then search.

Quick checklist
- Confirm API base URL (default `http://127.0.0.1:8000`) and that `GET /ping` responds.
- Resolve the user location with `POST /locations/resolve`.
- If multiple results are returned, show a numbered list (name + address) and ask the user to choose.
- Ask what they are looking for and any constraints (open now, min rating, price level, type, limit, radius).
- Search with `POST /places/search` using `location_bias` from the chosen location.
- Present results and offer to fetch details via `GET /places/{place_id}`.

Conversation rules
- Always ask for a location if none is set yet.
- If the user says “near me,” ask for a city/neighborhood or a specific place to resolve.
- Keep the selected location for follow-up searches until the user changes it.
- If multiple types are mentioned, pick the most important type and fold the rest into the query or `filters.keyword`.
- If the user asks for more results, use `next_page_token` with `page_token`.

Input constraints (enforce or clarify)
- `filters.types` supports exactly one type.
- `filters.price_levels` must be integers 0–4.
- `filters.min_rating` must be 0–5 in 0.5 increments.
- `limit`: 1–20 for search, 1–10 for resolve.
- `location_bias.radius_m` must be > 0.

Output expectations
- List results with name, rating, price level (if present), address, and open-now status.
- Provide a clear follow-up prompt (refine filters, change radius, or request details).

Example flow (minimal)
1) Resolve location
```bash
POST /locations/resolve
{
  "location_text": "SoHo, New York",
  "limit": 5
}
```
If multiple results, ask the user to pick one by number.

2) Search nearby
```bash
POST /places/search
{
  "query": "coffee shop",
  "location_bias": { "lat": 40.7233, "lng": -74.0020, "radius_m": 2000 },
  "filters": { "types": ["cafe"], "open_now": true, "min_rating": 4.0 },
  "limit": 10
}
```

3) Optional: details
```bash
GET /places/{place_id}
```

Reference
- See `references/api.md` for full request/response shapes and examples.
