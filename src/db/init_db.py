from src.db.session import engine
from src.models.base import Base


async def create_db() -> None:
    """
    Creates tables in database.
    Does nothing if tables are already exist

    :return: None
    Just creates table if it doesn't exist and returns nothing
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
