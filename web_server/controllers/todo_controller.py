from __future__ import annotations

import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from web_server import repository, domain

router = APIRouter(
    prefix="/api/todos",
    tags=["todos"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class TodoItemIn(BaseModel):
    title: str = Field(min_length=1)
    desc: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    created_at: datetime.datetime | None = Field(alias='createdAt', default=None)
    due_to: datetime.datetime | None = Field(alias='dueTo', default=None)

    def to_domain(self) -> domain.TodoItem:
        return domain.TodoItem(title=self.title, priority=self.priority, desc=self.desc, created_at=self.created_at,
                               due_to=self.due_to)


class TodoItemInUpdate(BaseModel):
    title: str | None = Field(min_length=1)
    desc: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    created_at: datetime.datetime | None = Field(alias='createdAt', default=None)
    due_to: datetime.datetime | None = Field(alias='dueTo', default=None)

    def to_domain(self) -> domain.TodoItem:
        return domain.TodoItem(title=self.title, desc=self.desc, created_at=self.created_at, due_to=self.due_to)


class TodoItemOut(BaseModel):
    id: UUID
    title: str
    desc: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    created_at: datetime.datetime | None = Field(alias='createdAt', default=None)
    due_to: datetime.datetime | None = Field(alias='dueTo', default=None)

    @staticmethod
    def from_domain(item: domain.TodoItem) -> TodoItemOut:
        out = TodoItemOut(id=item.id, title=item.title, priority=item.priority, desc=item.desc)

        out.created_at = item.created_at
        out.due_to = item.due_to

        return out


@router.get("")
def get_todo_items() -> list[TodoItemOut]:
    items = repository.get_todo_items()
    return [TodoItemOut.from_domain(i) for i in items]


@router.get("/{item_id}")
def get_todo_item(item_id: UUID) -> Optional[TodoItemOut]:
    item = repository.get_item_by_id(item_id)
    if item is None:
        return None

    return TodoItemOut.from_domain(item)


@router.post("", status_code=status.HTTP_201_CREATED)
def add_todo_item(item: TodoItemIn) -> Optional[TodoItemOut]:
    if item.created_at is None:
        item.created_at = datetime.datetime.utcnow()

    out_domain_item = repository.add_todo_item(item.to_domain())
    return TodoItemOut.from_domain(out_domain_item)


@router.put("/{item_id}")
def update_todo_item(item_id: UUID, item_in: TodoItemInUpdate) -> Optional[TodoItemOut]:
    item = repository.update_todo_item(item_id, item_in.to_domain())
    return TodoItemOut.from_domain(item)


@router.delete("/{item_id}")
def delete_todo_item(item_id: UUID) -> Optional[TodoItemOut]:
    item = repository.delete_item(item_id)
    if item is None:
        return None

    return TodoItemOut.from_domain(item)
