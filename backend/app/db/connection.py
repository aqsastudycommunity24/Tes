"""MongoDB connection management"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global database instance
db: AsyncDatabase = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global db
    try:
        client = AsyncClient(settings.MONGO_URL)
        db = client.get_database()
        # Verify connection
        await db.command("ping")
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global db
    if db:
        db.client.close()
        logger.info("Closed MongoDB connection")


def get_db() -> AsyncDatabase:
    """Get database instance"""
    return db
