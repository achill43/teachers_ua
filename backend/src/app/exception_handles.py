import traceback
from typing import List, Optional, Tuple, TypedDict, Union

from app.exceptions import EntityAlreadyExistsException, ErrorInfoModel, ValidationError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

Loc = Tuple[Union[int, str], ...]


class ValidationErrorDict(TypedDict):
    loc: Loc | None
    msg: str | None
    type: str | None


class ErrorInfoContainer:
    # General errors
    unhandled_error = ErrorInfoModel(code=1, message="Internal server error")
    could_not_get_excepted_response = ErrorInfoModel(
        code=2, message="Could not get expected response"
    )
    model_validation_error = ErrorInfoModel(code=3, message="Model validation error")
    not_found_error = ErrorInfoModel(code=4, message="Not found")


class ErrorResponseModel(BaseModel):
    error_code: int | None = None
    error_message: str | None = None
    error_detail: list | None = None
    validation_errors: list[ValidationErrorDict] | None = None


class ExceptionHandlers:
    @staticmethod
    def __get_error_content(
        error_info: ErrorInfoModel, error_detail: Optional[List] = None
    ):
        return jsonable_encoder(
            ErrorResponseModel(
                error_code=error_info.code,
                error_message=error_info.message,
                error_detail=error_detail,
                validation_errors=None,
            ).dict()
        )

    @staticmethod
    def __get_stack_trace(exc: Exception) -> str:
        return "".join(traceback.TracebackException.from_exception(exc).format())

    @staticmethod
    def unhandled_exception(_, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ExceptionHandlers.__get_error_content(
                error_info=ErrorInfoContainer.unhandled_error,
                error_detail=[ExceptionHandlers.__get_stack_trace(exc)],
            ),
        )

    @staticmethod
    def internal_validation_exception(_, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ExceptionHandlers.__get_error_content(error_info=exc.error_info),
        )

    @staticmethod
    def already_exists(_, exc: EntityAlreadyExistsException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ExceptionHandlers.__get_error_content(error_info=exc.error_info),
        )
