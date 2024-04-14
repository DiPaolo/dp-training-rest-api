from fastapi import FastAPI

from web_server import config
from web_server.controllers import todo_controller, version_controller

app = FastAPI(
    title='WTF title',
    description='desssscrrrrr',
    version=f'{config.VERSION_MAJOR}.{config.VERSION_MINOR}.{config.VERSION_PATCH}.{config.VERSION_BUILD}',
)
app.include_router(version_controller.router)
app.include_router(todo_controller.router)


# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     # dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
