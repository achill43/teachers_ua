from uuid import uuid4

from app.exceptions import EntityAlreadyExistsException, ValidationError
from config import Settings
from injector import Inject
from models.users import UserSQL
from pydantic import BaseModel, EmailStr, model_validator
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse
from repositories.user_repository import UserRepository
from schemas.users import SessionReponce, UserResponse

# from utils.email import send_email
from utils.jwt_token import generate_token, generate_token_data
from utils.password import get_hashed_password


class CreateUserRequest(BaseModel, BaseRequest):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    r_password: str

    @model_validator(mode="before")
    @classmethod
    def verify_password_match(cls, values: dict) -> dict:
        if values.get("password") != values.get("r_password"):
            raise ValidationError("The passwords and r_password must be the same.")
        return values


class CreateUserResponse(BaseModel, BaseResponse):
    user: UserResponse
    session: SessionReponce


class CreateUserHandler(BaseHandler):
    def __init__(
        self, user_repository: Inject[UserRepository], settings: Inject[Settings]
    ):
        self.user_repository = user_repository
        self._settings = settings

    async def handle(self, req: CreateUserRequest) -> CreateUserResponse:  # type: ignore
        user = await self.user_repository.get_user_by_email(email=req.email)
        if user:
            raise EntityAlreadyExistsException("User with this email already exist")
        user_item = req.dict()
        coded_password = get_hashed_password(req.password)
        user_item["password"] = coded_password
        del user_item["r_password"]
        user = await self.user_repository.create_user(UserSQL(**user_item))
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
        # send_email(
        #     subject="Welcome to the club",
        #     body=f"Hello {user.first_name},\n\nWelcome to the club.\n\nBest regards,\n\nThe Club",
        #     sender="sergei.ahill@gmail.com",
        #     recipients=[user.email],
        # )
        return CreateUserResponse(
            user=UserResponse.from_orm(user),
            session=SessionReponce(
                access_token=access_token, refresh_token=refresh_token
            ),
        )
