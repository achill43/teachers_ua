from typing import cast

import pytest
from fastapi import HTTPException
from use_cases.users.refresh_token import RefreshTokenRequest, RefreshTokenResponse
from use_cases.users.user_login import UserLoginRequest, UserLoginResponse


@pytest.mark.asyncio
async def test_user_succes_login(test_app, user_fixture):
    _, _, pydiator = test_app
    user = user_fixture
    responce = cast(
        UserLoginResponse,
        await pydiator.send(
            req=UserLoginRequest(
                email=str(user.email),
                password="String1234",
            )
        ),
    )
    assert responce.user.email == user_fixture.email


@pytest.mark.asyncio
async def test_user_wrong_email(test_app, user_fixture):
    _, _, pydiator = test_app
    is_error = False
    try:
        await pydiator.send(
            req=UserLoginRequest(
                email="test+2@gmail.com",
                password="String1234",
            )
        )
    except HTTPException:
        is_error = True
    assert is_error is True


@pytest.mark.asyncio
async def test_user_wrong_password(test_app, user_fixture):
    _, _, pydiator = test_app
    user = user_fixture
    is_error = False
    try:
        await pydiator.send(
            req=UserLoginRequest(
                email=str(user.email),
                password="String",
            )
        )
    except HTTPException:
        is_error = True
    assert is_error is True


@pytest.mark.asyncio
async def test_user_refresh_token_succes(test_app, user_fixture):
    _, _, pydiator = test_app
    user = user_fixture
    responce = cast(
        UserLoginResponse,
        await pydiator.send(
            req=UserLoginRequest(
                email=str(user.email),
                password="String1234",
            )
        ),
    )
    responce_token = cast(
        RefreshTokenResponse,
        await pydiator.send(
            req=RefreshTokenRequest(refresh_token=responce.session.refresh_token)
        ),
    )
    assert responce.user.email == user.email
    assert responce_token.session.access_token is not None
    assert responce_token.session.refresh_token == responce.session.refresh_token


@pytest.mark.asyncio
async def test_user_refresh_token_wrong(test_app):
    _, _, pydiator = test_app
    is_validate_error = False
    try:
        await pydiator.send(req=RefreshTokenRequest(refresh_token="wrong_token"))
    except HTTPException:
        is_validate_error = True
    assert is_validate_error is not None
