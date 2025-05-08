from inspect import signature
from typing import Any, Type

from injector import Injector
from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import BaseHandler, MediatrContainer


def setup_pydiator(injector: Injector):
    mediatr_container = MediatrContainer()

    class RequestHandlerInjectionDecorator(BaseHandler):
        """Adds Injector DI resolution to request handlers."""

        def __init__(self, wrapped: Type[BaseHandler]):
            self.wrapped = wrapped

        async def handle(self, req: Any) -> Any:
            handler: BaseHandler = injector.get(self.wrapped)
            return await handler.handle(req)

    # Get all descendants from BaseHandler and register them
    base_handler_subclasses = BaseHandler.__subclasses__()
    for subclass in base_handler_subclasses:
        if subclass == RequestHandlerInjectionDecorator:
            continue
        request_param = list(signature(subclass.handle).parameters.values())[1]
        mediatr_container.register_request(
            request_param.annotation, RequestHandlerInjectionDecorator(subclass)
        )

    # Start
    pydiator.is_ready = False
    pydiator.ready(container=mediatr_container)
    return pydiator
