from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.models.database import init_db
from app.routers import analyze, history, results, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Solo inicializa la DB al arrancar. El modelo se carga de forma lazy en el
    # primer request de análisis para que el health check responda rápido y
    # Render no mate el proceso por timeout durante el cold start.
    await init_db()
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
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(analyze.router, prefix=PREFIX)
app.include_router(history.router, prefix=PREFIX)
app.include_router(results.router, prefix=PREFIX)
app.include_router(admin.router, prefix=PREFIX)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok", "service": "VehiclEye API"}
