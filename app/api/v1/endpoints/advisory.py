from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.get_db import get_db
from app.core.security import get_current_user
from app.schemas.product import ProductRead
from app.services.advisory_service import recommend_products


router = APIRouter(prefix="/advisory", tags=["advisory"])


@router.get("/recommendations", response_model=list[ProductRead])
def recommendations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return recommend_products(db, current_user.id)
