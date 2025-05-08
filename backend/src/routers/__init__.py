from routers.users_router import users_router


def include_routes(app):
    app.include_router(users_router)
