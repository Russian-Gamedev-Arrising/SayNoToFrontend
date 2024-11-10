#!/bin/sh

echo "Starting entrypoint script..."
echo "Migrations"
python manage.py migrate

echo "Executing command: $@"
exec "$@"
