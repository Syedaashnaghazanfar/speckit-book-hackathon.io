import asyncpg
from ..config import settings

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        db_url = settings.get_database_url
        if not db_url:
            print("Warning: DATABASE_URL/NEON_DATABASE_URL not set. Database features will be disabled.")
            return
        
        try:
            self.pool = await asyncpg.create_pool(db_url)
            await self.create_users_table()
            print("Successfully connected to Neon database")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def create_users_table(self):
        if not self.pool:
            return
            
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query)

    async def get_db(self):
        if not self.pool:
            yield None
            return
            
        async with self.pool.acquire() as conn:
            yield conn

db = Database()
