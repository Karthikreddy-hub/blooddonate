# LifeLine — Blood Donation Network

A refreshed blood donor directory built with Flask, SQLAlchemy and PostgreSQL. The old Django project and ambiguous `untitled2pro` folder are replaced by a clearly named `backend/` application.

## Architecture

This is intentionally a **modular monolith**, not a collection of artificial microservices:
- **web** — Flask 3.1 application served by Gunicorn.
- **db** — PostgreSQL 17 using the official upstream image.

Only the application needs a custom Dockerfile. PostgreSQL is already distributed as a maintained container image, so the project uses that image rather than maintaining a custom database image.

## Project layout

```text
blooddonate/
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   └── lifeline/
│       ├── __init__.py
│       ├── config.py
│       ├── extensions.py
│       ├── forms.py
│       ├── models.py
│       ├── routes.py
│       ├── static/css/app.css
│       └── templates/site.html
├── docker-compose.yml
├── .env.example
└── README.md
```

## Run with Docker Compose

Requirements: Docker Engine/Desktop and the Docker Compose plugin.

1. Clone the repository and enter its root directory.
2. Create a local environment file: `cp .env.example .env`.
3. Edit `.env`. Set a long, unique `FLASK_SECRET_KEY` and a strong `POSTGRES_PASSWORD`.
4. Build and start: `docker compose up -d --build`.
5. Check status and logs: `docker compose ps` and `docker compose logs -f web`.
6. Open [http://localhost:8000](http://localhost:8000).

The web container waits for PostgreSQL to become healthy and runs initial table setup before Gunicorn starts. PostgreSQL data is kept in the named `postgres_data` volume.

Useful commands:

```bash
docker compose exec web flask --app lifeline:create_app init-db
docker compose exec web flask --app lifeline:create_app routes
docker compose down
# Destructive: removes the database volume and all account/donor data.
docker compose down -v
```

## Run locally

Use Python 3.14 and a reachable PostgreSQL instance.

```bash
cd backend
python -m venv .venv
# Activate the virtual environment, then:
pip install -r requirements.txt
```

Set the variables from the root `.env.example`, but point `DATABASE_HOST` to your local PostgreSQL server. Then run:

```bash
flask --app lifeline:create_app init-db
flask --app lifeline:create_app run --debug
```

## Features

- Account registration with password hashing and session-based login/logout.
- Donor profile creation and update.
- Authenticated donor directory with blood-group and location/name filtering.
- Donor contact details shown only to signed-in members, and only when the donor explicitly consents.
- Responsive LifeLine interface with CSRF-protected forms.
- Database-aware health endpoint at `/health/`.

## Data and privacy notes

- The old Django SQLite database is not automatically migrated. Export and verify records you need **before** replacing an existing deployment.
- Donor name, phone number and email are personal data. Obtain clear consent, apply a retention policy, use HTTPS, and review applicable privacy requirements before real-world use.
- This is an educational directory, not a medical service. Blood-bank staff and healthcare professionals must confirm donor eligibility, compatibility and availability.
- The repository previously tracked a SQLite database. Removing it from the current project tree does not erase it from older Git history. Review that historical file and rewrite repository history if it contains real personal data; coordinate with collaborators first.

## Database migrations

The `init-db` command creates missing tables for a new demo deployment. SQLAlchemy `create_all` does **not** alter existing schemas. Add and review versioned Alembic migrations before changing an established database.

## Production checklist

Replace example secrets and store them in a secrets manager; set `SESSION_COOKIE_SECURE=true` behind HTTPS; terminate TLS at a trusted reverse proxy; configure backups, monitoring, rate limiting, email verification and account recovery; and restrict access to donor contact data.
