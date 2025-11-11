from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .dependencies import get_todo_service
from .schemas import TodoCreate, TodoRead, TodoUpdate
from ..domain.services import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoRead])
def list_todos(service: TodoService = Depends(get_todo_service)) -> list[TodoRead]:
    return [TodoRead.from_domain(todo) for todo in service.list_todos()]


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int, service: TodoService = Depends(get_todo_service)
) -> TodoRead:
    todo = service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoRead.from_domain(todo)


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: TodoCreate, service: TodoService = Depends(get_todo_service)
) -> TodoRead:
    try:
        todo = service.create_todo(payload.title, payload.description, payload.date)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return TodoRead.from_domain(todo)


@router.put("/{todo_id}", response_model=TodoRead)
def replace_todo(
    todo_id: int,
    payload: TodoCreate,
    service: TodoService = Depends(get_todo_service),
) -> TodoRead:
    try:
        todo = service.update_todo(
            todo_id,
            title=payload.title,
            description=payload.description,
            date=payload.date if hasattr(payload, 'date') else None,
        )
    except LookupError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return TodoRead.from_domain(todo)


@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    service: TodoService = Depends(get_todo_service),
) -> TodoRead:
    if not payload.has_changes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes supplied",
        )
    try:
        todo = service.update_todo(
            todo_id,
            title=payload.title,
            description=payload.description,
            completed=payload.completed,
            date=payload.date,
        )
    except LookupError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return TodoRead.from_domain(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)) -> Response:
    try:
        service.delete_todo(todo_id)
    except LookupError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
