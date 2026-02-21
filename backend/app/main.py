from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.cbc import router as cbc_router
from app.api.orchestrator import router as orchestrator_router

app = FastAPI(title="WISE AI")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def root():
    """API root - links to docs and health."""
    return {
        "message": "WISE AI API",
        "docs": "/docs",
        "health": "/health",
        "openapi": "/openapi.json",
    }


# ⚠️ Only keep this if you are NOT using Alembic for schema creation
#from app.db.models import Base
#from app.db.session import engine
#Base.metadata.create_all(bind=engine)

# Routers
app.include_router(health_router)
app.include_router(cbc_router, prefix="/cbc")
app.include_router(orchestrator_router)
