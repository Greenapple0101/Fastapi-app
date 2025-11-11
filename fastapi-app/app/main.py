from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .api.routes import router as todo_router

BASE_DIR = Path(__file__).resolve().parent
# Docker 컨테이너 내 경로: /app/fastapi-app/app -> /app/fastapi-app -> /app
# 로컬 개발: fastapi-app/app -> fastapi-app -> 프로젝트 루트
PROJECT_ROOT = BASE_DIR.parent.parent
STATIC_DIR = PROJECT_ROOT / "static"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Docker 컨테이너 내에서 실행 시 경로 확인
# WORKDIR이 /app/fastapi-app이므로 static은 /app/static에 있음
# 하지만 PROJECT_ROOT는 /app이 되어야 함
if not STATIC_DIR.exists():
    # Docker 컨테이너 내 경로 재시도
    STATIC_DIR = Path("/app/static")
if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR = Path("/app/templates")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):  # type: ignore[override]
        response: Response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        csp = "default-src 'self'; img-src 'self' data: http: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
        response.headers.setdefault("Content-Security-Policy", csp)
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Todos", version="2.0.0")

    # Static 파일 경로 확인 및 마운트
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
        print(f"✅ Static files mounted from: {STATIC_DIR}")
    else:
        print(f"⚠️ Static directory not found at: {STATIC_DIR}")
        # 절대 경로로 재시도
        alt_static = Path("/app/static")
        if alt_static.exists():
            app.mount("/static", StaticFiles(directory=str(alt_static)), name="static")
            print(f"✅ Static files mounted from: {alt_static}")

    templates = Jinja2Templates(directory=TEMPLATES_DIR)

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

    app.include_router(todo_router)

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/health", tags=["health"])
    async def healthcheck() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    return app


app = create_app()
