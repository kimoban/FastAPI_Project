from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.models.product import PolicyProduct


def compute_premium(product: PolicyProduct, age: int | None = None, region: str | None = None) -> int:
    base = product.base_premium
    # Simple illustrative adjustments
    if age is not None:
        if age < 25:
            base = int(base * 1.2)
        elif age > 60:
            base = int(base * 1.1)
    if region:
        if region.lower() in {"ny", "ca"}:
            base = int(base * 1.15)
    return max(base, 1)


def create_policy(db: Session, user_id: int, product: PolicyProduct, premium: int) -> Policy:
    policy = Policy(user_id=user_id, product_id=product.id, premium=premium)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def list_policies(db: Session, user_id: int) -> list[Policy]:
    return db.query(Policy).filter(Policy.user_id == user_id).order_by(Policy.id.desc()).all()


def get_policy(db: Session, user_id: int, policy_id: int) -> Policy | None:
    return db.query(Policy).filter(Policy.user_id == user_id, Policy.id == policy_id).first()
