from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    base_premium: int
    coverage_limit: int
    model_config = ConfigDict(from_attributes=True)
