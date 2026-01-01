# My API

FastAPI starter template.

## Run locally

```bash
uv venv
uv pip install -e ".[dev]"
uv run uvicorn my_api.main:app --host 0.0.0.0 --reload
```

Open the API docs at http://127.0.0.1:8000/docs.

## Test

```bash
uv run pytest
```
