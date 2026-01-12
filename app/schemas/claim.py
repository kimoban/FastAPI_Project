from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClaimCreate(BaseModel):
    policy_id: int
    description: str
    amount: float


class ClaimRead(BaseModel):
    id: int
    policy_id: int
    description: str
    amount: float
    status: str
    created_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
