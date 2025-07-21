from fastapi import APIRouter, Depends, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.services.order_service import OrderService
from app.models.order import OrderCreate, OrderListResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=201)
async def create_order(order_data, db: AsyncIOMotorDatabase = Depends(get_database)):
    service = OrderService(db)
    order_id = await service.create_order(order_data)
    return {"id": order_id}

@router.get("/{user_id}", response_model=OrderListResponse)
async def get_user_orders(
    user_id: str = Path(..., description="User ID to get orders for"),
    limit: int = Query(10, ge=1, le=100, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    service = OrderService(db)
    orders, page_info = await service.get_user_orders(
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    
    return OrderListResponse(data=orders, page=page_info)