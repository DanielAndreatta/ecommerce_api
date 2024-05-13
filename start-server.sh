#!/usr/bin/env bash

python ecommerce_api/manage.py makemigrations --no-input
python ecommerce_api/manage.py migrate
python ecommerce_api/manage.py collectstatic --no-input

# Crea el superusuario si se especifica
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd ecommerce_api; python manage.py createsuperuser --no-input)
fi

# Inicia Gunicorn y Nginx
(cd ecommerce_api; gunicorn ecommerce_api.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"



