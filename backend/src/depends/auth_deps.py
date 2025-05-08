from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from injector import Injector
from repositories.user_repository import UserRepository
from request_context import RequestContextProvider, RequestUserDataDict
from schemas.users import UserResponse
from utils.jwt_token import check_expired_token, decode_token


async def get_current_user(
    request: Request,
    access_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> UserResponse:
    injector: Injector = request.app.state.injector
    user_repo = injector.get(UserRepository)
    context = injector.get(RequestContextProvider)
    decoded_token = decode_token(access_token.credentials)

    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not check_expired_token(decoded_token.get("date_exp", None)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.get_user_by_email(email=decoded_token.get("email", ""))
    context.set_user(user=RequestUserDataDict(user_id=user.id, user_email=user.email))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    request.state.user = UserResponse.from_orm(user)
    return request.state.user
