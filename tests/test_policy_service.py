from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.product import PolicyProduct
from app.services.product_service import list_products
from app.services.policy_service import (
    compute_premium,
    create_policy,
    list_policies,
    get_policy,
)


def setup_module(module):
    # Ensure tables exist for direct service testing
    Base.metadata.create_all(bind=engine)


def test_compute_premium_rules():
    # Use a real PolicyProduct instance to satisfy type-checking
    p = PolicyProduct(
        name="Test Product",
        description=None,
        base_premium=100,
        coverage_limit=1000,
        risk_factor=1.0,
    )
    assert compute_premium(p) == 100
    assert compute_premium(p, age=20) == 120
    assert compute_premium(p, age=65) == 110
    assert compute_premium(p, region="TX") == 100
    # Combined age and region (NY) adjustments; note integer truncation per step
    assert compute_premium(p, age=20, region="NY") == 138


def test_create_and_list_policy():
    db = SessionLocal()
    try:
        # Ensure at least one product exists
        products = list_products(db)
        assert products, "No products available for creating a policy"
        product = products[0]

        # Create a distinct user to avoid unique email conflicts with API tests
        user = User(email="svc_user@example.com", hashed_password="x")
        db.add(user)
        db.commit()
        db.refresh(user)

        premium = compute_premium(product, age=30, region="TX")
        policy = create_policy(db, user_id=user.id, product=product, premium=premium)

        assert policy.id is not None
        assert policy.user_id == user.id
        assert policy.product_id == product.id
        assert policy.premium == premium

        listed = list_policies(db, user_id=user.id)
        assert listed and listed[0].id == policy.id

        fetched = get_policy(db, user_id=user.id, policy_id=policy.id)
        assert fetched is not None and fetched.id == policy.id
    finally:
        db.close()
