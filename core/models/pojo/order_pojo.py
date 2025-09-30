"""
Order POJO Model
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Order item model"""
    product_id: int
    product_name: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    total_price: Decimal = Field(..., gt=0)


class OrderPOJO(BaseModel):
    """Order POJO class for JSON serialization/deserialization"""

    id: Optional[int] = None
    user_id: int
    order_number: str
    order_date: datetime
    status: OrderStatus = OrderStatus.PENDING
    items: List[OrderItem]
    subtotal: Decimal = Field(..., gt=0)
    tax: Decimal = Field(..., ge=0)
    shipping_cost: Decimal = Field(..., ge=0)
    total_amount: Decimal = Field(..., gt=0)
    shipping_address: str
    billing_address: Optional[str] = None
    payment_method: str
    payment_status: str = "pending"
    tracking_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1001,
                "user_id": 1,
                "order_number": "ORD-2025-001",
                "status": "confirmed",
                "subtotal": 99.99,
                "tax": 9.00,
                "shipping_cost": 5.99,
                "total_amount": 114.98,
                "payment_method": "credit_card"
            }
        }