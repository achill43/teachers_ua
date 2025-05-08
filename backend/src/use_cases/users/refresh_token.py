from config import Settings
from fastapi import HTTPException, status
from injector import Inject
from pydantic import BaseModel
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse
from repositories.user_repository import UserRepository
from schemas.users import SessionReponce
from utils.jwt_token import (
    check_expired_token,
    decode_token,
    generate_token,
    generate_token_data,
)


class RefreshTokenRequest(BaseModel, BaseRequest):
    refresh_token: str


class RefreshTokenResponse(BaseModel, BaseResponse):
    session: SessionReponce


class RefreshTokenHandler(BaseHandler):
    def __init__(
        self, user_repository: Inject[UserRepository], settings: Inject[Settings]
    ):
        self.user_repository = user_repository
        self._settings = settings

    async def handle(self, req: RefreshTokenRequest) -> RefreshTokenResponse:  # type: ignore
        decoded_token = decode_token(req.refresh_token)

        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token!",
            )

        if not check_expired_token(decoded_token.get("date_exp", None)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token expired. You have to relogin!",
            )

        user = await self.user_repository.get_user_by_email(
            email=decoded_token.get("email", "")
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email not exist",
            )
        jti = decoded_token.get("jti")
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token!",
            )
        token_data = generate_token_data(
            user=user,
            jti=jti,
            live_time=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            token_type="access",
        )
        access_token = generate_token(token_data=token_data)
        refresh_token = req.refresh_token
        return RefreshTokenResponse(
            session=SessionReponce(
                access_token=access_token, refresh_token=refresh_token
            ),
        )
