from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate


def create_item(db: Session, owner_id: int, item_in: ItemCreate) -> Item:
    item = Item(title=item_in.title, description=item_in.description, owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_items_for_user(db: Session, owner_id: int) -> list[Item]:
    return db.query(Item).filter(Item.owner_id == owner_id).all()
