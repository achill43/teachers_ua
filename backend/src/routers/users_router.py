from depends.auth_deps import get_current_user
from fastapi import APIRouter, Depends, status
from pydiator_core.mediatr import pydiator
from schemas.users import UserResponse
from use_cases.users.create_user import CreateUserRequest, CreateUserResponse
from use_cases.users.refresh_token import RefreshTokenRequest, RefreshTokenResponse
from use_cases.users.user_login import UserLoginRequest, UserLoginResponse

users_router = APIRouter(prefix="/users")


@users_router.post(
    "/sign_up/",
    summary="Create new user",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": CreateUserResponse},
    },
)
async def sign_up(req: CreateUserRequest):
    return await pydiator.send(req=req)


@users_router.post(
    "/sign_in/",
    summary="Login in system",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserLoginResponse},
    },
)
async def sign_in(req: UserLoginRequest):
    return await pydiator.send(req=req)


@users_router.post(
    "/refresh_token/",
    summary="Refresh access token",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": RefreshTokenResponse},
    },
)
async def refresh_token(req: RefreshTokenRequest):
    return await pydiator.send(req=req)


@users_router.get(
    "/me/",
    summary="Get details of currently logged in user",
    response_model=UserResponse,
)
async def get_me(user: UserResponse = Depends(get_current_user)):
    return user
