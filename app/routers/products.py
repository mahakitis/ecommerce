from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.services.product_service import ProductService
from app.models.product import ProductCreate, ProductListResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    service = ProductService(db)
    product_id = await service.create_product(product_data)
    return {"id": product_id}

@router.get("/", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name"),
    size: Optional[str] = Query(None, description="Filter by product size"),
    limit: int = Query(10, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    service = ProductService(db)
    products, page_info = await service.get_products(
        name=name, 
        size=size, 
        limit=limit, 
        offset=offset
    )
    
    return ProductListResponse(data=products, page=page_info)