# 포트 정보

## 🚀 서비스 포트 목록

| 서비스 | 설명 | 포트 | 접속 URL |
|--------|------|------|----------|
| **fastapi-app** | FastAPI 백엔드 애플리케이션 | `5001:5001` | http://localhost:5001 |
| **prometheus** | 메트릭 수집 및 저장 | `7070:9090` | http://localhost:7070 |
| **grafana** | 대시보드 시각화 | `3000:3000` | http://localhost:3000 |
| **loki** | 로그 수집 시스템 | `3100:3100` | http://localhost:3100 |
| **promtail** | 로그 수집 에이전트 | 내부 전용 | - |
| **node-exporter** | 시스템 메트릭 수집 | `7100:9100` | http://localhost:7100 |
| **cadvisor** | 컨테이너 메트릭 수집 | `8081:8080` | http://localhost:8081 |
| **sonarqube** | 코드 품질 분석 | `9000:9000` | http://localhost:9000 |

## 📊 모니터링 스택

### 메트릭 수집
- **Prometheus**: http://localhost:7070
  - FastAPI 메트릭: `fastapi-app:5001/metrics`
  - Node Exporter: `node-exporter:9100`
  - cAdvisor: `cadvisor:8080`

### 로그 수집
- **Loki**: http://localhost:3100
  - Promtail이 로그를 수집하여 Loki로 전송

### 시각화
- **Grafana**: http://localhost:3000
  - 기본 로그인: `admin` / `admin`
  - 데이터 소스:
    - Prometheus: `http://prometheus:9090`
    - Loki: `http://loki:3100`

## 🔍 주요 엔드포인트

### FastAPI
- 메인 페이지: http://localhost:5001/
- API 문서: http://localhost:5001/docs
- Health Check: http://localhost:5001/health
- Prometheus 메트릭: http://localhost:5001/metrics

### Prometheus
- 메인 UI: http://localhost:7070
- 타겟 상태: http://localhost:7070/targets
- 쿼리: http://localhost:7070/graph

### Grafana
- 대시보드: http://localhost:3000
- 데이터 소스 설정: http://localhost:3000/connections/datasources

### cAdvisor
- 컨테이너 메트릭: http://localhost:8081

### SonarQube
- 코드 분석: http://localhost:9000
- 기본 로그인: `admin` / `admin`

## 🌐 원격 서버 (EC2)

EC2 서버에서 실행 시:
- FastAPI: http://3.34.155.126:5001
- Prometheus: http://3.34.155.126:7070
- Grafana: http://3.34.155.126:3000
- Loki: http://3.34.155.126:3100

