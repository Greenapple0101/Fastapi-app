# FastAPI Todos
![Uploading image.png…]()


FastAPI 기반의 투두 애플리케이션입니다. 도메인 주도 설계(DDD) 스타일로 백엔드를 재구성하고, Prometheus + Grafana + cAdvisor + Node Exporter + SonarQube 까지 포함한 운영 스택을 한 번에 배포할 수 있도록 정리했습니다.

## 1. 아키텍처 개요
- **FastAPI 애플리케이션 (`fastapi-app`)**
  - 도메인 계층: `app/domain`
    - `models.py`: Todo 애그리게이트, 유효성 및 상태 전환 로직
    - `repositories.py`: Repository 추상화
    - `services.py`: 애플리케이션 서비스 (생성/조회/수정/삭제)
  - 인프라 계층: `app/infrastructure`
    - `json_repository.py`: JSON 파일 기반 저장소 어댑터 (원자적 쓰기)
  - API 계층: `app/api`
    - `schemas.py`: Pydantic DTO (Create/Update/Read)
    - `routes.py`: RESTful 엔드포인트 (GET/POST/PUT/PATCH/DELETE)
    - `dependencies.py`: DI 컨테이너 및 서비스 공급자
  - 진입점: `app/main.py` → 보안 헤더, TrustedHost, 정적 자원, Prometheus metric(`/metrics`), `create_app()` 팩토리 제공
  - 레거시 호환: 루트 `main.py`는 `app.main.app`을 재노출하여 기존 실행 스크립트 유지
- **프론트엔드 (`templates/index.html`)**
  - REST API 구조에 맞게 `POST(201)`, `PATCH`, `DELETE` 호출
  - 체크박스 토글 시 `PATCH /todos/{id}`로 상태 갱신
- **테스트 (`tests/test_main.py`)**
  - 의존성 주입 오버라이드로 JSON 저장소를 임시 경로에 생성
  - CRUD + 패치 예외 흐름까지 검증

## 2. 배포 스택 구성
`docker-compose.yml` 한 번으로 다음 서비스를 띄울 수 있습니다.

| 서비스 | 설명 | 주요 포트 |
| --- | --- | --- |
| `fastapi-app` | FastAPI 백엔드 + 정적 자원 + Prometheus metrics | `5001` |
| `prometheus` | 메트릭 수집( FastAPI / node-exporter / cAdvisor ) | `7070 -> 9090` |
| `grafana` | 대시보드 시각화, 기본 비밀번호 `admin / admin` | `3000` |
| `cadvisor` | 컨테이너별 자원(CPU, Memory, Disk, Network) 수집 | `8081 -> 8080` |
| `node-exporter` | 호스트 OS 자원 지표 | `7100 -> 9100` |
| `sonarqube` | 정적 분석 및 품질 게이트 | `9000` |

### Prometheus 타깃 설정 (`prometheus/prometheus.yml`)
- `fastapi`: `fastapi-app:5001`
- `node`: `node-exporter:9100`
- `cadvisor`: `cadvisor:8080`

### Grafana 대시보드
- `ID 193` (Docker Monitoring by cAdvisor + Prometheus) → 컨테이너별 자원 현황
- `ID 179` (Node Exporter Full) → 시스템 수준 메트릭

## 3. 실행 절차
```bash
git clone https://github.com/Greenapple0101/FastApi_Todos.git
cd FastApi_Todos

docker compose down            # 기존 컨테이너가 있다면 정리
docker compose up -d --build
```

> 새 구조 반영을 위해 컨테이너 이름 변경 후에는 반드시 `docker compose down` → `up` 순으로 재생성해야 합니다.

### 배포 후 확인 체크리스트
1. `docker compose ps` → 모든 컨테이너 `Up` 상태
2. `http://<호스트>:5001/` → 투두 UI / API 동작
3. `http://<호스트>:5001/metrics` → Prometheus 포맷 지표
4. `http://<호스트>:7070/targets` → `fastapi`, `node`, `cadvisor` 상태가 `UP`
5. `http://<호스트>:3000/` → Grafana 로그인 후 대시보드 Import (ID 193, 179)
6. `http://<호스트>:8081/` → cAdvisor UI (컨테이너 리소스 실시간 확인)
7. `http://<호스트>:9000/` → SonarQube (최초 `admin/admin`, 비밀번호 변경)

## 4. 품질 및 모니터링 워크플로우
- FastAPI는 `prometheus_fastapi_instrumentator`로 요청/응답 메트릭 자동 노출
- cAdvisor + Node Exporter 조합으로 컨테이너/호스트 레벨 리소스 추적
- Grafana에 Alert Rule을 설정하면 CPU/Mem 이상 시 Slack/Webhook 연동 가능
- SonarQube `sonar-project.properties` 활용하여 CI 또는 로컬에서 정적 분석 수행
  ```bash
  sonar-scanner \
    -Dsonar.projectKey=fastapi-todos \
    -Dsonar.sources=fastapi-app \
    -Dsonar.host.url=http://<호스트>:9000 \
    -Dsonar.login=<토큰>
  ```

## 5. 로컬 개발 & 테스트
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest   # 현재 샌드박스에서는 pytest 명령이 미설치 → 로컬 환경에서 실행 필요
```
- 테스트 픽스처는 FastAPI `create_app()`을 사용하여 의존성 주입이 제대로 동작하는지 검증합니다.
- `tests/test_main.py`를 참고하면 REST 계약(201 응답, PATCH 유효성, 404 처리 등)을 빠르게 파악할 수 있습니다.

## 6. 운영 팁
- 새 코드를 배포할 때는 `docker compose down && docker compose up -d --build`
- 컨테이너 이름/포트 변경 시 Prometheus 타깃도 맞춰야 `State = UP` 유지
- Grafana 대시보드에서 `Refresh every 5s`로 설정하면 실시간 모니터링 가능
- JSON 스토리지를 다른 백엔드(예: RDB)로 교체하려면 `TodoRepository` 구현만 추가하면 됩니다.

---

### 📌 요약
- DDD 구조로 서비스/도메인/인프라 분리 → 유지보수 용이
- RESTful API (`GET/POST/PUT/PATCH/DELETE`)와 프론트엔드 동작 완전 매칭
- Prometheus + Grafana + cAdvisor + Node Exporter + SonarQube 까지 한 번에 배포
- README만 따라도 동일한 환경을 재현 가능

필요한 추가 자료나 대시보드 커스터마이징이 있으면 말씀해 주세요! :)

## 7. 릴리즈 기록
- 최신 릴리즈 및 변경 이력은 GitHub Releases 페이지에서 확인할 수 있습니다.
  - https://github.com/Greenapple0101/FastApi_Todos/releases
