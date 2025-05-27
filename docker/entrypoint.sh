#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is up!"

alembic upgrade head

pytest

python create_superuser.py

exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
