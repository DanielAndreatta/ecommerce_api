FROM python:3.8

ENV PYTHONNUMBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

# Ejecutar las migraciones de Django
RUN python ecommerce_api/manage.py makemigrations --no-input
RUN python ecommerce_api/manage.py migrate

# Recolectar los archivos estaticos de Django
RUN python ecommerce_api/manage.py collectstatic --noinput

CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "ecommerce_api", "ecommerce_api.wsgi:application"]