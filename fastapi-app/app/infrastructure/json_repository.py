from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Iterable, Optional

from ..domain.models import Todo
from ..domain.repositories import TodoRepository


class JsonTodoRepository(TodoRepository):
    def __init__(self, storage_path: str | Path) -> None:
        self._path = Path(storage_path)
        self._lock = Lock()
        self._ensure_file()

    def list(self) -> Iterable[Todo]:
        with self._lock:
            return [Todo.from_dict(item) for item in self._read_items()]

    def get(self, todo_id: int) -> Optional[Todo]:
        with self._lock:
            for stored in self._read_items():
                if int(stored["id"]) == todo_id:
                    return Todo.from_dict(stored)
        return None

    def add(self, todo: Todo) -> Todo:
        with self._lock:
            items = self._read_items()
            items.append(todo.to_dict())
            self._write_items(items)
        return todo

    def update(self, todo: Todo) -> Todo:
        with self._lock:
            items = self._read_items()
            for index, stored in enumerate(items):
                if int(stored["id"]) == todo.id:
                    items[index] = todo.to_dict()
                    self._write_items(items)
                    return todo
        raise LookupError(f"Todo {todo.id} not found")

    def remove(self, todo_id: int) -> None:
        with self._lock:
            items = self._read_items()
            filtered = [item for item in items if int(item["id"]) != todo_id]
            self._write_items(filtered)

    # Internal helpers -------------------------------------------------

    def _ensure_file(self) -> None:
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._write_items([])

    def _read_items(self) -> list[dict]:
        if not self._path.exists():
            return []
        if self._path.stat().st_size == 0:
            return []
        with self._path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_items(self, items: list[dict]) -> None:
        tmp_path = self._path.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(items, handle, indent=2, ensure_ascii=False)
        tmp_path.replace(self._path)
