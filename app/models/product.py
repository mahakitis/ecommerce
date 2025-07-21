from typing import List, Optional
from pydantic import BaseModel, Field

class ProductSize(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[ProductSize] = []

class ProductResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    price: float
    sizes: Optional[List[ProductSize]] = []
    
    class Config:
        populate_by_name = True
        from_attributes = True

class ProductListResponse(BaseModel):
    data: List[ProductResponse]
    page: dict