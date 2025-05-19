from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.models.user import RoleEnum, User

SessionDep = Annotated[AsyncSession, Depends(get_session)]

if TYPE_CHECKING:
    from src.auth.auth import current_user


def require_role(required_role: RoleEnum):
    async def checker(user: User = Depends(current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {user.role}, required: {required_role}",
            )
        return user

    return checker


def require_roles(*roles: RoleEnum):
    async def checker(user: User = Depends(current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {user.role}, allowed: {roles}",
            )
        return user

    return checker
