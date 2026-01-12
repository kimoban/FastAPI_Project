from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductRead


class QuoteRequest(BaseModel):
    product_id: int
    age: int | None = None
    region: str | None = None


class QuoteResponse(BaseModel):
    product_id: int
    premium: int


class PolicyCreate(BaseModel):
    product_id: int


class PolicyRead(BaseModel):
    id: int
    product: ProductRead
    premium: int
    status: str
    model_config = ConfigDict(from_attributes=True)
