import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings."""
    
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    PORT: int = int(os.getenv("PORT"))
    
    # Collection names
    PRODUCTS_COLLECTION = "products"
    ORDERS_COLLECTION = "orders"

settings = Settings()