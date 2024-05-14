#!/bin/bash

# Ejecutar las migraciones de Django
python ecommerce_api/manage.py makemigrations --no-input
python ecommerce_api/manage.py migrate

# Recolectar los archivos estáticos de Django
python ecommerce_api/manage.py collectstatic --noinput

# Ejecutar el comando de gunicorn
exec gunicorn -c config/gunicorn/conf.py --bind :8000 --chdir ecommerce_api ecommerce_api.wsgi:application
