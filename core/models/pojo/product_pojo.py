"""
Product POJO Model
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ProductPOJO(BaseModel):
    """Product POJO class for JSON serialization/deserialization"""

    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    discount_price: Optional[Decimal] = None
    category: str
    brand: Optional[str] = None
    sku: str = Field(..., min_length=1)
    stock_quantity: int = Field(..., ge=0)
    is_available: bool = True
    images: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 101,
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse",
                "price": 29.99,
                "category": "Electronics",
                "sku": "WM-001",
                "stock_quantity": 50,
                "is_available": True,
                "rating": 4.5,
                "review_count": 120
            }
        }