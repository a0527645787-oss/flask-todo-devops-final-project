# World Cup Seat Booking DevOps Project

This is a DevOps final project built around a Flask web application for booking seats at World Cup matches.

The application lets users view matches, choose a seat type, create a booking, manage an existing booking, and cancel a booking. It also includes a simple admin area for viewing bookings and match statistics.

The project is intentionally beginner-friendly: the application is small enough to understand, but the deployment flow includes real DevOps pieces such as Docker, Docker Compose, GitHub Actions, Docker Hub, AWS EC2, Nginx, Gunicorn, MySQL, Prometheus, Grafana, and health checks.

## Project Overview

Main application features:

- Flask web application for World Cup seat booking.
- MySQL database for persistent production data.
- SQLAlchemy ORM for working with database tables through Python models.
- Nginx reverse proxy in front of the Flask app.
- Gunicorn as the production WSGI server.
- Docker Compose for local and production-style runtime.
- GitHub Actions CI/CD pipeline.
- Docker Hub image publishing with `latest` and short SHA tags.
- AWS EC2 deployment using Docker Compose.
- `IMAGE_TAG` based production image selection.
- Automatic rollback in the deployment workflow if the new image fails the health check.
- `/health` endpoint for health checks.
- `/metrics` endpoint for Prometheus metrics.
- Prometheus and Grafana monitoring.
- Cron-based health check script for basic production monitoring.

## Architecture

Production request flow:

```text
User -> Nginx -> Gunicorn -> Flask -> SQLAlchemy -> MySQL
```

What each part does:

- `User` sends HTTP requests from a browser.
- `Nginx` receives public traffic on port `80` and proxies requests to the app container.
- `Gunicorn` runs the Flask application inside the app container.
- `Flask` handles routes, forms, sessions, bookings, and admin pages.
- `SQLAlchemy` maps Python classes to database tables.
- `MySQL` stores stadiums, matches, seat types, and bookings.

Production containers:

- `nginx_proxy_prod`
- `flask_app_prod`
- `mysql_prod`
- `prometheus_prod`
- `grafana_prod`

## Database Model

The application uses four main SQLAlchemy models.

### Stadiums

`Stadium` stores information about each stadium:

- `id`
- `name`
- `city`
- `capacity`

Relationship:

- One stadium can host many matches.

### Matches

`Match` stores information about each World Cup match:

- `id`
- `home_team`
- `away_team`
- `match_date`
- `stadium_id`

Relationships:

- Each match belongs to one stadium.
- Each match can have many seat types.
- Each match can have many bookings.

### SeatTypes

`SeatType` stores the available ticket categories for a match:

- `id`
- `name`
- `price`
- `total_seats`
- `match_id`

Examples:

- `Regular`
- `Premium`
- `VIP`

Relationship:

- Each seat type belongs to one match.

### Bookings

`Booking` stores user reservations:

- `id`
- `booking_code`
- `customer_name`
- `customer_email`
- `seats_count`
- `is_cancelled`
- `created_at`
- `match_id`
- `seat_type_id`

Relationships:

- Each booking belongs to one match.
- Each booking belongs to one seat type.

Cancelled bookings are not deleted from the database. Instead, they are marked with `is_cancelled=True`. This keeps a useful history and makes the logic easier to audit.

### Why MySQL Instead Of SQLite?

SQLite is used only for fast automated tests, where a temporary in-memory database is useful.

MySQL is used for the real Docker and production environment because it is closer to a real-world deployment:

- It runs as a separate service.
- It persists data in a Docker volume.
- It supports multiple connections better than SQLite.
- It demonstrates how an application container connects to a database container.

## Local Development

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Run the local stack:

```powershell
docker compose up --build
```

Open the app:

```text
http://localhost:5001
```

Health check:

```powershell
curl http://localhost:5001/health
```

## Environment Variables

`.env.example` documents the expected environment variables. The real `.env` file is local only and must not be committed.

Important variables:

- `APP_ENV` - application environment, such as `development` or `production`.
- `IMAGE_TAG` - Docker image tag used by production Compose.
- `SESSION_COOKIE_SECURE` - whether session cookies require HTTPS.
- `ADMIN_PASSWORD` - admin login password.
- `SECRET_KEY` - Flask session signing key.
- `DB_USER` - MySQL username.
- `DB_PASSWORD` - MySQL password.
- `DB_NAME` - MySQL database name.
- `MYSQL_ROOT_PASSWORD` - MySQL root password.

## DevOps Pipeline

CI/CD flow:

```text
Developer -> GitHub -> GitHub Actions -> Tests -> Docker Build -> Docker Hub -> EC2 -> Docker Compose -> Health Check
```

On every push to `main`, GitHub Actions:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies from `requirements.txt`.
4. Runs tests with `pytest`.
5. Builds the Docker image.
6. Logs in to Docker Hub using GitHub Secrets.
7. Pushes the Docker image to Docker Hub.
8. Connects to the EC2 server over SSH.
9. Pulls the latest code on EC2.
10. Updates the production `.env` file with the new `IMAGE_TAG`.
11. Pulls and starts the production Docker Compose stack.
12. Checks `http://localhost/health`.

GitHub Secrets used by the workflow:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`

## Docker Image Tagging

Docker images are pushed to Docker Hub under:

```text
shlomodevops/devops-final-projectshlomo
```

Each successful build publishes two tags:

- `latest`
- a 7-character short commit SHA tag, such as `abc1234`

`latest` is convenient, but it moves every time a new image is pushed. A short SHA tag points to a specific Git commit, which makes production deployments easier to verify and roll back.

Production Compose uses:

```text
image: shlomodevops/devops-final-projectshlomo:${IMAGE_TAG:-latest}
```

This means:

- If `IMAGE_TAG` exists, production runs that exact image tag.
- If `IMAGE_TAG` is missing, Docker Compose falls back to `latest`.

The CI/CD workflow updates the EC2 `.env` file with:

```env
IMAGE_TAG=<short-sha>
```

Then it runs:

```bash
docker compose --env-file .env -f docker-compose.prod.yml pull app
docker compose --env-file .env -f docker-compose.prod.yml up -d
```

## Rollback

Rollback means returning production to a previous working Docker image.

The workflow saves the previous image tag in:

```text
.previous_image_tag
```

If the new deployment fails the health check, the workflow:

1. Restores the previous `IMAGE_TAG` in `.env`.
2. Pulls the previous app image.
3. Runs Docker Compose again.
4. Checks `http://localhost/health`.
5. Prints container status and logs if rollback fails.

Manual rollback steps on EC2:

```bash
cd ~/seat-booking-devops
grep IMAGE_TAG .env
```

Edit `.env` and set a previous working tag:

```env
IMAGE_TAG=abc1234
```

Then run:

```bash
docker compose --env-file .env -f docker-compose.prod.yml pull app
docker compose --env-file .env -f docker-compose.prod.yml up -d
curl http://localhost/health
```

Verify the running image:

```bash
docker inspect flask_app_prod --format='{{.Config.Image}}'
```

## Monitoring

The project includes three levels of monitoring.

### Health Endpoint

The app exposes:

```text
/health
```

It returns a simple JSON response when the app is alive:

```json
{"status": "ok"}
```

Production health check URL on EC2:

```text
http://localhost/health
```

### Metrics Endpoint

The app exposes Prometheus metrics at:

```text
/metrics
```

Metrics include default Python/process metrics from `prometheus-client` and a Flask request counter.

### Prometheus

Prometheus scrapes the Flask app at:

```text
app:5000/metrics
```

The config file is:

```text
monitoring/prometheus/prometheus.yml
```

For demo/debug use, Prometheus is exposed on:

```text
http://SERVER_IP:9090
```

### Grafana

Grafana visualizes metrics collected by Prometheus.

Grafana is exposed on:

```text
http://SERVER_IP:3000
```

The Prometheus data source is provisioned from:

```text
monitoring/grafana/provisioning/datasources/prometheus.yml
```

In a real production environment, ports `9090` and `3000` should not be open to the whole internet.

### Cron Health Check

The project also includes a simple cron-based health check:

```text
monitoring/health_check.sh
monitoring/install_cron.sh
```

The script checks:

```text
http://localhost/health
```

It retries failed checks, logs errors, captures Docker status and Flask logs, and attempts to restart `flask_app_prod` only after repeated failure.

Install it on the server:

```bash
chmod +x monitoring/install_cron.sh
./monitoring/install_cron.sh
```

View logs:

```bash
tail -f monitoring/health_check.log
```

## Production Stack

Production is run on AWS EC2 with:

```bash
docker compose --env-file .env -f docker-compose.prod.yml up -d
```

Services:

- `nginx` - public HTTP reverse proxy.
- `app` - Flask app running with Gunicorn.
- `mysql` - MySQL 8 database.
- `prometheus` - metrics scraping.
- `grafana` - metrics dashboards.

Named volumes:

- `mysql-prod-data`
- `prometheus_data`
- `grafana_data`

## Security Notes

Production secrets must not be hardcoded in source code.

This project uses environment variables for sensitive values:

- Admin password
- Flask secret key
- Database password
- MySQL root password
- EC2 SSH key through GitHub Secrets
- Docker Hub token through GitHub Secrets

Rules followed by this project:

- `.env` is not committed.
- `.env.example` contains placeholders only.
- GitHub Actions uses repository secrets.
- Production `.env` stays on the EC2 server.
- Docker image tags do not contain secrets.
- Monitoring logs should not print environment variables or secrets.

For real production use:

- Use strong passwords and a long random `SECRET_KEY`.
- Use HTTPS and set `SESSION_COOKIE_SECURE=true`.
- Restrict Grafana and Prometheus access.
- Restrict EC2 security groups to only the ports you actually need.
- Change default Grafana credentials before exposing it beyond a demo.

## Useful Commands

Check production health:

```bash
curl http://localhost/health
```

Check selected image tag:

```bash
grep IMAGE_TAG .env
```

Check running app image:

```bash
docker inspect flask_app_prod --format='{{.Config.Image}}'
```

Check production containers:

```bash
docker compose --env-file .env -f docker-compose.prod.yml ps
```

View Flask logs:

```bash
docker logs --tail=120 flask_app_prod
```
