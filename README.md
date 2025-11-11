# FastAPI Todos

This project hosts a FastAPI based to-do application instrumented with quality gates and observability tooling. It is containerised for local or remote deployment.

## Stack Overview
- `fastapi-app`: core CRUD API with HTML front-end (`/`), REST endpoints (`/todos`), and Prometheus metrics (`/metrics`).
- `sonarqube`: static analysis and code quality dashboard.
- `prometheus`: collects metrics from FastAPI, Node Exporter, and cAdvisor.
- `grafana`: dashboards backed by Prometheus (import dashboard ID `193` for cAdvisor views).
- `node-exporter`: host-level CPU, memory, and disk metrics.
- `cadvisor`: container-level resource metrics.

## Prerequisites
- Docker & Docker Compose
- Ports open on the host: `5001`, `7070`, `3000`, `7100`, `8080`, `9000` (and port 22 for SSH if working on a remote host).

## Quick Start
```bash
git clone https://github.com/Greenapple0101/FastApi_Todos.git
cd FastApi_Todos
docker compose down
docker compose up -d --build
```

### Services & URLs
| Service | URL | Notes |
| --- | --- | --- |
| FastAPI UI | `http://<host>:5001/` | To-do web interface |
| FastAPI metrics | `http://<host>:5001/metrics` | Prometheus scrape target |
| Prometheus | `http://<host>:7070/` | Check `Status → Targets` to ensure all jobs are `UP` |
| Grafana | `http://<host>:3000/` | Default credentials `admin / admin` |
| SonarQube | `http://<host>:9000/` | First login `admin / admin`, change password on first use |
| cAdvisor | `http://<host>:8081/` | Live container metrics |

## Grafana Dashboards
1. Log in to Grafana → `Dashboards → Import`.
2. Enter ID `193` → Load.
3. Select `prometheus` data source → Import.
4. Dashboards now show per-container CPU, memory, and network metrics gathered via cAdvisor.

## SonarQube Analysis
- Configure the token and project key via the SonarQube UI.
- Run analysis (from host or CI):
```bash
sonar-scanner -Dsonar.projectKey=fastapi-todos -Dsonar.sources=fastapi-app -Dsonar.host.url=http://<host>:9000 -Dsonar.login=<token>
```

## Automated Tests
The repo ships with `pytest` suites for the API.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Maintenance Notes
- `requirements.txt` includes `prometheus-fastapi-instrumentator` to expose request metrics.
- `Dockerfile` sets build context at the repo root and runs `uvicorn` from `fastapi-app/main.py`.
- Rebuild containers after dependency or configuration updates: `docker compose up -d --build`.
