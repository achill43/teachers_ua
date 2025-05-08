class ErrorInfoModel:
    VALIDATION_ERROR_CODE = 1
    ALREADY_EXISTS = 2

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self):
        return f"code:{self.code},message:{self.message}"


class BaseException(Exception):
    def __init__(
        self, error_info: ErrorInfoModel, exception: Exception | None = None
    ) -> None:
        super().__init__()
        self.exception = exception
        self.error_info = error_info


class ValidationError(BaseException):
    def __init__(self, message: str, exception: Exception | None = None) -> None:
        super().__init__(
            ErrorInfoModel(ErrorInfoModel.VALIDATION_ERROR_CODE, message), exception
        )


class EntityAlreadyExistsException(BaseException):
    def __init__(
        self, message: str = "Entity already exists", exception: Exception | None = None
    ) -> None:
        super().__init__(
            ErrorInfoModel(ErrorInfoModel.ALREADY_EXISTS, message), exception
        )
