from typing import TypedDict


class RequestUserDataDict(TypedDict):
    user_id: int
    user_email: str


class RequestEmbeddableDataDict(TypedDict):
    register_ids: list[int]


class RequestContextValuesDict(TypedDict):
    user: RequestUserDataDict | None


class RequestContextProvider:
    def __init__(self):
        self._values = RequestContextValuesDict(user=None)

    def set_user(self, user: RequestUserDataDict):
        self._values["user"] = user

    def get_user(self) -> RequestUserDataDict:
        if not self._values["user"]:
            # Potentially breaks all celery tasks
            raise Exception("User is not set in request context")
        return self._values["user"]
