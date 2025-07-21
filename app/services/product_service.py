from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import settings
from app.models.product import ProductCreate, ProductResponse
import re

class ProductService:
    """Product service for business logic."""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.collection = database[settings.PRODUCTS_COLLECTION]
    
    async def create_product(self, product_data: ProductCreate) -> str:
        """Create a new product."""
        product_dict = product_data.model_dump()
        result = await self.collection.insert_one(product_dict)
        return str(result.inserted_id)
    
    async def get_products(
        self, 
        name: Optional[str] = None,
        size: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[dict], dict]:
        """Get products with filtering and pagination."""
        
        # Build query
        query = {}
        
        if name:
            query["name"] = {"$regex": re.escape(name), "$options": "i"}
        
        if size:
            query["sizes.size"] = size
        
        # Get total count for pagination
        total_count = await self.collection.count_documents(query)
        
        # Get products with pagination
        cursor = self.collection.find(query).sort("_id", 1).skip(offset).limit(limit)
        products = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for product in products:
            product["_id"] = str(product["_id"])
        
        # Calculate pagination info
        next_offset = offset + limit if offset + limit < total_count else None
        previous_offset = max(0, offset - limit) if offset > 0 else None
        
        page_info = {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": len(products),
            "previous": str(previous_offset) if previous_offset is not None else None
        }
        
        return products, page_info
    
    async def get_product_by_id(self, product_id: str) -> Optional[dict]:
        """Get product by ID."""
        try:
            product = await self.collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product["_id"] = str(product["_id"])
            return product
        except:
            return None