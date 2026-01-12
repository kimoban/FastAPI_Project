from sqlalchemy import Column, Integer, String, Float, Text

from app.db.base import Base


class PolicyProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    base_premium = Column(Integer, nullable=False)
    coverage_limit = Column(Integer, nullable=False)
    risk_factor = Column(Float, nullable=True)
