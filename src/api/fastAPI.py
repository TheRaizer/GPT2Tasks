from fastapi import FastAPI, status
from routers import text

app = FastAPI()


# routers
app.include_router(text.router)


@app.get("/health", status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {"health": "Everything OK!"}
