"""Database seeding script for initial setup"""

import asyncio
from motor.motor_asyncio import AsyncClient
from app.core.config import settings
from app.core.security import PasswordHasher
from datetime import datetime

password_hasher = PasswordHasher()


async def seed_database():
    """Seed the database with initial data"""
    client = AsyncClient(settings.MONGO_URL)
    db = client.get_database()
    
    try:
        # Check if users collection exists and has data
        user_count = await db["users"].count_documents({})
        
        if user_count == 0:
            # Create default superadmin
            superadmin = {
                "email": "admin@qurahub.test",
                "password_hash": password_hasher.hash_password("AdminPassword123!"),
                "name": "Superadmin",
                "role": "superadmin",
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await db["users"].insert_one(superadmin)
            print(f"✅ Created default superadmin with ID: {result.inserted_id}")
            print(f"   Email: {superadmin['email']}")
            print(f"   Password: AdminPassword123!")
            print(f"   Role: superadmin")
        else:
            print(f"⚠️  Database already has {user_count} user(s), skipping seed")
        
        # Create indexes
        await db["users"].create_index("email", unique=True)
        await db["contents"].create_index("slug", unique=True)
        await db["contents"].create_index("pillar")
        await db["contents"].create_index("status")
        print("✅ Database indexes created")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        client.close()


if __name__ == "__main__":
    print("🌱 Seeding Quran Hub database...")
    asyncio.run(seed_database())
    print("✨ Database seeding completed!")
