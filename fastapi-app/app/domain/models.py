from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Todo:
    """Aggregate root representing a single to-do item."""

    id: int
    title: str
    description: str
    completed: bool = False
    date: str | None = None  # 날짜 필드 추가 (YYYY-MM-DD 형식)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def rename(self, title: str, description: str) -> None:
        title = title.strip()
        description = description.strip()
        if not title:
            raise ValueError("Title must not be empty")
        if not description:
            raise ValueError("Description must not be empty")
        self.title = title
        self.description = description
        self.touch()

    def mark_complete(self) -> None:
        self.completed = True
        self.touch()

    def mark_incomplete(self) -> None:
        self.completed = False
        self.touch()

    def apply_completion(self, completed: bool) -> None:
        self.completed = bool(completed)
        self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "date": self.date,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(payload: dict) -> "Todo":
        return Todo(
            id=int(payload["id"]),
            title=str(payload["title"]),
            description=str(payload["description"]),
            completed=bool(payload.get("completed", False)),
            date=payload.get("date"),
            created_at=datetime.fromisoformat(payload.get("created_at"))
            if payload.get("created_at")
            else datetime.utcnow(),
            updated_at=datetime.fromisoformat(payload.get("updated_at"))
            if payload.get("updated_at")
            else datetime.utcnow(),
        )
