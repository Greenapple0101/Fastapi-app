# EC2 배포 가이드

## 🚀 EC2에서 서비스 실행하기

### 1단계: 기존 컨테이너 정리

```bash
cd ~/FastApi_Todos

# 모든 컨테이너 중지 및 제거
docker compose down

# 혹시 남아있는 컨테이너가 있다면 강제 제거
docker rm -f prometheus loki grafana promtail node-exporter cadvisor fastapi-app 2>/dev/null || true
```

### 2단계: 최신 코드 가져오기

```bash
git pull origin main
```

### 3단계: 서비스 실행

```bash
# 모든 서비스 실행 (loki, prometheus 포함)
docker compose up -d
```

### 4단계: 컨테이너 상태 확인

```bash
# 모든 컨테이너 상태 확인
docker compose ps

# 또는
docker ps
```

**정상 상태 예시:**
```
NAME            STATUS
prometheus      Up
loki            Up
grafana         Up
promtail        Up
node-exporter   Up
cadvisor        Up
fastapi-app     Up
```

### 5단계: 로그 확인

```bash
# Prometheus 로그
docker logs prometheus --tail 20

# Loki 로그
docker logs loki --tail 20

# Grafana 로그
docker logs grafana --tail 20

# Promtail 로그
docker logs promtail --tail 20
```

---

## 🔍 문제 해결

### Loki/Prometheus가 보이지 않을 때

```bash
# 1. 모든 컨테이너 확인
docker ps -a

# 2. 특정 컨테이너 확인
docker ps | grep -E "loki|prometheus"

# 3. 컨테이너가 없다면 다시 실행
docker compose up -d loki prometheus

# 4. 로그 확인
docker logs loki
docker logs prometheus
```

### 컨테이너 이름 충돌 에러

```bash
# 기존 컨테이너 모두 제거
docker compose down
docker rm -f $(docker ps -aq) 2>/dev/null || true

# 네트워크도 정리 (필요시)
docker network prune -f

# 다시 실행
docker compose up -d
```

---

## 📊 서비스 접속 확인

### Prometheus
```bash
# 브라우저에서 접속
http://3.34.155.126:7070

# 또는 curl로 확인
curl http://localhost:7070/-/healthy
```

### Loki
```bash
# 브라우저에서 접속
http://3.34.155.126:3100/ready

# 또는 curl로 확인
curl http://localhost:3100/ready
```

### Grafana
```bash
# 브라우저에서 접속
http://3.34.155.126:3000
# 로그인: admin / admin
```

---

## ✅ 전체 체크리스트

```bash
# 1. 컨테이너 상태
docker compose ps

# 2. 네트워크 확인
docker network ls | grep monitoring

# 3. Prometheus 타겟 확인
curl http://localhost:7070/api/v1/targets

# 4. Loki 헬스체크
curl http://localhost:3100/ready

# 5. Grafana 접속
curl http://localhost:3000/api/health
```

---

## 🎯 빠른 재시작

```bash
cd ~/FastApi_Todos
docker compose down
docker compose up -d
docker compose ps
```

