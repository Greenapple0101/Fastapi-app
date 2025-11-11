# EC2에서 Promtail 설정 가이드

## 🔧 Promtail 디렉토리 생성 (한 번만 실행)

```bash
# Promtail 컨테이너로 들어가서 디렉토리 생성
docker run -it --rm \
  --name promtail-init \
  grafana/promtail:2.9.1 \
  sh

# 컨테이너 안에서 실행:
mkdir -p /etc/promtail
exit
```

## 🚀 Promtail 실행 (수동 실행 시)

```bash
# 기존 Promtail 컨테이너 제거
docker rm -f promtail || true

# Promtail 실행
docker run -d \
  --name promtail \
  --network monitor-net \
  -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
  -v ~/FastApi_Todos/monitoring/promtail-config.yml:/etc/promtail/config.yml \
  grafana/promtail:2.9.1 \
  -config.file=/etc/promtail/config.yml
```

## ✅ Promtail 로그 확인

```bash
docker logs promtail --tail 20
```

**정상 로그 예시:**
```
level=info ... server listening
level=info ... client is healthy
```

## 🎯 docker-compose 사용 (권장)

```bash
cd ~/FastApi_Todos
git pull origin main
docker-compose down
docker-compose up -d
```

## 📊 Grafana에서 로그 확인

1. Grafana 접속: http://3.34.155.126:3000 (admin/admin)
2. Explore → Data source: **Loki** 선택
3. Query 입력: `{container="fastapi-app"}`
4. 로그가 나오면 성공! 🎉

