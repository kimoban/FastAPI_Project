from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.get_db import get_db
from app.core.security import get_current_user
from app.schemas.claim import ClaimCreate, ClaimRead
from app.services.claim_service import create_claim, list_claims


router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/", response_model=ClaimRead)
def file_claim(payload: ClaimCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        claim = create_claim(db, current_user.id, payload.policy_id, payload.description, payload.amount)
        return claim
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[ClaimRead])
def my_claims(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_claims(db, current_user.id)
