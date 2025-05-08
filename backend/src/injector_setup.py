from fastapi import FastAPI
from injector import Injector
from module import CoreModule, configure_for_production


def injector_setup(app: FastAPI):
    injector = Injector(
        [
            configure_for_production,
            CoreModule,
        ]
    )
    return injector
