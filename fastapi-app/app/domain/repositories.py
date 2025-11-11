from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Optional

from .models import Todo


class TodoRepository(ABC):
    """Repository abstraction for working with Todo aggregates."""

    @abstractmethod
    def list(self) -> Iterable[Todo]:
        raise NotImplementedError

    @abstractmethod
    def get(self, todo_id: int) -> Optional[Todo]:
        raise NotImplementedError

    @abstractmethod
    def add(self, todo: Todo) -> Todo:
        raise NotImplementedError

    @abstractmethod
    def update(self, todo: Todo) -> Todo:
        raise NotImplementedError

    @abstractmethod
    def remove(self, todo_id: int) -> None:
        raise NotImplementedError
