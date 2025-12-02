import asyncio
import os
import sys

# Add the parent directory to sys.path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.db import db
from src.config import settings

async def check_users():
    print(f"🔌 Connecting to Database...")
    print(f"   URL: {settings.get_database_url[:25]}... (Hidden for security)")
    
    await db.connect()
    
    if not db.pool:
        print("❌ Failed to connect.")
        return

    try:
        async with db.pool.acquire() as conn:
            # Count users
            count = await conn.fetchval("SELECT COUNT(*) FROM users")
            print(f"\n✅ Connection Successful! Found {count} registered user(s).")

            # List users
            rows = await conn.fetch("SELECT id, email, full_name, created_at FROM users")
            print("\n📋 User List:")
            print("-" * 80)
            print(f"{ 'ID':<5} | {'Email':<30} | {'Name':<20} | {'Created At'}")
            print("-" * 80)
            for row in rows:
                print(f"{row['id']:<5} | {row['email']:<30} | {row['full_name'] or 'N/A':<20} | {row['created_at']}")
            print("-" * 80)

    finally:
        await db.disconnect()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_users())
