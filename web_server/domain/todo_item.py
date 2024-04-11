from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass
from typing import Dict
from uuid import UUID


@dataclass
class TodoItem:
    id: UUID
    title: str
    desc: str
    created_at: datetime.datetime
    due_to: datetime.datetime

    def __init__(self, title: str, desc: str = None, created_at: datetime.datetime = None,
                 due_to: datetime.datetime = None):
        self.id = uuid.uuid4()
        self.title = title
        self.desc = desc
        self.created_at = created_at
        self.due_to = due_to

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'createdAt': self.created_at,
            'dueTo': self.due_to
        }

    @staticmethod
    def from_dict(data: Dict) -> TodoItem:
        item = TodoItem(
            title=data['title'],
            desc=data['desc'],
            created_at=data['createdAt'],
            due_to=data['dueTo']
        )

        item.id = data['id']
        return item
