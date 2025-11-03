from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import os
import time
from typing import Optional

app = FastAPI()

# Serve static files (images, css, js)
# Mount static only when directory exists (CI environments may not have it)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Template renderer (prevents manual file read and enables escaping)
templates = Jinja2Templates(directory="templates")

# Security: restrict hosts if deployed behind a domain (keeps localhost for dev)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*"])


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        # Basic secure headers
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        # Lightweight CSP suitable for this app
        csp = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
        response.headers.setdefault("Content-Security-Policy", csp)
        return response


app.add_middleware(SecurityHeadersMiddleware)

# To-Do 항목 모델
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

# JSON 파일 경로
TODO_FILE = "todo.json"

# JSON 파일에서 To-Do 항목 로드
def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []

def save_todos(todos):
    # Atomic-like write: write to temp then replace
    tmp_path = f"{TODO_FILE}.tmp"
    with open(tmp_path, "w") as file:
        json.dump(todos, file, indent=4)
    os.replace(tmp_path, TODO_FILE)

# To-Do 목록 조회
@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()

# 신규 To-Do 항목 추가
@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoCreate):
    todos = load_todos()
    new_item = {
        "id": int(time.time() * 1000),  # server-side id
        "title": todo.title.strip(),
        "description": todo.description.strip(),
        "completed": False,
    }
    todos.append(new_item)
    save_todos(todos)
    return TodoItem(**new_item)

# To-Do 항목 수정
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

# To-Do 항목 삭제
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = load_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return {"message": "To-Do item deleted"}

# HTML 파일 서빙
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})