from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pythonjsonlogger import jsonlogger
from app.api.v1.router import api_router
from app.middleware.logging import LoggingMiddleware
from app.db.session import engine
from app.db.base import Base
# Ensure models are imported so metadata includes them
from app.models import user as user_model  # noqa: F401
from app.models import item as item_model  # noqa: F401
from app.models import product as product_model  # noqa: F401
from app.models import policy as policy_model  # noqa: F401
from app.models import claim as claim_model  # noqa: F401
from app.db.session import SessionLocal
from app.core.config import get_settings
from app.services.product_service import seed_default_products


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="FastAPI Project", version="1.0.0")
    # Configure JSON logging
    logger = logging.getLogger()
    logger.handlers = []
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    app.add_middleware(LoggingMiddleware)
    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api/v1")

    if settings.auto_create_db:
        # Ensure tables exist even when TestClient doesn't trigger lifespan events
        Base.metadata.create_all(bind=engine)
        # Seed default products in development/test if none exist
        db = None
        try:
            db = SessionLocal()
            seed_default_products(db)
        finally:
            if db is not None:
                db.close()

    return app


app = create_app()
