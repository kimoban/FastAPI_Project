from sqlalchemy.orm import Session

from app.models.product import PolicyProduct


def list_products(db: Session) -> list[PolicyProduct]:
    return db.query(PolicyProduct).order_by(PolicyProduct.id.asc()).all()


def seed_default_products(db: Session) -> None:
    count = db.query(PolicyProduct).count()
    if count == 0:
        defaults = [
            PolicyProduct(
                name="Basic Health",
                description="Affordable health coverage",
                base_premium=100,
                coverage_limit=10000,
                risk_factor=1.0,
            ),
            PolicyProduct(
                name="Comprehensive Auto",
                description="Full auto coverage with roadside assistance",
                base_premium=150,
                coverage_limit=20000,
                risk_factor=1.2,
            ),
            PolicyProduct(
                name="Home Protect",
                description="Home and contents protection",
                base_premium=120,
                coverage_limit=50000,
                risk_factor=0.9,
            ),
        ]
        db.add_all(defaults)
        db.commit()
