# 로그 수집 가이드 (Promtail 없이도 가능)

## 📋 Promtail 없이 로그 수집하는 방법

### 방법 1: Promtail 사용 (현재 설정)

```bash
# Promtail 포함하여 실행
docker compose --profile with-promtail up -d
```

**장점:**
- 시스템 로그 (`/var/log/*.log`) 수집 가능
- Docker 컨테이너 로그 자동 수집
- 파일 기반 로그 수집 가능

---

### 방법 2: Promtail 없이 사용

```bash
# Promtail 없이 실행
docker compose up -d
```

**Promtail 없이도 로그를 볼 수 있는 방법:**

#### 1. Docker 컨테이너 로그 직접 확인

```bash
# FastAPI 앱 로그
docker logs fastapi-app --tail 100 -f

# 모든 컨테이너 로그
docker compose logs -f
```

#### 2. Grafana에서 직접 로그 쿼리 (Promtail 없이)

Promtail 없이도 Loki는 작동하지만, **로그를 수동으로 보내야 합니다.**

**Loki API로 직접 로그 전송:**

```bash
# curl로 로그 전송 예시
curl -X POST http://localhost:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [{
      "stream": {"job": "manual", "container": "fastapi-app"},
      "values": [["'$(date +%s)000000000'", "테스트 로그 메시지"]]
    }]
  }'
```

#### 3. 애플리케이션에서 직접 Loki로 로그 전송

FastAPI 앱에서 Python으로 직접 Loki에 로그를 보낼 수 있습니다:

```python
import requests
import time

def send_log_to_loki(message, level="info"):
    url = "http://loki:3100/loki/api/v1/push"
    timestamp = str(int(time.time() * 1000000000))
    
    payload = {
        "streams": [{
            "stream": {
                "job": "fastapi-app",
                "level": level,
                "container": "fastapi-app"
            },
            "values": [[timestamp, message]]
        }]
    }
    
    requests.post(url, json=payload)
```

---

## 🎯 권장 방법

### Promtail 사용 (권장)
- **장점**: 자동 로그 수집, 파일 로그 지원, 설정 간단
- **단점**: 추가 컨테이너 필요

### Promtail 없이 사용
- **장점**: 리소스 절약, 간단한 구성
- **단점**: 수동 로그 전송 필요, 파일 로그 수집 어려움

---

## 🔧 Promtail 제거하고 실행하기

```bash
# 1. Promtail 제거
docker compose rm -f promtail

# 2. 나머지 서비스만 실행
docker compose up -d

# 3. 로그 확인 (Docker 로그 직접)
docker logs fastapi-app -f
```

---

## 📊 Grafana에서 로그 보기

### Promtail 있을 때:
```
Query: {job="containerlogs"}
Query: {job="varlogs"}
```

### Promtail 없을 때:
- 수동으로 전송한 로그만 표시됨
- 또는 Docker 로그를 직접 확인

---

## 💡 결론

**Promtail은 선택 사항입니다!**

- **필요하면**: `docker compose --profile with-promtail up -d`
- **불필요하면**: `docker compose up -d` (Promtail 제외)

현재 설정은 Promtail을 선택적으로 사용할 수 있도록 `profiles`로 설정되어 있습니다.

