from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..domain.models import Todo


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)  # 선택적 필드로 변경
    date: str | None = Field(None, description="날짜 (YYYY-MM-DD 형식)")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, min_length=1, max_length=2000)
    completed: bool | None = None
    date: str | None = Field(None, description="날짜 (YYYY-MM-DD 형식)")

    def has_changes(self) -> bool:
        return any(
            value is not None
            for value in (self.title, self.description, self.completed, self.date)
        )


class TodoRead(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    date: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_domain(todo: Todo) -> "TodoRead":
        return TodoRead(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            date=todo.date,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

    class Config:
        orm_mode = True
        json_encoders: dict[type[Any], Any] = {datetime: lambda dt: dt.isoformat()}
