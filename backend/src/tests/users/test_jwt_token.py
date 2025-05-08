from typing import cast
from uuid import uuid4

import pytest
from models.users import UserSQL
from sqlalchemy import select
from utils.jwt_token import decode_token, generate_token, generate_token_data


@pytest.mark.asyncio
async def test_generate_token_data(test_app, db_session, user_fixture):
    _, _, pydiator = test_app
    user = user_fixture
    user = await db_session.scalar(select(UserSQL).where(UserSQL.email == user.email))
    jti = uuid4().hex
    responce = cast(
        dict,
        generate_token_data(user=user, jti=jti, live_time=3600, token_type="access"),
    )
    assert responce.get("user_id") == user_fixture.id
    assert responce.get("email") == user_fixture.email


@pytest.mark.asyncio
async def test_generate_token(test_app, db_session, user_fixture):
    _, _, pydiator = test_app
    user = user_fixture
    user = await db_session.scalar(select(UserSQL).where(UserSQL.email == user.email))
    jti = uuid4().hex
    token_data = cast(
        dict,
        generate_token_data(user=user, jti=jti, live_time=3600, token_type="access"),
    )
    token = generate_token(token_data=token_data)
    assert token is not None
    assert token != ""


@pytest.mark.asyncio
async def test_decode_token(test_app, db_session, user_fixture):
    _, _, pydiator = test_app
    user = user_fixture
    user = await db_session.scalar(
        select(UserSQL).where(UserSQL.email == user_fixture.email)
    )
    jti = uuid4().hex
    token_data = cast(
        dict,
        generate_token_data(user=user, jti=jti, live_time=3600, token_type="access"),
    )
    token = generate_token(token_data=token_data)
    decode_token_data = decode_token(token=token)
    assert decode_token_data is not None
    assert decode_token_data.get("user_id") == token_data.get("user_id")
    assert decode_token_data.get("email") == token_data.get("email")


@pytest.mark.asyncio
async def test_decode_token_wrong_token(test_app):
    _, _, pydiator = test_app
    decode_token_data = decode_token(token="wrong")
    assert decode_token_data is None
