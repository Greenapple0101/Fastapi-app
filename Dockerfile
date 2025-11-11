# Python 3.9 베이스 이미지 사용
FROM python:3.9

# 애플리케이션 루트 디렉터리
WORKDIR /app

# 의존성 파일만 먼저 복사하여 캐시 활용
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 애플리케이션 파일 복사
COPY fastapi-app ./fastapi-app
COPY templates ./templates
COPY tests ./tests
COPY prometheus ./prometheus
COPY docker-compose.yml .
COPY sonar-project.properties .

# FastAPI 애플리케이션 코드가 위치한 디렉터리로 이동
WORKDIR /app/fastapi-app

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]

