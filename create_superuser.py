import asyncio

from fastapi_users.exceptions import UserNotExists
from pydantic import EmailStr

from src.auth.manager import UserManager, get_user_db, get_user_manager
from src.models.user import RoleEnum, User
from src.schemas.user import UserCreateSchema


async def create_superuser():
    user_db_gen = get_user_db()
    user_db = await anext(user_db_gen)
    user_manager = UserManager(user_db)

    try:
        existing_user = await user_manager.get_by_email("admin@admin.com")
        if existing_user:
            print("Admin user already exists.")
            return
    except UserNotExists:
        user = await user_manager.create(
            UserCreateSchema(
                email="admin@admin.com",
                password="admin",
                is_active=True,
                is_superuser=True,
                is_verified=True,
                first_name="Admin",
                last_name="User",
            )
        )
        print("Admin user created:", user.email)


if __name__ == "__main__":
    asyncio.run(create_superuser())
