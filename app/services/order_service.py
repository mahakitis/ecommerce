from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import settings
from app.models.order import OrderCreate
from app.services.product_service import ProductService

class OrderService:
    """Order service for business logic."""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.collection = database[settings.ORDERS_COLLECTION]
        self.product_service = ProductService(database)
    
    async def create_order(self, order_data: OrderCreate) -> str:
        """Create a new order."""
        # Calculate total and get product details
        total = 0.0
        items_with_details = []
        
        for item in order_data.items:
            product = await self.product_service.get_product_by_id(item.productId)
            if product:
                item_total = product["price"] * item.qty
                total += item_total
                
                items_with_details.append({
                    "productDetails": {
                        "name": product["name"],
                        "id": product["_id"]
                    },
                    "qty": item.qty
                })
        
        order_dict = {
            "userId": order_data.userId,
            "items": items_with_details,
            "total": total
        }
        
        result = await self.collection.insert_one(order_dict)
        return str(result.inserted_id)
    
    async def get_user_orders(
        self, 
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[dict], dict]:
        """Get orders for a specific user."""
        
        query = {"userId": user_id}
        
        # Get total count
        total_count = await self.collection.count_documents(query)
        
        # Get orders with pagination
        cursor = self.collection.find(query).sort("_id", 1).skip(offset).limit(limit)
        orders = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for order in orders:
            order["_id"] = str(order["_id"])
        
        # Calculate pagination info
        next_offset = offset + limit if offset + limit < total_count else None
        previous_offset = max(0, offset - limit) if offset > 0 else None
        
        page_info = {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": len(orders),
            "previous": str(previous_offset) if previous_offset is not None else None
        }
        
        return orders, page_info