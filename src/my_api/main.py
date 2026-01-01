from fastapi import FastAPI

app = FastAPI(title="My API")


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("my_api.main:app", host="0.0.0.0", port=8000)
