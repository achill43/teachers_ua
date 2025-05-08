import injector
from config import Settings, settings
from db import SessionLocal
from fastapi_injector import request_scope
from repositories.user_repository import UserRepository
from request_context import RequestContextProvider
from sqlalchemy.ext.asyncio.session import AsyncSession


def configure_for_production(binder: injector.Binder) -> None:
    binder.bind(Settings, to=settings)


class CoreModule(injector.Module):
    @injector.provider
    @request_scope
    def get_request_context(self) -> RequestContextProvider:
        return RequestContextProvider()

    @injector.provider
    @request_scope
    def get_session(self) -> AsyncSession:
        return SessionLocal()

    @injector.provider
    @request_scope
    def get_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)
