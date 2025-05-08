from typing import Tuple, cast
from uuid import uuid4

import pytest
import pytest_asyncio
from app.server import app
from db import Base, get_db
from fastapi import Depends, FastAPI
from fastapi_injector import InjectorMiddleware, attach_injector, request_scope
from fastapi_injector.request_scope import RequestScope, _request_id_ctx
from injector import Injector
from injector_setup import injector_setup
from pydiator_core.mediatr import Mediatr
from pydiator_setup import setup_pydiator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from use_cases.users.create_user import CreateUserRequest, CreateUserResponse

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
TestSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture(scope="session")
def db_engine():
    return engine


@pytest_asyncio.fixture
async def db_session(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def test_app(db_session) -> Tuple[FastAPI, Injector, Mediatr]:
    injector = injector_setup(app)
    attach_injector(app, injector)
    app.add_middleware(InjectorMiddleware, injector=injector)

    # Override get_db dependency
    app.dependency_overrides[get_db] = Depends(db_session)
    injector.binder.bind(AsyncSession, to=db_session, scope=request_scope)

    pydiator = setup_pydiator(injector)

    # Set up request scope cache
    request_id = uuid4()
    _request_id_ctx.set(request_id)
    request_scope_obj = injector.get(RequestScope)
    request_scope_obj.cache[request_id] = {}

    return app, injector, pydiator


@pytest_asyncio.fixture
async def user_fixture(test_app):
    _, _, pydiator = test_app
    response = cast(
        CreateUserResponse,
        await pydiator.send(
            req=CreateUserRequest(
                email="email+1@gmail.com",
                first_name="Test",
                last_name="Test",
                password="String1234",
                r_password="String1234",
            )
        ),
    )
    return response.user
