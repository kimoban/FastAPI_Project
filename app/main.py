from fastapi import FastAPI
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
from app.services.product_service import seed_default_products


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Project", version="1.0.0")
    app.add_middleware(LoggingMiddleware)
    app.include_router(api_router, prefix="/api/v1")

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

    return app


app = create_app()
