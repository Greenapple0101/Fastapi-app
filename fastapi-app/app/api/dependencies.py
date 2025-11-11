from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from ..domain.services import TodoService
from ..infrastructure.json_repository import JsonTodoRepository

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR.parent / "todo.json"


@lru_cache(maxsize=1)
def get_repository() -> JsonTodoRepository:
    return JsonTodoRepository(DATA_PATH)


def get_todo_service() -> TodoService:
    repository = get_repository()
    return TodoService(repository)
