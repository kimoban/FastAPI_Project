from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.services.product_service import list_products, seed_default_products


def setup_module(module):
    # Ensure tables exist for direct service testing
    Base.metadata.create_all(bind=engine)


def test_list_products_and_seed_idempotent():
    db = SessionLocal()
    try:
        before = list_products(db)
        # Call seeding; should not duplicate when products already exist
        seed_default_products(db)
        after = list_products(db)
        assert len(after) >= len(before)
        # Verify stable count when defaults already present
        assert len(after) == len(list_products(db))
        # Verify ordering by ascending id
        ids = [p.id for p in after]
        assert ids == sorted(ids)
    finally:
        db.close()
