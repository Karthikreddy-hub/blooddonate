#!/bin/sh
set -eu
# Compose waits for PostgreSQL to become healthy before starting this container.
# create_all handles first-time setup; use versioned migrations for schema changes.
flask --app lifeline:create_app init-db
exec "$@"
