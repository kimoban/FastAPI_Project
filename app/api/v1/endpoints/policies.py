from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.get_db import get_db
from app.core.security import get_current_user
from app.models.product import PolicyProduct
from app.schemas.policy import QuoteRequest, QuoteResponse, PolicyCreate, PolicyRead
from app.services.policy_service import compute_premium, create_policy, list_policies, get_policy


router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("/quote", response_model=QuoteResponse)
def quote(req: QuoteRequest, db: Session = Depends(get_db)):
    product = db.query(PolicyProduct).filter(PolicyProduct.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    premium = compute_premium(product, age=req.age, region=req.region)
    return QuoteResponse(product_id=product.id, premium=premium)


@router.post("/", response_model=PolicyRead)
def purchase(payload: PolicyCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    product = db.query(PolicyProduct).filter(PolicyProduct.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    premium = compute_premium(product)
    policy = create_policy(db, current_user.id, product, premium)
    return policy


@router.get("/", response_model=list[PolicyRead])
def my_policies(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_policies(db, current_user.id)


@router.get("/{policy_id}", response_model=PolicyRead)
def get_policy_detail(policy_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    policy = get_policy(db, current_user.id, policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy
