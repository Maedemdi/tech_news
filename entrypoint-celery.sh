#!/bin/bash
set -e

echo "waiting for celery beat table..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1 FROM django_celery_beat_crontabschedule LIMIT 1;" >/dev/null 2>&1; do
  sleep 2
done

echo "celery table exists."

exec "$@"
