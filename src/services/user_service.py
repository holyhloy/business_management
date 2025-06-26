from fastapi import HTTPException
from sqlalchemy import select

from src.dependencies.deps import SessionDep
from src.models import User


async def get_all_users(session: SessionDep) -> list[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail=f"Some error while getting users")
