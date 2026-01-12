from sqlalchemy.orm import Session

from app.models.claim import Claim
from app.models.policy import Policy


def create_claim(db: Session, user_id: int, policy_id: int, description: str, amount: float) -> Claim:
    policy = db.query(Policy).filter(Policy.id == policy_id, Policy.user_id == user_id).first()
    if not policy:
        raise ValueError("Policy not found or not owned by user")
    claim = Claim(policy_id=policy_id, user_id=user_id, description=description, amount=amount)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def list_claims(db: Session, user_id: int) -> list[Claim]:
    return db.query(Claim).filter(Claim.user_id == user_id).order_by(Claim.id.desc()).all()
