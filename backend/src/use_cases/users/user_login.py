from uuid import uuid4

from config import Settings
from fastapi import HTTPException, status
from injector import Inject
from pydantic import BaseModel, EmailStr
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse
from repositories.user_repository import UserRepository
from schemas.users import SessionReponce, UserResponse
from utils.jwt_token import generate_token, generate_token_data
from utils.password import verify_password


class UserLoginRequest(BaseModel, BaseRequest):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel, BaseResponse):
    user: UserResponse
    session: SessionReponce


class CreateUserHandler(BaseHandler):
    def __init__(
        self, user_repository: Inject[UserRepository], settings: Inject[Settings]
    ):
        self.user_repository = user_repository
        self._settings = settings

    async def handle(self, req: UserLoginRequest) -> UserLoginResponse:  # type: ignore
        user = await self.user_repository.get_user_by_email(email=req.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email not exist",
            )
        if not verify_password(password=req.password, hashed_pass=user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password"
            )
        jti = uuid4().hex
        token_data = generate_token_data(
            user=user,
            jti=jti,
            live_time=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            token_type="access",
        )
        access_token = generate_token(token_data=token_data)
        token_data = generate_token_data(
            user=user,
            jti=jti,
            live_time=self._settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            token_type="refresh",
        )
        refresh_token = generate_token(token_data=token_data)
        return UserLoginResponse(
            user=UserResponse.from_orm(user),
            session=SessionReponce(
                access_token=access_token, refresh_token=refresh_token
            ),
        )
