from typing import List
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderItemResponse(BaseModel):
    productDetails: dict
    qty: int

class OrderResponse(BaseModel):
    id: str = Field(alias="_id")
    items: List[OrderItemResponse]
    total: float
    
    class Config:
        populate_by_name = True
        from_attributes = True

class OrderListResponse(BaseModel):
    data: List[OrderResponse]
    page: dict