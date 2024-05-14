FROM python:3.8

ENV PYTHONNUMBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

# Ejecutar el script setup.sh
COPY setup.sh /code/
RUN chmod +x /code/setup.sh
CMD ["/code/setup.sh"]