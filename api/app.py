from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router
from persistence.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Tower of Lucas API",
    description="API REST para o RPG de texto Tower of Lucas com persistencia SQLite",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def read_root():
    return {
        "game": "Tower of Lucas",
        "status": "online",
        "docs_url": "/docs",
    }
