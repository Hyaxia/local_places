from __future__ import annotations

import json
from pathlib import Path

from local_places.main import app


def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "openapi.json"
    schema = app.openapi()
    output_path.write_text(json.dumps(schema, indent=2, sort_keys=True))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
