from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.get_db import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import create_item, get_items_for_user
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemRead)
def create(item_in: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = create_item(db, owner_id=current_user.id, item_in=item_in)
    return item


@router.get("/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_items_for_user(db, owner_id=current_user.id)
