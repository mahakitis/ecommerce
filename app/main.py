from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import products, orders
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

# Create FastAPI app
app = FastAPI(
    title="Ecommerce Backend API",
    description="FastAPI backend for ecommerce application",
    lifespan=lifespan,
)

# Include routers
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Ecommerce Backend API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}