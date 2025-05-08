from typing import cast

from models.users import UserSQL
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserSQL) -> UserSQL:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> UserSQL:
        result = await self.db.execute(select(UserSQL).filter_by(id=user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> UserSQL:
        result = await self.db.execute(select(UserSQL).filter_by(email=email))
        return result.scalar_one_or_none()

    async def delete_by_id(self, user_id: int):
        user = cast(
            UserSQL,
            await self.db.scalar(select(UserSQL).where(UserSQL.id == user_id)),
        )
        if not user:
            return None
        await self.db.execute(delete(UserSQL).where(UserSQL.id == user_id))
        await self.db.commit()
