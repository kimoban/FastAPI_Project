from sqlalchemy.orm import Session

from app.models.product import PolicyProduct
from app.models.policy import Policy


def recommend_products(db: Session, user_id: int) -> list[PolicyProduct]:
    # Recommend products the user doesn't already have, cheapest first
    owned_product_ids = {p.product_id for p in db.query(Policy).filter(Policy.user_id == user_id).all()}
    products = (
        db.query(PolicyProduct)
        .filter(~PolicyProduct.id.in_(owned_product_ids) if owned_product_ids else True)
        .order_by(PolicyProduct.base_premium.asc())
        .all()
    )
    return products
