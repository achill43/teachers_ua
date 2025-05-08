from models.users import UserSQL
from repositories.user_repository import UserRepository
from schemas.users import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> UserSQL:
        user = UserSQL(**user_create)
        return await self.user_repository.create_user(user)
