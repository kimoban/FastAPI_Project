from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.items import router as items_router
from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.policies import router as policies_router
from app.api.v1.endpoints.claims import router as claims_router
from app.api.v1.endpoints.advisory import router as advisory_router
from app.api.v1.endpoints.health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(items_router)
api_router.include_router(products_router)
api_router.include_router(policies_router)
api_router.include_router(claims_router)
api_router.include_router(advisory_router)
api_router.include_router(health_router)
