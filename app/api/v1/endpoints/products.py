from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.get_db import get_db
from app.schemas.product import ProductRead
from app.services.product_service import list_products


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return list_products(db)
