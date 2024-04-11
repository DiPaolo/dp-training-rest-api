from __future__ import annotations

import datetime
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel, Field

from web_server import repository, domain

app = FastAPI(separate_input_output_schemas=True)


class TodoItemIn(BaseModel):
    title: str
    desc: str | None = None
    created_at: datetime.datetime | None = Field(alias='createdAt', default=None)
    due_to: datetime.datetime | None = Field(alias='dueTo', default=None)

    def to_domain(self) -> domain.TodoItem:
        return domain.TodoItem(title=self.title, desc=self.desc, created_at=self.created_at, due_to=self.due_to)


class TodoItemOut(BaseModel):
    id: UUID
    title: str
    desc: str | None = None
    created_at: datetime.datetime | None = Field(alias='createdAt', default=None)
    due_to: datetime.datetime | None = Field(alias='dueTo', default=None)

    @staticmethod
    def from_domain(item: domain.TodoItem) -> TodoItemOut:
        out = TodoItemOut(id=item.id, title=item.title, desc=item.desc)

        out.created_at = item.created_at
        out.due_to = item.due_to

        return out


@app.get("/api/todos")
def get_todo_items() -> list[TodoItemOut]:
    items = repository.get_todo_items()
    return [TodoItemOut.from_domain(i) for i in items]


@app.post("/api/todos")
def add_todo_item(item: TodoItemIn) -> TodoItemOut:
    if item.created_at is None:
        item.created_at = datetime.datetime.utcnow()

    out_domain_item = repository.add_todo_item(item.to_domain())
    fff = TodoItemOut.from_domain(out_domain_item)
    return fff