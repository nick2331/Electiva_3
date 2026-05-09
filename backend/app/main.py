from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.models.database import init_db
from app.routers import analyze, history, results, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Carga el modelo en memoria al arrancar para que el primer request no pague el costo
    from app.services.classifier import get_model
    get_model()
    yield


app = FastAPI(
    title="VehiclEye API",
    description="Sistema de identificación automática de vehículos mediante visión por computador.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(analyze.router, prefix=PREFIX)
app.include_router(history.router, prefix=PREFIX)
app.include_router(results.router, prefix=PREFIX)
app.include_router(admin.router, prefix=PREFIX)


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok", "service": "VehiclEye API"}
