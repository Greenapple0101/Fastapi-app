from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import json
import os
import time
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(ROOT_DIR, "templates")
TODO_FILE = os.path.join(BASE_DIR, "todo.json")

app = FastAPI()

# 정적 파일 제공
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory=TEMPLATE_DIR)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        csp = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
        response.headers.setdefault("Content-Security-Policy", csp)
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*"])

# Prometheus 메트릭스 엔드포인트 (/metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []


def save_todos(todos):
    tmp_path = f"{TODO_FILE}.tmp"
    with open(tmp_path, "w") as file:
        json.dump(todos, file, indent=4, ensure_ascii=False)
    os.replace(tmp_path, TODO_FILE)


@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()


@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoCreate):
    todos = load_todos()
    new_item = {
        "id": int(time.time() * 1000),
        "title": todo.title.strip(),
        "description": todo.description.strip(),
        "completed": False,
    }
    todos.append(new_item)
    save_todos(todos)
    return TodoItem(**new_item)


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            if updated_todo.title is not None:
                todo["title"] = updated_todo.title.strip()
            if updated_todo.description is not None:
                todo["description"] = updated_todo.description.strip()
            if updated_todo.completed is not None:
                todo["completed"] = bool(updated_todo.completed)
            save_todos(todos)
            return TodoItem(**todo)
    raise HTTPException(status_code=404, detail="To-Do item not found")


@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = load_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return {"message": "To-Do item deleted"}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})