from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from web_server import config

router = APIRouter(
    prefix="/api/version",
    tags=["version"],
    responses={404: {"description": "Not found"}},
)


class VersionOut(BaseModel):
    major: int
    minor: int
    patch: int
    build: int


@router.get("")
def get_todo_items() -> VersionOut:
    return VersionOut(
        major=config.VERSION_MAJOR,
        minor=config.VERSION_MINOR,
        patch=config.VERSION_PATCH,
        build=config.VERSION_BUILD
    )
