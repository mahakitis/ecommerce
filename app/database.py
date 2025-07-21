import motor.motor_asyncio
from app.config import settings

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    database: motor.motor_asyncio.AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    db.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    db.database = db.client[settings.DATABASE_NAME]

async def close_mongo_connection():
    if db.client:
        db.client.close()

def get_database() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return db.database