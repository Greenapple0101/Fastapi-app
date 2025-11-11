from __future__ import annotations

import time
from typing import Callable, Iterable, Optional

from .models import Todo
from .repositories import TodoRepository


class TodoService:
    """Application service that encapsulates to-do operations."""

    def __init__(
        self,
        repository: TodoRepository,
        id_provider: Callable[[], int] | None = None,
    ) -> None:
        self._repository = repository
        self._id_provider = id_provider or (lambda: time.time_ns())

    def list_todos(self) -> Iterable[Todo]:
        return self._repository.list()

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self._repository.get(todo_id)

    def create_todo(self, title: str, description: str) -> Todo:
        title = title.strip()
        description = description.strip()
        if not title:
            raise ValueError("Title must not be empty")
        if not description:
            raise ValueError("Description must not be empty")
        todo = Todo(id=self._id_provider(), title=title, description=description)
        return self._repository.add(todo)

    def update_todo(
        self,
        todo_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        completed: bool | None = None,
    ) -> Todo:
        todo = self._require(todo_id)
        if title is not None or description is not None:
            todo.rename(
                title if title is not None else todo.title,
                description if description is not None else todo.description,
            )
        if completed is not None:
            todo.apply_completion(completed)
        return self._repository.update(todo)

    def delete_todo(self, todo_id: int) -> None:
        self._require(todo_id)
        self._repository.remove(todo_id)

    def _require(self, todo_id: int) -> Todo:
        todo = self._repository.get(todo_id)
        if todo is None:
            raise LookupError(f"Todo {todo_id} not found")
        return todo
