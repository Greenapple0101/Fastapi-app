FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . .

# FastAPI 실행 (main.py 안에 app이 존재할 때)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
