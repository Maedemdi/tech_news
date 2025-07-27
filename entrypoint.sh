#!/bin/bash
set -e

echo "waiting for postgresql..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  sleep 2
done

echo "postgresql is up."

python manage.py migrate --noinput 
python manage.py collectstatic --noinput &&

exec "$@"
