# 24/7 Local Automation Stack with Live Dashboard

This repository provides a dockerized homelab-style stack to run 24/7 on your local network. It includes:

- Homer dashboard (landing page)
- Task Service (FastAPI) with scheduled jobs and Prometheus metrics
- Node-RED for visual automations
- Prometheus + Grafana for metrics/monitoring
- Loki + Promtail for centralized logs
- Dozzle for live container logs
- Portainer for container management
- cAdvisor + node-exporter for system/container metrics

## Quick start

Prerequisites: Docker + Docker Compose

1. Clone this repo on your machine running Docker
2. Optional: set `TZ` env var for timezone (e.g., `export TZ=America/New_York`)
3. Start the stack:

```bash
make up
```

4. Open services:
   - Homer: http://localhost:8080
   - Task Service (API/Docs): http://localhost:8000/docs
   - Node-RED: http://localhost:1880
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090
   - Dozzle (live logs): http://localhost:9999
   - Portainer: http://localhost:9000

## Task Service

- Recurring jobs are scheduled: `heartbeat` (30s), `web_check` (1m), `cpu_burn` (10m)
- Run a task immediately:

```bash
curl -X POST http://localhost:8000/tasks/run \
  -H 'content-type: application/json' \
  -d '{"name":"web_check","kwargs":{"url":"https://example.com"}}'
```

- List scheduled jobs: `GET http://localhost:8000/tasks`
- Metrics: `GET http://localhost:8000/metrics` (scraped by Prometheus)

## Monitoring & Logs

- Prometheus scrapes: task-service, cAdvisor, node-exporter
- Grafana auto-provisioned with Prometheus and Loki datasources
- Promtail tails Docker logs and ships to Loki
- Dozzle shows live logs directly from Docker socket

## Customization

- Update `homer/config.yml` to customize the dashboard tiles
- Add your own tasks in `task-service/app/tasks.py` and map them in `app/main.py`
- Import or create dashboards in Grafana (uses a persisted volume)

## Security Notes

- Services are exposed on localhost by default. For LAN access, bind Docker to your LAN IP or add a reverse proxy with auth.
- Portainer/Dozzle use the Docker socket; grant access only on trusted hosts.

## Maintenance

```bash
make ps       # status
make logs     # follow logs
make restart  # restart all services
make down     # stop
make clean    # stop + remove volumes
```
