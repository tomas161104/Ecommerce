set -e

if [ "${WAIT_FOR_DB}" = "1" ]; then
  echo "Waiting for database ${DB_HOST}:${DB_PORT}..."
  while ! nc -z ${DB_HOST} ${DB_PORT}; do
    sleep 0.5
  done
fi

echo "Apply database migrations"
python manage.py migrate --noinput

if [ -f "/app/fixtures/demo_data.json" ]; then
  echo "Loading demo fixtures (if any)"
  python manage.py loaddata fixtures/demo_data.json || true
fi

if [ "${DJANGO_ENV}" = "development" ]; then
  echo "Starting Django development server"
  python manage.py runserver 0.0.0.0:8000
else
  echo "Starting Gunicorn"
  exec gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
