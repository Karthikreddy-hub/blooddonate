# LifeLine — Blood Donation Network

A Django-based blood donor community application modernized for container deployment.

## Architecture

This repository currently contains **one Django web application**, not independently deployable Python microservices. Docker Compose runs:
- `web`: Django served by Gunicorn (port 8000)
- `db`: PostgreSQL 16 with persistent storage

The app container has its own Dockerfile at `untitled2pro/Dockerfile`. PostgreSQL uses the official upstream image.

## Run locally with Docker

1. Install Docker Desktop or Docker Engine with the Compose plugin.
2. From the repository root, create the environment file:

   ```bash
   cp untitled2pro/.env.example untitled2pro/.env
   ```

3. Edit `untitled2pro/.env`. Set a strong, unique `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`. For local browser access, the defaults for allowed hosts and CSRF origins are suitable.
4. Start the stack:

   ```bash
   docker compose up -d --build
   ```

5. Apply database migrations and collect static assets:

   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py collectstatic --noinput
   ```

6. Create an admin account:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

7. Visit [http://localhost:8000](http://localhost:8000). Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/). Health: [http://localhost:8000/health/](http://localhost:8000/health/).

Useful commands:

```bash
docker compose ps
docker compose logs -f web
docker compose down
# Preserve data volumes when stopping. To permanently delete DB/uploads/static volumes:
# docker compose down -v
```

## Application features

- Account registration and Django session authentication
- Authenticated donor registration
- Authenticated searchable donor directory (blood group and location/name)
- Responsive LifeLine interface

## Important notes

- This is an educational/community demo, not a medical service. Donor eligibility, blood compatibility, availability and identity must be verified by healthcare professionals.
- Donor contact details are personal data. The directory is restricted to authenticated accounts in this demo; deploy only with appropriate consent, access controls, privacy notice, retention policy and HTTPS.
- The old SQLite database is not migrated automatically. Back up and migrate any records separately before replacing an existing deployment.
- The initial project migration contains legacy registration/login tables. The updated application uses Django's built-in User model; the old tables are retained in migration history for safe schema continuity.
- For production, terminate TLS at a trusted reverse proxy/load balancer, set production host/origin values, rotate secrets, configure backups, and review privacy/legal requirements.

## Development

```bash
cd untitled2pro
python -m venv .venv
# Activate the virtual environment, then:
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
